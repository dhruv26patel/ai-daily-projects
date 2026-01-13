from typing import List, Dict, Any, Tuple
import numpy as np


def cosine_similarity(a: List[float], b: List[float]) -> float:
    """
    Cosine similarity = how close two vectors are (1.0 is very similar).
    """
    va = np.array(a, dtype=np.float32)
    vb = np.array(b, dtype=np.float32)

    denom = (np.linalg.norm(va) * np.linalg.norm(vb))
    if denom == 0:
        return 0.0

    return float(np.dot(va, vb) / denom)


def top_k(query_embedding: List[float], indexed_items: List[Dict[str, Any]], k: int = 3) -> List[Tuple[float, Dict[str, Any]]]:
    """
    Scores every indexed item vs the query embedding and returns top k matches.
    Returns: list of (score, item)
    """
    scored = []
    for item in indexed_items:
        score = cosine_similarity(query_embedding, item["embedding"])
        scored.append((score, item))

    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:k]
