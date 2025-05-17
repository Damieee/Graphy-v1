# Graphy v1 - FastAPI Backend

A modular FastAPI backend for PDF-to-Neo4j GraphRAG using OpenAI and LangChain.

## Features

- Upload a PDF and extract its content into a Neo4j graph database.
- Ask questions in natural language and get answers via graph-based retrieval.
- Modular code: OpenAI, Neo4j, and business logic are separated for maintainability.
- CORS enabled for frontend integration.
- Health check and root endpoints.

## Setup

1. **Clone the repository** and navigate to this folder.

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   - Copy `.env.example` to `.env` and fill in your credentials.

4. **Run the server:**
   ```bash
   uvicorn fastapi_app.main:app --reload
   ```

## API Endpoints

- `POST /upload_pdf/`  
  Upload a PDF and process it into the Neo4j graph.  
  **Form fields:**  
  - `file`: PDF file  
  - `neo4j_url`, `neo4j_username`, `neo4j_password`, `openai_api_key`

- `POST /ask`  
  Ask a question about the ingested data.  
  **JSON body:**  
  ```json
  {
    "question": "Your question here",
    "neo4j_url": "...",
    "neo4j_username": "...",
    "neo4j_password": "...",
    "openai_api_key": "..."
  }
  ```

- `GET /health`  
  Health check endpoint.

## Node and Relationship Types

The backend currently uses a fixed set of allowed node and relationship types for graph extraction:
- **Nodes:** `Patient`, `Disease`, `Medication`, `Test`, `Symptom`, `Doctor`
- **Relationships:** `HAS_DISEASE`, `TAKES_MEDICATION`, `UNDERWENT_TEST`, `HAS_SYMPTOM`, `TREATED_BY`

> **Note:**  
> If your PDFs contain entities or relationships outside these types, you will need to update the `allowed_nodes` and `allowed_relationships` lists in `graph_utils.py` to match your data domain.

## License

MIT License
