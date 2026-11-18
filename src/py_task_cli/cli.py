"""CLI entry point for py-task-cli."""

import logging
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from py_task_cli.models import Priority, Task
from py_task_cli.storage import TaskStore

app = typer.Typer(help="Task manager CLI.")
console = Console()
logger = logging.getLogger(__name__)


def _get_store() -> TaskStore:
    return TaskStore()


_DEFAULT_PRIORITY = Priority.medium


@app.command()
def add(
    title: str = typer.Argument(..., help="Task description."),
    priority: Annotated[
        Priority, typer.Option("--priority", "-p", help="Priority level.")
    ] = _DEFAULT_PRIORITY,
) -> None:
    """Add a new task."""
    store = _get_store()
    task = Task(title=title, priority=priority)
    store.save(task)
    console.print(f"[green]Added[/green] task #{task.id}: {title} ({priority.value})")
    logger.info("Added task id=%s", task.id)


@app.command(name="list")
def list_tasks(
    all: bool = typer.Option(False, "--all", "-a", help="Show completed tasks too."),
) -> None:
    """List tasks."""
    store = _get_store()
    tasks = store.list_all() if all else store.list_pending()

    if not tasks:
        console.print("[yellow]No tasks.[/yellow]")
        return

    table = Table(title="Tasks", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="cyan", justify="right")
    table.add_column("Title")
    table.add_column("Priority", justify="center")
    table.add_column("Status", justify="center")

    for task in tasks:
        status = "[green]done[/green]" if task.done else "[yellow]pending[/yellow]"
        priority_style = {
            Priority.low: "blue",
            Priority.medium: "white",
            Priority.high: "red",
        }.get(task.priority, "white")
        table.add_row(
            str(task.id) if task.id is not None else "-",
            task.title,
            f"[{priority_style}]{task.priority.value}[/{priority_style}]",
            status,
        )

    console.print(table)


@app.command()
def done(task_id: int = typer.Argument(..., help="Task id to mark as done.")) -> None:
    """Mark a task as done."""
    store = _get_store()
    task = store.mark_done(task_id)
    if task is None:
        console.print(f"[red]Task #{task_id} not found.[/red]")
        raise typer.Exit(code=1)
    console.print(f"[green]Marked done[/green]: #{task.id} {task.title}")
    logger.info("Marked task id=%s as done", task.id)


@app.command()
def delete(
    task_id: int = typer.Argument(..., help="Task id to delete."),
) -> None:
    """Delete a task."""
    store = _get_store()
    if store.delete(task_id):
        console.print(f"[green]Deleted[/green] task #{task_id}")
        logger.info("Deleted task id=%s", task_id)
    else:
        console.print(f"[red]Task #{task_id} not found.[/red]")
        raise typer.Exit(code=1)


@app.command()
def export(
    path: str = typer.Argument(..., help="Output Markdown file path."),
    all: bool = typer.Option(False, "--all", "-a", help="Export completed tasks too."),
) -> None:
    """Export tasks to a Markdown file."""
    store = _get_store()
    tasks = store.list_all() if all else store.list_pending()

    lines = ["# Tasks", ""]
    if not tasks:
        lines.append("*No tasks.*")
    else:
        for task in tasks:
            status = "[x]" if task.done else "[ ]"
            prio = task.priority.value
            lines.append(f"- {status} #{task.id} {task.title} (priority: {prio})")

    content = "\n".join(lines) + "\n"
    out_path = Path(path)
    out_path.write_text(content, encoding="utf-8")
    console.print(f"[green]Exported[/green] {len(tasks)} tasks to {out_path}")
    logger.info("Exported %d tasks to %s", len(tasks), out_path)


@app.command()
def ui() -> None:
    """Launch the interactive TUI."""
    store = _get_store()
    tasks = store.list_pending()

    table = Table(title="Pending Tasks", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="cyan", justify="right")
    table.add_column("Title")
    table.add_column("Priority", justify="center")

    for task in tasks:
        priority_style = {
            Priority.low: "blue",
            Priority.medium: "white",
            Priority.high: "red",
        }.get(task.priority, "white")
        table.add_row(
            str(task.id) if task.id is not None else "-",
            task.title,
            f"[{priority_style}]{task.priority.value}[/{priority_style}]",
        )

    pending = store.count_pending()
    total = store.count()
    console.print(
        Panel(
            table,
            title=f"py-task-cli — {pending} pending / {total} total",
            border_style="green",
        )
    )
    console.print("[dim]Commands: add, list, done <id>, export <file>[/dim]")


if __name__ == "__main__":
    app()
