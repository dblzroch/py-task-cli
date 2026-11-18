"""Tests for py-task-cli CLI (typer)."""

import os

from typer.testing import CliRunner

from py_task_cli.cli import app
from py_task_cli.models import Task


def _env(store):
    return {**os.environ, "TASK_DB_PATH": str(store.db_path)}


def test_add_and_list(store):
    runner = CliRunner()
    result = runner.invoke(
        app, ["add", "Buy milk", "--priority", "high"], env=_env(store)
    )
    assert result.exit_code == 0
    assert "Buy milk" in result.output

    result = runner.invoke(app, ["list"], env=_env(store))
    assert result.exit_code == 0
    assert "Buy milk" in result.output


def test_list_no_tasks(store):
    runner = CliRunner()
    result = runner.invoke(app, ["list"], env=_env(store))
    assert result.exit_code == 0
    assert "No tasks" in result.output


def test_done(store):
    task = store.save(Task(title="To complete"))

    runner = CliRunner()
    result = runner.invoke(app, ["done", str(task.id)], env=_env(store))
    assert result.exit_code == 0
    assert "Marked done" in result.output

    fetched = store.get(task.id)
    assert fetched.done is True


def test_done_not_found(store):
    runner = CliRunner()
    result = runner.invoke(app, ["done", "999"], env=_env(store))
    assert result.exit_code == 1


def test_delete(store):
    task = store.save(Task(title="To delete"))

    runner = CliRunner()
    result = runner.invoke(app, ["delete", str(task.id)], env=_env(store))
    assert result.exit_code == 0
    assert "Deleted" in result.output

    assert store.get(task.id) is None


def test_delete_not_found(store):
    runner = CliRunner()
    result = runner.invoke(app, ["delete", "999"], env=_env(store))
    assert result.exit_code == 1


def test_export(store):
    store.save(Task(title="Export task"))

    runner = CliRunner()
    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as tmp:
        out_path = Path(tmp) / "tasks.md"
        result = runner.invoke(app, ["export", str(out_path)], env=_env(store))
        assert result.exit_code == 0
        assert "Exported" in result.output
        assert out_path.exists()


def test_export_empty(store):
    runner = CliRunner()
    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as tmp:
        out_path = Path(tmp) / "empty.md"
        result = runner.invoke(app, ["export", str(out_path)], env=_env(store))
        assert result.exit_code == 0
        assert "Exported" in result.output


def test_ui(store):
    store.save(Task(title="UI task"))

    runner = CliRunner()
    result = runner.invoke(app, ["ui"], env=_env(store))
    assert result.exit_code == 0
    assert "py-task-cli" in result.output
