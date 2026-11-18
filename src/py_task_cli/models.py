"""Domain models for py-task-cli."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any


class Priority(StrEnum):
    """Task priority levels.

    Attributes:
        low: Low priority tasks.
        medium: Medium priority tasks (default).
        high: High priority tasks.
    """

    low = "low"
    medium = "medium"
    high = "high"


@dataclass
class Task:
    """Represents a task in the task manager.

    Attributes:
        id: Unique identifier for the task (auto-assigned).
        title: The task description.
        priority: Task priority level.
        done: Whether the task is completed.
        created_at: Timestamp when the task was created.
    """

    id: int | None = None
    title: str = ""
    priority: Priority = Priority.medium
    done: bool = False
    created_at: datetime | None = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict[str, Any]:
        """Convert the task to a dictionary for storage.

        Returns:
            Dictionary representation of the task.
        """
        return {
            "id": self.id,
            "title": self.title,
            "priority": self.priority.value,
            "done": self.done,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Task":
        """Create a Task instance from a dictionary.

        Args:
            data: Dictionary containing task data.

        Returns:
            A new Task instance.
        """
        created_at = None
        if data.get("created_at"):
            created_at = datetime.fromisoformat(data["created_at"])

        priority_str = data.get("priority", "medium")
        try:
            priority = Priority(priority_str)
        except ValueError:
            priority = Priority.medium

        return cls(
            id=data.get("id"),
            title=data.get("title", ""),
            priority=priority,
            done=bool(data.get("done", False)),
            created_at=created_at,
        )
