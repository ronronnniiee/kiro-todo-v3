"""
Authentication Blueprint Package.

This blueprint handles user registration, login, and logout.
A blueprint is like a mini-app that groups related routes together,
keeping your code organized as the project grows.
"""
from flask import Blueprint

# Create the auth blueprint
# url_prefix='/auth' means all routes in this blueprint start with /auth/
# e.g., /auth/login, /auth/register, /auth/logout
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Import routes so they get registered with the blueprint
from app.auth import routes  # noqa: E402, F401
