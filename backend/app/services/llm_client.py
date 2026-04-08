from __future__ import annotations

import json
import os
from typing import Any


MAX_INPUT_CHARS = 12000


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
    """Generate plain text using OpenAI if credentials are configured."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    try:
        from openai import OpenAI  # type: ignore

        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": _truncate_text(user_prompt)},
            ],
        )

        content = response.choices[0].message.content
        return (content or "").strip() or None
    except Exception:
        # Return None so caller can use deterministic fallback logic.
        return None


def generate_json(system_prompt: str, user_prompt: str, temperature: float = 0.2) -> dict[str, Any] | None:
    """Generate structured JSON using OpenAI if credentials are configured."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    try:
        from openai import OpenAI  # type: ignore

        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": _truncate_text(user_prompt)},
            ],
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content or ""
        return _extract_json(content)
    except Exception:
        return None
