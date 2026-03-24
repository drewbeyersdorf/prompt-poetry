"""Core abstractions: Transform and Pipeline."""

from __future__ import annotations


class Transform:
    """A prompt transform — takes a string, returns an enhanced string.

    Subclass and implement __call__ to create a technique.
    Compose with | (pipe operator) to chain techniques.
    """

    def __call__(self, prompt: str) -> str:
        raise NotImplementedError

    def __or__(self, other: Transform) -> Pipeline:
        left = self.transforms if isinstance(self, Pipeline) else [self]
        right = other.transforms if isinstance(other, Pipeline) else [other]
        return Pipeline(left + right)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


class Pipeline(Transform):
    """A chain of transforms applied left to right."""

    def __init__(self, transforms: list[Transform] | None = None):
        self.transforms = transforms or []

    def __call__(self, prompt: str) -> str:
        result = prompt
        for t in self.transforms:
            result = t(result)
        return result

    def __repr__(self) -> str:
        names = [repr(t) for t in self.transforms]
        return f"Pipeline([{', '.join(names)}])"
