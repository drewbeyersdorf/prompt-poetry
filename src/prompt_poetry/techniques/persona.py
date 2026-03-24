from __future__ import annotations

from prompt_poetry.core import Transform


class _PersonaTransform(Transform):
    def __init__(self, identity: str, context: str | None = None):
        self.identity = identity
        self.context = context

    def __call__(self, prompt: str) -> str:
        parts = [f"You are a {self.identity}."]
        if self.context:
            parts.append(f"Your area of focus: {self.context}.")
        parts.append("")
        parts.append(prompt)
        return "\n".join(parts)

    def __repr__(self) -> str:
        if self.context:
            return f"persona({self.identity!r}, context={self.context!r})"
        return f"persona({self.identity!r})"


def persona(identity: str, context: str | None = None) -> _PersonaTransform:
    return _PersonaTransform(identity, context)
