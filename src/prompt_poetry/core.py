"""Core abstractions: Transform and Pipeline."""

from __future__ import annotations


class Transform:
    """A prompt transform — takes a string, returns an enhanced string.

    Subclass and implement __call__ to create a technique.
    Compose with | (pipe operator) to chain techniques.
    """

    def __call__(self, prompt: str) -> str:
        raise NotImplementedError


class Pipeline(Transform):
    """A chain of transforms applied left to right."""
    pass
