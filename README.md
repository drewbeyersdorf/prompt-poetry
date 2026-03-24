# prompt-poetry

Composable prompt engineering techniques for biohacking LLMs. Every word is a probability lever.

## Install

```bash
pip install -e .
```

## Usage

```python
from prompt_poetry import persona, prime, constrain, ritual

# Single technique
result = persona("senior data analyst")("What's our revenue trend?")

# Compose with pipe operator
enhanced = persona("systems architect") | prime("precision") | constrain("under 200 words")
result = enhanced("Design a caching layer")

# Pre-built presets
from prompt_poetry.presets import analyst, debugger, researcher

result = analyst("Why did deliveries spike last week?")
result = debugger("The labor ETL is producing NULL values")
```

## The 8 Techniques

| # | Technique | What it does | API |
|---|-----------|-------------|-----|
| 1 | **Persona** | Identity injection — tunes probability distributions | `persona("master craftsman")` |
| 2 | **Primer** | Emotional/tonal temperature control | `prime("urgency")` |
| 3 | **Constraint** | Haiku principle — tighter bounds, better output | `constrain("under 100 words")` |
| 4 | **Ritual** | Chain-of-thought as mandatory intermediate states | `ritual("step by step")` |
| 5 | **Meta** | Prompt improves itself before executing | `meta()` |
| 6 | **Narrative** | Story structure activates different pathways | `narrative("case study")` |
| 7 | **Toggle** | Binary knobs for voice, depth, creativity | `toggle(depth="deep")` |
| 8 | **Constitution** | Persistent identity block | `constitution(role="analyst", rules=[...])` |

## Presets

```python
from prompt_poetry.presets import analyst, debugger, researcher, evaluator, writer
```

Each preset is a pre-built pipeline of techniques optimized for a task type.

## How it works

Every technique is a **Transform** — a callable that takes a prompt string and returns an enhanced prompt string. Transforms compose with `|` (pipe operator). That's it.

```python
# This is the entire abstraction:
enhanced_prompt = technique_a | technique_b | technique_c
result_string = enhanced_prompt("your original prompt")
```

Zero dependencies. Pure Python. 52 tests.

## Thesis

The best prompt engineers aren't engineers — they're poets who understand that every word shifts attention weights. This package turns that insight into composable, testable code.

## License

MIT
