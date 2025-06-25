"""
create_vectorstore.py
---------------------
This script loads a reference PDF, splits it into text chunks, generates embeddings using a HuggingFace model, and uploads the embeddings to a Qdrant vector database for semantic search and retrieval.

Steps:
1. Load PDF document
2. Split into manageable text chunks
3. Generate embeddings (GPU if available)
4. Create/reset Qdrant collection
5. Batch embed and upload to Qdrant
6. (Optional) Add documents to LangChain Qdrant vectorstore
"""

# Import required libraries for document loading, splitting, embedding, and vector DB
from langchain_huggingface import HuggingFaceEmbeddings  # For embedding generation
from langchain_text_splitters import RecursiveCharacterTextSplitter  # For chunking text
from langchain_community.document_loaders import PyPDFLoader  # For loading PDF
from langchain_qdrant import Qdrant  # LangChain Qdrant integration

from qdrant_client import QdrantClient  # Qdrant Python client
from qdrant_client.http import models  # Qdrant HTTP models

from tqdm import tqdm  # For progress tracking
import multiprocessing  # For potential parallelism (not used directly here)
import torch  # For device selection (GPU/CPU)

# ---------------------- Step 1: Load PDF ------------------------------ #
loader = PyPDFLoader("data/nephrology_reference.pdf")  # Path to reference PDF
# Load all pages as LangChain Document objects
documents = loader.load()

# ---------------------- Step 2: Split documents ----------------------- #
# Split into chunks for embedding (1000 chars, 200 overlap)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = text_splitter.split_documents(documents)
print(f"✅ Loaded and split into {len(docs)} chunks.")

# ---------------------- Step 3: Embedding Model ----------------------- #
# Use GPU if available, else fallback to CPU
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# Initialize HuggingFace embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-large-en-v1.5",
    model_kwargs={"device": device},
)

# ---------------------- Step 4: Qdrant Setup -------------------------- #
client = QdrantClient(url="http://localhost:6333")  # Qdrant server URL
collection_name = "nephrology"  # Name for this collection
# Determine vector size from embedding model
vector_size = len(embeddings.embed_query("test"))

# Reset (delete if exists) and create collection
try:
    client.delete_collection(collection_name=collection_name)
except Exception:
    pass  # Ignore if collection does not exist

client.create_collection(
    collection_name=collection_name,
    vectors_config=models.VectorParams(
        size=vector_size,
        distance=models.Distance.COSINE
    )
)

# ---------------------- Step 5: Batch Embedding & Upload -------------- #
batch_size = 64  # Tune based on available memory
texts = [doc.page_content for doc in docs]  # Extract text from each chunk
metadatas = [doc.metadata for doc in docs]  # Extract metadata

print("Embedding documents and uploading to Qdrant...")

# Embed and upload in batches for efficiency
for i in tqdm(range(0, len(texts), batch_size)):
    batch_texts = texts[i:i + batch_size]
    batch_metadatas = metadatas[i:i + batch_size]
    batch_embeddings = embeddings.embed_documents(batch_texts)
    client.upload_collection(
        collection_name=collection_name,
        vectors=batch_embeddings,
        payload=batch_metadatas,
        ids=None,
        batch_size=batch_size
    )

print("✅ All documents embedded and uploaded to Qdrant.")

# ---------------------- Step 6: (Optional) LangChain Vectorstore ------ #
# This allows you to use LangChain's Qdrant wrapper for further operations
vectorstore = Qdrant(
    client=client,
    collection_name=collection_name,
    embeddings=embeddings
)

vectorstore.add_documents(docs)  # Add docs for LangChain retrieval
# print("✅ Documents added to Qdrant vectorstore successfully.")