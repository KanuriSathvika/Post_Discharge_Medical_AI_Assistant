
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_qdrant import Qdrant

from qdrant_client import QdrantClient
from qdrant_client.http import models

from tqdm import tqdm  # for progress tracking
import multiprocessing

# Step 1: Load PDF
loader = PyPDFLoader("C:/Users/Kanuri Sathvika/Downloads/nephrology_reference.pdf")
documents = loader.load()

# Step 2: Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = text_splitter.split_documents(documents)
print(f"✅ Loaded and split into {len(docs)} chunks.")

# Step 3: Use GPU if available, else fallback to CPU
import torch
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-large-en-v1.5",
    model_kwargs={"device": device},
)

# Step 4: Initialize Qdrant
client = QdrantClient(url="http://localhost:6333")
collection_name = "nephrology"
vector_size = len(embeddings.embed_query("test"))

# Reset collection
try:
    client.delete_collection(collection_name=collection_name)
except:
    pass

client.create_collection(
    collection_name=collection_name,
    vectors_config=models.VectorParams(
        size=vector_size,
        distance=models.Distance.COSINE
    )
)

# Step 5: Batch embedding & upload
# Recommended batch size: 64 or 128 based on memory
batch_size = 64

# Embed documents in parallel to avoid one-by-one slowness
texts = [doc.page_content for doc in docs]
metadatas = [doc.metadata for doc in docs]

print("Embedding documents and uploading to Qdrant...")

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

# # Step 6: Create Qdrant vectorstore
vectorstore = Qdrant(
    client=client,
    collection_name=collection_name,
    embeddings=embeddings
)

vectorstore.add_documents(docs)
# print("✅ Documents added to Qdrant vectorstore successfully.")