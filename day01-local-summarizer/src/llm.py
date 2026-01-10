import json
import re
from typing import Any, Dict

import requests
from pydantic import ValidationError

from .schema import SummaryResult


OLLAMA_URL = "http://localhost:11434/api/generate"


def _extract_json(text: str) -> Dict[str, Any]:
  match = re.search(r"\{.*\}", text, re.DOTALL)
  if not match: 
    raise ValueError("No JSON object found in the text.")
  return json.loads(match.group(0))


def summarize_with_ollama(text: str, model: str = "llama3.2:1b") -> SummaryResult:
  prompt = f"""
You are a helpful assistant that analyzes logs or text.

Return ONLY valid JSON with this exact shape:
{{
  "summary": "string",
  "top_issues": ["string", "string"],
  "action_items": ["string", "string"],
  "severity": "low|medium|high"
}}

Rules:
- Do not include any extra keys.
- Do not include markdown or explanations.
- Keep summary under 3 lines.
- top_issues: 3 to 6 bullet-like strings
- action_items: 3 to 6 clear next steps

TEXT:
{text}
""".strip()

  payload = {
    "model": model,
    "prompt": prompt,
    "stream": False,
    "format": "json",
  }

  response = requests.post(OLLAMA_URL, json=payload, timeout=120)
  response.raise_for_status()
  data = response.json()
  print("Ollama response data:", data)

  raw_output = data.get("response", "")
  if not raw_output.strip():
    raise ValueError("Empty response from LLM")

  parsed = _extract_json(raw_output)

  try:
    return SummaryResult(**parsed)
  except ValidationError as e:
    raise ValueError(f"Response validation error: {e}")