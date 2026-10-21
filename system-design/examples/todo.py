#!/usr/bin/env python3
"""Unit 1: one trusted local user; explicit service/storage boundary.

Run: python3 system-design/examples/todo.py
No network, external packages, or persistent files are required by the demo.
This is not an HTTP server or a multi-user authorization implementation.
"""
from dataclasses import dataclass, asdict
from pathlib import Path
import sqlite3
import tempfile


@dataclass(frozen=True)
class Task:
    id: int
    title: str
    done: bool


class SQLiteTasks:
    """Each insert owns its transaction; return only after commit succeeds."""
    def __init__(self, path):
        self.connection = sqlite3.connect(path)
        self.connection.execute('PRAGMA synchronous = FULL')
        self.connection.execute('''CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL CHECK(length(title) BETWEEN 1 AND 200),
            done INTEGER NOT NULL DEFAULT 0 CHECK(done IN (0, 1)))''')
        self.connection.commit()

    def insert(self, title):
        with self.connection:
            cursor = self.connection.execute(
                'INSERT INTO tasks(title) VALUES (?)', (title,))
            task_id = cursor.lastrowid
        # The context manager commits before this return; errors propagate.
        return Task(task_id, title, False)

    def list(self):
        return [Task(row[0], row[1], bool(row[2])) for row in
                self.connection.execute('SELECT id, title, done FROM tasks ORDER BY id')]

    def set_done(self, task_id):
        with self.connection:
            cursor = self.connection.execute(
                'UPDATE tasks SET done = 1 WHERE id = ?', (task_id,))
            if cursor.rowcount != 1:
                raise KeyError(task_id)
            row = self.connection.execute(
                'SELECT id, title, done FROM tasks WHERE id = ?', (task_id,)).fetchone()
        return Task(row[0], row[1], bool(row[2]))

    def close(self):
        self.connection.close()


class TaskService:
    def __init__(self, repository):
        self.repository = repository

    def create(self, title):
        if not isinstance(title, str):
            raise ValueError('title must be text')
        title = title.strip()
        if not 1 <= len(title) <= 200:
            raise ValueError('title must contain 1–200 characters after trimming')
        return self.repository.insert(title)

    def complete(self, task_id):
        if type(task_id) is not int or task_id <= 0:
            raise ValueError('task id must be a positive integer')
        return self.repository.set_done(task_id)


def demo():
    with tempfile.TemporaryDirectory(prefix='system-atlas-') as directory:
        path = Path(directory)/'tasks.sqlite'
        repository = SQLiteTasks(path)
        try:
            task = TaskService(repository).create('  Read  ')
            print('Created:', asdict(task))
        finally:
            repository.close()
        recovered = SQLiteTasks(path)
        try:
            print('After reopen:', [asdict(t) for t in recovered.list()])
            print('Completed:', asdict(TaskService(recovered).complete(task.id)))
        finally:
            recovered.close()


if __name__ == '__main__':
    demo()
