"""
courses/ai.py
─────────────
AI Integration Placeholder Module for EduHub.

Replace the body of `generate_summary()` with your own text-summarization
logic (e.g. HuggingFace transformers, OpenAI API, or any custom pipeline).
"""


def generate_summary(text: str) -> str:
    """
    ┌─────────────────────────────────────────────────────────┐
    │  AI PLACEHOLDER — plug your summarisation model here.   │
    │                                                         │
    │  Input:  `text`  — the full lesson content (str)        │
    │  Output: a concise summary string                       │
    │                                                         │
    │  Example integration with HuggingFace:                  │
    │                                                         │
    │    from transformers import pipeline                     │
    │    summariser = pipeline("summarization",               │
    │                          model="facebook/bart-large-cnn")│
    │    result = summariser(text,                             │
    │                        max_length=130,                   │
    │                        min_length=30,                    │
    │                        do_sample=False)                  │
    │    return result[0]["summary_text"]                      │
    └─────────────────────────────────────────────────────────┘
    """
    # ── Default: first 200 chars as a naive summary ─────────
    if not text:
        return ""
    return text[:200].rsplit(" ", 1)[0] + "…" if len(text) > 200 else text
