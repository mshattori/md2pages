from md2pages.config import load_config
from md2pages.utils import find_markdown_files


def test_find_markdown_files_respects_gitignore(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()

    (docs / ".gitignore").write_text(".venv\n", encoding="utf-8")

    keep = docs / "note.md"
    keep.write_text("# Note", encoding="utf-8")

    license_path = docs / ".venv" / "lib" / "python3.12" / "site-packages" / "markdown" / "LICENSE.md"
    license_path.parent.mkdir(parents=True)
    license_path.write_text("license", encoding="utf-8")

    config = load_config(docs)
    results = find_markdown_files(docs, config.exclude)

    assert keep in results
    assert license_path not in results
