"""Tests for core Transform and Pipeline."""

from prompt_poetry.core import Transform, Pipeline


class PrefixTransform(Transform):
    """Test helper — prepends a prefix."""

    def __init__(self, prefix: str):
        self.prefix = prefix

    def __call__(self, prompt: str) -> str:
        return f"{self.prefix}\n\n{prompt}"


class SuffixTransform(Transform):
    """Test helper — appends a suffix."""

    def __init__(self, suffix: str):
        self.suffix = suffix

    def __call__(self, prompt: str) -> str:
        return f"{prompt}\n\n{self.suffix}"


def test_transform_is_callable():
    t = PrefixTransform("Hello")
    result = t("World")
    assert result == "Hello\n\nWorld"


def test_pipe_two_transforms():
    a = PrefixTransform("First")
    b = SuffixTransform("Last")
    pipeline = a | b
    assert isinstance(pipeline, Pipeline)
    result = pipeline("Middle")
    assert result == "First\n\nMiddle\n\nLast"


def test_pipe_three_transforms():
    a = PrefixTransform("A")
    b = PrefixTransform("B")
    c = SuffixTransform("C")
    pipeline = a | b | c
    result = pipeline("X")
    assert "A" in result
    assert "B" in result
    assert "C" in result
    assert "X" in result


def test_pipeline_pipe_pipeline():
    p1 = PrefixTransform("A") | PrefixTransform("B")
    p2 = SuffixTransform("C") | SuffixTransform("D")
    combined = p1 | p2
    assert isinstance(combined, Pipeline)
    assert len(combined.transforms) == 4


def test_single_transform_callable():
    t = PrefixTransform("Only")
    assert t("input") == "Only\n\ninput"


def test_pipeline_preserves_order():
    a = PrefixTransform("FIRST")
    b = PrefixTransform("SECOND")
    pipeline = a | b
    result = pipeline("original")
    assert result.startswith("SECOND")
    assert "FIRST" in result
    assert result.endswith("original")


def test_empty_pipeline():
    p = Pipeline([])
    assert p("hello") == "hello"


def test_repr():
    a = PrefixTransform("A")
    b = SuffixTransform("B")
    pipeline = a | b
    r = repr(pipeline)
    assert "Pipeline" in r
