"""Pre-built technique pipelines for common task types.

Each preset is a ready-to-use Pipeline. Import and call directly,
or extend with | to add more techniques.

    from prompt_poetry.presets import analyst
    result = analyst("What's driving the cost increase?")

    # Extend a preset
    custom = analyst | constrain("under 50 words")
"""

from prompt_poetry.techniques import (
    persona, prime, constrain, ritual, narrative, toggle,
)

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

__all__ = ["analyst", "debugger", "researcher", "evaluator", "writer"]
