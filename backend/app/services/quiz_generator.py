from __future__ import annotations

import random

from app.services.llm_client import generate_json


DEFAULT_OPTIONS = [
    "All of the above",
    "Only the first statement is true",
    "Only the second statement is true",
    "None of the above",
]


def generate_quiz(text: str, num_questions: int = 5) -> list[dict]:
    """Generate multiple-choice quiz questions from text.

    This placeholder creates basic MCQs from extracted statements.
    For production quality, use an LLM prompt or a dedicated QA generation model.
    """
    clean_text = " ".join(text.split())

    # Preferred path: generate pedagogically strong MCQs using an LLM.
    llm_payload = generate_json(
        system_prompt=(
            "You create high-quality multiple-choice quizzes for study revision. "
            "Return strict JSON only."
        ),
        user_prompt=(
            "Create a quiz from this material. Return JSON with shape: "
            "{\"quiz\": [{\"question\": string, \"options\": [string, string, string, string], \"answer\": string}]}. "
            f"Generate {num_questions} questions. Rules: exactly 4 options per question, one correct answer, "
            "plausible distractors, no trick wording, and answer must be one of the options.\n\n"
            f"TEXT:\n{clean_text}"
        ),
        temperature=0.3,
    )

    if llm_payload and isinstance(llm_payload.get("quiz"), list):
        cleaned_quiz: list[dict] = []
        for item in llm_payload["quiz"]:
            if not isinstance(item, dict):
                continue
            question = str(item.get("question", "")).strip()
            options_raw = item.get("options", [])
            answer = str(item.get("answer", "")).strip()

            if not question or not isinstance(options_raw, list):
                continue

            options = [str(opt).strip() for opt in options_raw if str(opt).strip()]
            if len(options) < 4:
                continue

            options = options[:4]
            if answer not in options:
                continue

            cleaned_quiz.append(
                {
                    "question": question,
                    "options": options,
                    "answer": answer,
                }
            )

            if len(cleaned_quiz) >= num_questions:
                break

        if cleaned_quiz:
            return cleaned_quiz

    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if len(s.strip()) > 20]

    if not sentences:
        return [
            {
                "question": "What is the main topic of the provided content?",
                "options": [
                    "The text was empty or too short",
                    "A detailed scientific paper",
                    "A historical timeline",
                    "A cooking recipe",
                ],
                "answer": "The text was empty or too short",
            }
        ]

    random.shuffle(sentences)
    selected = sentences[:num_questions]

    quiz: list[dict] = []
    for statement in selected:
        question = f"Which option best matches this statement: '{statement[:80]}...'?"

        # Use one correct paraphrase + generic distractors as starter logic.
        correct_answer = f"It refers to: {statement[:60]}..."
        options = [correct_answer] + DEFAULT_OPTIONS[:]
        random.shuffle(options)

        quiz.append(
            {
                "question": question,
                "options": options,
                "answer": correct_answer,
            }
        )

    return quiz
