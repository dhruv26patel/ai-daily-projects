import requests
from typing import List

OLLAMA_EMBED_URL = "http://localhost:11434/api/embeddings"


def embed_text(text: str, model: str = "nomic-embed-text") -> List[float]:
    """
    Sends text to Ollama's embedding endpoint and returns a vector (list of floats).
    """
    payload = {"model": model, "prompt": text}
    resp = requests.post(OLLAMA_EMBED_URL, json=payload, timeout=120)
    resp.raise_for_status()

    data = resp.json()

    # Ollama returns: {"embedding": [0.1, 0.2, ...]}
    embedding = data.get("embedding")
    if not embedding:
        raise RuntimeError("No embedding returned from Ollama.")
    return embedding
