# from langchain_community.vectorstores import Qdrant
from langchain_qdrant import Qdrant
from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client import QdrantClient

def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-large-en-v1.5", model_kwargs={'device': 'cpu'})
    client = QdrantClient(url="http://localhost:6333")
    
    return Qdrant(
        client=client,
        collection_name="nephrology",
        embeddings=embeddings
    )

# ret=load_vectorstore().as_retriever()
# print(ret)    