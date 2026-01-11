import json
import re
from typing import Any, Dict

import requests
from pydantic import ValidationError

from .schema import SummaryResult

OLLAMA_URL = "http://localhost:11434/api/generate"


def _extract_json(text: str) -> Dict[str, Any]:
    """
    Find the first JSON object in a string and return it as a dict.
    """
    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in the model output.")
    return json.loads(match.group(0))


def summarize_with_ollama(text: str, model: str = "llama3.2:1b") -> SummaryResult:
    """
    Call Ollama locally and return a validated SummaryResult.
    """
    prompt = f"""
You extract action items from notes.

Return ONLY a single JSON object.
No extra text. No markdown. No explanations.

Top-level JSON MUST have EXACTLY these keys:
- summary
- action_items

Each item in action_items MUST be an object with EXACTLY these keys:
- task
- owner
- priority
- due_date

Rules:
- priority must be one of: low, medium, high
- due_date must be 'unknown' OR in YYYY-MM-DD format
- owner must be 'unknown' OR a person's name

Example (follow exactly):
{{
  "summary": "string",
  "action_items": [
    {{
      "task": "Investigate Redis slowness",
      "owner": "John Doe",
      "priority": "high",
      "due_date": "unknown"
    }}
  ]
}}

TEXT:
{text}
""".strip()

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }

    resp = requests.post(OLLAMA_URL, json=payload, timeout=120)
    resp.raise_for_status()
    data = resp.json()

    # Optional debug print
    print("Ollama response data:", data)

    raw_output = data.get("response", "")
    if not raw_output.strip():
        raise ValueError("Empty response from Ollama.")

    parsed = _extract_json(raw_output)

    # Safety: drop accidental extra top-level keys if the model adds them
    allowed_top_keys = {"summary", "action_items"}
    parsed = {k: v for k, v in parsed.items() if k in allowed_top_keys}

    try:
        return SummaryResult(**parsed)
    except ValidationError as e:
        raise ValueError(f"Response validation error: {e}") from e
