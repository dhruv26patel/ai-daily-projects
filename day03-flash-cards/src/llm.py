import json
import re
from typing import Any, Dict

import requests
from pydantic import ValidationError

from .schema import TopicSummaryResult

OLLAMA_URL = "http://localhost:11434/api/generate"


def _extract_json(text: str) -> Dict[str, Any]:
    """
    Find the first JSON object in a string and return it as a dict.
    """
    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in the model output.")
    return json.loads(match.group(0))


def summarize_with_ollama(text: str, model: str = "llama3.2:1b") -> TopicSummaryResult:
    """
    Call Ollama locally and return a validated TopicSummaryResult.
    """
    prompt = f"""
You extract topics and create flash cards from text.

Return ONLY a single JSON object.
No extra text. No markdown. No explanations.

Top-level JSON MUST have EXACTLY these keys:
- topic
- flash_cards

Each item in flash_cards MUST be an object with EXACTLY these keys:
- question
- answer
- difficulty

Rules:
- topics must be a list of strings summarizing main topics
- question and answer must be non-empty strings
- question should be concise and clear
- answer should be accurate and to the point
- difficulty must be one of: easy, medium, hard

Example (follow exactly):
{{
  "topics": ["string"],
  "flash_cards": [
    {{
      "question": "What is Redis?",
      "answer": "Redis is an in-memory data structure store.",
      "difficulty": "easy"
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
    allowed_top_keys = {"topics", "flash_cards"}
    parsed = {k: v for k, v in parsed.items() if k in allowed_top_keys}

    try:
        return TopicSummaryResult(**parsed)
    except ValidationError as e:
        raise ValueError(f"Response validation error: {e}") from e
