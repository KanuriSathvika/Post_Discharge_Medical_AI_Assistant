"""
llm_model.py
------------
Initializes the main language model (LLM) for the AI assistant system using Google's Gemini model via LangChain.
Loads the API key from Streamlit Cloud secrets (or environment variable for local development).
"""

import os  # For environment variable access

try:
    import streamlit as st
    api_key = st.secrets["GOOGLE_API_KEY"]
except (ImportError, KeyError):
    # Fallback for local development
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

from langchain_google_genai import ChatGoogleGenerativeAI  # LangChain wrapper for Google GenAI

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",  # Model name
    google_api_key=api_key      # API key from Streamlit secrets or env
)
