from __future__ import annotations

import json
import os
from typing import Any

# Gemini 2.5 Flash has a large context window, so we can support more text.
MAX_INPUT_CHARS = 100000


def _truncate_text(text: str) -> str:
    """Trim overly large inputs to keep latency/cost predictable."""
    text = " ".join(text.split())
    if len(text) <= MAX_INPUT_CHARS:
        return text
    return text[:MAX_INPUT_CHARS] + " ...[truncated]"


def _extract_json(text: str) -> dict[str, Any] | None:
    """Best-effort extraction for JSON that may be wrapped in markdown."""
    text = text.strip()

    # Handle fenced blocks like ```json ... ```
    if text.startswith("```"):
        text = text.strip("`")
        text = text.replace("json", "", 1).strip()

    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            return parsed
        return None
    except json.JSONDecodeError:
        pass

    # Fallback: parse the outermost object if extra text is included.
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None

    try:
        parsed = json.loads(text[start : end + 1])
        if isinstance(parsed, dict):
            return parsed
        return None
    except json.JSONDecodeError:
        return None


def generate_text(system_prompt: str, user_prompt: str, temperature: float = 0.2) -> str | None:
    """Generate plain text using Gemini if credentials are configured."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None

    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=model,
            contents=_truncate_text(user_prompt),
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=temperature,
            ),
        )

        content = response.text
        return (content or "").strip() or None
    except Exception as e:
        print(f"Gemini API Error: {e}")
        # Return None so caller can use deterministic fallback logic.
        return None


def generate_json(system_prompt: str, user_prompt: str, temperature: float = 0.2) -> dict[str, Any] | None:
    """Generate structured JSON using Gemini if credentials are configured."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None

    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=model,
            contents=_truncate_text(user_prompt),
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=temperature,
                response_mime_type="application/json",
            ),
        )

        content = response.text or ""
        return _extract_json(content)
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return None
