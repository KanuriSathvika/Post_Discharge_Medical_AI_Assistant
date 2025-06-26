"""
clinical_agent.py
----------------
Defines the Clinical Agent for the AI assistant system. This agent uses a combination of Retrieval-Augmented Generation (RAG) and web search to answer medical questions, with clear rules for when to use each source. It is built using LangGraph and LangChain tools.
"""

import sys
import os
# Ensure local imports work regardless of execution context
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from langgraph.prebuilt import create_react_agent  # For agent creation
from langgraph.graph import START, END, StateGraph  # For workflow graphs (not used directly here)
from langchain_google_genai import ChatGoogleGenerativeAI  # (Optional) Google GenAI LLM
from dotenv import load_dotenv  # For environment variable management
from agents.clinical_agent.tools.rag_tool import rag_tool_function  # RAG tool for internal reference
from agents.clinical_agent.tools.web_search_tool import web_search_tool  # Web search tool
from langgraph_swarm import create_handoff_tool  # For agent handoff
from agents.llm_model import llm  # Main language model
from typing import TypedDict

# ---------------------- State Schema ---------------------------------- #
class ClinicalState(TypedDict):
    """
    State schema for the clinical agent workflow.
    Attributes:
        query (str): The user's question.
        patient_report (str | None): Optional patient report.
        name (str): Patient name.
        output (str): LLM generation/output.
    """
    query: str
    patient_report: str | None
    name: str
    output: str

# ---------------------- Prompt Template ------------------------------- #
prompt = """
    You are a Clinical AI Expert supporting patients and medical staff. Always prefix your response with:

👩‍⚕️ Clinical Expert:

You have access to:
1. ✅ Internal medical reference materials (via a RAG system powered by vector search on nephrology documents of medical knowledge)
2. 🌐 External web search (for general/latest medical information)

---

📌 **HOW TO RESPOND:**

1. **Try RAG search first.**
   - If relevant chunks are returned, answer based only on that.
   - Respond:
     ✅ **From Reference Materials:** [Your answer]

2. If RAG has **no relevant content** (empty or low relevance):
   - Use general knowledge or trigger a web search.
   - Respond:
     🌐 **From Web Search:** [Your answer]

3. If the question is **requires sensitive medical judgment**:
   - Respond:
     ⚠️ This specific clinical information requires consultation with a licensed medical professional.

---

🧠 **Your Rules:**
- NEVER mix sources without indicating which info came from where
- DO NOT hallucinate content that wasn’t found in RAG
- Answer concisely, professionally, and use bullet points where helpful
    """

from langchain_core.prompts import PromptTemplate  # For prompt formatting (if needed)

# ---------------------- Clinical Agent Creation ----------------------- #
clinical_assistant = create_react_agent(
    llm,
    [rag_tool_function, web_search_tool, create_handoff_tool(
        agent_name="receptionist_assistant",)],
    name="clinical_assistant",
    prompt=prompt,
)




