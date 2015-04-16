#!/usr/bin/env python
import os
from random import randint
from datetime import datetime, timedelta
from app import create_app, db
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from app.models import Task

app = create_app(os.getenv('FLASK_CONFIG') or 'development')

manager = Manager(app)
migrate = Migrate(app, db)


def random_date(start, end):
    """helper function for random dates in dummy data"""
    delta = abs(int((end - start).total_seconds()))
    seconds = randint(0, delta)
    return start + timedelta(seconds=seconds)


def make_shell_context():
    return dict(app=app, db=db, Task=Task)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def test():
    """Run the unit tests."""
    import unittest2 as unittest
    tests = unittest.TestLoader().discover('./tests/')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def init_dummy_data():
    """Prefill database with random ."""

    current_time = datetime.utcnow()
    past_time = datetime.utcnow() - timedelta(seconds=100)

    # up to date tasks
    for x in range(0, 10):
        task = Task(randint(100, 1000))
        task.progress = randint(100, 200)
        task.created_at = current_time
        task.updated_at = current_time
        db.session.add(task)
    #
    for x in range(0, 10):
        task = Task(randint(100, 1000))
        task.progress = randint(100, 200)
        task.created_at = past_time
        task.updated_at = past_time
        db.session.add(task)
    db.session.commit()

if __name__ == '__main__':
    manager.run()
