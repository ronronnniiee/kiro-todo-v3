"""
Application Factory for the Kanban Task Manager.

The "app factory" pattern creates the Flask app inside a function.
This makes it easy to create multiple instances (useful for testing)
and keeps everything organized.

How it works:
1. Create the Flask app
2. Load configuration settings
3. Initialize extensions (database, login manager, etc.)
4. Register blueprints (groups of related routes)
5. Return the ready-to-use app
"""
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

from config import Config

# ─── Initialize Extensions ──────────────────────────────────────────────────
# These are created here (outside the factory) so other files can import them.
# They get connected to the actual app inside create_app().

db = SQLAlchemy()          # Database ORM - lets us use Python classes instead of raw SQL
migrate = Migrate()        # Database migrations - tracks changes to your models
login_manager = LoginManager()  # Handles user sessions (who is logged in)
csrf = CSRFProtect()       # CSRF protection for forms


def create_app():
    """Create and configure the Flask application.

    Returns:
        Flask app instance, ready to run.
    """
    # Create the Flask app instance
    app = Flask(__name__)

    # Load settings from our Config class
    app.config.from_object(Config)

    # ─── Connect Extensions to App ──────────────────────────────────────────
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Tell Flask-Login which page to redirect to when a user needs to log in
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    # ─── Register Blueprints ────────────────────────────────────────────────
    # Blueprints are like mini-apps that group related routes together
    from app.auth import auth_bp
    from app.tasks import tasks_bp

    app.register_blueprint(auth_bp)   # Routes: /auth/login, /auth/register, /auth/logout
    app.register_blueprint(tasks_bp)  # Routes: /tasks/, /tasks/new, /tasks/<id>/edit, etc.

    # ─── Import Models ──────────────────────────────────────────────────────
    # We import models here so Flask-Migrate can detect them
    from app import models  # noqa: F401

    # ─── Context Processor ──────────────────────────────────────────────────
    # Makes 'today' available in ALL templates (used for overdue date detection)
    @app.context_processor
    def inject_today():
        from datetime import date
        return {'today': date.today()}

    # ─── Root Route ─────────────────────────────────────────────────────────
    @app.route('/')
    def index():
        """Redirect to the board if logged in, otherwise to login page."""
        if current_user.is_authenticated:
            return redirect(url_for('tasks.board'))
        return redirect(url_for('auth.login'))

    # ─── Error Handlers ─────────────────────────────────────────────────────
    @app.errorhandler(404)
    def not_found_error(error):
        from flask import render_template
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        from flask import render_template
        db.session.rollback()  # Roll back any failed database transactions
        return render_template('errors/500.html'), 500

    return app
