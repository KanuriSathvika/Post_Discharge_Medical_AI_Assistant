# Post-Discharge Medical AI Assistant

## Problem Overview
Patients discharged from hospitals often require ongoing support to understand their medical reports, follow care instructions, and access reliable information. Manual follow-up is resource-intensive and prone to gaps, leading to poor outcomes. This application addresses these challenges by providing an AI-powered assistant for post-discharge patient support.

## What is this Application?
This is an AI-powered assistant designed to help patients after hospital discharge. It can answer questions about medical reports, provide reference information, retrieve patient-specific data, and perform web searches for up-to-date medical knowledge. The system uses a multi-agent architecture, retrieval-augmented generation (RAG), and integrates with vector databases and web search tools.

## Architecture Overview

### LLM Selection
- **Model:** Google Gemini-2.5-Flash
- **Purpose:** Natural language understanding and generation for medical and general queries.
- **Location:** `agents/llm_model.py`

### Vector Database
- **Model:** Qdrant (cloud-native vector DB)
- **Purpose:** Stores and retrieves document embeddings for similarity search.
- **Location:** `qdrant_data/`, `agents/clinical_agent/rag/`

### RAG Implementation
- **Technique:** Retrieval-Augmented Generation pipeline using LLM + vector search
- **Purpose:** Retrieves relevant context from vector DB and augments LLM responses.
- **Location:** `agents/clinical_agent/rag/create_vectorstore.py`, `agents/clinical_agent/rag/load_vectorstore.py`

### Multi-Agent Framework
- **Technique:** Modular agent design (Receptionist Agent, Clinical Agent)
- **Purpose:** Task-specific agents for patient interaction and clinical Q&A.
- **Location:** `agents/receptionist_agent/receptionist_agent.py`, `agents/clinical_agent/clinical_agent.py`, `agents/graph_builder.py`, `agents/receptionist_agent/`, `agents/clinical_agent/`

### Web Search Integration
- **Tool:** Custom web search tool (e.g., DuckDuckGo via LangChain)
- **Purpose:** Fallback to fetch latest medical info from the web.
- **Location:** `agents/clinical_agent/rag/tools/web_search_tool.py`

### Patient Data Retrieval
- **Storage:** MongoDB or JSON-based storage, custom access layer
- **Purpose:** Secure retrieval and summarization of patient-specific data.
- **Location:** `backend/mongo_database.py`, `backend/logger.py`, `data/patient_reports.json`

## Project Structure

```text
app/
    main.py                        # Streamlit UI entry point
    main_api.py                    # FastAPI backend (optional)

agents/
    graph_builder.py               # LangGraph workflow setup
    llm_model.py                   # LLM API integration
    clinical_agent/
        __init__.py
        clinical_agent.py          # Clinical agent logic
        rag/
            create_vectorstore.py      # Build vector DB
            load_vectorstore.py        # Load/query vector DB
            tools/
                rag_tool.py            # RAG utilities
                web_search_tool.py     # Web search tool
    receptionist_agent/
        receptionist_agent.py      # Receptionist agent logic
        load_reports.py            # Load patient reports
        patient_report_tool.py     # Patient report utilities

backend/
    mongo_database.py              # MongoDB access
    logger.py                      # Logging

data/
    patient_reports.json           # Dummy reports
    nephrology_reference.pdf       # Reference material

qdrant_data/                       # Qdrant vector DB data
logs/                              # Log files
requirements.txt                   # Python dependencies
README.md                          # Project documentation
```

## How to Run

1. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```
2. **(Optional) Start with Docker:**
   ```powershell
   docker-compose up --build
   ```
3. **Run the Streamlit app:**
   ```powershell
   streamlit run app/main.py
   ```
4. **Access the app:**
   Open your browser and go to [http://localhost:8501](http://localhost:8501)

---

## Notes
- Ensure MongoDB and Qdrant are running locally or update connection URIs as needed.
- The `.env` file should contain your Google API key for Gemini: `GOOGLE_API_KEY=...`
- For development, logs are saved in the `logs/` directory.
- For API usage, you can run the FastAPI backend with:
  ```powershell
  uvicorn app.main_api:fastapi_app --reload
  ```

## License
This project is for educational and research purposes only. Not for clinical use.
