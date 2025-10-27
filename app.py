from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(title="RAG API", version="1.1")


MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"
logger.info(f"Loading tokenizer and model: {MODEL_NAME}")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,
    device_map="auto"
)
logger.info("Model loaded successfully.")

class RAGQuery(BaseModel):
    query: str
    context: str  
    max_tokens: int = 200  


RAG_PROMPT_TEMPLATE = """
You are a highly intelligent assistant. Answer the user's question using ONLY the information provided in the context.
- Context may contain multiple documents; read all carefully.
- Provide concise, clear, and complete answers.
- Do NOT invent answers. If the answer is not in the context, reply: "I don't know."
- Return only the answer text. Do not repeat the question or context.

Context:
{context}

Question:
{query}
Answer:
"""

def generate_rag_response(query: str, context: str, max_tokens: int):
    prompt = RAG_PROMPT_TEMPLATE.format(query=query, context=context)
    logger.debug(f"Prompt:\n{prompt}")

    try:
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True).to(model.device)
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.7,
            pad_token_id=tokenizer.eos_token_id
        )
        text = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

        if "Answer:" in text:
            text = text.split("Answer:")[-1].strip()

        logger.info(f"Generated answer: {text}")
        return text

    except Exception as e:
        logger.error(f"Error generating RAG response: {e}", exc_info=True)
        raise e

@app.post("/rag")
def rag_endpoint(request: RAGQuery):
    logger.info(f"Received request: {request.dict()}")
    try:
        answer = generate_rag_response(
            request.query,
            request.context,
            request.max_tokens
        )
        return {"answer": answer}
    except Exception as e:
        logger.error(f"Error in endpoint: {e}", exc_info=True)
        return {"answer": f"Error: {str(e)}"}
