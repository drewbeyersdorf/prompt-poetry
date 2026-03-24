"""Pre-built technique pipelines for common task types.

Each preset is a ready-to-use Pipeline. Import and call directly,
or extend with | to add more techniques.

    from prompt_poetry.presets import analyst
    result = analyst("What's driving the cost increase?")

    # Extend a preset
    custom = analyst | constrain("under 50 words")
"""

from prompt_poetry.techniques import (
    persona, prime, constrain, ritual, meta, narrative, toggle, constitution,
)

# ---------------------------------------------------------------------------
# Engineering
# ---------------------------------------------------------------------------

#: Data analysis — commits to answers, goes deep, cites evidence.
analyst = persona("senior data analyst") | toggle(confidence="commit", depth="deep") | constrain("cite specific numbers and evidence")

#: Debugging — systematic, precise, root-cause focused.
debugger = persona("principal engineer specializing in debugging") | ritual("step by step") | prime("precision") | constrain("identify root cause only, not symptoms")

#: Research — thorough, creative, case-study framing.
researcher = persona("investigative researcher") | narrative("case study") | toggle(depth="deep", creativity="high")

#: Evaluation — precise scoring, no hedging.
evaluator = persona("quality auditor") | prime("precision") | ritual("score each dimension explicitly") | toggle(confidence="commit")

#: Writing — casual voice, creative, no jargon.
writer = persona("direct communicator who writes like they talk") | toggle(voice="casual", creativity="high") | constrain("no jargon, no corporate language")

# ---------------------------------------------------------------------------
# Business / Operations
# ---------------------------------------------------------------------------

#: Executive briefing — conclusion first, then evidence, then recommendation.
briefer = persona("executive briefer") | narrative("briefing") | toggle(confidence="commit", depth="surface") | constrain("lead with the conclusion", "under 200 words")

#: Operations review — systematic, numbers-driven, action-oriented.
ops_reviewer = persona("operations manager") | prime("precision") | ritual("enumerate") | constrain("cite specific metrics", "end with action items")

#: Meeting prep — structured, time-efficient, decision-focused.
meeting_prep = persona("chief of staff preparing an executive for a meeting") | narrative("briefing") | constrain("3-5 key points", "flag open decisions", "note who owns what")

#: Customer response — empathetic but precise, solution-oriented.
customer_responder = persona("senior customer success manager") | prime("calm") | toggle(voice="casual", confidence="commit") | constrain("acknowledge the issue first", "propose a concrete next step")

#: Financial analysis — conservative, evidence-based, P&L-focused.
financial_analyst = persona("senior financial analyst") | prime("precision") | ritual("show reasoning") | toggle(confidence="commit") | constrain("cite dollar amounts", "calculate P&L impact", "flag assumptions")

# ---------------------------------------------------------------------------
# Knowledge / RAG
# ---------------------------------------------------------------------------

#: Anti-hallucination RAG — strict sourcing, explicit uncertainty.
rag_strict = constitution(
    role="knowledge assistant",
    rules=[
        "ONLY use information from the provided context",
        "If context is insufficient, say so rather than guessing",
        "Cite every claim with [N] references",
        "Never attribute quotes without source evidence",
    ],
) | prime("precision") | ritual("show reasoning")

#: Summarizer — compress without losing signal.
summarizer = persona("expert summarizer") | toggle(depth="surface") | constrain("preserve key numbers and names", "no opinions, only facts", "under 150 words")

__all__ = [
    # Engineering
    "analyst", "debugger", "researcher", "evaluator", "writer",
    # Business
    "briefer", "ops_reviewer", "meeting_prep", "customer_responder", "financial_analyst",
    # Knowledge
    "rag_strict", "summarizer",
]
