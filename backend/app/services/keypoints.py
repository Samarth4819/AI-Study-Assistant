from __future__ import annotations

from app.services.llm_client import generate_json


def extract_key_points(text: str, max_points: int = 5) -> list[str]:
    """Extract key points from text.

    This baseline strategy picks informative lines/sentences.
    Replace this with embeddings, LLM prompts, or keyword ranking for better results.
    """
    clean_text = " ".join(text.split())
    if not clean_text:
        return ["No key points could be extracted from the provided text."]

    # Preferred path: use LLM extraction for stronger relevance and phrasing.
    llm_payload = generate_json(
        system_prompt=(
            "You extract high-signal learning takeaways from educational content. "
            "Return strict JSON only. Use engaging and aesthetic language."
        ),
        user_prompt=(
            "Extract the most important concepts from the following text. "
            f"Return JSON with shape: {{\"key_points\": [string, ...]}} and include {max_points} points. "
            "Each point should be one concise sentence and start with a highly relevant, aesthetic emoji.\n\n"
            f"TEXT:\n{clean_text}"
        ),
        temperature=0.3,
    )

    if llm_payload and isinstance(llm_payload.get("key_points"), list):
        points = [str(p).strip() for p in llm_payload["key_points"] if str(p).strip()]
        if points:
            return points[:max_points]

    lines = [ln.strip(" -\t") for ln in text.splitlines() if ln.strip()]

    candidates: list[str] = []
    if lines:
        candidates = lines
    else:
        candidates = [s.strip() for s in text.split(".") if s.strip()]

    # Keep distinct points while preserving order.
    seen: set[str] = set()
    unique_points: list[str] = []
    for point in candidates:
        normalized = point.lower()
        if normalized in seen:
            continue
        seen.add(normalized)
        unique_points.append(point)
        if len(unique_points) >= max_points:
            break

    if not unique_points:
        return ["No key points could be extracted from the provided text."]

    return unique_points
