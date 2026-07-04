"""
Tasks Blueprint Package.

This blueprint handles all task-related operations:
- Kanban board view (main dashboard)
- Creating, editing, and deleting tasks
- Drag-and-drop status updates via AJAX
"""
from flask import Blueprint

# Create the tasks blueprint
# url_prefix='/tasks' means all routes start with /tasks/
tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

# Import routes so they get registered with the blueprint
from app.tasks import routes  # noqa: E402, F401
