# rag_engine.py

import os
import chromadb
from chromadb.utils import embedding_functions

CHROMA_PATH = "vector_store"
COLLECTION_NAME = "visa_direct_docs"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

def chunk_text(text: str) -> list[str]:
    """Split text into overlapping chunks"""
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i + CHUNK_SIZE])
        chunks.append(chunk)
        i += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks

def build_vector_store():
    """Build ChromaDB vector store from knowledge base"""
    
    # Load knowledge base
    with open("visa_docs/visa_direct_kb.txt", "r") as f:
        text = f.read()

    # Chunk the text
    chunks = chunk_text(text)

    # Setup ChromaDB with sentence-transformers embeddings
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    # Delete existing collection if exists
    try:
        client.delete_collection(COLLECTION_NAME)
    except:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_fn
    )

    # Add chunks to collection
    collection.add(
        documents=chunks,
        ids=[f"chunk_{i}" for i in range(len(chunks))]
    )

    print(f"Vector store built with {len(chunks)} chunks.")

def retrieve_relevant_chunks(question: str, top_k: int = 4) -> str:
    """Retrieve most relevant chunks for a question"""
    
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    collection = client.get_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_fn
    )

    results = collection.query(
        query_texts=[question],
        n_results=top_k
    )

    # Join top chunks into one context
    relevant_context = "\n\n".join(results["documents"][0])
    
    return relevant_context

if __name__ == "__main__":
    build_vector_store()
