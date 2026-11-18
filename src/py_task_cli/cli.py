"""CLI entry point for py-task-cli."""

import typer

app = typer.Typer(help="Task manager CLI.")


@app.command()
def add(title: str, priority: str = "medium"):
    """Add a new task."""
    typer.echo(f"Not implemented yet: {title} ({priority})")


@app.command()
def list():
    """List pending tasks."""
    typer.echo("Not implemented yet.")


if __name__ == "__main__":
    app()
