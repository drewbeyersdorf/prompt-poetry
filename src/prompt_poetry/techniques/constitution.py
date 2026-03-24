from __future__ import annotations

from prompt_poetry.core import Transform


class _ConstitutionTransform(Transform):
    def __init__(self, role: str, rules: list[str] | None = None, values: list[str] | None = None):
        self.role = role
        self.rules = rules or []
        self.values = values or []

    def __call__(self, prompt: str) -> str:
        parts = [f"# Identity\nYou are {self.role}."]
        if self.rules:
            rules_block = "\n".join(f"- {r}" for r in self.rules)
            parts.append(f"\n# Rules\n{rules_block}")
        if self.values:
            values_block = "\n".join(f"- {v}" for v in self.values)
            parts.append(f"\n# Values\n{values_block}")
        parts.append(f"\n# Task\n{prompt}")
        return "\n".join(parts)

    def __repr__(self) -> str:
        return f"constitution(role={self.role!r})"


def constitution(role: str, rules: list[str] | None = None, values: list[str] | None = None) -> _ConstitutionTransform:
    return _ConstitutionTransform(role, rules, values)
