from prompt_poetry.core import Transform

# === PERSONA ===
from prompt_poetry.techniques.persona import persona


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


# === PRIMER ===
from prompt_poetry.techniques.primer import prime


def test_prime_returns_transform():
    t = prime("urgency")
    assert isinstance(t, Transform)


def test_prime_urgency():
    t = prime("urgency")
    result = t("Review this data")
    assert "Review this data" in result
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


# === CONSTRAINT ===
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


# === RITUAL ===
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
