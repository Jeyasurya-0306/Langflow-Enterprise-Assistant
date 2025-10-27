Langflow Enterprise Assistant: Multi-Tool Orchestrator (RAG & MongoDB)

💡 Project Summary

A robust, dual-function enterprise assistant built on Langflow (1.1.2) for rapid deployment of specialized LLM-powered services. This system acts as a unified core intelligence, capable of routing natural language queries to the correct tool flow for both Knowledge Retrieval (RAG) and Database Querying (MongoDB).

The project demonstrates modular design, high efficiency, and professional FastAPI integration for enterprise deployment.

🎯 Strategic Viability & Dual Functionality

This single-interface architecture provides high-value intelligence across two critical business needs:
Function	Solution Flow	Business Value
Knowledge Retrieval	RAG Pipeline (final demo rag flow.json)	Provides immediate, evidence-based Q&A over internal Strategy and Report PDFs.
Database Querying	NL-to-Mongo Flow (final demo mongo flow.json)	Allows non-technical users to translate natural language (e.g., "top 5 sales from France") into executable MongoDB queries for real-time analytics.

🏗️ Technical Architecture & Core Components

The system is orchestrated by a central Groq Agent that routes the user's input to one of two custom-hosted API services:

1. Langflow Flows

Flow Name	Description	Key Components
final flow.json	The Central Router	Primary user interface. It employs an Agent with a system prompt to dynamically select the RAG or MongoDB tool flow.
final demo rag flow.json	RAG Tool	Utilizes FAISS Vector Store and HuggingFace Embeddings, calling the external RAG API for final answer generation.
final demo mongo flow.json	MongoDB Tool	Calls the Mongo Query Extractor API, executes the query against a database, and uses an LLM to generate a natural, user-friendly response.

2. Custom Python APIs (FastAPI)

Two high-performance custom API endpoints were built to execute complex logic external to Langflow:
File	Framework	Core Function	Model Used
app.py	FastAPI (uvicorn)	Hosts the RAG endpoint, generating the final answer text based on context retrieved by the RAG flow.	mistralai/Mistral-7B-Instruct-v0.2
mongo.py	FastAPI (uvicorn)	Hosts the Mongo Query Extractor, translating natural language into a structured JSON query object for MongoDB.	mistralai/Mistral-7B-Instruct-v0.2

⚙️ Setup and Prerequisites

Tested Development Environment

The project was developed and verified on the following configuration:
Component	Specification
Operating System	Ubuntu 22.04.5 LTS (64-bit)
Memory	32.0 GiB (Recommended Minimum)
Processor	Intel® Core™ i5-4690K CPU @ 3.50GHz × 4

Installation Steps

    Clone the Repository:
    Bash

git clone https://github.com/[Your Username]/Langflow-Enterprise-Assistant.git
cd Langflow-Enterprise-Assistant

Environment Setup: Create a Python virtual environment and install all dependencies:
Bash

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

    Run APIs: The two backend services must be running simultaneously before launching Langflow. Follow the detailed steps in setup.txt:

        Terminal 1 (Mongo Extractor): uvicorn mongo:app --reload

        Terminal 2 (RAG API): uvicorn app:app --reload

    Run Langflow: Start your local Langflow instance and import the three .json flow files (final flow.json is the main entry point).

📄 Deliverables & Further Documentation

File Name	Purpose
langflow project report .docx	Comprehensive Project Report detailing the Strategic Viability, Architectural Breakdown, and Technical Execution.
final flow.json	The main Langflow orchestrator file.
setup.txt	Detailed guide for running both FastAPI services and troubleshooting.
requirements.txt	Full list of Python dependencies, including fastapi and langflow.

🧑‍💻 Author

Jeya Surya | [Link to your LinkedIn Profile] | [Your Professional Email Address]
