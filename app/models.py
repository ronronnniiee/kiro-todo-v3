"""
Database Models for the Kanban Task Manager.

Models define the structure of your database tables using Python classes.
Flask-SQLAlchemy translates these classes into PostgreSQL tables automatically.

We have two models:
- User: Stores account information (username, email, password)
- Task: Stores task data (title, status, priority, etc.)

Each user has many tasks (one-to-many relationship).
"""
from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


# ─── User Loader ────────────────────────────────────────────────────────────
# Flask-Login needs this to reload the user from the session cookie
@login_manager.user_loader
def load_user(user_id):
    """Load a user by their ID (called automatically by Flask-Login on each request)."""
    return User.query.get(int(user_id))


# ─── User Model ─────────────────────────────────────────────────────────────
class User(UserMixin, db.Model):
    """Represents a registered user.

    UserMixin provides default implementations for:
    - is_authenticated: True if user is logged in
    - is_active: True (we don't deactivate accounts)
    - is_anonymous: False for real users
    - get_id(): Returns the user ID as a string

    Attributes:
        id: Unique identifier (auto-generated)
        username: Display name (must be unique)
        email: Email address (must be unique, used for login)
        password_hash: Hashed password (never store plain text passwords!)
        created_at: When the account was created
        tasks: List of tasks belonging to this user
    """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship: One user has many tasks
    # backref='owner' lets you access task.owner to get the User who owns it
    tasks = db.relationship('Task', backref='owner', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        """Hash and store the password. Never stores plain text!

        Args:
            password: The plain text password from the user.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the stored hash.

        Args:
            password: The plain text password to verify.

        Returns:
            True if password is correct, False otherwise.
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


# ─── Task Model ─────────────────────────────────────────────────────────────
class Task(db.Model):
    """Represents a task on the Kanban board.

    Attributes:
        id: Unique identifier (auto-generated)
        title: Task title (required, max 200 chars)
        description: Optional detailed description
        status: Current column - 'todo', 'in_progress', or 'done'
        priority: Importance level - 'low', 'medium', or 'high'
        due_date: Optional deadline
        tags: Optional comma-separated labels (e.g., "work,urgent,meeting")
        created_at: When the task was created
        user_id: ID of the user who owns this task (foreign key)
    """
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)

    # Status determines which Kanban column the task appears in
    # Allowed values: 'todo', 'in_progress', 'done'
    status = db.Column(db.String(20), nullable=False, default='todo')

    # Priority determines the color of the badge on the card
    # Allowed values: 'low' (green), 'medium' (yellow), 'high' (red)
    priority = db.Column(db.String(10), nullable=False, default='medium')

    # Optional due date - displayed on the card, highlighted if overdue
    due_date = db.Column(db.Date, nullable=True)

    # Tags are stored as a comma-separated string (e.g., "work,urgent")
    # This is simpler than a many-to-many relationship for beginners
    tags = db.Column(db.String(200), nullable=True)

    # Automatically set when the task is created
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Foreign key linking this task to its owner
    # If the user is deleted, their tasks are also deleted (cascade)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Task {self.title} [{self.status}]>'

    @property
    def tags_list(self):
        """Return tags as a list (splits the comma-separated string).

        Returns:
            List of tag strings, or empty list if no tags.
        """
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
        return []
