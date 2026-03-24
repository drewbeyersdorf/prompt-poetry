"""Tests for all presets — engineering, business, and knowledge."""

from prompt_poetry.presets import (
    # Engineering
    analyst, debugger, writer, researcher, evaluator,
    # Business
    briefer, ops_reviewer, meeting_prep, customer_responder, financial_analyst,
    # Knowledge
    rag_strict, summarizer,
)
from prompt_poetry.core import Transform, Pipeline


# --- Engineering presets ---

def test_analyst_is_pipeline():
    assert isinstance(analyst, (Transform, Pipeline))


def test_debugger_is_pipeline():
    assert isinstance(debugger, (Transform, Pipeline))


def test_writer_is_pipeline():
    assert isinstance(writer, (Transform, Pipeline))


def test_researcher_is_pipeline():
    assert isinstance(researcher, (Transform, Pipeline))


def test_evaluator_is_pipeline():
    assert isinstance(evaluator, (Transform, Pipeline))


def test_analyst_produces_output():
    result = analyst("What's our revenue trend?")
    assert "What's our revenue trend?" in result
    assert len(result) > len("What's our revenue trend?")


def test_debugger_produces_output():
    result = debugger("Why is this test failing?")
    assert "Why is this test failing?" in result


def test_presets_are_composable():
    from prompt_poetry.techniques import constrain
    custom = analyst | constrain("under 50 words")
    result = custom("Analyze this")
    assert "Analyze this" in result
    assert "under 50 words" in result


# --- Business presets ---

def test_briefer_is_pipeline():
    assert isinstance(briefer, (Transform, Pipeline))


def test_briefer_output():
    result = briefer("What's the status of the vendor negotiation?")
    assert "vendor negotiation" in result
    assert any(word in result.lower() for word in ["conclusion", "briefing", "lead"])


def test_ops_reviewer_is_pipeline():
    assert isinstance(ops_reviewer, (Transform, Pipeline))


def test_ops_reviewer_output():
    result = ops_reviewer("Review last week's delivery performance")
    assert "delivery performance" in result
    assert "action items" in result.lower()


def test_meeting_prep_is_pipeline():
    assert isinstance(meeting_prep, (Transform, Pipeline))


def test_meeting_prep_output():
    result = meeting_prep("Prep for the Q4 planning meeting")
    assert "Q4 planning meeting" in result
    assert any(word in result.lower() for word in ["key points", "decision", "owns"])


def test_customer_responder_is_pipeline():
    assert isinstance(customer_responder, (Transform, Pipeline))


def test_customer_responder_output():
    result = customer_responder("Customer reported missing items in their order")
    assert "missing items" in result
    assert any(word in result.lower() for word in ["acknowledge", "next step"])


def test_financial_analyst_is_pipeline():
    assert isinstance(financial_analyst, (Transform, Pipeline))


def test_financial_analyst_output():
    result = financial_analyst("What's the P&L impact of the new shipping contract?")
    assert "shipping contract" in result
    assert any(word in result.lower() for word in ["dollar", "p&l", "assumptions"])


# --- Knowledge presets ---

def test_rag_strict_is_pipeline():
    assert isinstance(rag_strict, (Transform, Pipeline))


def test_rag_strict_has_anti_hallucination():
    result = rag_strict("What was revenue last quarter?")
    assert "revenue last quarter" in result
    # Should contain anti-hallucination rules
    assert any(word in result.lower() for word in ["only use", "context", "cite", "guessing"])


def test_summarizer_is_pipeline():
    assert isinstance(summarizer, (Transform, Pipeline))


def test_summarizer_output():
    result = summarizer("Summarize the board meeting notes")
    assert "board meeting notes" in result
    assert any(word in result.lower() for word in ["under 150", "facts", "numbers"])


# --- All presets produce non-empty output ---

def test_all_presets_produce_output():
    """Every preset should return a string longer than the input."""
    presets = [
        analyst, debugger, researcher, evaluator, writer,
        briefer, ops_reviewer, meeting_prep, customer_responder, financial_analyst,
        rag_strict, summarizer,
    ]
    for preset in presets:
        result = preset("test input")
        assert isinstance(result, str)
        assert len(result) > len("test input"), f"Preset {preset!r} didn't enhance"
