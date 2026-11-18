"""Placeholder tests for py-task-cli."""

from py_task_cli.models import Task, Priority


def test_task_defaults():
    task = Task(title="Buy milk")
    assert task.title == "Buy milk"
    assert task.priority == Priority.medium
    assert task.done is False
