import argparse
import json
from pathlib import Path

from .llm import summarize_with_ollama


def main():
    """
    This is the command-line program.

    Example:
      python -m src.main --input data/sample_log.txt --model llama3.2:1b
    """
    parser = argparse.ArgumentParser(description="Local log/text summarizer using Ollama")
    parser.add_argument("--input", required=True, help="Path to input text file")
    parser.add_argument("--model", default="llama3.2:1b", help="Ollama model name")
    parser.add_argument("--out", default="out/result.json", help="Output JSON path")
    args = parser.parse_args()

    input_path = Path(args.input)
    out_path = Path(args.out)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    text = input_path.read_text(encoding="utf-8")

    result = summarize_with_ollama(text=text, model=args.model)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(result.model_dump_json(indent=2), encoding="utf-8")

    # Pretty terminal output (so it feels like a real tool)
    print("\n=== SUMMARY ===")
    print(result.summary)

    print("\n=== TOP ISSUES ===")
    for i, issue in enumerate(result.top_issues, 1):
        print(f"{i}. {issue}")

    print("\n=== ACTION ITEMS ===")
    for i, item in enumerate(result.action_items, 1):
        print(f"{i}. {item}")

    print(f"\n=== SEVERITY: {result.severity.upper()} ===")
    print(f"\nSaved JSON to: {out_path}\n")


if __name__ == "__main__":
    main()
