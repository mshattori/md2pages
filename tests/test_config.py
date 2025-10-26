import yaml

from md2pages.config import load_config


def test_load_config_defaults(tmp_path):
    config = load_config(tmp_path)

    assert config.exclude == []
    assert config.respect_gitignore is True


def test_load_config_merges_excludes_and_respects_flag(tmp_path):
    (tmp_path / ".gitignore").write_text("build/\n", encoding="utf-8")
    config_file = tmp_path / ".site.yml"
    config_file.write_text(
        yaml.safe_dump(
            {
                "exclude": ["drafts/**"],
                "respect_gitignore": False,
            }
        ),
        encoding="utf-8",
    )

    config = load_config(tmp_path)

    assert config.respect_gitignore is False
    assert "drafts/**" in config.exclude
    assert "build/**" not in config.exclude


def test_load_config_includes_gitignore_patterns(tmp_path):
    (tmp_path / ".gitignore").write_text("/site/\nnotes.md\n.venv\n", encoding="utf-8")

    config = load_config(tmp_path)

    assert "site/**" in config.exclude
    assert "notes.md" in config.exclude
    assert ".venv" in config.exclude
    assert ".venv/**" in config.exclude
