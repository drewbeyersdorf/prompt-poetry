# Cookbook

Copy-paste recipes for common tasks. Each one saves you time today.

---

## Slack / Email

**Draft a message that sounds like you, not a robot:**
```python
from prompt_poetry.presets import writer
writer("Tell the team that the deploy is delayed until Thursday due to the staging bug")
```

**Respond to a frustrated customer:**
```python
from prompt_poetry.presets import customer_responder
customer_responder("Customer says their last 3 orders arrived damaged and wants a refund")
```

## Meetings

**Prep for a meeting in 30 seconds:**
```python
from prompt_poetry.presets import meeting_prep
meeting_prep("Vendor review with ColdTrack — they overbilled us $4K last month")
```

**Summarize notes after a meeting:**
```python
from prompt_poetry.presets import summarizer
summarizer(f"Summarize these meeting notes:\n\n{notes}")
```

**Turn a meeting into action items:**
```python
from prompt_poetry import persona, constrain, ritual
action_extractor = persona("project manager") | ritual("enumerate") | constrain("bullet list only", "include owner and deadline for each")
action_extractor(f"Extract action items from:\n\n{transcript}")
```

## Analysis

**Figure out why a number changed:**
```python
from prompt_poetry.presets import analyst
analyst("Why did labor costs jump 3% this week vs last week?")
```

**Compare two options:**
```python
from prompt_poetry import persona, ritual, toggle
comparer = persona("strategy consultant") | ritual("devil's advocate") | toggle(confidence="commit")
comparer("Should we renew the Intercom contract at $50K/yr or switch to Heymarket at $20K/yr?")
```

**Financial impact analysis:**
```python
from prompt_poetry.presets import financial_analyst
financial_analyst("What's the annual P&L impact of reducing delivery windows from 5 to 3?")
```

## Operations

**Daily ops review:**
```python
from prompt_poetry.presets import ops_reviewer
ops_reviewer("Review yesterday's production metrics and flag anything off")
```

**Executive briefing:**
```python
from prompt_poetry.presets import briefer
briefer("Brief the CEO on where we stand with the warehouse expansion")
```

## Engineering

**Debug something:**
```python
from prompt_poetry.presets import debugger
debugger("The ETL pipeline succeeded but the destination table has NULL values in 30% of rows")
```

**Research a technical decision:**
```python
from prompt_poetry.presets import researcher
researcher("Should we use Kafka or SQS for our event pipeline? We process ~10K events/day")
```

**Code review prompt:**
```python
from prompt_poetry import persona, prime, ritual, constrain
reviewer = persona("senior engineer who has seen production outages caused by bad PRs") | prime("precision") | ritual("enumerate") | constrain("cite file:line for each issue", "classify as critical/important/minor")
reviewer("Review this PR for security and reliability issues")
```

## Knowledge / RAG

**Ask a question with anti-hallucination:**
```python
from prompt_poetry.presets import rag_strict
rag_strict(f"Question: {question}\n\nContext:\n{context_chunks}")
```

**Build a strict knowledge assistant:**
```python
from prompt_poetry import constitution, prime, constrain
assistant = constitution(
    role="company knowledge base",
    rules=["only cite provided sources", "say 'I don't know' if unsure", "include dates"],
    values=["accuracy over completeness"]
) | prime("precision") | constrain("cite with [N] references")
```

## Custom Pipelines

**Build a pipeline for your specific role:**
```python
from prompt_poetry import persona, prime, constrain, ritual, toggle

# Product manager
pm = persona("product manager balancing user needs, engineering capacity, and business goals") | ritual("enumerate") | toggle(confidence="commit") | constrain("prioritize by impact")

# Sales engineer
sales_eng = persona("technical sales engineer") | toggle(voice="casual", depth="deep") | constrain("explain like the prospect is technical but unfamiliar with our product")

# QA tester
qa = persona("QA engineer who finds edge cases others miss") | prime("precision") | ritual("enumerate") | constrain("list test cases as given/when/then")
```

## CLI One-Liners

```bash
# Quick analysis
prompt-poetry -p analyst "Why did churn spike in March?"

# Debug help
prompt-poetry -p debugger "CI passes locally but fails on GitHub Actions"

# Meeting prep
prompt-poetry --persona "chief of staff" --narrative briefing "Prep for board meeting on Q1 results"

# Pipe from clipboard
wl-paste | prompt-poetry -p summarizer
```
