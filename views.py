from flask import Blueprint, render_template, redirect, url_for, request
from task import Task

# Create a blueprint
main_blueprint = Blueprint('main', __name__)

# simple in-memory tasks store
# store Task instances converted to dicts when rendering
TASKS = []

def _next_id():
    return max((t['id'] for t in TASKS), default=0) + 1


@main_blueprint.route('/', methods=['GET', 'POST'])
def todo():
    if request.method == 'POST':
        text = request.form.get('task-text', '').strip()
        priority = request.form.get('task-priority', 'low').strip().lower()
        if priority not in ('low', 'medium', 'high'):
            priority = 'low'

        if text:
            new_task = Task(id=_next_id(), text=text, priority=priority)
            TASKS.append(new_task.to_dict())
        return redirect(url_for('main.todo'))

    return render_template('todo.html', tasks=TASKS)


@main_blueprint.route('/remove/<int:task_id>', methods=['POST'])
def remove_task(task_id):
    global TASKS
    TASKS = [t for t in TASKS if t['id'] != task_id]
    return redirect(url_for('main.todo'))


@main_blueprint.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    # find the task
    task = next((t for t in TASKS if t['id'] == task_id), None)
    if not task:
        return redirect(url_for('main.todo'))

    if request.method == 'POST':
        text = request.form.get('task-text', '').strip()
        priority = request.form.get('task-priority', 'low').strip().lower()
        if priority not in ('low', 'medium', 'high'):
            priority = 'low'

        if text:
            # update in-place
            task['text'] = text
            task['priority'] = priority
        return redirect(url_for('main.todo'))

    return render_template('edit.html', task=task)