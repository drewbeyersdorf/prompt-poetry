"""Example: auto-select techniques for an agent system.

Classify tasks by keyword, apply the right preset automatically.
This is how you'd integrate prompt-poetry into a multi-agent framework.
"""

import re
from prompt_poetry.presets import analyst, debugger, researcher, evaluator, writer
from prompt_poetry import persona, prime, constrain, ritual, toggle

# Pattern → preset mapping (first match wins)
TASK_PATTERNS = [
    (re.compile(r"\b(debug|fix|bug|error|fail|crash)\b", re.I), debugger),
    (re.compile(r"\b(build|implement|create|add|code)\b", re.I),
     persona("senior engineer") | prime("precision") | ritual("step by step") | constrain("write tests first")),
    (re.compile(r"\b(write|draft|compose|blog|post)\b", re.I), writer),
    (re.compile(r"\b(review|audit|evaluate|score)\b", re.I), evaluator),
    (re.compile(r"\b(research|investigate|explore)\b", re.I), researcher),
    (re.compile(r"\b(analyze|data|metric|trend|report)\b", re.I), analyst),
]

DEFAULT = prime("precision") | toggle(confidence="commit", depth="deep")


def enhance(task: str) -> str:
    """Auto-enhance a task prompt based on keywords."""
    for pattern, preset in TASK_PATTERNS:
        if pattern.search(task):
            return preset(task)
    return DEFAULT(task)


if __name__ == "__main__":
    tasks = [
        "Debug why the API returns 500 on /users",
        "Research how Stripe handles webhook retries",
        "Analyze customer churn by cohort",
        "Write a launch announcement for v2",
        "Build a rate limiter middleware",
    ]

    for task in tasks:
        print(f"{'─' * 60}")
        print(f"TASK: {task}")
        print(f"{'─' * 60}")
        enhanced = enhance(task)
        # Show just the first 3 lines of enhancement
        lines = enhanced.strip().split("\n")
        preview = "\n".join(lines[:3])
        print(f"{preview}")
        if len(lines) > 3:
            print(f"  ... ({len(lines) - 3} more lines)")
        print()
