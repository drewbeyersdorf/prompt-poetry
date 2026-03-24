from __future__ import annotations

from prompt_poetry.core import Transform


class _ConstraintTransform(Transform):
    def __init__(self, constraints: tuple[str, ...]):
        self.constraints = constraints

    def __call__(self, prompt: str) -> str:
        constraint_block = "\n".join(f"- {c}" for c in self.constraints)
        return f"{prompt}\n\nConstraints:\n{constraint_block}"

    def __repr__(self) -> str:
        return f"constrain({', '.join(repr(c) for c in self.constraints)})"


def constrain(*constraints: str) -> _ConstraintTransform:
    return _ConstraintTransform(constraints)
