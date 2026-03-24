<p align="center">
  <h1 align="center">prompt-poetry</h1>
  <p align="center">
    <strong>The best prompt engineers aren't engineers — they're poets.</strong>
  </p>
  <p align="center">
    <a href="https://github.com/drewbeyersdorf/prompt-poetry/actions"><img src="https://github.com/drewbeyersdorf/prompt-poetry/workflows/tests/badge.svg" alt="Tests"></a>
    <a href="https://pypi.org/project/prompt-poetry/"><img src="https://img.shields.io/pypi/v/prompt-poetry?color=blue" alt="PyPI"></a>
    <a href="https://github.com/drewbeyersdorf/prompt-poetry/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-green" alt="License"></a>
    <a href="https://github.com/drewbeyersdorf/prompt-poetry"><img src="https://img.shields.io/badge/dependencies-zero-orange" alt="Zero Dependencies"></a>
    <a href="https://github.com/drewbeyersdorf/prompt-poetry"><img src="https://img.shields.io/badge/python-3.11%2B-blue" alt="Python 3.11+"></a>
  </p>
</p>

---

Every word in a prompt shifts attention weights. `prompt-poetry` gives you **8 composable techniques** that snap together with `|` — like Unix pipes for prompt engineering.

```python
from prompt_poetry import persona, prime, constrain

enhanced = persona("systems architect") | prime("precision") | constrain("under 200 words")
print(enhanced("Design a caching layer"))
```
```
Be meticulous and exact. Double-check every claim. Rigorous accuracy is non-negotiable.

You are a systems architect.

Design a caching layer

Constraints:
- under 200 words
```

That's it. Transforms in, enhanced prompts out. Zero dependencies. Works with any LLM.

---

## Before / After

<table>
<tr><td><strong>Without prompt-poetry</strong></td><td><strong>With prompt-poetry</strong></td></tr>
<tr>
<td>

```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    messages=[{
        "role": "user",
        "content": "Why did costs increase?"
    }]
)
# Vague question → vague answer
```

</td>
<td>

```python
from prompt_poetry.presets import analyst

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    messages=[{
        "role": "user",
        "content": analyst("Why did costs increase?")
    }]
)
# Precise persona + depth + constraints → precise answer
```

</td>
</tr>
<tr>
<td>❌ Generic response, no numbers, hedging</td>
<td>✅ Commits to an answer, cites evidence, goes deep</td>
</tr>
</table>

**One line changes your prompt. Zero lines change your LLM call.**

---

## Install

```bash
pip install prompt-poetry
```

## The 8 Techniques

| # | Technique | What it does | One-liner |
|---|-----------|-------------|-----------|
| 1 | **Persona** | Tunes the probability distribution | `persona("master craftsman")` |
| 2 | **Primer** | Sets emotional temperature | `prime("urgency")` |
| 3 | **Constraint** | Tighter bounds → better output | `constrain("under 100 words")` |
| 4 | **Ritual** | Forces intermediate reasoning | `ritual("step by step")` |
| 5 | **Meta** | Prompt improves itself first | `meta()` |
| 6 | **Narrative** | Activates story pathways | `narrative("postmortem")` |
| 7 | **Toggle** | Binary behavioral knobs | `toggle(depth="deep")` |
| 8 | **Constitution** | Persistent identity block | `constitution(role="auditor", rules=[...])` |

<details>
<summary><strong>See each technique with output ↓</strong></summary>

### Persona — identity injection
Like tuning a radio. Same hardware, different signal.
```python
>>> persona("forensic accountant")("Review these invoices")
'You are a forensic accountant.\n\nReview these invoices'
```

### Primer — emotional temperature
Language-level knobs that act like adjusting temperature.
```python
>>> prime("urgency")("Check the production server")
'This is critical and time-sensitive. Prioritize accuracy and speed. Every detail matters immediately.\n\nCheck the production server'
```

### Constraint — the haiku principle
Sonnets produced Shakespeare. Constraints force the model off the beaten path.
```python
>>> constrain("3 bullet points", "no jargon")("Explain kubernetes")
'Explain kubernetes\n\nConstraints:\n- 3 bullet points\n- no jargon'
```

### Ritual — chain of thought as ceremony
The ritual creates the state. Monks chant before meditation for the same reason.
```python
>>> ritual("devil's advocate")("Should we migrate to microservices?")
"Before answering, argue the opposite position. Then reconcile both views into your final answer.\n\nShould we migrate to microservices?"
```

### Meta — prompts writing prompts
The model knows its own landscape better than you do.
```python
>>> meta()("Write a cold email")
'Before executing the task below, first rewrite it as a clearer, more specific prompt that will produce the best possible result. Then execute your improved version.\n\nOriginal task:\nWrite a cold email'
```

### Narrative — story as structure
Lincoln told parables, not policy papers. Stories activate different pathways.
```python
>>> narrative("postmortem")("Why did the deploy fail?")
'Treat this as a postmortem. What happened, why, what was the impact, and what prevents recurrence.\n\nWhy did the deploy fail?'
```

### Toggle — binary switches
```python
>>> toggle(creativity="high", confidence="commit")("Propose a solution")
'Be bold, surprising, and unconventional. Prefer novel approaches. Pick the best option and commit to it. No hedging.\n\nPropose a solution'
```

### Constitution — persistent identity
Your CLAUDE.md / system prompt as composable code.
```python
>>> constitution(role="security auditor", rules=["flag all risks", "cite CVEs"])("Review this PR")
'# Identity\nYou are security auditor.\n\n# Rules\n- flag all risks\n- cite CVEs\n\n# Task\nReview this PR'
```

</details>

---

## Composition

The power is in the pipe. Build reusable prompt pipelines:

```python
from prompt_poetry import persona, prime, constrain, ritual, toggle

# A debugging pipeline
debug = (
    persona("principal SRE")
    | prime("precision")
    | ritual("step by step")
    | constrain("root cause only")
)

# A research pipeline
research = (
    persona("investigative journalist")
    | narrative("case study")
    | toggle(depth="deep", creativity="high")
)

# Use them everywhere
debug("Why is latency spiking on /api/users?")
research("How do top YC companies handle billing?")
```

## Presets

Five ready-to-use pipelines:

```python
from prompt_poetry.presets import analyst, debugger, researcher, evaluator, writer

analyst("What's driving the margin decrease?")     # Commits, cites numbers, goes deep
debugger("Tests pass locally but fail in CI")      # Step-by-step, root cause, precise
researcher("How do competitors handle X?")         # Case study, creative, thorough
evaluator("Score these three proposals")           # Scoring ritual, no hedging
writer("Draft a launch announcement")              # Casual voice, bold, no jargon
```

Presets compose too:

```python
custom = analyst | constrain("under 50 words")  # Extend any preset
```

---

## Works with everything

prompt-poetry enhances the prompt string. It doesn't care what LLM you send it to.

<table>
<tr><td><strong>OpenAI</strong></td><td><strong>Anthropic</strong></td><td><strong>Local (Ollama)</strong></td></tr>
<tr>
<td>

```python
from openai import OpenAI
from prompt_poetry.presets import analyst

client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{
        "role": "user",
        "content": analyst("Analyze churn")
    }]
)
```

</td>
<td>

```python
import anthropic
from prompt_poetry.presets import analyst

client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": analyst("Analyze churn")
    }]
)
```

</td>
<td>

```python
import requests
from prompt_poetry.presets import analyst

requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3",
        "prompt": analyst("Analyze churn")
    }
)
```

</td>
</tr>
</table>

---

## How it works

Two classes. That's the whole framework.

```python
class Transform:
    """Takes a string, returns a better string."""
    def __call__(self, prompt: str) -> str: ...
    def __or__(self, other) -> Pipeline: ...

class Pipeline(Transform):
    """Chains transforms left to right."""
    def __call__(self, prompt: str) -> str:
        for t in self.transforms:
            prompt = t(prompt)
        return prompt
```

No framework. No config files. No magic. No dependencies.

---

## Use cases

**Agent systems** — Auto-select techniques by task type. Research tasks get the researcher preset, debugging tasks get debugger.

**RAG pipelines** — Wrap retrieval prompts with precision priming and anti-hallucination constitutions. Measurably reduces fabrication.

**Fine-tuning** — Enhance training data system prompts so models internalize the techniques. The model learns to be its own poet.

**CI/CD** — Test that prompts contain required techniques before deploying.

**Prompt optimization** — Use as the search space for DSPy, TextGrad, or other algorithmic optimizers.

---

## vs. alternatives

| | prompt-poetry | Raw prompts | LangChain PromptTemplate | DSPy |
|---|---|---|---|---|
| Composable | ✅ Pipe operator | ❌ Copy-paste | ⚠️ Chains but verbose | ✅ Modules |
| Testable | ✅ Pure functions | ❌ | ⚠️ | ✅ |
| Zero deps | ✅ | ✅ | ❌ 50+ deps | ❌ |
| Human-readable | ✅ Reads like prose | ✅ | ❌ YAML/templates | ❌ Compiled |
| Algorithmic optimization | 🔜 DSPy integration | ❌ | ❌ | ✅ Native |
| Learning curve | 5 minutes | 0 | Hours | Days |

prompt-poetry is the **missing layer** between raw strings and full frameworks. Use it standalone or as the human-readable layer that feeds into DSPy.

---

## Contributing

```bash
git clone https://github.com/drewbeyersdorf/prompt-poetry.git
cd prompt-poetry
pip install -e ".[dev]"
pytest
```

52 tests. They run in 0.05 seconds.

---

<p align="center">
  <sub>Built by <a href="https://github.com/drewbeyersdorf">Drew Beyersdorf</a>.</sub>
</p>
