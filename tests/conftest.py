"""Pytest fixtures for py-task-cli."""

import shutil
import tempfile
from pathlib import Path

import pytest

from py_task_cli.storage import TaskStore


@pytest.fixture
def store():
    """Provide a TaskStore backed by a temp SQLite file, closed after the test."""
    tmp = tempfile.mkdtemp()
    db_path = Path(tmp) / "tasks.db"
    s = TaskStore(db_path)
    s.db_path = db_path  # exposed so CLI tests can set TASK_DB_PATH
    yield s
    s.db.conn.close()
    shutil.rmtree(tmp, ignore_errors=True)
