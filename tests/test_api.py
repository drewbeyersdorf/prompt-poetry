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
    from prompt_poetry import persona, prime, constrain
    enhanced = persona("systems architect") | prime("precision") | constrain("under 200 words")
    result = enhanced("Design a caching layer")
    assert "systems architect" in result
    assert "Design a caching layer" in result
    assert "under 200 words" in result
    assert isinstance(result, str)
