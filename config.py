"""
Configuration settings for the Kanban Task Manager.

This file contains all the settings Flask and its extensions need to run.
You can override these by setting environment variables on your system.
"""
import os


class Config:
    """Base configuration class.

    Attributes:
        SECRET_KEY: Used by Flask to sign session cookies and CSRF tokens.
                    IMPORTANT: Change this to a random string in production!
        SQLALCHEMY_DATABASE_URI: Connection string for your PostgreSQL database.
                                Format: postgresql://username:password@host:port/database_name
        SQLALCHEMY_TRACK_MODIFICATIONS: Disabled to save memory (we don't need it).
        WTF_CSRF_ENABLED: Enables CSRF protection on all forms for security.
    """

    # Secret key for session signing - set the SECRET_KEY environment variable in production!
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # PostgreSQL database connection string
    # Change 'postgres:postgres' to your actual PostgreSQL username:password
    # Change 'kanban_tasks' to your database name if different
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql+psycopg://postgres:277353@localhost:5432/kanban_tasks'

    # Disable modification tracking (saves memory, we don't use it)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Enable CSRF protection for all forms
    WTF_CSRF_ENABLED = True
