
from dotenv import load_dotenv
import os
load_dotenv()


from langchain_community.tools import DuckDuckGoSearchRun

def web_search_tool(query: str) -> str:
    """Searches DuckDuckgo using Langchain's DuskcDucksGoSearchRun tool."""
    search = DuckDuckGoSearchRun()
    return search.run(query)

# example
# res=web_search_tool("wWhat's the latest research on SGLT2 inhibitors for kidney disease?")
# print(res)