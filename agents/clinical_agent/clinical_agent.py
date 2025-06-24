
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))


from langgraph.prebuilt import create_react_agent
from langgraph.graph import START, END, StateGraph
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
# from agents.receptionist_agent.receptionist_agent import receptionist_assistant
# from langchain_core.messages import AIMessage, HumanMessage
from tools.rag_tool import rag_tool_function
# from agents.clinical_agent.tools.web_tool import web_tool
from agents.clinical_agent.tools.web_search_tool import web_search_tool
from langgraph_swarm import create_handoff_tool
from agents.llm_model import llm




# Define the tools
tools = [rag_tool_function, web_search_tool]

# Create the ReAct agent
# react_agent = create_react_agent(
#                 model=llm,
#                 tools=tools,
#                 name="clinical_agent",
#                 prompt="You are a knowledgeable and trustworthy clinical AI assistant that supports patients with medical questions after discharge. Your primary knowledge source is a nephrology reference book, and if needed, you can use a trusted web search tool.\n\nYour job is to:\n- Answer clearly and in simple language.\n- Cite the nephrology reference if used.\n- If the answer comes from the web, say so clearly.\n- Never guess. If unsure, recommend consulting a doctor.\n\nUse this format:\n\nAnswer:\n[response]\n\nSource: [Nephrology Reference Book / Web Search]",
#                 )

from typing import TypedDict

class ClinicalState(TypedDict):
    """State schema for the clinical agent workflow.
        Attributes:
        input: question
        output: LLM generation
    """
    query: str
    patient_report: str | None
    name:str  # Optional patient report
    output: str




prompt="""
    You are a Clinical AI Assistant supporting patients and medical staff. You have access to:

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
from langchain_core.prompts import PromptTemplate

clinical_assistant=create_react_agent(
    llm,
    [rag_tool_function, web_search_tool,create_handoff_tool(
        agent_name="receptionist_assistant",)],
    name="clinical_assistant",
    prompt="You are an Intelligent Clinical AI Assistant supporting patients and medical staff. You have access to:\n\n1. ✅ Internal medical reference materials (via a RAG system powered by vector search on nephrology documents)\n2. 🌐 External web search (for general or latest medical information)\n\nUse the following rules to decide how to respond:\n\n---\n\n📌 **WHEN TO USE INTERNAL REFERENCE (RAG VECTOR SEARCH)**\n\n- The question relates to nephrology or post-discharge care covered in the reference materials\n- Examples:\n- “What are the symptoms of chronic kidney disease?”\n- “Which diet is recommended after nephrology surgery?”\n\nIf confident matches are found in the vector store:\n→ Retrieve and generate answer based only on that.\n\nRespond with:\n✅ **From Reference Materials:** [Answer]\n\n---\n\n🌐 **WHEN TO USE WEB SEARCH**\n\n- The query is **not covered** in the internal documents\n- OR, it needs **updated information** (e.g., guidelines, drugs, or statistics,latest research information)\n- OR, the match from RAG is low-confidence or unrelated\n\nExamples:\n- “What are the 2024 KDIGO guidelines?”\n- “Any recent research on gene therapy in nephrology?”\n- “Alternative medicine for CKD treatment?”\n\nRespond with:\n✅ **From Reference Materials:** [state if not found or insufficient]\n🌐 **From Web Search:** [Answer with source and disclaimer]\n\n---\n\n# ⚠️ **WHEN NEITHER CAN HELP**\n\n# - The topic is too specialized or unclear even after web search\n# - It may involve sensitive clinical judgment or diagnosis\n\n# Respond with:\n# ⚠️ “This specific clinical information requires consultation with a licensed medical professional.”\n\n---\n\n🧠 Your job is to:\n- Always **try RAG search first**\n- If RAG is insufficient, automatically **trigger a web search**\n- Clearly indicate in the output where each piece of information came from\n- Never mix sources without saying which is which",
)

# ans=clinical_assistant.invoke({
#     "messages": [  
#         {"role": "user", "content": "What's the latest research on SGLT2 inhibitors for kidney disease?"}
#     ]})
# I'm having swelling in my legs. What could be the cause? Can you help me understand if this is related to  nephrology surgery?
# # print(ans)

# for m in ans["messages"]:
#     print(m.pretty_print())