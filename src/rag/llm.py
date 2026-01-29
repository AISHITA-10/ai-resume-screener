from __future__ import annotations

import json
from typing import Any, Dict

import requests


class BaseLLM:
    def complete_json(self, *, system: str, user: str) -> Dict[str, Any]:
        raise NotImplementedError

    def complete_markdown(self, *, system: str, user: str) -> str:
        raise NotImplementedError


class OllamaLLM(BaseLLM):
    """
    Simple wrapper around a local Ollama server.
    Uses the /api/chat endpoint and returns the final message content.
    """

    def __init__(self, model: str = "llama3.1", base_url: str = "http://127.0.0.1:11434"):
        self._model = model
        self._base_url = base_url.rstrip("/")

    def _chat(self, *, system: str, user: str) -> str:
        url = f"{self._base_url}/api/chat"
        payload = {
            "model": self._model,
            "stream": False,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }
        resp = requests.post(url, json=payload, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        # Ollama's /api/chat returns {"message": {"role": "...", "content": "..."}, ...}
        return (data.get("message", {}) or {}).get("content", "") or ""

    def complete_markdown(self, *, system: str, user: str) -> str:
        return self._chat(system=system, user=user).strip()

    def complete_json(self, *, system: str, user: str) -> Dict[str, Any]:
        text = self._chat(system=system, user=user).strip()
        try:
            return json.loads(text)
        except Exception:
            # If the model doesn't strictly obey JSON, wrap as best-effort.
            return {"raw": text}

