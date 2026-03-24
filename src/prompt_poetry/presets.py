from prompt_poetry.techniques import (
    persona, prime, constrain, ritual, narrative, toggle, constitution,
)

analyst = persona("senior data analyst") | toggle(confidence="commit", depth="deep") | constrain("cite specific numbers and evidence")
debugger = persona("principal engineer specializing in debugging") | ritual("step by step") | prime("precision") | constrain("identify root cause only, not symptoms")
researcher = persona("investigative researcher") | narrative("case study") | toggle(depth="deep", creativity="high")
evaluator = persona("quality auditor") | prime("precision") | ritual("score each dimension explicitly") | toggle(confidence="commit")
writer = persona("direct communicator who writes like they talk") | toggle(voice="casual", creativity="high") | constrain("no jargon, no corporate language")

__all__ = ["analyst", "debugger", "researcher", "evaluator", "writer"]
