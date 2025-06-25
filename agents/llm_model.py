"""
llm_model.py
------------
Initializes the main language model (LLM) for the AI assistant system using Google's Gemini model via LangChain.
Loads the API key from environment variables for secure access.
"""

# ---------------------- Environment Setup ----------------------------- #
# Load environment variables from .env file (must contain GOOGLE_API_KEY)
from dotenv import load_dotenv  # For loading .env files
load_dotenv()

# ---------------------- LLM Initialization ---------------------------- #
# Create the LLM instance using Gemini 2.5 Flash model
from langchain_google_genai import ChatGoogleGenerativeAI  # LangChain wrapper for Google GenAI
import os  # For environment variable access

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",  # Model name
    google_api_key=os.getenv("GOOGLE_API_KEY")  # API key from environment
)
