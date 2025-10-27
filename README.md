# Langflow Enterprise Assistant: Multi-Tool Orchestrator (RAG & MongoDB)

## 💡 Project Summary

A robust, dual-function enterprise assistant built on **Langflow (1.1.2)** for rapid deployment of specialized LLM-powered services. This system acts as a **unified core intelligence**, capable of routing natural language queries to the correct tool flow for both **Knowledge Retrieval (RAG)** and **Database Querying (MongoDB)**.

The project demonstrates modular design, high efficiency, and professional **FastAPI** integration for enterprise deployment.

---

## 🎯 Strategic Viability & Dual Functionality

This single-interface architecture provides high-value intelligence across two critical business needs:

| Function | Solution Flow | Key Technology |
| :--- | :--- | :--- |
| **Knowledge Retrieval** | **RAG Pipeline (`final demo rag flow.json`)** | Provides immediate, evidence-based Q&A over internal **Strategy and Report PDFs** using FAISS. |
| **Database Querying** | **NL-to-Mongo Flow (`final demo mongo flow.json`)** | Translates natural language into executable **MongoDB queries** for real-time analytics. |

---

## 🏗️ Technical Architecture & Core Components

The system is orchestrated by a central **Agent (`final flow.json`)** that dynamically routes the user's input to one of two custom-hosted API services.

### 1. Langflow Flows

| File Name | Description | Role in System |
| :--- | :--- | :--- |
| **`final flow.json`** | **The Central Router** | Primary user interface, employing a **Groq Agent** to select either the RAG Tool or the MongoDB Tool flow. |
| **`final demo rag flow.json`** | **RAG Tool Flow** | Handles vector store retrieval (FAISS), calling the external `app.py` API for final answer generation. |
| **`final demo mongo flow.json`** | **MongoDB Tool Flow** | Calls the `mongo.py` API to generate a structured query, executes it, and formats the result. |

### 2. Custom Python APIs (FastAPI)

Two high-performance custom API endpoints were developed using **FastAPI** to execute specialized, model-heavy logic:

| File | Endpoint Function | LLM Model Used |
| :--- | :--- | :--- |
| **`app.py`** | RAG Answer Generator | `mistralai/Mistral-7B-Instruct-v0.2` |
| **`mongo.py`** | Mongo Query Extractor (NL-to-JSON) | `mistralai/Mistral-7B-Instruct-v0.2` |

---

## ⚙️ Setup and Prerequisites

### Tested Development Environment

| Component | Specification |
| :--- | :--- |
| **Operating System** | **Ubuntu 22.04.5 LTS** (64-bit) |
| **Memory** | **32.0 GiB** (Recommended Minimum) |
| **Frameworks** | Langflow (1.1.2), FastAPI (0.115.0) |

### Installation Steps

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/](https://github.com/)Jeyasurya-0306/Langflow-Enterprise-Assistant.git
    cd Langflow-Enterprise-Assistant
    ```
2.  **Install Dependencies:** Install all necessary libraries listed in `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run APIs:** The two backend services must be running simultaneously. Follow the detailed instructions in **`setup.txt`**:
    * **Terminal 1 (Mongo Extractor):** `uvicorn mongo:app --reload` (Runs on `http://127.0.0.1:8080`)
    * **Terminal 2 (RAG API):** `uvicorn app:app --reload` (Runs on `http://127.0.0.1:8000`)
4.  **Run Langflow:** Start your local Langflow instance and import the three `.json` flow files to begin testing the integrated system.

---

## 📄 Documentation

* **Comprehensive Project Report:** The full documentation is included as **`langflow project report .docx`**.
* **Setup Guide:** Detailed execution instructions for all components are in **`setup.txt`**.

## 🧑‍💻 Author

**Jeya Surya** |https://www.linkedin.com/in/jeya-surya-2b8931378?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app | jeyasurya.m02@gmail.com
