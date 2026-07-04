"""
Task Routes.

This file defines all task-related URL routes:
- /tasks/          - Kanban board view (main dashboard)
- /tasks/new       - Create a new task
- /tasks/<id>/edit - Edit an existing task
- /tasks/<id>/delete - Delete a task
- /tasks/<id>/status - Update task status via AJAX (drag-and-drop)
"""
from flask import render_template, redirect, url_for, flash, request, jsonify, abort
from flask_login import login_required, current_user

from app import db
from app.tasks import tasks_bp
from app.tasks.forms import TaskForm
from app.models import Task


@tasks_bp.route('/')
@login_required
def board():
    """Display the Kanban board with tasks organized in columns.

    Queries the current user's tasks and groups them by status
    into three lists: To Do, In Progress, and Done.
    """
    # Get all tasks for the current user, organized by status
    # We only show tasks belonging to the logged-in user (personal tasks)
    todo_tasks = Task.query.filter_by(
        user_id=current_user.id, status='todo'
    ).order_by(Task.created_at.desc()).all()

    in_progress_tasks = Task.query.filter_by(
        user_id=current_user.id, status='in_progress'
    ).order_by(Task.created_at.desc()).all()

    done_tasks = Task.query.filter_by(
        user_id=current_user.id, status='done'
    ).order_by(Task.created_at.desc()).all()

    return render_template('tasks/board.html',
                           todo_tasks=todo_tasks,
                           in_progress_tasks=in_progress_tasks,
                           done_tasks=done_tasks)


@tasks_bp.route('/new', methods=['GET', 'POST'])
@login_required
def create_task():
    """Create a new task.

    GET: Display the empty task form.
    POST: Validate and save the new task to the database.
    """
    form = TaskForm()

    if form.validate_on_submit():
        # Create a new task with data from the form
        task = Task(
            title=form.title.data,
            description=form.description.data,
            status=form.status.data,
            priority=form.priority.data,
            due_date=form.due_date.data,
            tags=form.tags.data,
            user_id=current_user.id  # Link the task to the current user
        )

        # Save to database
        db.session.add(task)
        db.session.commit()

        flash('Task created successfully! 🎉', 'success')
        return redirect(url_for('tasks.board'))

    return render_template('tasks/task_form.html', form=form, title='New Task')


@tasks_bp.route('/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    """Edit an existing task.

    GET: Display the task form pre-filled with current data.
    POST: Validate and update the task in the database.

    Args:
        task_id: The ID of the task to edit.
    """
    # Get the task or return 404 if it doesn't exist
    task = Task.query.get_or_404(task_id)

    # Security check: make sure the task belongs to the current user
    if task.user_id != current_user.id:
        abort(403)  # Forbidden - can't edit someone else's task

    # Pre-fill the form with existing task data
    form = TaskForm(obj=task)

    if form.validate_on_submit():
        # Update the task with new form data
        task.title = form.title.data
        task.description = form.description.data
        task.status = form.status.data
        task.priority = form.priority.data
        task.due_date = form.due_date.data
        task.tags = form.tags.data

        db.session.commit()

        flash('Task updated successfully! ✏️', 'success')
        return redirect(url_for('tasks.board'))

    return render_template('tasks/task_form.html', form=form, title='Edit Task')


@tasks_bp.route('/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    """Delete a task.

    Only accepts POST requests (for security - prevents accidental deletion via URL).

    Args:
        task_id: The ID of the task to delete.
    """
    task = Task.query.get_or_404(task_id)

    # Security check: make sure the task belongs to the current user
    if task.user_id != current_user.id:
        abort(403)

    db.session.delete(task)
    db.session.commit()

    flash('Task deleted. 🗑️', 'success')
    return redirect(url_for('tasks.board'))


@tasks_bp.route('/<int:task_id>/status', methods=['PATCH'])
@login_required
def update_status(task_id):
    """Update a task's status via AJAX (used by drag-and-drop).

    This endpoint receives a JSON request with the new status
    when a user drags a task card to a different column.

    Expected JSON body: {"status": "todo" | "in_progress" | "done"}

    Returns:
        JSON response indicating success or failure.
    """
    # Valid status values that match our Kanban columns
    valid_statuses = ['todo', 'in_progress', 'done']

    # Get the task
    task = Task.query.get_or_404(task_id)

    # Security check
    if task.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Permission denied.'}), 403

    # Get the new status from the JSON request body
    data = request.get_json()

    if not data or 'status' not in data:
        return jsonify({'success': False, 'error': 'No status provided.'}), 400

    new_status = data['status']

    # Validate the new status
    if new_status not in valid_statuses:
        return jsonify({
            'success': False,
            'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'
        }), 400

    # Update the task status
    task.status = new_status
    db.session.commit()

    return jsonify({'success': True, 'new_status': new_status})
