from datetime import datetime, timedelta
from . import db
from sqlalchemy import and_

class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Integer, nullable=False)
    progress = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, total):
        self.total = total
        self.progress = 0
        time = datetime.utcnow()
        self.created_at = time
        self.updated_at = time


    def to_dict(self):
        return {
            'id': self.id,
            'total': self.total,
            'progress': self.progress,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __repr__(self):
        return '<Task {}>'.format(self.id)

    @classmethod
    def create(cls, total):
        if not isinstance(total, int):
            raise TypeError
        try:
            task = Task(total)
            db.session.add(task)
            db.session.commit()
            return task
        except Exception, e:
            db.session.rollback()

    @classmethod
    def find_recent(cls, task_id, seconds=60):
        if not isinstance(task_id, int) or not isinstance(seconds, int):
            raise TypeError
        task = Task.query.get(task_id)
        if task and task.updated_at > datetime.utcnow() - timedelta(seconds=seconds):
            return task

    @classmethod
    def update(cls, task_id, progress, inc=False):
        if not isinstance(task_id, int) or not isinstance(progress, int):
            raise TypeError
        if progress < 0:
            raise ValueError
        try:
            task = Task.query.get(task_id)
            if inc:
                task.progress += progress
            else:
                task.progress = progress
            task.updated_at = datetime.utcnow()
            db.session.add(task)
            db.session.commit()
            return task
        except Exception, e:
            db.session.rollback()


    @classmethod
    def delete(cls, task_id):
        if not isinstance(task_id, int):
            raise TypeError
        try:
            task = Task.query.get(task_id)
            db.session.delete(task)
            db.session.commit()
            return True
        except Exception, e:
            db.session.rollback()
            return False

    @classmethod
    def get_recent_tasks(cls, seconds=60):
        if not isinstance(seconds, int):
            raise TypeError
        return Task.query.filter(Task.updated_at > datetime.utcnow() - timedelta(seconds=seconds)).all()
