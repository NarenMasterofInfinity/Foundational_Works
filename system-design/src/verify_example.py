#!/usr/bin/env python3
"""Check the actual teaching promises, including abrupt process loss."""
import importlib.util
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile

EXAMPLE=Path(__file__).resolve().parents[1]/'examples'/'todo.py'
spec=importlib.util.spec_from_file_location('todo_example',EXAMPLE)
todo=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=todo
spec.loader.exec_module(todo)

with tempfile.TemporaryDirectory(prefix='atlas-todo-test-') as directory:
    path=Path(directory)/'tasks.sqlite'
    repo=todo.SQLiteTasks(path);service=todo.TaskService(repo)
    for title in ('','  ','x'*201,None,17):
        try:service.create(title)
        except ValueError:pass
        else:raise AssertionError('Invalid title accepted')
    assert repo.list()==[]
    task=service.create('  Read  ')
    assert task.title=='Read' and task.done is False
    repo.close()
    reopened=todo.SQLiteTasks(path)
    assert reopened.list()==[task]
    completed=todo.TaskService(reopened).complete(task.id)
    assert completed.done is True
    assert todo.TaskService(reopened).complete(task.id)==completed
    try:todo.TaskService(reopened).complete(999)
    except KeyError:pass
    else:raise AssertionError('Unknown task completed successfully')
    reopened.close()
    persisted=todo.SQLiteTasks(path)
    assert persisted.list()==[completed]
    persisted.close()

    class FailingRepository:
        def insert(self,title):raise OSError('injected storage failure')
    try:todo.TaskService(FailingRepository()).create('Read')
    except OSError:pass
    else:raise AssertionError('Storage failure returned success')

    # Kill the writer without normal cleanup, once before commit and once after.
    child='''import os,sqlite3,sys
c=sqlite3.connect(sys.argv[1])
c.execute("INSERT INTO tasks(title) VALUES (?)",(sys.argv[2],))
if sys.argv[3]=="commit":c.commit()
os._exit(0)
'''
    for label,action in [('uncommitted','no-commit'),('committed-before-reply','commit')]:
        subprocess.run([sys.executable,'-c',child,str(path),label,action],check=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
    with sqlite3.connect(path) as connection:
        titles=[row[0] for row in connection.execute('SELECT title FROM tasks ORDER BY id')]
    assert titles==['Read','committed-before-reply'],titles

print('PASS: validation, no inserts on invalid input, trim, reopen persistence, committed completion, repeated completion, missing task, propagated storage failure, abrupt loss before and after commit.')
