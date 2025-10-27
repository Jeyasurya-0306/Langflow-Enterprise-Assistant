from fastapi import FastAPI, Request
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import json
import re

app = FastAPI(title="Mongo Query Extractor API", version="1.3.2")

MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"
model_device = "cuda" if torch.cuda.is_available() else "cpu"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,
).to(model_device)

class QueryRequest(BaseModel):
    query: str
    max_tokens: int = 100

PROMPT_TEMPLATE = """
You are an intelligent assistant that converts any natural language question into a structured MongoDB query format by inferring the correct field and value based on context and data type, not predefined keywords.

Data Context
The database collection is named "sales".
Fields and their expected content types:

- InvoiceNo: Large, unique integer IDs (e.g., 536365)
- StockCode: Alphanumeric product codes (e.g., "85123A")
- Description: Product text strings (e.g., "WHITE HANGING HEART T-LIGHT HOLDER")
- Quantity: Integers representing count (e.g., 6, 12)
- CustomerID: Medium-sized integer IDs (e.g., 17850)
- Country: Geographic location strings (e.g., "United Kingdom", "France", "California")

Rules
1. Output Format:
   Return ONLY a valid JSON object with the following keys:
   collection_name, field_name, field_value, limit

2. Collection Name:
   Always set to "sales"

3. Field Mapping (Inference ONLY):
   Determine the field_name solely based on the nature of the value, not on predefined keywords.
   - Geographic strings → Country
   - Alphanumeric codes → StockCode
   - Large integers (6+ digits) → InvoiceNo
   - Medium integers (5 digits) → CustomerID
   - Descriptive text → Description
   - Small numeric values indicating count → Quantity

4. Limit:
   Detect the number of requested results (e.g., "top 5", "limit 10").
   Default: 1

5. Defaults (if uncertain):
   {{
     "collection_name": "sales",
     "field_name": "unknown",
     "field_value": "unknown",
     "limit": 1
   }}

6. Response Constraint:
   Respond ONLY with the JSON object.
   Do NOT include explanations, prefixes, or extra text.

Examples
Natural Language Query: What are the first 10 sales from Germany?
Inferred Field: Country
Output:
{{"collection_name": "sales", "field_name": "Country", "field_value": "Germany", "limit": 10}}

User Question:
"{query}"
"""

DEFAULT_JSON = {
     "collection_name": "sales",
     "field_name": "unknown",
     "field_value": "unknown",
     "limit": 1
}

def generate_mongo_query_llm(query: str, max_tokens: int):
    prompt = PROMPT_TEMPLATE.format(query=query)

    prompt_with_template = f"<s>[INST] {prompt} [/INST]"

    try:
        inputs = tokenizer(prompt_with_template, return_tensors="pt").to(model.device)
        
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id
        )
        text = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
        
        if "[/INST]" in text:
            text = text.split("[/INST]", 1)[1].strip()

        cleaned_text = re.sub(r'```json|```|json\s*|Output:\s*', '', text, flags=re.IGNORECASE).strip()
        
        start_index = cleaned_text.find('{')
        end_index = cleaned_text.rfind('}')
        
        if start_index == -1 or end_index == -1 or start_index > end_index:
            return DEFAULT_JSON

        json_string = cleaned_text[start_index:end_index + 1]
        
        query_json = json.loads(json_string)

        query_json.setdefault("collection_name", DEFAULT_JSON["collection_name"])
        query_json.setdefault("field_name", DEFAULT_JSON["field_name"])
        query_json.setdefault("field_value", DEFAULT_JSON["field_value"])
        query_json.setdefault("limit", DEFAULT_JSON["limit"])

        if isinstance(query_json["limit"], str) and query_json["limit"].isdigit():
            query_json["limit"] = int(query_json["limit"])
            
        numeric_fields = ["InvoiceNo", "Quantity", "CustomerID"]
        if isinstance(query_json["field_value"], str) and query_json["field_name"] in numeric_fields:
            try:
                query_json["field_value"] = int(query_json["field_value"])
            except ValueError:
                pass

        return query_json

    except Exception as e:
        print(f"Error during LLM processing: {e}")
        return DEFAULT_JSON

@app.post("/extract_mongo")
async def extract_mongo(request: Request):
    try:
        body = await request.json()
        print("Incoming Body:", body)

        query = body.get("query", "")
        max_tokens = int(body.get("max_tokens", 100))

        if not query:
            return {"error": "Missing 'query' in request body"}

        query_json = generate_mongo_query_llm(query, max_tokens)
        return {"mongo_query": query_json}

    except Exception as e:
        print("Error:", e)
        return {"error": "Failed to process query.", "details": str(e)}
