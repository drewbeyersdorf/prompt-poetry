from __future__ import annotations

from prompt_poetry.core import Transform

_RITUALS: dict[str, str] = {
    "step by step": "Think through this step by step. Show each stage of your reasoning before reaching a conclusion.",
    "show reasoning": "Show your reasoning explicitly. State what you observe, what you infer, and why, before giving your answer.",
    "enumerate": "First, list all relevant factors. Then evaluate each one. Only then draw your conclusion.",
    "devil's advocate": "Before answering, argue the opposite position. Then reconcile both views into your final answer.",
}


class _RitualTransform(Transform):
    def __init__(self, ritual_type: str):
        self.ritual_type = ritual_type
        self.text = _RITUALS.get(ritual_type, f"Before answering: {ritual_type}.")

    def __call__(self, prompt: str) -> str:
        return f"{self.text}\n\n{prompt}"

    def __repr__(self) -> str:
        return f"ritual({self.ritual_type!r})"


def ritual(ritual_type: str) -> _RitualTransform:
    return _RitualTransform(ritual_type)
