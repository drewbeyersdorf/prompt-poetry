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

## Rules
- Zero dependencies in main package. Only stdlib.
- Every technique is a Transform. No exceptions.
- Tests use plain assert, no mocking needed (pure string transforms).
