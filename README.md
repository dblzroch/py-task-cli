# py-task-cli

> Task manager CLI with SQLite, rich TUI and Markdown export.

[![CI](https://github.com/dblzroch/py-task-cli/actions/workflows/ci.yml/badge.svg)](https://github.com/dblzroch/py-task-cli/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](pyproject.toml)

Quickstart:

```bash
uv sync --dev
uv run task --help
```

Run the interactive TUI:

```bash
uv run task ui
```

Add a task:

```bash
uv run task add "Review pull request" --priority high
```

List pending tasks:

```bash
uv run task list
```

Export to Markdown:

```bash
uv run task export tasks.md
```

## How it works

- **CLI**: Typer-based commands (`add`, `list`, `done`, `export`, `ui`).
- **Storage**: SQLite via `sqlite-utils`, one database file.
- **UI**: `rich` table + live panel for the interactive mode.
- **Tests**: `pytest` with coverage gate at 80%.
- **CI**: GitHub Actions runs ruff, mypy and pytest on every push/PR.

## Tests

```bash
make test
```

## License

MIT
