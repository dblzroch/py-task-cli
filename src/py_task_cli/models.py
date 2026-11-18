"""Domain models for py-task-cli."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


@dataclass
class Task:
    id: int | None = None
    title: str = ""
    priority: Priority = Priority.medium
    done: bool = False
    created_at: datetime | None = None
