# Prompt Poetry Design — 2026-03-23

## What
Python package that turns Drew's 8 prompt biohacking techniques into composable transforms. Phase 1 ships the techniques as a library. Phase 2 wires DSPy as an optimizer that searches over technique combinations. Phase 3 feeds winning prompts back into fine-tuning data.

## Why
21 militia agents run 24/7. 38 Claude Code skills fire every session. Brain v3 serves every query. Training pipeline builds every model version. A 5% improvement to prompts across all surfaces compounds into massive leverage. Today prompts are hand-written and never optimized. This package makes every prompt surface better with one `pip install`.

## Architecture

### Core Abstraction: Transform

A Transform takes a prompt string and returns an enhanced prompt string. That's the entire abstraction.

```python
from prompt_poetry import persona, constrain, prime, narrative

# Each technique is a Transform
enhanced = persona("master systems architect") | constrain("under 200 words") | prime("high stakes")
result = enhanced("Analyze this delivery data for anomalies")
# Returns the original prompt wrapped with persona framing, constraints, and emotional priming
```

Transforms compose with `|` (pipe operator). Order matters — leftmost wraps outermost.

### The 8 Techniques (Phase 1)

| # | Technique | What it does | API |
|---|-----------|-------------|-----|
| 1 | **Persona** | Injects identity that activates different probability distributions | `persona("master craftsman")` |
| 2 | **Primer** | Emotional/urgency priming — language-level temperature control | `prime("urgency")`, `prime("precision")`, `prime("creativity")` |
| 3 | **Constraint** | Tighter constraints → more creative output (haiku principle) | `constrain("under 100 words")`, `constrain("exactly 3 steps")` |
| 4 | **Ritual** | Chain-of-thought as mandatory intermediate states | `ritual("show reasoning")`, `ritual("step by step")` |
| 5 | **Meta** | Prompt asks the model to improve the prompt first | `meta("rewrite this prompt for maximum clarity")` |
| 6 | **Narrative** | Wraps task in story structure — activates different pathways | `narrative("scene")`, `narrative("parable")`, `narrative("case study")` |
| 7 | **Toggle** | Binary switches for verbosity, creativity, confidence, voice, depth | `toggle(creativity="high", confidence="commit", depth="deep")` |
| 8 | **Constitution** | Persistent identity block prepended to every prompt | `constitution({"role": "Drew's analyst", "rules": ["P&L first", "evidence before assertions"]})` |

### Presets

Pre-built technique combinations for common use cases:

```python
from prompt_poetry.presets import analyst, debugger, writer, researcher, evaluator

# analyst = persona("senior data analyst") | toggle(confidence="commit", depth="deep") | constrain("cite numbers")
# debugger = persona("principal engineer") | ritual("step by step") | prime("precision") | constrain("root cause only")
# researcher = persona("investigative journalist") | narrative("case study") | toggle(depth="deep", creativity="high")
# evaluator = persona("quality auditor") | prime("precision") | ritual("score each dimension") | toggle(confidence="commit")
# writer = persona("direct communicator") | toggle(voice="casual", creativity="high") | constrain("no jargon")
```

### Integration Points

**1. Militia agents (21 on nerve) — highest immediate ROI**
Worker prompt template (`eaurl.ai/src/worker_prompt.md`) gets a `{{PROMPT_POETRY}}` slot. The loop controller selects technique combos based on task type (research → `researcher`, analysis → `analyst`, writing → `writer`).

**2. Claude Code skills (38 skills)**
Skills that generate prompts for subagents (dispatching-parallel-agents, multi-agent-orchestration, loop-controller) import prompt_poetry to enhance dispatched prompts.

**3. Brain v3/v4 query layer**
System prompt for Brain RAG queries gets wrapped with `analyst | constrain("cite sources") | prime("precision")`. Directly addresses the 8/13 hallucination rate.

**4. Fine-tuning training pipeline**
The "expected answer" in training pairs gets generated through prompt_poetry transforms. Better expected answers → better training data → better model.

**5. eaurl.ai loop machine**
`loopd.py` worker dispatch integrates prompt_poetry for all task prompts.

### Phase 2: DSPy Optimization (when charlie ML stack is online)

Each technique becomes a DSPy-optimizable parameter:

```python
import dspy
from prompt_poetry.dspy_modules import TechniqueSelector

class OptimizedPrompt(dspy.Module):
    def __init__(self):
        self.persona = TechniqueSelector(technique="persona", options=["analyst", "engineer", "researcher", "craftsman"])
        self.primer = TechniqueSelector(technique="primer", options=["urgency", "precision", "creativity", "calm"])
        self.constraint = TechniqueSelector(technique="constraint", options=["concise", "detailed", "structured", "freeform"])

    def forward(self, task, context):
        # DSPy's MIPROv2 optimizes which combination works best
        enhanced = self.persona(task) | self.primer(task) | self.constraint(task)
        return dspy.Predict("enhanced_task, context -> result")(enhanced_task=enhanced, context=context)
```

Feed it eval datasets:
- Brain: 13+ scored pairs (growing via Argilla)
- Militia: output quality scores from loop logs
- Skills: session success/failure signals

DSPy finds optimal technique combinations per surface automatically.

### Phase 3: Recursive Self-Improvement

Winning prompt compositions from Phase 2 → new training pairs for fine-tuning → model internalizes the techniques → model becomes its own poet. The package teaches the model to do what the package does, then the package is no longer needed for that model. This is the productizable loop.

## Package Details

- **Python:** 3.11+
- **Dependencies (Phase 1):** None. Pure Python. Zero deps.
- **Dependencies (Phase 2):** `dspy-ai` (optional extra: `pip install prompt-poetry[dspy]`)
- **Package manager:** uv
- **License:** MIT
- **Repo:** `drewbeyersdorf/prompt-poetry`

```
prompt-poetry/
├── src/prompt_poetry/
│   ├── __init__.py
│   ├── core.py              # Transform base class + pipe operator
│   ├── techniques/
│   │   ├── __init__.py
│   │   ├── persona.py
│   │   ├── primer.py
│   │   ├── constraint.py
│   │   ├── ritual.py
│   │   ├── meta.py
│   │   ├── narrative.py
│   │   ├── toggle.py
│   │   └── constitution.py
│   ├── presets.py
│   ├── compose.py           # __or__ chaining logic
│   └── dspy_modules/        # Phase 2
│       ├── __init__.py
│       ├── selectors.py
│       └── optimizers.py
├── tests/
│   ├── test_core.py
│   ├── test_techniques.py
│   ├── test_compose.py
│   └── test_presets.py
├── pyproject.toml
├── CLAUDE.md
└── README.md
```

## Success Criteria

1. `pip install prompt-poetry` works from the repo
2. All 8 techniques produce measurably different outputs vs raw prompts
3. Techniques compose with `|` — any combination, any order
4. Presets cover the 5 most common agent types
5. Integration with militia worker template takes < 10 lines of code change
6. Zero dependencies in Phase 1
7. DSPy modules pass type checking and basic optimization in Phase 2

## What's NOT in scope

- GUI / web interface
- Prompt versioning / history (that's eaurl.ai's job)
- Model-specific optimizations (Claude vs GPT vs Gemini) — techniques are model-agnostic
- Automatic technique selection without DSPy (Phase 1 is manual selection)
