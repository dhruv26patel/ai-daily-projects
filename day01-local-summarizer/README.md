# Day 01 — Local Summarizer CLI (Ollama)

This project is a simple AI Engineering mini-tool:
- Reads a text/log file
- Sends it to a local LLM via Ollama
- Gets back structured JSON (summary, issues, action items, severity)
- Saves output to `out/result.json`

## Prereqs
1) Install Ollama
2) Pull a small model:
   - `ollama pull llama3.2:1b`

Make sure Ollama is running.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
