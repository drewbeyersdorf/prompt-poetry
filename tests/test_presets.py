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
    from prompt_poetry.techniques import constrain
    custom = analyst | constrain("under 50 words")
    result = custom("Analyze this")
    assert "Analyze this" in result
    assert "under 50 words" in result
