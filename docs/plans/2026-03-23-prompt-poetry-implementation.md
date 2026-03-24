# Prompt Poetry Phase 1 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Ship `prompt-poetry` — a zero-dependency Python package with 8 composable prompt techniques, pipe operator, presets, and full test coverage.

**Architecture:** Each technique is a Transform (callable that takes a string, returns a string). Transforms compose via `|` (pipe operator using `__or__`). Presets are pre-built chains of transforms. Everything is pure Python, no deps.

**Tech Stack:** Python 3.11+, uv, pytest

---

### Task 1: Project Scaffolding

**Files:**
- Create: `pyproject.toml`
- Create: `src/prompt_poetry/__init__.py`
- Create: `src/prompt_poetry/core.py`
- Create: `tests/__init__.py`
- Create: `CLAUDE.md`

**Step 1: Create pyproject.toml**

```toml
[project]
name = "prompt-poetry"
version = "0.1.0"
description = "Composable prompt engineering techniques for biohacking LLMs"
readme = "README.md"
license = "MIT"
requires-python = ">=3.11"
authors = [{ name = "Drew Beyersdorf", email = "drewbeyersdorf@gmail.com" }]

[project.optional-dependencies]
dspy = ["dspy-ai>=2.5"]
dev = ["pytest>=8.0", "pytest-cov>=5.0"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/prompt_poetry"]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

**Step 2: Create CLAUDE.md**

```markdown
# prompt-poetry

## What
Composable prompt engineering techniques. 8 techniques, pipe operator, presets. Zero dependencies.

## Commands
- Test: `uv run pytest tests/ -v`
- Install: `uv pip install -e ".[dev]"`
- Single test: `uv run pytest tests/test_core.py::test_name -v`

## Architecture
- `core.py` — Transform base class with `__or__` pipe and `__call__`
- `techniques/` — 8 technique modules, each exports a factory function returning a Transform
- `presets.py` — pre-built Transform chains
- `compose.py` — Pipeline class for chaining multiple transforms

## Rules
- Zero dependencies in main package. Only stdlib.
- Every technique is a Transform. No exceptions.
- Tests use plain assert, no mocking needed (pure string transforms).
```

**Step 3: Create empty src/prompt_poetry/__init__.py and tests/__init__.py**

```python
# src/prompt_poetry/__init__.py
"""Prompt Poetry — composable prompt engineering techniques for biohacking LLMs."""

from prompt_poetry.core import Transform, Pipeline

__version__ = "0.1.0"
__all__ = ["Transform", "Pipeline"]
```

```python
# tests/__init__.py
```

**Step 4: Create stub core.py**

```python
# src/prompt_poetry/core.py
"""Core abstractions: Transform and Pipeline."""

from __future__ import annotations


class Transform:
    """A prompt transform — takes a string, returns an enhanced string."""

    def __call__(self, prompt: str) -> str:
        raise NotImplementedError

    def __or__(self, other: Transform) -> Pipeline:
        return Pipeline([self, other])


class Pipeline(Transform):
    """A chain of transforms applied left to right."""

    def __init__(self, transforms: list[Transform] | None = None):
        self.transforms = transforms or []

    def __call__(self, prompt: str) -> str:
        raise NotImplementedError

    def __or__(self, other: Transform) -> Pipeline:
        if isinstance(other, Pipeline):
            return Pipeline(self.transforms + other.transforms)
        return Pipeline(self.transforms + [other])
```

**Step 5: Initialize uv and verify install**

Run: `cd ~/projects/prompt-poetry && uv venv && uv pip install -e ".[dev]"`
Expected: Successful install with 0 dependencies

**Step 6: Run empty test suite**

Run: `cd ~/projects/prompt-poetry && uv run pytest tests/ -v`
Expected: "no tests ran" or 0 collected (no test files yet with actual tests)

**Step 7: Commit**

```bash
cd ~/projects/prompt-poetry
git add pyproject.toml CLAUDE.md src/ tests/__init__.py docs/
git commit -m "feat: project scaffolding with Transform/Pipeline stubs"
```

---

### Task 2: Transform Core + Pipe Operator (TDD)

**Files:**
- Modify: `src/prompt_poetry/core.py`
- Create: `tests/test_core.py`

**Step 1: Write failing tests for Transform and Pipeline**

```python
# tests/test_core.py
"""Tests for core Transform and Pipeline."""

from prompt_poetry.core import Transform, Pipeline


class PrefixTransform(Transform):
    """Test helper — prepends a prefix."""

    def __init__(self, prefix: str):
        self.prefix = prefix

    def __call__(self, prompt: str) -> str:
        return f"{self.prefix}\n\n{prompt}"


class SuffixTransform(Transform):
    """Test helper — appends a suffix."""

    def __init__(self, suffix: str):
        self.suffix = suffix

    def __call__(self, prompt: str) -> str:
        return f"{prompt}\n\n{self.suffix}"


def test_transform_is_callable():
    t = PrefixTransform("Hello")
    result = t("World")
    assert result == "Hello\n\nWorld"


def test_pipe_two_transforms():
    a = PrefixTransform("First")
    b = SuffixTransform("Last")
    pipeline = a | b
    assert isinstance(pipeline, Pipeline)
    result = pipeline("Middle")
    assert result == "First\n\nMiddle\n\nLast"


def test_pipe_three_transforms():
    a = PrefixTransform("A")
    b = PrefixTransform("B")
    c = SuffixTransform("C")
    pipeline = a | b | c
    result = pipeline("X")
    # a runs first: "A\n\nX", then b: "B\n\nA\n\nX", then c: "B\n\nA\n\nX\n\nC"
    assert "A" in result
    assert "B" in result
    assert "C" in result
    assert "X" in result


def test_pipeline_pipe_pipeline():
    p1 = PrefixTransform("A") | PrefixTransform("B")
    p2 = SuffixTransform("C") | SuffixTransform("D")
    combined = p1 | p2
    assert isinstance(combined, Pipeline)
    assert len(combined.transforms) == 4


def test_single_transform_callable():
    t = PrefixTransform("Only")
    assert t("input") == "Only\n\ninput"


def test_pipeline_preserves_order():
    """Left-to-right: first transform runs first on the input."""
    a = PrefixTransform("FIRST")
    b = PrefixTransform("SECOND")
    pipeline = a | b
    result = pipeline("original")
    # a runs first: "FIRST\n\noriginal"
    # b runs second: "SECOND\n\nFIRST\n\noriginal"
    assert result.startswith("SECOND")
    assert "FIRST" in result
    assert result.endswith("original")


def test_empty_pipeline():
    p = Pipeline([])
    assert p("hello") == "hello"


def test_repr():
    a = PrefixTransform("A")
    b = SuffixTransform("B")
    pipeline = a | b
    r = repr(pipeline)
    assert "Pipeline" in r
```

**Step 2: Run tests to verify they fail**

Run: `cd ~/projects/prompt-poetry && uv run pytest tests/test_core.py -v`
Expected: Failures on Pipeline.__call__ (NotImplementedError)

**Step 3: Implement Transform and Pipeline**

```python
# src/prompt_poetry/core.py
"""Core abstractions: Transform and Pipeline."""

from __future__ import annotations


class Transform:
    """A prompt transform — takes a string, returns an enhanced string.

    Subclass and implement __call__ to create a technique.
    Compose with | (pipe operator) to chain techniques.
    """

    def __call__(self, prompt: str) -> str:
        raise NotImplementedError

    def __or__(self, other: Transform) -> Pipeline:
        left = self.transforms if isinstance(self, Pipeline) else [self]
        right = other.transforms if isinstance(other, Pipeline) else [other]
        return Pipeline(left + right)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


class Pipeline(Transform):
    """A chain of transforms applied left to right.

    First transform touches the input first. Each subsequent transform
    receives the output of the previous one.
    """

    def __init__(self, transforms: list[Transform] | None = None):
        self.transforms = transforms or []

    def __call__(self, prompt: str) -> str:
        result = prompt
        for t in self.transforms:
            result = t(result)
        return result

    def __repr__(self) -> str:
        names = [repr(t) for t in self.transforms]
        return f"Pipeline([{', '.join(names)}])"
```

**Step 4: Run tests to verify they pass**

Run: `cd ~/projects/prompt-poetry && uv run pytest tests/test_core.py -v`
Expected: All 8 tests PASS

**Step 5: Commit**

```bash
cd ~/projects/prompt-poetry
git add src/prompt_poetry/core.py tests/test_core.py
git commit -m "feat: Transform base class and Pipeline with pipe operator"
```

---

### Task 3: Persona Technique (TDD)

**Files:**
- Create: `src/prompt_poetry/techniques/__init__.py`
- Create: `src/prompt_poetry/techniques/persona.py`
- Create: `tests/test_techniques.py`

**Step 1: Write failing tests**

```python
# tests/test_techniques.py
"""Tests for all 8 techniques."""

from prompt_poetry.techniques.persona import persona
from prompt_poetry.core import Transform


def test_persona_returns_transform():
    t = persona("master craftsman")
    assert isinstance(t, Transform)


def test_persona_wraps_prompt():
    t = persona("senior data analyst")
    result = t("Analyze the delivery data")
    assert "senior data analyst" in result
    assert "Analyze the delivery data" in result


def test_persona_with_context():
    t = persona("principal engineer", context="debugging production systems")
    result = t("Find the root cause")
    assert "principal engineer" in result
    assert "debugging production systems" in result
    assert "Find the root cause" in result


def test_persona_callable_as_string():
    t = persona("poet")
    result = t("Write something")
    assert isinstance(result, str)
    assert len(result) > len("Write something")
```

**Step 2: Run tests to verify they fail**

Run: `cd ~/projects/prompt-poetry && uv run pytest tests/test_techniques.py::test_persona_returns_transform -v`
Expected: ImportError

**Step 3: Implement persona**

```python
# src/prompt_poetry/techniques/__init__.py
"""Prompt Poetry techniques — 8 composable prompt transforms."""

from prompt_poetry.techniques.persona import persona
from prompt_poetry.techniques.primer import prime
from prompt_poetry.techniques.constraint import constrain
from prompt_poetry.techniques.ritual import ritual
from prompt_poetry.techniques.meta import meta
from prompt_poetry.techniques.narrative import narrative
from prompt_poetry.techniques.toggle import toggle
from prompt_poetry.techniques.constitution import constitution

__all__ = [
    "persona", "prime", "constrain", "ritual",
    "meta", "narrative", "toggle", "constitution",
]
```

Note: the __init__.py will fail imports until all 8 technique files exist. Create stubs for the others that raise NotImplementedError, or defer the __init__.py until Task 10. **Recommended:** Create the __init__.py with only persona imported, add each import as techniques are built.

Revised __init__.py for Task 3:

```python
# src/prompt_poetry/techniques/__init__.py
"""Prompt Poetry techniques — composable prompt transforms."""

from prompt_poetry.techniques.persona import persona

__all__ = ["persona"]
```

```python
# src/prompt_poetry/techniques/persona.py
"""Strategy 1: Persona Framing — identity injection.

Activates different probability distributions by establishing who the model
is before it processes the task. Like tuning a radio — same hardware,
different signal.
"""

from __future__ import annotations

from prompt_poetry.core import Transform


class _PersonaTransform(Transform):
    """Wraps a prompt with a persona identity frame."""

    def __init__(self, identity: str, context: str | None = None):
        self.identity = identity
        self.context = context

    def __call__(self, prompt: str) -> str:
        parts = [f"You are a {self.identity}."]
        if self.context:
            parts.append(f"Your area of focus: {self.context}.")
        parts.append("")
        parts.append(prompt)
        return "\n".join(parts)

    def __repr__(self) -> str:
        if self.context:
            return f"persona({self.identity!r}, context={self.context!r})"
        return f"persona({self.identity!r})"


def persona(identity: str, context: str | None = None) -> _PersonaTransform:
    """Create a persona transform.

    Args:
        identity: Who the model should be (e.g. "master craftsman", "senior analyst")
        context: Optional focus area (e.g. "debugging production systems")
    """
    return _PersonaTransform(identity, context)
```

**Step 4: Run tests to verify they pass**

Run: `cd ~/projects/prompt-poetry && uv run pytest tests/test_techniques.py -v -k persona`
Expected: All 4 persona tests PASS

**Step 5: Commit**

```bash
cd ~/projects/prompt-poetry
git add src/prompt_poetry/techniques/ tests/test_techniques.py
git commit -m "feat: persona technique — identity injection transform"
```

---

### Task 4: Primer Technique (TDD)

**Files:**
- Create: `src/prompt_poetry/techniques/primer.py`
- Modify: `src/prompt_poetry/techniques/__init__.py` (add import)
- Modify: `tests/test_techniques.py` (add tests)

**Step 1: Write failing tests**

Append to `tests/test_techniques.py`:

```python
from prompt_poetry.techniques.primer import prime


def test_prime_returns_transform():
    t = prime("urgency")
    assert isinstance(t, Transform)


def test_prime_urgency():
    t = prime("urgency")
    result = t("Review this data")
    assert "Review this data" in result
    # Should contain urgency language
    assert any(word in result.lower() for word in ["critical", "immediate", "urgent", "time-sensitive", "priority"])


def test_prime_precision():
    t = prime("precision")
    result = t("Analyze this")
    assert "Analyze this" in result
    assert any(word in result.lower() for word in ["exact", "precise", "accurate", "rigorous", "meticulous"])


def test_prime_creativity():
    t = prime("creativity")
    result = t("Write something")
    assert "Write something" in result
    assert any(word in result.lower() for word in ["creative", "novel", "unexpected", "bold", "unconventional", "innovative"])


def test_prime_custom():
    t = prime("melancholy")
    result = t("Describe the scene")
    assert "melancholy" in result.lower()
    assert "Describe the scene" in result
```

**Step 2: Run tests to verify they fail**

Run: `cd ~/projects/prompt-poetry && uv run pytest tests/test_techniques.py -v -k prime`
Expected: ImportError

**Step 3: Implement primer**

```python
# src/prompt_poetry/techniques/primer.py
"""Strategy 2: Emotional Priming — temperature through language.

Urgency, stakes, and tone in natural language act like adjusting temperature.
Inspirational speakers compress energy into fewer words — same principle.
"""

from __future__ import annotations

from prompt_poetry.core import Transform

# Built-in primer moods with their language
_PRIMERS: dict[str, str] = {
    "urgency": "This is critical and time-sensitive. Prioritize accuracy and speed. Every detail matters immediately.",
    "precision": "Be meticulous and exact. Double-check every claim. Rigorous accuracy is non-negotiable.",
    "creativity": "Think boldly and unconventionally. Explore unexpected angles. The novel approach is preferred over the safe one.",
    "calm": "Take your time. Think carefully and thoroughly. There is no rush — depth matters more than speed.",
    "confidence": "Be decisive. Commit to your best judgment. State conclusions directly, not as possibilities.",
}


class _PrimerTransform(Transform):
    """Wraps a prompt with emotional/tonal priming."""

    def __init__(self, mood: str):
        self.mood = mood
        self.text = _PRIMERS.get(mood, f"Approach this with a sense of {mood}.")

    def __call__(self, prompt: str) -> str:
        return f"{self.text}\n\n{prompt}"

    def __repr__(self) -> str:
        return f"prime({self.mood!r})"


def prime(mood: str) -> _PrimerTransform:
    """Create an emotional primer transform.

    Built-in moods: urgency, precision, creativity, calm, confidence.
    Custom moods generate a generic primer with that word.
    """
    return _PrimerTransform(mood)
```

Update `techniques/__init__.py`:

```python
from prompt_poetry.techniques.persona import persona
from prompt_poetry.techniques.primer import prime

__all__ = ["persona", "prime"]
```

**Step 4: Run tests**

Run: `cd ~/projects/prompt-poetry && uv run pytest tests/test_techniques.py -v -k prime`
Expected: All 5 PASS

**Step 5: Commit**

```bash
cd ~/projects/prompt-poetry
git add src/prompt_poetry/techniques/primer.py src/prompt_poetry/techniques/__init__.py tests/test_techniques.py
git commit -m "feat: primer technique — emotional/tonal priming transform"
```

---

### Task 5: Constraint Technique (TDD)

**Files:**
- Create: `src/prompt_poetry/techniques/constraint.py`
- Modify: `src/prompt_poetry/techniques/__init__.py`
- Modify: `tests/test_techniques.py`

**Step 1: Write failing tests**

```python
from prompt_poetry.techniques.constraint import constrain


def test_constrain_returns_transform():
    t = constrain("under 100 words")
    assert isinstance(t, Transform)


def test_constrain_adds_constraint():
    t = constrain("exactly 3 bullet points")
    result = t("List the key findings")
    assert "exactly 3 bullet points" in result
    assert "List the key findings" in result


def test_constrain_multiple():
    t = constrain("under 100 words", "no jargon", "cite sources")
    result = t("Explain this")
    assert "under 100 words" in result
    assert "no jargon" in result
    assert "cite sources" in result
```

**Step 2: Run tests to verify failure**

Run: `cd ~/projects/prompt-poetry && uv run pytest tests/test_techniques.py -v -k constrain`

**Step 3: Implement**

```python
# src/prompt_poetry/techniques/constraint.py
"""Strategy 3: Constraint as Liberation — the haiku principle.

Tighter constraints produce more creative output. Sonnets produced Shakespeare.
14 lines of iambic pentameter — that prison produced the best work.
"""

from __future__ import annotations

from prompt_poetry.core import Transform


class _ConstraintTransform(Transform):
    """Appends constraints to a prompt."""

    def __init__(self, constraints: tuple[str, ...]):
        self.constraints = constraints

    def __call__(self, prompt: str) -> str:
        constraint_block = "\n".join(f"- {c}" for c in self.constraints)
        return f"{prompt}\n\nConstraints:\n{constraint_block}"

    def __repr__(self) -> str:
        return f"constrain({', '.join(repr(c) for c in self.constraints)})"


def constrain(*constraints: str) -> _ConstraintTransform:
    """Create a constraint transform. Accepts one or more constraint strings."""
    return _ConstraintTransform(constraints)
```

Update __init__.py to add `constrain`.

**Step 4: Run tests, verify pass**

Run: `cd ~/projects/prompt-poetry && uv run pytest tests/test_techniques.py -v -k constrain`

**Step 5: Commit**

```bash
git add src/prompt_poetry/techniques/constraint.py src/prompt_poetry/techniques/__init__.py tests/test_techniques.py
git commit -m "feat: constraint technique — haiku principle transform"
```

---

### Task 6: Ritual Technique (TDD)

**Files:**
- Create: `src/prompt_poetry/techniques/ritual.py`
- Modify: `src/prompt_poetry/techniques/__init__.py`
- Modify: `tests/test_techniques.py`

**Step 1: Write failing tests**

```python
from prompt_poetry.techniques.ritual import ritual


def test_ritual_returns_transform():
    t = ritual("show reasoning")
    assert isinstance(t, Transform)


def test_ritual_step_by_step():
    t = ritual("step by step")
    result = t("Solve this problem")
    assert "step by step" in result.lower() or "step-by-step" in result.lower()
    assert "Solve this problem" in result


def test_ritual_show_reasoning():
    t = ritual("show reasoning")
    result = t("Why did this fail?")
    assert "reasoning" in result.lower()
    assert "Why did this fail?" in result


def test_ritual_custom():
    t = ritual("enumerate assumptions before concluding")
    result = t("Evaluate this")
    assert "assumptions" in result.lower()
```

**Step 2: Verify failure**

**Step 3: Implement**

```python
# src/prompt_poetry/techniques/ritual.py
"""Strategy 4: Chain of Thought as Ritual — showing the work.

Forces intermediate states to exist. Monks chant before meditation for
the same reason — the ritual creates the state.
"""

from __future__ import annotations

from prompt_poetry.core import Transform

_RITUALS: dict[str, str] = {
    "step by step": "Think through this step by step. Show each stage of your reasoning before reaching a conclusion.",
    "show reasoning": "Show your reasoning explicitly. State what you observe, what you infer, and why, before giving your answer.",
    "enumerate": "First, list all relevant factors. Then evaluate each one. Only then draw your conclusion.",
    "devil's advocate": "Before answering, argue the opposite position. Then reconcile both views into your final answer.",
}


class _RitualTransform(Transform):
    """Injects a thinking ritual before the task."""

    def __init__(self, ritual_type: str):
        self.ritual_type = ritual_type
        self.text = _RITUALS.get(ritual_type, f"Before answering: {ritual_type}.")

    def __call__(self, prompt: str) -> str:
        return f"{self.text}\n\n{prompt}"

    def __repr__(self) -> str:
        return f"ritual({self.ritual_type!r})"


def ritual(ritual_type: str) -> _RitualTransform:
    """Create a chain-of-thought ritual transform.

    Built-in rituals: 'step by step', 'show reasoning', 'enumerate', 'devil's advocate'.
    Custom strings become direct instructions.
    """
    return _RitualTransform(ritual_type)
```

**Step 4: Run tests, verify pass**

**Step 5: Commit**

```bash
git add src/prompt_poetry/techniques/ritual.py src/prompt_poetry/techniques/__init__.py tests/test_techniques.py
git commit -m "feat: ritual technique — chain-of-thought ritual transform"
```

---

### Task 7: Meta Technique (TDD)

**Files:**
- Create: `src/prompt_poetry/techniques/meta.py`
- Modify: `src/prompt_poetry/techniques/__init__.py`
- Modify: `tests/test_techniques.py`

**Step 1: Write failing tests**

```python
from prompt_poetry.techniques.meta import meta


def test_meta_returns_transform():
    t = meta()
    assert isinstance(t, Transform)


def test_meta_default():
    t = meta()
    result = t("Analyze this data")
    # Should ask the model to improve the prompt first
    assert "Analyze this data" in result
    assert any(word in result.lower() for word in ["rewrite", "improve", "refine", "optimize", "rephrase"])


def test_meta_custom_instruction():
    t = meta("rewrite for maximum clarity and specificity")
    result = t("Do the thing")
    assert "clarity" in result.lower()
    assert "Do the thing" in result
```

**Step 3: Implement**

```python
# src/prompt_poetry/techniques/meta.py
"""Strategy 5: The Meta-Prompt — prompts writing prompts.

Recursive. The model knows its own probability landscape better than you.
Asking it to navigate itself = asking a river where it wants to flow.
"""

from __future__ import annotations

from prompt_poetry.core import Transform

_DEFAULT_META = (
    "Before executing the task below, first rewrite it as a clearer, "
    "more specific prompt that will produce the best possible result. "
    "Then execute your improved version."
)


class _MetaTransform(Transform):
    """Wraps a prompt with a meta-instruction to self-improve it."""

    def __init__(self, instruction: str | None = None):
        self.instruction = instruction or _DEFAULT_META

    def __call__(self, prompt: str) -> str:
        return f"{self.instruction}\n\nOriginal task:\n{prompt}"

    def __repr__(self) -> str:
        return "meta()" if self.instruction == _DEFAULT_META else f"meta({self.instruction!r})"


def meta(instruction: str | None = None) -> _MetaTransform:
    """Create a meta-prompt transform.

    The model improves the prompt before executing it.
    Default instruction asks for clarity and specificity rewrite.
    """
    return _MetaTransform(instruction)
```

**Step 4-5: Run tests, commit**

```bash
git commit -m "feat: meta technique — self-improving prompt transform"
```

---

### Task 8: Narrative Technique (TDD)

**Files:**
- Create: `src/prompt_poetry/techniques/narrative.py`
- Modify: `src/prompt_poetry/techniques/__init__.py`
- Modify: `tests/test_techniques.py`

**Step 1: Write failing tests**

```python
from prompt_poetry.techniques.narrative import narrative


def test_narrative_returns_transform():
    t = narrative("case study")
    assert isinstance(t, Transform)


def test_narrative_case_study():
    t = narrative("case study")
    result = t("Analyze the delivery failures")
    assert "Analyze the delivery failures" in result
    assert any(word in result.lower() for word in ["case study", "case", "scenario", "situation"])


def test_narrative_scene():
    t = narrative("scene")
    result = t("Describe the warehouse flow")
    assert "Describe the warehouse flow" in result


def test_narrative_parable():
    t = narrative("parable")
    result = t("Explain why constraints help")
    assert "Explain why constraints help" in result
```

**Step 3: Implement**

```python
# src/prompt_poetry/techniques/narrative.py
"""Strategy 6: Narrative Scaffolding — story as structure.

Stories activate different pathways than instructions. Lincoln told
parables, not policy papers. A scene gives instinct, a lecture gives theory.
"""

from __future__ import annotations

from prompt_poetry.core import Transform

_NARRATIVES: dict[str, str] = {
    "case study": "Approach this as a case study. Present the situation, analyze the factors, and deliver findings with evidence.",
    "scene": "Set the scene first. Describe what's happening, who's involved, and what's at stake before diving into analysis.",
    "parable": "Frame your answer as a lesson learned. What happened, what it teaches, and what to do differently.",
    "briefing": "Structure this as an executive briefing. Lead with the conclusion, then supporting evidence, then recommendations.",
    "postmortem": "Treat this as a postmortem. What happened, why, what was the impact, and what prevents recurrence.",
}


class _NarrativeTransform(Transform):
    """Wraps a prompt with narrative scaffolding."""

    def __init__(self, style: str):
        self.style = style
        self.text = _NARRATIVES.get(style, f"Frame your response as a {style}.")

    def __call__(self, prompt: str) -> str:
        return f"{self.text}\n\n{prompt}"

    def __repr__(self) -> str:
        return f"narrative({self.style!r})"


def narrative(style: str) -> _NarrativeTransform:
    """Create a narrative scaffolding transform.

    Built-in styles: 'case study', 'scene', 'parable', 'briefing', 'postmortem'.
    Custom strings generate a generic framing instruction.
    """
    return _NarrativeTransform(style)
```

**Step 4-5: Run tests, commit**

```bash
git commit -m "feat: narrative technique — story scaffolding transform"
```

---

### Task 9: Toggle Technique (TDD)

**Files:**
- Create: `src/prompt_poetry/techniques/toggle.py`
- Modify: `src/prompt_poetry/techniques/__init__.py`
- Modify: `tests/test_techniques.py`

**Step 1: Write failing tests**

```python
from prompt_poetry.techniques.toggle import toggle


def test_toggle_returns_transform():
    t = toggle(creativity="high")
    assert isinstance(t, Transform)


def test_toggle_single():
    t = toggle(depth="deep")
    result = t("Explain this concept")
    assert "Explain this concept" in result
    assert any(word in result.lower() for word in ["deep", "thorough", "comprehensive", "detail"])


def test_toggle_multiple():
    t = toggle(creativity="high", confidence="commit", voice="casual")
    result = t("Write about this")
    assert "Write about this" in result


def test_toggle_off_values():
    t = toggle(verbosity="low", creativity="low")
    result = t("Summarize")
    assert "Summarize" in result
    assert any(word in result.lower() for word in ["concise", "brief", "terse"])
```

**Step 3: Implement**

```python
# src/prompt_poetry/techniques/toggle.py
"""Strategy 7: Binary Toggles.

On/off switches for behavioral dimensions. Each toggle shifts the model's
output along a specific axis.
"""

from __future__ import annotations

from prompt_poetry.core import Transform

_TOGGLES: dict[str, dict[str, str]] = {
    "verbosity": {
        "high": "Explain thoroughly and in detail.",
        "low": "Be concise and brief. Minimum words, maximum signal.",
    },
    "creativity": {
        "high": "Be bold, surprising, and unconventional. Prefer novel approaches.",
        "low": "Be precise and conventional. Stick to proven approaches.",
    },
    "confidence": {
        "commit": "Pick the best option and commit to it. No hedging.",
        "explore": "List multiple options with trade-offs. Don't commit yet.",
    },
    "voice": {
        "casual": "Write like you talk. Direct, informal, no corporate language.",
        "formal": "Write formally and professionally.",
    },
    "depth": {
        "deep": "Go deep. Thorough analysis, comprehensive coverage, no shortcuts.",
        "surface": "High-level summary only. Skip the details.",
    },
}


class _ToggleTransform(Transform):
    """Applies binary toggle switches to a prompt."""

    def __init__(self, settings: dict[str, str]):
        self.settings = settings

    def __call__(self, prompt: str) -> str:
        instructions = []
        for dimension, value in self.settings.items():
            if dimension in _TOGGLES and value in _TOGGLES[dimension]:
                instructions.append(_TOGGLES[dimension][value])
            else:
                instructions.append(f"{dimension}: {value}.")
        block = " ".join(instructions)
        return f"{block}\n\n{prompt}"

    def __repr__(self) -> str:
        pairs = ", ".join(f"{k}={v!r}" for k, v in self.settings.items())
        return f"toggle({pairs})"


def toggle(**settings: str) -> _ToggleTransform:
    """Create a toggle transform with binary switches.

    Built-in dimensions: verbosity, creativity, confidence, voice, depth.
    Each accepts specific values (see _TOGGLES). Unknown combos pass through as-is.
    """
    return _ToggleTransform(settings)
```

**Step 4-5: Run tests, commit**

```bash
git commit -m "feat: toggle technique — binary switch transform"
```

---

### Task 10: Constitution Technique (TDD)

**Files:**
- Create: `src/prompt_poetry/techniques/constitution.py`
- Modify: `src/prompt_poetry/techniques/__init__.py`
- Modify: `tests/test_techniques.py`

**Step 1: Write failing tests**

```python
from prompt_poetry.techniques.constitution import constitution


def test_constitution_returns_transform():
    t = constitution(role="analyst", rules=["cite sources"])
    assert isinstance(t, Transform)


def test_constitution_with_role_and_rules():
    t = constitution(role="Drew's operations analyst", rules=["P&L first", "evidence before assertions", "no jargon"])
    result = t("What's our labor cost trend?")
    assert "Drew's operations analyst" in result
    assert "P&L first" in result
    assert "evidence before assertions" in result
    assert "What's our labor cost trend?" in result


def test_constitution_role_only():
    t = constitution(role="senior engineer")
    result = t("Debug this")
    assert "senior engineer" in result
    assert "Debug this" in result


def test_constitution_with_values():
    t = constitution(role="advisor", rules=["be honest"], values=["simplicity", "leverage"])
    result = t("Evaluate this")
    assert "simplicity" in result
    assert "leverage" in result
```

**Step 3: Implement**

```python
# src/prompt_poetry/techniques/constitution.py
"""Strategy 8: The Constitution — persistent identity.

CLAUDE.md as compressed language that shapes behavior across time.
'Drew steers, Claude drives' isn't an instruction — it's a mantra
that fires every turn.
"""

from __future__ import annotations

from prompt_poetry.core import Transform


class _ConstitutionTransform(Transform):
    """Prepends a persistent identity block to every prompt."""

    def __init__(self, role: str, rules: list[str] | None = None, values: list[str] | None = None):
        self.role = role
        self.rules = rules or []
        self.values = values or []

    def __call__(self, prompt: str) -> str:
        parts = [f"# Identity\nYou are {self.role}."]
        if self.rules:
            rules_block = "\n".join(f"- {r}" for r in self.rules)
            parts.append(f"\n# Rules\n{rules_block}")
        if self.values:
            values_block = "\n".join(f"- {v}" for v in self.values)
            parts.append(f"\n# Values\n{values_block}")
        parts.append(f"\n# Task\n{prompt}")
        return "\n".join(parts)

    def __repr__(self) -> str:
        return f"constitution(role={self.role!r})"


def constitution(role: str, rules: list[str] | None = None, values: list[str] | None = None) -> _ConstitutionTransform:
    """Create a constitution transform — persistent identity block.

    Args:
        role: Who this agent is
        rules: Non-negotiable behavioral rules
        values: Guiding principles
    """
    return _ConstitutionTransform(role, rules, values)
```

Update `techniques/__init__.py` to final form with all 8 imports.

**Step 4-5: Run tests, commit**

```bash
git commit -m "feat: constitution technique — persistent identity transform"
```

---

### Task 11: Presets (TDD)

**Files:**
- Create: `src/prompt_poetry/presets.py`
- Create: `tests/test_presets.py`

**Step 1: Write failing tests**

```python
# tests/test_presets.py
"""Tests for pre-built technique combinations."""

from prompt_poetry.presets import analyst, debugger, writer, researcher, evaluator
from prompt_poetry.core import Transform, Pipeline


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
    """Presets can be further composed with other techniques."""
    from prompt_poetry.techniques import constrain
    custom = analyst | constrain("under 50 words")
    result = custom("Analyze this")
    assert "Analyze this" in result
    assert "under 50 words" in result
```

**Step 3: Implement**

```python
# src/prompt_poetry/presets.py
"""Pre-built technique combinations for common agent types.

These are ready-to-use Pipelines. Import and call directly,
or compose further with |.
"""

from prompt_poetry.techniques import (
    persona, prime, constrain, ritual, narrative, toggle, constitution,
)

# Senior data analyst — commits to answers, goes deep, cites numbers
analyst = persona("senior data analyst") | toggle(confidence="commit", depth="deep") | constrain("cite specific numbers and evidence")

# Principal debugging engineer — systematic, precise, root-cause focused
debugger = persona("principal engineer specializing in debugging") | ritual("step by step") | prime("precision") | constrain("identify root cause only, not symptoms")

# Investigative researcher — thorough, creative, case-study framing
researcher = persona("investigative researcher") | narrative("case study") | toggle(depth="deep", creativity="high")

# Quality evaluator — precise scoring, no hedging
evaluator = persona("quality auditor") | prime("precision") | ritual("score each dimension explicitly") | toggle(confidence="commit")

# Direct writer — casual voice, creative, no jargon
writer = persona("direct communicator who writes like they talk") | toggle(voice="casual", creativity="high") | constrain("no jargon, no corporate language")

__all__ = ["analyst", "debugger", "researcher", "evaluator", "writer"]
```

**Step 4-5: Run tests, commit**

```bash
git commit -m "feat: presets — 5 pre-built technique combinations"
```

---

### Task 12: Public API + Final __init__.py

**Files:**
- Modify: `src/prompt_poetry/__init__.py`
- Create: `tests/test_api.py`

**Step 1: Write failing tests**

```python
# tests/test_api.py
"""Tests for the public API — everything importable from prompt_poetry."""


def test_import_techniques():
    from prompt_poetry import persona, prime, constrain, ritual, meta, narrative, toggle, constitution
    assert callable(persona)
    assert callable(prime)


def test_import_presets():
    from prompt_poetry import presets
    assert callable(presets.analyst)


def test_import_core():
    from prompt_poetry import Transform, Pipeline
    assert Transform is not None


def test_version():
    from prompt_poetry import __version__
    assert __version__ == "0.1.0"


def test_full_composition():
    """End-to-end: compose techniques, call with a prompt, get enhanced string."""
    from prompt_poetry import persona, prime, constrain

    enhanced = persona("systems architect") | prime("precision") | constrain("under 200 words")
    result = enhanced("Design a caching layer")

    assert "systems architect" in result
    assert "Design a caching layer" in result
    assert "under 200 words" in result
    assert isinstance(result, str)
```

**Step 3: Update __init__.py**

```python
# src/prompt_poetry/__init__.py
"""Prompt Poetry — composable prompt engineering techniques for biohacking LLMs.

Usage:
    from prompt_poetry import persona, prime, constrain

    enhanced = persona("analyst") | prime("precision") | constrain("cite sources")
    result = enhanced("What's our revenue trend?")
"""

from prompt_poetry.core import Transform, Pipeline
from prompt_poetry.techniques import (
    persona, prime, constrain, ritual, meta, narrative, toggle, constitution,
)

__version__ = "0.1.0"

__all__ = [
    "Transform", "Pipeline",
    "persona", "prime", "constrain", "ritual",
    "meta", "narrative", "toggle", "constitution",
]
```

**Step 4-5: Run full test suite, commit**

Run: `cd ~/projects/prompt-poetry && uv run pytest tests/ -v`
Expected: All tests pass (should be ~35-40 tests)

```bash
git add -A
git commit -m "feat: public API — all techniques and presets importable from prompt_poetry"
```

---

### Task 13: Full Test Suite Run + Coverage

**Step 1: Run with coverage**

Run: `cd ~/projects/prompt-poetry && uv run pytest tests/ -v --cov=prompt_poetry --cov-report=term-missing`
Expected: All tests pass, >90% coverage

**Step 2: Fix any gaps**

If coverage shows untested branches, add targeted tests.

**Step 3: Commit any new tests**

```bash
git commit -m "test: full coverage pass"
```

---

### Task 14: Create GitHub Repo + Push

**Step 1: Create repo**

Run: `cd ~/projects/prompt-poetry && gh repo create drewbeyersdorf/prompt-poetry --public --source=. --push`

**Step 2: Verify**

Run: `gh repo view drewbeyersdorf/prompt-poetry`
Expected: Repo exists with all code

**Step 3: Create main branch from staging**

```bash
git checkout -b main
git push -u origin main
git checkout staging
```
