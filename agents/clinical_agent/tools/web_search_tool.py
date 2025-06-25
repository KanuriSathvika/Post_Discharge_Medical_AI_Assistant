"""
web_search_tool.py
-----------------
This module provides a function to perform web search using DuckDuckGo via LangChain's DuckDuckGoSearchRun tool.
It is used as a fallback when the RAG tool cannot answer a query from the reference book.
"""

from dotenv import load_dotenv  # For loading environment variables from .env
import os
load_dotenv()  # Load environment variables (if any)

from langchain_community.tools import DuckDuckGoSearchRun  # LangChain DuckDuckGo search tool
from backend.logger import logger  # Custom logger for logging search events


def web_search_tool(query: str, agent_name: str = "ClinicalAgent") -> str:
    """
    Searches DuckDuckGo using LangChain's DuckDuckGoSearchRun tool.

    Args:
        query (str): The search query string.
        agent_name (str): Name of the agent calling the tool (for logging).

    Returns:
        str: The search result as a string (may be a summary or snippet).
    """
    logger.info(f"[WebSearch] Called by: {agent_name} | Query: {query}")
    search = DuckDuckGoSearchRun()
    result = search.run(query)
    logger.info(f"[WebSearch] Responded by: {agent_name} | Result: {str(result)[:200]}")
    return result

# Example usage (uncomment to test):
# res = web_search_tool("What's the latest research on SGLT2 inhibitors for kidney disease?")
# print(res)