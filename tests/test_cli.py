"""Tests for the CLI."""

from prompt_poetry.cli import main


def test_preset_analyst(capsys):
    main(["--preset", "analyst", "Why did costs increase?"])
    out = capsys.readouterr().out
    assert "Why did costs increase?" in out
    assert "senior data analyst" in out.lower()


def test_preset_debugger(capsys):
    main(["--preset", "debugger", "Tests fail in CI"])
    out = capsys.readouterr().out
    assert "Tests fail in CI" in out
    assert "step" in out.lower()


def test_persona_flag(capsys):
    main(["--persona", "jazz musician", "Improvise a melody"])
    out = capsys.readouterr().out
    assert "jazz musician" in out
    assert "Improvise a melody" in out


def test_prime_flag(capsys):
    main(["--prime", "urgency", "Check the servers"])
    out = capsys.readouterr().out
    assert "Check the servers" in out
    assert "critical" in out.lower()


def test_constrain_flag(capsys):
    main(["--constrain", "under 50 words, no jargon", "Explain DNS"])
    out = capsys.readouterr().out
    assert "Explain DNS" in out
    assert "under 50 words" in out


def test_combined_flags(capsys):
    main(["--persona", "architect", "--prime", "precision", "--constrain", "3 sentences", "Design a cache"])
    out = capsys.readouterr().out
    assert "architect" in out
    assert "Design a cache" in out
    assert "3 sentences" in out


def test_list_presets(capsys):
    main(["--list-presets"])
    out = capsys.readouterr().out
    assert "analyst" in out
    assert "debugger" in out
    assert "writer" in out


def test_list_techniques(capsys):
    main(["--list-techniques"])
    out = capsys.readouterr().out
    assert "persona" in out
    assert "ritual" in out
    assert "constitution" in out


def test_meta_flag(capsys):
    main(["--meta", "Write an email"])
    out = capsys.readouterr().out
    assert "Write an email" in out
    assert "rewrite" in out.lower()


def test_toggle_flag(capsys):
    main(["--toggle", "depth=deep,creativity=high", "Brainstorm ideas"])
    out = capsys.readouterr().out
    assert "Brainstorm ideas" in out
    assert "deep" in out.lower() or "thorough" in out.lower()


def test_narrative_flag(capsys):
    main(["--narrative", "postmortem", "What happened?"])
    out = capsys.readouterr().out
    assert "What happened?" in out
    assert "postmortem" in out.lower()
