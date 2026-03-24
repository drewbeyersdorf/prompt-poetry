from __future__ import annotations

from prompt_poetry.core import Transform

_PRIMERS: dict[str, str] = {
    "urgency": "This is critical and time-sensitive. Prioritize accuracy and speed. Every detail matters immediately.",
    "precision": "Be meticulous and exact. Double-check every claim. Rigorous accuracy is non-negotiable.",
    "creativity": "Think boldly and unconventionally. Explore unexpected angles. The novel approach is preferred over the safe one.",
    "calm": "Take your time. Think carefully and thoroughly. There is no rush — depth matters more than speed.",
    "confidence": "Be decisive. Commit to your best judgment. State conclusions directly, not as possibilities.",
}


class _PrimerTransform(Transform):
    def __init__(self, mood: str):
        self.mood = mood
        self.text = _PRIMERS.get(mood, f"Approach this with a sense of {mood}.")

    def __call__(self, prompt: str) -> str:
        return f"{self.text}\n\n{prompt}"

    def __repr__(self) -> str:
        return f"prime({self.mood!r})"


def prime(mood: str) -> _PrimerTransform:
    return _PrimerTransform(mood)
