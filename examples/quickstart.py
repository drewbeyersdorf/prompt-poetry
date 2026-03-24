#!/usr/bin/env python3
"""prompt-poetry in 60 seconds.

Run this file to see every technique in action:
    python examples/quickstart.py
"""

from prompt_poetry import persona, prime, constrain, ritual, meta, narrative, toggle, constitution
from prompt_poetry.presets import analyst, debugger, researcher, evaluator, writer


def section(title: str) -> None:
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}\n")


# --- 1. Single technique ---
section("1. SINGLE TECHNIQUE")
print("Just call it like a function:\n")
print(">>> persona('forensic accountant')('Review these invoices')")
print()
result = persona("forensic accountant")("Review these invoices")
print(result)

# --- 2. Pipe composition ---
section("2. PIPE COMPOSITION")
print("Chain techniques with |:\n")
print(">>> enhanced = persona('SRE') | prime('precision') | constrain('root cause only')")
print(">>> enhanced('Why is the API slow?')")
print()
enhanced = persona("SRE") | prime("precision") | constrain("root cause only")
print(enhanced("Why is the API slow?"))

# --- 3. Presets ---
section("3. PRESETS (ready to use)")
print("Five pre-built pipelines:\n")

for name, preset in [("analyst", analyst), ("debugger", debugger), ("researcher", researcher), ("evaluator", evaluator), ("writer", writer)]:
    result = preset("Example task for this preset")
    line_count = len(result.strip().split("\n"))
    first_line = result.strip().split("\n")[0][:70]
    print(f"  {name:12s} -> {first_line}...  ({line_count} lines)")

# --- 4. Real-world examples ---
section("4. REAL-WORLD EXAMPLES")

print("Anti-hallucination RAG:")
rag = constitution(
    role="knowledge assistant",
    rules=["only use provided context", "cite with [N]", "say 'I don't know' if unsure"]
) | prime("precision")
print(rag("What was our Q3 revenue?")[:150] + "...\n")

print("Meeting prep:")
prep = persona("executive briefer") | narrative("briefing") | constrain("3 key points", "under 100 words")
print(prep("Summarize the vendor negotiation status")[:150] + "...\n")

print("Code review:")
review = persona("senior engineer") | prime("precision") | ritual("enumerate") | constrain("cite file:line for each issue")
print(review("Review this PR for security issues")[:150] + "...\n")

# --- 5. Build your own ---
section("5. BUILD YOUR OWN")
print("Extend a preset:")
print(">>> custom = analyst | constrain('under 50 words')")
print()
custom = analyst | constrain("under 50 words")
result = custom("What's driving the cost increase?")
print(result)

section("DONE")
print("Full docs: https://github.com/drewbeyersdorf/prompt-poetry")
print("Install:   pip install git+https://github.com/drewbeyersdorf/prompt-poetry.git")
