# prompt-poetry

[![Tests](https://img.shields.io/badge/tests-52%20passed-brightgreen)]()
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()
[![Dependencies](https://img.shields.io/badge/dependencies-zero-orange)]()

**The best prompt engineers aren't engineers — they're poets.**

Every word in a prompt shifts attention weights. `prompt-poetry` turns that insight into composable, testable Python. Eight techniques. One pipe operator. Zero dependencies.

```python
from prompt_poetry import persona, prime, constrain

enhanced = persona("systems architect") | prime("precision") | constrain("under 200 words")
result = enhanced("Design a caching layer")
```

## Why this exists

Prompt engineering today is copy-paste and vibes. You write a prompt, tweak it, hope it works. There's no composability, no reuse, no testing.

`prompt-poetry` treats prompt techniques as **transforms** — functions that take a string and return a better string. They compose with `|` like Unix pipes. You can test them, version them, and optimize them.

The thesis: the same linguistic principles that make speeches memorable, poetry powerful, and negotiations effective also make LLM prompts better. Persona framing, emotional priming, structural constraints, narrative scaffolding — these aren't tricks. They're how language has always worked. We just made them composable.

## Install

```bash
pip install prompt-poetry
```

Or from source:

```bash
git clone https://github.com/drewbeyersdorf/prompt-poetry.git
cd prompt-poetry
pip install -e ".[dev]"
```

## The 8 Techniques

### 1. Persona — identity injection
Activates different probability distributions. Like tuning a radio — same hardware, different signal.
```python
persona("master craftsman")("Build a data pipeline")
# → "You are a master craftsman.\n\nBuild a data pipeline"
```

### 2. Primer — emotional temperature
Urgency, precision, creativity — language-level knobs that act like adjusting temperature.
```python
prime("urgency")("Review this incident")
# → "This is critical and time-sensitive. Prioritize accuracy and speed...\n\nReview this incident"
```

### 3. Constraint — the haiku principle
Tighter constraints produce more creative output. Sonnets produced Shakespeare.
```python
constrain("under 100 words", "no jargon")("Explain transformers")
# → "Explain transformers\n\nConstraints:\n- under 100 words\n- no jargon"
```

### 4. Ritual — chain of thought as ceremony
Forces intermediate states to exist. The ritual creates the state.
```python
ritual("step by step")("Debug this failure")
# → "Think through this step by step...\n\nDebug this failure"
```

### 5. Meta — prompts writing prompts
The model knows its own probability landscape. Ask it to navigate itself.
```python
meta()("Write a marketing email")
# → "Before executing the task below, first rewrite it as a clearer, more specific prompt...\n\nOriginal task:\nWrite a marketing email"
```

### 6. Narrative — story as structure
Stories activate different pathways than instructions. Lincoln told parables, not policy papers.
```python
narrative("postmortem")("What caused the outage?")
# → "Treat this as a postmortem. What happened, why, what was the impact...\n\nWhat caused the outage?"
```

### 7. Toggle — binary switches
On/off knobs for behavioral dimensions.
```python
toggle(creativity="high", confidence="commit", depth="deep")("Propose a solution")
# → "Be bold, surprising... Pick the best option... Go deep...\n\nPropose a solution"
```

### 8. Constitution — persistent identity
CLAUDE.md as compressed language that shapes behavior across time.
```python
constitution(role="security auditor", rules=["flag all risks", "cite CVEs"], values=["thoroughness"])("Review this PR")
# → "# Identity\nYou are security auditor.\n\n# Rules\n- flag all risks\n- cite CVEs\n\n# Values\n- thoroughness\n\n# Task\nReview this PR"
```

## Composition

The power is in composition. Pipe techniques together — left to right, each one wrapping the result:

```python
from prompt_poetry import persona, prime, constrain, ritual, toggle

# Build a debugging pipeline
debug_prompt = (
    persona("principal engineer")
    | prime("precision")
    | ritual("step by step")
    | constrain("root cause only", "cite evidence")
)

# Use it
result = debug_prompt("Why is the API returning 500s on /users?")
```

## Presets

Pre-built pipelines for common tasks:

```python
from prompt_poetry.presets import analyst, debugger, researcher, evaluator, writer

# Each is a ready-to-use Pipeline
analyst("What's driving the cost increase?")
debugger("Tests pass locally but fail in CI")
researcher("How do competitors handle real-time tracking?")
evaluator("Score these three vendor proposals")
writer("Draft a launch announcement")
```

## How it works

Two classes. That's the whole framework.

**Transform**: A callable that takes a prompt string and returns an enhanced string. Each technique is a Transform.

**Pipeline**: A chain of Transforms applied left to right. Created automatically when you use `|`.

```python
# This is the entire core:
class Transform:
    def __call__(self, prompt: str) -> str: ...
    def __or__(self, other) -> Pipeline: ...

class Pipeline(Transform):
    def __call__(self, prompt: str) -> str:
        for t in self.transforms:
            prompt = t(prompt)
        return prompt
```

No framework. No config files. No magic. Transforms in, strings out.

## Use cases

- **Agent systems**: Auto-select techniques based on task type. Research tasks get the researcher preset, debugging tasks get the debugger preset.
- **RAG pipelines**: Wrap your retrieval prompts with precision priming and anti-hallucination constitutions.
- **Fine-tuning**: Enhance training data system prompts so models internalize the techniques.
- **CI/CD**: Test that your prompts contain the right techniques before deploying.
- **Prompt optimization**: Use as the search space for algorithmic optimizers like DSPy.

## License

MIT
