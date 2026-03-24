from __future__ import annotations

from prompt_poetry.core import Transform

_NARRATIVES: dict[str, str] = {
    "case study": "Approach this as a case study. Present the situation, analyze the factors, and deliver findings with evidence.",
    "scene": "Set the scene first. Describe what's happening, who's involved, and what's at stake before diving into analysis.",
    "parable": "Frame your answer as a lesson learned. What happened, what it teaches, and what to do differently.",
    "briefing": "Structure this as an executive briefing. Lead with the conclusion, then supporting evidence, then recommendations.",
    "postmortem": "Treat this as a postmortem. What happened, why, what was the impact, and what prevents recurrence.",
}


class _NarrativeTransform(Transform):
    def __init__(self, style: str):
        self.style = style
        self.text = _NARRATIVES.get(style, f"Frame your response as a {style}.")

    def __call__(self, prompt: str) -> str:
        return f"{self.text}\n\n{prompt}"

    def __repr__(self) -> str:
        return f"narrative({self.style!r})"


def narrative(style: str) -> _NarrativeTransform:
    return _NarrativeTransform(style)
