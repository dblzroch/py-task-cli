"""Storage layer for py-task-cli."""

from pathlib import Path


class TaskStore:
    def __init__(self, db_path: Path):
        self.db_path = db_path

    def save(self, task):
        raise NotImplementedError

    def list_pending(self):
        raise NotImplementedError
