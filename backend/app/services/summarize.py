from __future__ import annotations

import os

from app.services.llm_client import generate_text


def summarize_text(text: str) -> str:
    """Return a concise summary of the input text.

    This starter uses simple heuristics by default for a dependable local setup.
    To upgrade quality, replace this block with HuggingFace or OpenAI calls.
    """
    clean_text = " ".join(text.split())
    if not clean_text:
        return "No text provided."

    # Preferred path: use an LLM for high-quality, context-aware summarization.
    llm_summary = generate_text(
        system_prompt=(
            "You are an expert academic assistant. Write clear, accurate summaries "
            "with no hallucinations. Use an aesthetic markdown format with appropriate emojis."
        ),
        user_prompt=(
            "Summarize the following study material in 1 elegantly formatted paragraph, then add "
            "3 concise bullet points titled '✨ Key Highlights ✨'. Make it visually engaging and aesthetic.\n\n"
            f"STUDY MATERIAL:\n{clean_text}"
        ),
        temperature=0.4,
    )
    if llm_summary:
        return llm_summary

    use_transformers = os.getenv("USE_TRANSFORMERS", "false").lower() == "true"

    if use_transformers:
        # Optional NLP path:
        # 1) Install transformers + torch
        # 2) Use a summarization pipeline model (e.g. facebook/bart-large-cnn)
        # 3) Return model output text
        try:
            from transformers import pipeline  # type: ignore

            summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
            output = summarizer(clean_text, max_length=140, min_length=50, do_sample=False)
            return output[0]["summary_text"]
        except Exception:
            # Fallback avoids crashing if model download is unavailable.
            pass

    # Heuristic fallback: take the first few sentences as a concise summary.
    sentences = [s.strip() for s in clean_text.replace("\n", " ").split(".") if s.strip()]
    summary = ". ".join(sentences[:3])
    if summary and not summary.endswith("."):
        summary += "."
    return summary or clean_text[:300]
