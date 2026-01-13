import argparse
from pathlib import Path
from typing import List, Dict, Any

from .embedder import embed_text
from .store import save_index, load_index
from .search import top_k


DEFAULT_NOTES_DIR = Path("data/notes")
DEFAULT_INDEX_PATH = Path("store/index.json")


def read_all_note_files(notes_dir: Path) -> List[Path]:
    return sorted([p for p in notes_dir.glob("*.txt") if p.is_file()])


def build_index(notes_dir: Path, index_path: Path, model: str) -> None:
    files = read_all_note_files(notes_dir)
    if not files:
        raise RuntimeError(f"No .txt files found in {notes_dir}")

    items: List[Dict[str, Any]] = []
    for f in files:
        text = f.read_text(encoding="utf-8").strip()
        if not text:
            continue

        emb = embed_text(text, model=model)
        items.append({
            "file_path": str(f),
            "text": text,
            "embedding": emb,
        })

    save_index(index_path, items)
    print(f"Indexed {len(items)} files → {index_path}")


def run_query(index_path: Path, query: str, model: str, k: int) -> None:
    items = load_index(index_path)
    if not items:
        raise RuntimeError("Index is empty. Run `index` first.")

    q_emb = embed_text(query, model=model)
    results = top_k(q_emb, items, k=k)

    print("\n=== TOP MATCHES ===")
    for rank, (score, item) in enumerate(results, 1):
        print(f"\n{rank}) {item['file_path']}")
        print(f"   score: {score:.4f}")
        preview = item["text"].splitlines()[0][:120]
        print(f"   preview: {preview}")


def main():
    parser = argparse.ArgumentParser(description="Day 04: Local Semantic Search (Ollama embeddings)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_index = sub.add_parser("index", help="Build embeddings index from notes folder")
    p_index.add_argument("--notes_dir", default=str(DEFAULT_NOTES_DIR))
    p_index.add_argument("--index_path", default=str(DEFAULT_INDEX_PATH))
    p_index.add_argument("--model", default="nomic-embed-text")

    p_query = sub.add_parser("query", help="Search notes using a query")
    p_query.add_argument("--index_path", default=str(DEFAULT_INDEX_PATH))
    p_query.add_argument("--q", required=True, help="Query string")
    p_query.add_argument("--k", type=int, default=3)
    p_query.add_argument("--model", default="nomic-embed-text")

    args = parser.parse_args()

    if args.cmd == "index":
        build_index(Path(args.notes_dir), Path(args.index_path), model=args.model)
    elif args.cmd == "query":
        run_query(Path(args.index_path), query=args.q, model=args.model, k=args.k)


if __name__ == "__main__":
    main()
