# Post-Discharge Medical AI Assistant

## Problem Overview
Patients discharged from hospitals often require ongoing support to understand their medical reports, follow care instructions, and access reliable information. Manual follow-up is resource-intensive and prone to gaps, leading to poor outcomes. This application addresses these challenges by providing an AI-powered assistant for post-discharge patient support.

## What is this Application?
This is an AI-powered assistant designed to help patients after hospital discharge. It can answer questions about medical reports, provide reference information, retrieve patient-specific data, and perform web searches for up-to-date medical knowledge. The system uses a multi-agent architecture, retrieval-augmented generation (RAG), and integrates with vector databases and web search tools.

## Architecture Justification (Techniques & Models)

### LLM Selection
- **Technique/Model:** OpenAI GPT-3.5/4 (or compatible LLM via API)
- **Usage:** Natural language understanding and generation for medical and general queries.
- **Location:** `agents/llm_model.py`

### Vector Database
- **Technique/Model:** FAISS (local vector store) or Qdrant (cloud-native vector DB)
- **Usage:** Stores and retrieves document embeddings for similarity search.
- **Location:** `data/vector_store/` (FAISS), `faiss_index/`, `qdrant_data/`, `agents/rag/`

### RAG Implementation
- **Technique/Model:** Retrieval-Augmented Generation pipeline using LLM + vector search
- **Usage:** Retrieves relevant context from vector DB and augments LLM responses.
- **Location:** `agents/rag/create_vectorstore.py`, `agents/rag/load_vectorstore.py`, `agents/clinical_agent/rag/`

### Multi-Agent Framework
- **Technique/Model:** Modular agent design (Receptionist Agent, Clinical Agent)
- **Usage:** Task-specific agents for patient interaction and clinical Q&A.
- **Location:** `agents/receptionist_agent.py`, `agents/clinical_agent.py`, `agents/graph_builder.py`, `agents/clinical_agent/`, `agents/receptionist_agent/`

### Web Search Integration
- **Technique/Model:** Custom web search tool (e.g., Bing API, SerpAPI, or scraping)
- **Usage:** Fallback to fetch latest medical info from the web.
- **Location:** `agents/clinical_agent/tools/web_search_tool.py`, `search/web_search_tool.py`

### Patient Data Retrieval
- **Technique/Model:** MongoDB or JSON-based storage, custom access layer
- **Usage:** Secure retrieval and summarization of patient-specific data.
- **Location:** `backend/database.py`, `data/patient_reports.json`, `backend/mongo_database.py`

## Project Structure (with File Mapping)

```
app/
    main.py                        # Streamlit UI entry point

agents/
    graph_builder.py               # LangGraph workflow setup
    llm_model.py                   # LLM API integration
    __pycache__/
    clinical_agent/
        __init__.py
        clinical_agent.py          # Clinical agent logic (modular)
        rag/
            create_vectorstore.py      # Build vector DB
            load_vectorstore.py        # Load/query vector DB
            __pycache__/
            tools/
                rag_tool.py            # RAG utilities
                web_search_tool.py     # Web search tool
                __pycache__/
    receptionist_agent/
        receptionist_agent.py      # Receptionist agent logic (modular)
        load_reports.py            # Load patient reports
        patient_report_tool.py     # Patient report utilities
        __pycache__/

backend/
    mongo_database.py              # MongoDB access
    logger.py                      # Logging
    __pycache__/

data/
    patient_reports.json           # 25+ dummy reports
    nephrology_reference.pdf       # Reference material

faiss_index/                       # FAISS index data
qdrant_data/                       # Qdrant vector DB data
logs/
    interactions.log               # User interaction logs
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
   Open your browser and go to `http://localhost:8501`.
