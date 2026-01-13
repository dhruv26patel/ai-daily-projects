import json
from pathlib import Path
from typing import Dict, List, Any


def save_index(path: Path, items: List[Dict[str, Any]]) -> None:
    """
    Saves a list of items to disk.
    Each item includes: file_path, text, embedding
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(items, indent=2), encoding="utf-8")


def load_index(path: Path) -> List[Dict[str, Any]]:
    """
    Loads the index from disk. Returns empty list if it doesn't exist.
    """
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))
