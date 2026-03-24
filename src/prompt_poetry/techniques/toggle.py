from __future__ import annotations

from prompt_poetry.core import Transform

_TOGGLES: dict[str, dict[str, str]] = {
    "verbosity": {
        "high": "Explain thoroughly and in detail.",
        "low": "Be concise and brief. Minimum words, maximum signal.",
    },
    "creativity": {
        "high": "Be bold, surprising, and unconventional. Prefer novel approaches.",
        "low": "Be precise and conventional. Stick to proven approaches.",
    },
    "confidence": {
        "commit": "Pick the best option and commit to it. No hedging.",
        "explore": "List multiple options with trade-offs. Don't commit yet.",
    },
    "voice": {
        "casual": "Write like you talk. Direct, informal, no corporate language.",
        "formal": "Write formally and professionally.",
    },
    "depth": {
        "deep": "Go deep. Thorough analysis, comprehensive coverage, no shortcuts.",
        "surface": "High-level summary only. Skip the details.",
    },
}


class _ToggleTransform(Transform):
    def __init__(self, settings: dict[str, str]):
        self.settings = settings

    def __call__(self, prompt: str) -> str:
        instructions = []
        for dimension, value in self.settings.items():
            if dimension in _TOGGLES and value in _TOGGLES[dimension]:
                instructions.append(_TOGGLES[dimension][value])
            else:
                instructions.append(f"{dimension}: {value}.")
        block = " ".join(instructions)
        return f"{block}\n\n{prompt}"

    def __repr__(self) -> str:
        pairs = ", ".join(f"{k}={v!r}" for k, v in self.settings.items())
        return f"toggle({pairs})"


def toggle(**settings: str) -> _ToggleTransform:
    return _ToggleTransform(settings)
