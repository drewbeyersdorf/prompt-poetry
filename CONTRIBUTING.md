# Contributing

prompt-poetry is designed to be easy to extend. Every technique is one file, one class, one test file.

## Adding a technique

1. Create `src/prompt_poetry/techniques/your_technique.py`
2. Subclass `Transform`, implement `__call__`
3. Export a factory function (lowercase, matches the filename)
4. Add tests in `tests/test_techniques.py`
5. Add to `techniques/__init__.py`

Use any existing technique as a template. The simplest is `primer.py`.

## Adding a preset

1. Add to `src/prompt_poetry/presets.py`
2. Add tests in `tests/test_presets.py`
3. Add a recipe to `COOKBOOK.md`

## Running tests

```bash
pip install -e ".[dev]"
pytest
```

78 tests. They run in under a second.

## Style

- No dependencies in core. Pure Python only.
- Every technique is a Transform. No exceptions.
- Tests use plain assert. No mocking needed.
- Docstrings on modules and factory functions. Comments only where non-obvious.

## Pull requests

- One technique or preset per PR
- Tests required
- Keep it simple - if the technique needs more than 50 lines, it's probably two techniques
