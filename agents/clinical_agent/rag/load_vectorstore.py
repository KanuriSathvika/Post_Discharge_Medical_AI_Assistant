"""
load_vectorstore.py
------------------
This module provides a function to load a Qdrant vectorstore using LangChain and HuggingFace embeddings.
It connects to a local Qdrant instance and loads the 'nephrology' collection for semantic search/retrieval.
"""

# Import required modules for vectorstore and embeddings
from langchain_qdrant import Qdrant  # LangChain Qdrant integration
from langchain_huggingface import HuggingFaceEmbeddings  # For embedding model
from qdrant_client import QdrantClient  # Qdrant Python client


def load_vectorstore():
    """
    Loads the Qdrant vectorstore for the 'nephrology' collection using HuggingFace embeddings.
    Returns:
        Qdrant: LangChain Qdrant vectorstore object ready for retrieval/QA tasks.
    """
    # Initialize HuggingFace embedding model (CPU by default)
    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-large-en-v1.5",
        model_kwargs={'device': 'cpu'}
    )
    # Connect to local Qdrant instance
    client = QdrantClient(url="http://localhost:6333")
    # Return LangChain Qdrant vectorstore object
    return Qdrant(
        client=client,
        collection_name="nephrology",
        embeddings=embeddings
    )

# Example usage (uncomment to test):
# ret = load_vectorstore().as_retriever()
# print(ret)