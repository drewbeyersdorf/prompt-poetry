"""Example: build your own techniques.

prompt-poetry is extensible. Subclass Transform to create custom
techniques that compose with everything else via the pipe operator.
"""

from prompt_poetry.core import Transform


class Audience(Transform):
    """Tailor output for a specific audience."""

    def __init__(self, who: str, level: str = "intermediate"):
        self.who = who
        self.level = level

    def __call__(self, prompt: str) -> str:
        return (
            f"Your audience is {self.who} with {self.level}-level knowledge. "
            f"Adjust complexity and examples accordingly.\n\n{prompt}"
        )

    def __repr__(self) -> str:
        return f"Audience({self.who!r})"


class Format(Transform):
    """Force a specific output format."""

    def __init__(self, fmt: str):
        self.fmt = fmt
        self._templates = {
            "json": "Return your response as valid JSON.",
            "markdown": "Format your response as clean markdown with headers.",
            "bullet": "Use bullet points. No paragraphs.",
            "table": "Present data in a markdown table.",
            "oneliner": "Answer in exactly one sentence.",
        }

    def __call__(self, prompt: str) -> str:
        instruction = self._templates.get(self.fmt, f"Format: {self.fmt}")
        return f"{prompt}\n\n{instruction}"

    def __repr__(self) -> str:
        return f"Format({self.fmt!r})"


# Use them with built-in techniques
if __name__ == "__main__":
    from prompt_poetry import persona, prime

    # Custom technique composes with built-ins
    pipeline = (
        persona("senior engineer")
        | Audience("junior developers", level="beginner")
        | prime("calm")
        | Format("bullet")
    )

    result = pipeline("Explain how database indexes work")
    print(result)
