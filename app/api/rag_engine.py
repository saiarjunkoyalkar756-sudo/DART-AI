# app/api/rag_engine.py — Vector Embedding Search & RAG Context Engine
import re, math
from typing import List, Dict, Any
from app.api.embeddings import generate_embedding, cosine_similarity

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """Splits long text documents into overlapping semantic chunks."""
    words = text.split()
    if len(words) <= chunk_size:
        return [text]
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

def calculate_dense_similarity(query: str, documents: List[str]) -> List[Dict[str, Any]]:
    """Calculates dense vector embedding similarity scores for documents against a query."""
    query_vec = generate_embedding(query)
    if not documents:
        return []

    results = []
    for doc in documents:
        doc_vec = generate_embedding(doc)
        score = cosine_similarity(query_vec, doc_vec)
        results.append({"text": doc, "score": score})

    results.sort(key=lambda x: x["score"], reverse=True)
    return results

def query_rag_context(prompt: str, document_chunks: List[str], top_k: int = 3) -> str:
    """Retrieves top_k relevant context chunks using dense vector embedding search."""
    if not document_chunks:
        return ""
    ranked = calculate_dense_similarity(prompt, document_chunks)
    top_chunks = [r["text"] for r in ranked[:top_k] if r["score"] > 0.1]
    if not top_chunks:
        return ""
    return "\n\n---\n**RAG Vector Search Context:**\n" + "\n---\n".join(top_chunks) + "\n---\n"
