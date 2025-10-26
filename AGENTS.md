# Repository Guidelines

## Project Structure & Module Organization
- `md2pages/` holds the core package. Key modules: `cli.py` (entry point), `generator.py` (site orchestration), `converter.py` (Markdown ➝ HTML), `template.py` (Jinja rendering), and `utils.py` (file I/O helpers).
- `templates/` contains the Jinja templates (`base.html`, `page.html`, `index.html`) that define the rendered layout.
- `static/` serves shared assets (`style.css`, `script.js`) that are copied into every build.
- `test_input/` offers sample Markdown content for manual runs; expand `tests/` with pytest suites that mirror real project structures.

## Build, Test, and Development Commands
- `uv sync` installs runtime + dev dependencies from `pyproject.toml` and `uv.lock`.
- `uv run md2pages <input_dir>` converts Markdown under `<input_dir>` using `.site.yml` when present.
- `uv run pytest` executes the automated test suite; add `-k "pattern"` when you need to focus on a subset.
- `uv pip install -e .` enables editable installs for local experimentation in other environments.

## Coding Style & Naming Conventions
- Target Python ≥3.9, follow PEP 8 with 4-space indentation, and keep functions small and composable.
- Prefer `snake_case` for functions and variables, `PascalCase` for classes/dataclasses, and reuse existing type hints for new surfaces.
- Treat Jinja templates as the single source of markup; update `templates/` instead of embedding HTML strings.

## Testing Guidelines
- Use pytest; place files under `tests/` with `test_*.py` naming and fixture helpers when multiple scenarios share setup.
- Exercise conversions via temporary directories that mimic `test_input/`, covering success counts, error handling, and asset copying.
- When adding new configuration or CLI flags, pair them with regression tests to guard against template or file-walk regressions.

## Commit & Pull Request Guidelines
- Match the existing history by prefixing commits with a scope-based keyword (`fix:`, `update:`, `feat:`) followed by a concise imperative summary.
- Keep pull requests focused: describe the change, outline testing (`uv run pytest`, manual site checks), and link issues or screenshots for UI-affecting work.
- Highlight backward-compatibility considerations (e.g., config defaults, template markup) so reviewers can validate downstream impact.

## Configuration Tips
- Document behavior changes in `.site.yml`; note default values (`output_dir: site`, `exclude: [".git/**"]`, `site.title: "Site"`).
- For custom themes, add assets to `static/` and extend `templates/` with overrides instead of editing generated output.
