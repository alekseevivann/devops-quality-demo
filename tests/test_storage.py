import pytest

from app.storage import TaskStore


def test_add_assigns_sequential_ids():
    store = TaskStore()
    first = store.add("Первая")
    second = store.add("Вторая")
    assert (first["id"], second["id"]) == (1, 2)
    assert len(store.all()) == 2


def test_add_rejects_empty_title():
    store = TaskStore()
    with pytest.raises(ValueError):
        store.add("   ")
    with pytest.raises(ValueError):
        store.add(None)


def test_complete_marks_task_done():
    store = TaskStore()
    task = store.add("Сделать курсовую")
    assert store.complete(task["id"])["done"] is True


def test_complete_unknown_task_raises():
    store = TaskStore()
    with pytest.raises(KeyError):
        store.complete(42)
