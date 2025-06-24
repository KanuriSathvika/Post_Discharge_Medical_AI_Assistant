post_discharge_ai_assistant/
│
├── app/
│   └── main.py                    # Streamlit UI
│
├── agents/
│   ├── receptionist_agent.py     # Receptionist Agent logic
│   ├── clinical_agent.py         # Clinical Agent logic
│   └── graph_builder.py          # LangGraph workflow setup
│
├── backend/
│   ├── database.py               # Patient data access
│   └── logger.py                 # Logging
│
├── data/
│   ├── patient_reports.json      # 25+ dummy reports
│   ├── nephrology_reference.pdf  # Reference material
│   └── vector_store/             # FAISS vector db
│
├── rag/
│   ├── vectorstore.py            # Vector DB setup
│   ├── load_documents.py         # Load/chunk nephrology text
│
├── search/
│   └── web_search_tool.py        # Web search fallback
│
├── logs/
│   └── interactions.log
│
├── requirements.txt
└── README.md
