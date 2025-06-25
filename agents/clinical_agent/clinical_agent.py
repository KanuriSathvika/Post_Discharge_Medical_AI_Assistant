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
from tools.rag_tool import rag_tool_function  # RAG tool for internal reference
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
    You are a Clinical AI Expert supporting patients and medical staff.  "Mention this 👩‍⚕️ Clinical Expert: with your response.\n\n" . You have access to:
        
    1. ✅ Internal medical reference materials (via a RAG system powered by vector search on nephrology documents)
    2. 🌐 External web search (for general or latest medical information)

    Use the following rules to decide how to respond:

    ---

    📌 **WHEN TO USE INTERNAL REFERENCE (RAG VECTOR SEARCH)**

    - The question relates to nephrology or post-discharge care covered in the reference materials
    - Examples:
    - “What are the symptoms of chronic kidney disease?”
    - “Which diet is recommended after nephrology surgery?”

    If confident matches are found in the vector store:
    → Retrieve and generate answer based only on that.

    Respond with:
    ✅ **From Reference Materials:** [Answer]

    ---

    🌐 **WHEN TO USE WEB SEARCH**

    - The query is **not covered** in the internal documents
    - OR, it needs **updated information** (e.g., guidelines, drugs, or statistics)
    - OR, the match from RAG is low-confidence or unrelated

    Examples:
    - “What are the 2024 KDIGO guidelines?”
    - “Any recent research on gene therapy in nephrology?”
    - “Alternative medicine for CKD treatment?”

    Respond with:
    ✅ **From Reference Materials:** [state if not found or insufficient]

    🌐 **From Web Search:** [Answer with source and disclaimer]

    ---

    # ⚠️ **WHEN NEITHER CAN HELP**

    # - The topic is too specialized or unclear even after web search
    # - It may involve sensitive clinical judgment or diagnosis

    # Respond with:
    # ⚠️ “This specific clinical information requires consultation with a licensed medical professional.”

    ---

    🧠 Your job is to:
    - Always **try RAG search first**
    - If RAG is insufficient, automatically **trigger a web search**
    - Clearly indicate in the output where each piece of information came from
    - Never mix sources without saying which is which
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

