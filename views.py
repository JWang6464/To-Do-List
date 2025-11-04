from flask import Blueprint, render_template, redirect, url_for, request, abort
from flask_login import login_required, current_user
from models import db, Task

main_blueprint = Blueprint('main', __name__)

# add + list my tasks
@main_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def todo():
    if request.method == 'POST':
        title = (request.form.get('task-text') or '').strip()
        prio  = (request.form.get('priority') or 'low').strip().lower()
        if prio not in ('low', 'medium', 'high'):
            prio = 'low'
        if title:
            db.session.add(Task(title=title, priority=prio, user_id=current_user.id))
            db.session.commit()
        # PRG: after handling POST, redirect to GET so that reloads are safe
        return redirect(url_for('main.todo'))

    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('todo.html', tasks=tasks)

# toggle my task
@main_blueprint.route('/check/<int:task_id>')
@login_required
def check(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        abort(403)
    task.toggle()
    db.session.commit()
    return redirect(url_for('main.todo'))

# delete my task
@main_blueprint.route('/remove/<int:task_id>', methods=['GET', 'POST'])
@login_required
def remove_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        abort(403)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('main.todo'))

# edit title/priority
@main_blueprint.route('/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        abort(403)

    if request.method == 'POST':
        text = (request.form.get('task-text') or '').strip()
        prio = (request.form.get('priority') or 'low').strip().lower()
        if prio not in ('low', 'medium', 'high'):
            prio = 'low'       
        if text:
            task.title = text
            task.priority = prio
            db.session.commit()
        return redirect(url_for('main.todo'))

    return render_template('edit.html', task=task)
