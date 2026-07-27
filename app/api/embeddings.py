# app/api/embeddings.py — Dense Vector Embeddings Engine & Cosine Similarity
import math, re
from typing import List

def generate_embedding(text: str, dim: int = 16) -> List[float]:
    """
    Generates a normalized dense vector embedding for input text.
    """
    tokens = re.findall(r'\w+', text.lower())
    if not tokens:
        return [0.0] * dim

    vec = [0.0] * dim
    for idx, token in enumerate(tokens):
        h = sum(ord(c) for c in token)
        slot = h % dim
        vec[slot] += 1.0

    # L2 normalize vector
    magnitude = math.sqrt(sum(v * v for v in vec))
    if magnitude > 0:
        vec = [v / magnitude for v in vec]
    return vec

def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Computes cosine similarity score between two dense vectors."""
    if len(vec1) != len(vec2):
        return 0.0
    dot = sum(a * b for a, b in zip(vec1, vec2))
    mag1 = math.sqrt(sum(a * a for a in vec1))
    mag2 = math.sqrt(sum(b * b for b in vec2))
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot / (mag1 * mag2)
