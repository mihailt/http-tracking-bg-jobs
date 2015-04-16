from flask import request, jsonify
from . import main
from ..models import Task

@main.route('/')
def index():
    return jsonify({'version': 0.1})

@main.route('/tasks')
def tasks():
    tasks = Task.get_recent_tasks()
    tasks = [t.to_dict() for t in tasks]
    total = len(tasks)

    response = { 'tasks': tasks, 'total': total }
    return jsonify(response), 200


@main.route('/task', methods=['POST'])
def create_task():
    try:
        total=request.form['total']
        task = Task.create(int(total))
        return jsonify({'task_id': task.id}), 201
    except Exception, e:
        return jsonify({'status': 'error'}), 400


@main.route('/task/<int:task_id>')
def view_task(task_id=None):
    try:
        task = Task.find_recent(task_id)
        return jsonify({'task': task.to_dict()}), 200
    except Exception, e:
        return jsonify({'status': 'not found'}), 404

@main.route('/task/<int:task_id>', methods=['PUT'])
def update_task(task_id=None):
    try:
        progress = request.form['progress']
        task = Task.update(task_id, int(progress))
        return jsonify({'task': task.to_dict()}), 200
    except Exception, e:
        return jsonify({'status': 'not found'}), 404

@main.route('/task/<int:task_id>/<int:progress>', methods=['PUT'])
def update_task_increment(task_id=None, progress=None):
    try:
        task = Task.update(task_id, progress=progress, inc=True)
        return jsonify({'task': task.to_dict()}), 200
    except Exception, e:
        return jsonify({'status': 'not found'}), 404

@main.route('/task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id=None):

    try:
        if Task.delete(task_id):
            return jsonify({'status': 'deleted' }), 200
        else:
            return jsonify({'status': 'not found'}), 404
    except Exception, e:
        return jsonify({'status': 'not found'}), 404
