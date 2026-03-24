from __future__ import annotations

from prompt_poetry.core import Transform

_DEFAULT_META = (
    "Before executing the task below, first rewrite it as a clearer, "
    "more specific prompt that will produce the best possible result. "
    "Then execute your improved version."
)


class _MetaTransform(Transform):
    def __init__(self, instruction: str | None = None):
        self.instruction = instruction or _DEFAULT_META

    def __call__(self, prompt: str) -> str:
        return f"{self.instruction}\n\nOriginal task:\n{prompt}"

    def __repr__(self) -> str:
        return "meta()" if self.instruction == _DEFAULT_META else f"meta({self.instruction!r})"


def meta(instruction: str | None = None) -> _MetaTransform:
    return _MetaTransform(instruction)
