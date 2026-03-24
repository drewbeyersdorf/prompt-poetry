---
name: New preset
about: Propose a pre-built technique pipeline for a common task type
title: "New preset: "
labels: enhancement
---

## Preset name

<!-- One word, lowercase. e.g. "negotiator", "interviewer", "planner" -->

## Who uses this

<!-- What role or task type does this serve? -->

## Composition

```python
from prompt_poetry import persona, prime, constrain, ritual, toggle

your_preset = persona("...") | prime("...") | constrain("...")
```

## Example usage

```python
your_preset("A real task someone would use this for")
```
