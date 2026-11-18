# py-task-cli

> Task manager CLI with SQLite, rich TUI and Markdown export.

[![CI](https://github.com/dblzroch/py-task-cli/actions/workflows/ci.yml/badge.svg)](https://github.com/dblzroch/py-task-cli/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](pyproject.toml)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

A small, fast command-line task manager. Store tasks in SQLite, view them in a rich
terminal table, mark them done, and export to Markdown. Built with Typer + Rich +
sqlite-utils, managed with uv.

## Quickstart

```bash
# Clone
git clone https://github.com/dblzroch/py-task-cli.git
cd py-task-cli

# Install (uv)
uv sync --dev

# Add a task
uv run task add "Review pull request" --priority high

# List pending tasks
uv run task list

# Mark as done
uv run task done 1

# Export to Markdown
uv run task export tasks.md
```

## Commands

| Command | Description |
|---|---|
| `task add <title> --priority low|medium|high` | Add a new task |
| `task list [--all]` | List pending (or all) tasks |
| `task done <id>` | Mark a task as done |
| `task delete <id>` | Delete a task |
| `task export <file.md>` | Export tasks to Markdown |
| `task ui` | Show pending tasks in a rich table |

## How it works

- **CLI**: [Typer](https://typer.tiangolo.com/) commands (`add`, `list`, `done`, `delete`, `export`, `ui`).
- **Storage**: [sqlite-utils](https://sqlite-utils.datasette.io/) backed SQLite database.
- **UI**: [Rich](https://rich.readthedocs.io/) tables and panels.
- **Config**: database path via `TASK_DB_PATH` env var (defaults to `~/.local/share/py-task-cli/tasks.db`).
- **Tests**: `pytest` with coverage gate at 80%.
- **CI**: GitHub Actions runs ruff, mypy and pytest on every push/PR.

## Tests & quality

```bash
make test      # pytest with coverage
make lint      # ruff + mypy
make fmt       # ruff format
```

## License

MIT
