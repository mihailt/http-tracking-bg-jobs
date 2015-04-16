import unittest2 as unittest
from datetime import datetime, timedelta
import json
from flask import current_app, url_for
from app import create_app, db
from app.models import Task

class ViewsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_index_view(self):
        response = self.client.get(url_for('main.index'))
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['version'], 0.1)


    def test_tasks_view(self):
        response = self.client.get(url_for('main.tasks'))
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(data['tasks']), 0)
        self.assertEqual(data['total'], 0)

        task = Task.create(total=100)

        response = self.client.get(url_for('main.tasks'))
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(data['tasks']), 1)
        self.assertEqual(data['tasks'][0]['id'], task.id)
        self.assertEqual(data['total'], 1)

        task.updated_at = datetime.utcnow() - timedelta(seconds=100)
        db.session.add(task)
        db.session.commit()

        response = self.client.get(url_for('main.tasks'))
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(data['tasks']), 0)
        self.assertEqual(data['total'], 0)


    def test_task_view(self):
        response = self.client.get(url_for('main.view_task', task_id=1))
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['status'], 'not found')

        task = Task.create(total=100)
        response = self.client.get(url_for('main.view_task', task_id=task.id))
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['task']['id'], task.id)

    def test_create_view(self):
        response = self.client.post(
            url_for('main.create_task'),
            data=dict(total=1)
        )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 201)
        self.assertTrue(data['task_id'])

        response = self.client.post(
            url_for('main.create_task'),
            data=dict(total='asdasd')
        )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['status'], 'error')

        response = self.client.post(url_for('main.create_task'))
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['status'], 'error')


    def test_update_view(self):
        response = self.client.put(
            url_for('main.update_task', task_id=1),
            data=dict(total=1)
        )

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['status'], 'not found')

        task = Task.create(total=100)

        response = self.client.put(
            url_for('main.update_task', task_id=task.id),
        )

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['status'], 'not found')

        response = self.client.put(
            url_for('main.update_task', task_id=task.id),
            data=dict(progress=20)
        )

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['task']['progress'], 20)


    def test_update_incremental_view(self):

        response = self.client.put(
            url_for('main.update_task_increment', task_id=1, progress=1),
            data=dict(total=1)
        )

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['status'], 'not found')


        task = Task.create(total=100)
        response = self.client.put(
            url_for('main.update_task_increment', task_id=task.id, progress=1),
        )

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['task']['progress'], 1)

        response = self.client.put(
            url_for('main.update_task_increment', task_id=task.id, progress=1),
        )

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['task']['progress'], 2)

    def test_delete_view(self):

        response = self.client.delete(url_for('main.delete_task', task_id=1))
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['status'], 'not found')

        task = Task.create(total=100)

        response = self.client.delete(url_for('main.delete_task', task_id=task.id))
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'deleted')


