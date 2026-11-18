"""Tests for py-task-cli storage and models."""

from py_task_cli.models import Priority, Task


def test_save_and_get_task(store):
    task = Task(title="Test task", priority=Priority.high)
    saved = store.save(task)

    assert saved.id is not None
    assert saved.title == "Test task"
    assert saved.priority == Priority.high

    fetched = store.get(saved.id)
    assert fetched is not None
    assert fetched.title == "Test task"


def test_get_not_found(store):
    assert store.get(999) is None


def test_mark_done(store):
    task = store.save(Task(title="To complete"))

    store.mark_done(task.id)
    fetched = store.get(task.id)
    assert fetched.done is True


def test_mark_done_not_found(store):
    assert store.mark_done(999) is None


def test_list_pending_excludes_done(store):
    store.save(Task(title="Pending 1"))
    store.save(Task(title="Pending 2"))
    done_task = store.save(Task(title="Done one"))
    store.mark_done(done_task.id)

    pending = store.list_pending()
    assert len(pending) == 2
    assert all(not t.done for t in pending)


def test_list_all_returns_all(store):
    store.save(Task(title="Task 1"))
    done_task = store.save(Task(title="Task 2"))
    store.mark_done(done_task.id)

    all_tasks = store.list_all()
    assert len(all_tasks) == 2


def test_delete(store):
    task = store.save(Task(title="To delete"))

    assert store.delete(task.id) is True
    assert store.get(task.id) is None


def test_delete_not_found(store):
    assert store.delete(999) is False


def test_count_and_count_pending(store):
    assert store.count() == 0
    assert store.count_pending() == 0

    store.save(Task(title="One"))
    store.save(Task(title="Two"))
    assert store.count() == 2
    assert store.count_pending() == 2

    done_task = store.save(Task(title="Three"))
    store.mark_done(done_task.id)
    assert store.count() == 3
    assert store.count_pending() == 2


def test_task_model_defaults():
    task = Task(title="Minimal")
    assert task.title == "Minimal"
    assert task.priority == Priority.medium
    assert task.done is False
    assert task.id is None
    assert task.created_at is not None


def test_task_to_dict_and_from_dict(store):
    original = Task(title="Round trip", priority=Priority.low)
    saved = store.save(original)

    data = saved.to_dict()
    assert data["title"] == "Round trip"
    assert data["priority"] == "low"
    assert data["done"] is False

    restored = Task.from_dict(data)
    assert restored.title == "Round trip"
    assert restored.priority == Priority.low
    assert restored.done is False
