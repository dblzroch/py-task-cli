"""Storage layer for py-task-cli."""

import logging
import os
from pathlib import Path
from typing import Any, cast

from sqlite_utils import Database

from py_task_cli.models import Task

logger = logging.getLogger(__name__)

DEFAULT_DB_PATH = Path.home() / ".local" / "share" / "py-task-cli" / "tasks.db"


class TaskStore:
    """SQLite-backed task storage."""

    def __init__(self, db_path: Path | None = None):
        if db_path is None:
            env_path = os.getenv("TASK_DB_PATH")
            db_path = Path(env_path) if env_path else DEFAULT_DB_PATH
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.db = Database(self.db_path)
        self._tasks = cast(Any, self.db["tasks"])
        self._init_schema()

    def _init_schema(self) -> None:
        """Create the tasks table if it does not exist."""
        self._tasks.create(
            {
                "id": int,
                "title": str,
                "priority": str,
                "done": int,
                "created_at": str,
            },
            pk="id",
            if_not_exists=True,
        )
        logger.info("Storage initialized at %s", self.db_path)

    def save(self, task: Task) -> Task:
        """Insert or update a task and return it with its id assigned."""
        row = task.to_dict()
        task_id = row.pop("id", None)
        if task_id is None:
            inserted_id = self._tasks.insert(row).last_pk
            task.id = int(inserted_id) if inserted_id is not None else None
        else:
            self._tasks.update(task_id, row)
            task.id = task_id
        logger.info("Saved task id=%s title=%r", task.id, task.title)
        return task

    def get(self, task_id: int) -> Task | None:
        """Return a task by id, or None if not found."""
        rows = list(self._tasks.rows_where("id = ?", [task_id]))
        if not rows:
            return None
        return Task.from_dict(dict(rows[0]))

    def list_pending(self) -> list[Task]:
        """Return all not-done tasks ordered by created_at desc."""
        rows = self._tasks.rows_where("done = 0", order_by="-created_at")
        return [Task.from_dict(dict(row)) for row in rows]

    def list_all(self) -> list[Task]:
        """Return all tasks ordered by created_at desc."""
        rows = self._tasks.rows_where(order_by="-created_at")
        return [Task.from_dict(dict(row)) for row in rows]

    def mark_done(self, task_id: int) -> Task | None:
        """Mark a task as done. Returns the task or None if not found."""
        task = self.get(task_id)
        if task is None:
            return None
        task.done = True
        self.save(task)
        return task

    def delete(self, task_id: int) -> bool:
        """Delete a task by id. Returns True if deleted."""
        if self.get(task_id) is None:
            return False
        self._tasks.delete(task_id)
        return True

    def count(self) -> int:
        """Return total number of tasks."""
        return int(self._tasks.count)

    def count_pending(self) -> int:
        """Return number of pending tasks."""
        return int(self._tasks.count_where("done = 0"))
