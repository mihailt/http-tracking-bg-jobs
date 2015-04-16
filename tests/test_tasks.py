import unittest2 as unittest
from datetime import datetime, timedelta
from flask import current_app
from app import create_app, db
from app.models import Task

class TasksTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_task_create(self):
        task = Task.create(total=100)
        self.assertTrue(isinstance(task, Task))
        self.assertTrue(task.total is 100)
        self.assertTrue(task.progress is 0)
        self.assertTrue(isinstance(task, Task))
        self.assertTrue(isinstance(task, Task))

        with self.assertRaises(TypeError):
            Task.create()

        with self.assertRaises(TypeError):
            Task.create('asdasd')

    def test_task_find(self):
        task = Task.create(total=100)
        found = Task.find_recent(task.id)

        self.assertTrue(task.id is found.id)
        self.assertFalse(Task.find_recent(10))

        with self.assertRaises(TypeError):
            Task.find_recent('asdasd')

    def test_task_update(self):
        task = Task.create(total=100)
        prev_updated_at = task.updated_at

        self.assertTrue(Task.update(task.id, progress=1))
        self.assertTrue(task.total is 100)
        self.assertTrue(task.progress is 1)
        self.assertTrue(task.updated_at > prev_updated_at)

        Task.update(task.id, progress=100, inc=True)
        self.assertTrue(task.progress is 101)

        with self.assertRaises(TypeError):
            Task.update(task.id, 'asdasd')

        with self.assertRaises(TypeError):
            Task.update('asdasd', '12')

        with self.assertRaises(ValueError):
            Task.update(task.id, -10)


    def test_task_delete(self):
        task1 = Task.create(total=1)
        task2 = Task.create(total=2)
        self.assertTrue(Task.delete(task1.id))
        self.assertFalse(Task.find_recent(task1.id))
        self.assertTrue(Task.find_recent(task2.id))

        with self.assertRaises(TypeError):
            Task.delete('asdasd')

    def test_task_recent(self):
        task1 = Task.create(total=1)
        task2 = Task.create(total=2)
        task3 = Task.create(total=3)

        self.assertEqual(len(Task.get_recent_tasks()), 3)

        task3.updated_at = task3.updated_at - timedelta(60)
        db.session.add(task3)
        db.session.commit()

        self.assertEqual(len(Task.get_recent_tasks()), 2)

        task2.updated_at = task2.updated_at - timedelta(60)
        db.session.add(task2)
        db.session.commit()

        self.assertEqual(len(Task.get_recent_tasks()), 1)


        task1.updated_at = task1.updated_at - timedelta(60)
        db.session.add(task1)
        db.session.commit()

        self.assertEqual(len(Task.get_recent_tasks()), 0)

        task1.updated_at = datetime.utcnow()
        task2.updated_at = datetime.utcnow()
        task3.updated_at = datetime.utcnow()

        db.session.add(task1)
        db.session.add(task2)
        db.session.add(task3)
        db.session.commit()

        self.assertEqual(len(Task.get_recent_tasks()), 3)

        with self.assertRaises(TypeError):
            Task.get_recent_tasks('asdasd')
