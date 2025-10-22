from flask import Blueprint, render_template, redirect, url_for, request

# Create a blueprint
main_blueprint = Blueprint('main', __name__)

# simple in-memory tasks store
# each task is a dict: {'id': int, 'text': str}
TASKS = [
    {'id': 1, 'text': 'Learn HTML, CSS, and JavaScript.'},
    {'id': 2, 'text': 'Learn Flask.'},
    {'id': 3, 'text': 'Build a to-do app.'},
]


def _next_id():
    return max((t['id'] for t in TASKS), default=0) + 1


@main_blueprint.route('/', methods=['GET', 'POST'])
def todo():
    if request.method == 'POST':
        text = request.form.get('task-text', '').strip()
        if text:
            TASKS.append({'id': _next_id(), 'text': text})
        return redirect(url_for('main.todo'))

    return render_template('todo.html', tasks=TASKS)


@main_blueprint.route('/remove/<int:task_id>', methods=['POST'])
def remove_task(task_id):
    global TASKS
    TASKS = [t for t in TASKS if t['id'] != task_id]
    return redirect(url_for('main.todo'))