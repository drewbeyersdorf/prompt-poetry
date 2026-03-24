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
