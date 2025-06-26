"""
graph_builder.py
----------------
Builds and compiles the multi-agent workflow for the Post-Discharge Medical AI Assistant using LangGraph Swarm.
This script sets up the receptionist and clinical agents, manages agent handoff, and provides logging utilities for interactions and retrieval attempts.
"""

# from langgraph.graph import START,StateGraph, END  # Uncomment if using StateGraph directly
from langchain_google_genai import ChatGoogleGenerativeAI  # (Optional) Google GenAI LLM
from dotenv import load_dotenv  # For environment variable management
import sys
import os
# Ensure parent directory is in sys.path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from agents.receptionist_agent.receptionist_agent import receptionist_assistant  # Receptionist agent
from agents.clinical_agent.clinical_agent import clinical_assistant  # Clinical agent

from langgraph_swarm import create_swarm  # For multi-agent workflow
from langgraph_swarm import create_handoff_tool  # For agent handoff
from langgraph.checkpoint.memory import InMemorySaver  # For in-memory checkpointing
from backend.logger import logger  # Logger for tracking events

# ---------------------- Workflow Setup -------------------------------- #
# Create an in-memory checkpointer for session state
checkpointer = InMemorySaver()
# Create a swarm workflow with both agents, receptionist as default
workflow = create_swarm(
    [receptionist_assistant, clinical_assistant],
    default_active_agent="receptionist_assistant"
)
# Compile the workflow into an app object
app = workflow.compile(checkpointer=checkpointer)

# Configuration for the workflow (threading, etc.)
config = {"configurable": {"thread_id": "1"}}

# ---------------------- Logging Utilities ----------------------------- #
def log_interaction(role, content):
    """
    Log a user or agent interaction.
    Args:
        role (str): 'User' or 'Agent'.
        content (str): The message content.
    """
    logger.info(f"{role}: {content}")

def log_handoff(from_agent, to_agent, reason=None):
    """
    Log when a handoff occurs between agents.
    Args:
        from_agent (str): Name of the agent handing off.
        to_agent (str): Name of the agent receiving.
        reason (str, optional): Reason for handoff.
    """
    logger.info(f"Agent handoff from {from_agent} to {to_agent}. Reason: {reason if reason else 'N/A'}")

def log_retrieval_attempt(agent, query, result):
    """
    Log a retrieval attempt by an agent.
    Args:
        agent (str): Name of the agent.
        query (str): The query string.
        result (str): The retrieval result or status.
    """
    logger.info(f"{agent} retrieval attempt. Query: {query} | Result: {result}")

