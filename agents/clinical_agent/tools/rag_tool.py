from langchain.tools import Tool

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from rag.load_vectorstore import load_vectorstore
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from agents.llm_model import llm

# llm = ChatGoogleGenerativeAI(
#     model="gemini-1.5-flash",
#     google_api_key=os.getenv("GOOGLE_API_KEY")
# )

prompt_template = PromptTemplate.from_template(
    """Use the nephrology reference below to answer the question.
       if not enough information is available, use web search to find the answer.

    Context:
    {context}

    Question:
    {question}

    Answer:"""
)

retriever = load_vectorstore().as_retriever()

rag_chain = RetrievalQA.from_chain_type(
    
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    chain_type_kwargs={"prompt": prompt_template}
)

# def rag_query(question: str) -> str:
#     """Answers nephrology-related medical queries using a RAG pipeline."""
#     return rag_chain.run(question)

def rag_tool_function(query: str) -> str:
    """
    Function to handle queries using the RAG tool.

    Args:
        query (str): The medical question to be answered.

    Returns:
        str: The answer to the query based on the nephrology reference book.
    """
    # print(f"RAG Tool Function called with query: {query}")
    
    return rag_chain.invoke(query)

