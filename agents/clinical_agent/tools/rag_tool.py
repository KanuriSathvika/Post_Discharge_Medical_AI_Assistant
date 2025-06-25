"""
rag_tool.py
-----------
This module provides a Retrieval-Augmented Generation (RAG) tool for answering medical questions using a nephrology reference book and, if needed, web search. It uses LangChain, HuggingFace, and Qdrant for retrieval, and a language model for answer generation.
"""

from langchain.tools import Tool  # For tool integration in LangChain

import sys
import os
# Ensure the rag module is importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from rag.load_vectorstore import load_vectorstore  # Loads the Qdrant vectorstore
from langchain.chains import RetrievalQA  # For retrieval-augmented QA
from langchain_core.prompts import PromptTemplate  # For custom prompt templates
from langchain_google_genai import ChatGoogleGenerativeAI  # (Optional) Google GenAI LLM
from dotenv import load_dotenv  # For environment variable management
from agents.llm_model import llm  # The main language model
from backend.logger import logger  # Custom logger

# ---------------------- Prompt Template ------------------------------- #
prompt_template = PromptTemplate.from_template(
    """Use the nephrology reference below to answer the question.
       if not enough information is available, use web search to find the answer.

    Context:
    {context}

    Question:
    {question}

    Answer:"""
)

# ---------------------- Retriever Setup ------------------------------- #
retriever = load_vectorstore().as_retriever()  # Qdrant retriever for semantic search

# ---------------------- RAG Chain Setup ------------------------------- #
rag_chain = RetrievalQA.from_chain_type(
    llm=llm,  # Language model (from agents.llm_model)
    retriever=retriever,  # Qdrant retriever
    chain_type="stuff",  # Stuff all retrieved docs into prompt
    chain_type_kwargs={"prompt": prompt_template}  # Use custom prompt
)

# ---------------------- RAG Tool Function ----------------------------- #
def rag_tool_function(query: str, agent_name: str = "ClinicalAgent") -> str:
    """
    Handles queries using the RAG tool. Retrieves relevant context from the nephrology reference and generates an answer using the LLM.

    Args:
        query (str): The medical question to be answered.
        agent_name (str): Name of the agent calling the tool (for logging).

    Returns:
        str: The answer to the query based on the nephrology reference book (and web search if needed).
    """
    logger.info(f"[RAG] Called by: {agent_name} | Query: {query}")
    result = rag_chain.invoke(query)
    logger.info(f"[RAG] Responded by: {agent_name} | Result: {str(result)[:200]}")
    return result

