"""
Ultra-Fast Vector Store Creation
-------------------------------
Streamlined PDF processing and vector store creation with minimal overhead.
Optimized for maximum speed with clean, simple code.
"""

import time
import logging
import uuid
from typing import List, Dict, Generator
import fitz  # PyMuPDF - fastest PDF processing
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient, models, http
from qdrant_client.http.models import PointStruct

# Minimal logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class Config:
    """Configuration settings."""
    PDF_PATH = r"data\clinical_nephrology.pdf"
    COLLECTION_NAME = "nephrology_lc_fastembed"
    MODEL_NAME = "BAAI/bge-base-en-v1.5"
    CHUNK_SIZE = 2500
    CHUNK_OVERLAP = 700
    BATCH_SIZE = 64  # Optimized batch size

# --- Setup LangChain FastEmbedEmbeddings ---
logger.info(f"Initializing LangChain FastEmbedEmbeddings with model: {Config.MODEL_NAME}")
embeddings = FastEmbedEmbeddings(model_name=Config.MODEL_NAME)
logger.info("✅ LangChain FastEmbedEmbeddings model initialized.")


def extract_and_chunk_pdf(file_path: str) -> List[Dict]:
    """
    Efficiently extract text from PDF and create chunks.
    Single-pass processing for maximum speed.
    """
    logger.info("Starting PDF processing...")
    start_time = time.time()
    
    # Initialize text splitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=Config.CHUNK_SIZE, 
        chunk_overlap=Config.CHUNK_OVERLAP
    )
    
    chunks = []
    
    # Process PDF in a single pass
    with fitz.open(file_path) as doc:
        logger.info(f"Processing {len(doc)} pages...")
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text("text")
            
            if text.strip():  # Only process pages with content
                metadata = {"source": file_path, "page": page_num}
                page_chunks = splitter.create_documents([text], metadatas=[metadata])
                
                for chunk in page_chunks:
                    chunks.append({
                        "text": chunk.page_content,
                        "metadata": chunk.metadata
                    })
    
    processing_time = time.time() - start_time
    logger.info(f"✅ PDF processing complete: {len(chunks)} chunks in {processing_time:.2f}s")
    return chunks


def create_embeddings_batch(chunks: List[Dict]) -> List[PointStruct]:
    """Create embeddings for a batch of chunks."""
    texts = [chunk["text"] for chunk in chunks]
    # Add the text itself to the metadata for each chunk
    metadatas = [{**chunk["metadata"], "page_content": chunk["text"]} for chunk in chunks]
    
    # Generate embeddings
    vectors = embeddings.embed_documents(texts)
    
    # Create Qdrant points with UUIDs
    points = []
    for vector, metadata in zip(vectors, metadatas):
        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload=metadata
        ))
    
    return points


def process_in_batches(chunks: List[Dict], batch_size: int) -> Generator[List[PointStruct], None, None]:
    """Process chunks in batches for efficient embedding and upload."""
    total_batches = (len(chunks) + batch_size - 1) // batch_size
    
    for i in range(0, len(chunks), batch_size):
        batch_num = (i // batch_size) + 1
        batch = chunks[i:i + batch_size]
        
        logger.info(f"Processing batch {batch_num}/{total_batches} ({len(batch)} chunks)")
        
        # Create embeddings for this batch
        points = create_embeddings_batch(batch)
        yield points

# --- Main Execution ---
if __name__ == "__main__":
    start_time = time.time()
    logger.info("Starting optimized vectorstore ingestion...")

    # Setup Qdrant
    client = QdrantClient(url="http://localhost:6333")
    vector_size = len(embeddings.embed_query("test vector size"))

    # Delete collection if exists
    try:
        client.delete_collection(collection_name=Config.COLLECTION_NAME)
        logger.info("Deleted existing collection.")
    except http.exceptions.UnexpectedResponse:
        pass

    client.create_collection(
        collection_name=Config.COLLECTION_NAME,
        vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE),
    )
    logger.info(f"Collection '{Config.COLLECTION_NAME}' ready.")

    # Extract and chunk PDF
    chunks = extract_and_chunk_pdf(Config.PDF_PATH)
    logger.info(f"Total chunks created: {len(chunks)}")

    # Process in batches and upload to Qdrant
    total_uploaded = 0
    for batch_points in process_in_batches(chunks, Config.BATCH_SIZE):
        # Upload batch to Qdrant
        client.upload_points(
            collection_name=Config.COLLECTION_NAME,
            points=batch_points,
            wait=True
        )
        total_uploaded += len(batch_points)
        logger.info(f"Uploaded {len(batch_points)} points. Total: {total_uploaded}")

    total_time = time.time() - start_time
    logger.info(f"✅ Ingestion complete in {total_time:.2f} seconds.")
    logger.info(f"📊 Performance: {len(chunks)/total_time:.1f} chunks/second")