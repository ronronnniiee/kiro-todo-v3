"""
Authentication Routes.

This file defines the URL routes for user authentication:
- /auth/register - Create a new account
- /auth/login    - Log into an existing account
- /auth/logout   - Log out of the current session
"""
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from app import db
from app.auth import auth_bp
from app.auth.forms import RegistrationForm, LoginForm
from app.models import User


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration.

    GET: Display the registration form.
    POST: Validate the form and create a new user account.
    """
    # If user is already logged in, no need to register again
    if current_user.is_authenticated:
        return redirect(url_for('tasks.board'))

    form = RegistrationForm()

    # form.validate_on_submit() returns True only on POST with valid data
    if form.validate_on_submit():
        # Create a new user with hashed password
        user = User(
            username=form.username.data,
            email=form.email.data.lower()  # Store email in lowercase for consistency
        )
        user.set_password(form.password.data)  # Hash the password (never store plain text!)

        # Save the new user to the database
        db.session.add(user)
        db.session.commit()

        # Show a success message and redirect to login
        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    # If GET request or form has errors, show the registration page
    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login.

    GET: Display the login form.
    POST: Validate credentials and log the user in.
    """
    # If user is already logged in, redirect to their board
    if current_user.is_authenticated:
        return redirect(url_for('tasks.board'))

    form = LoginForm()

    if form.validate_on_submit():
        # Look up the user by email
        user = User.query.filter_by(email=form.email.data.lower()).first()

        # Check if user exists AND password is correct
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password. Please try again.', 'danger')
            return redirect(url_for('auth.login'))

        # Log the user in (creates a session)
        # remember=True keeps them logged in even after closing the browser
        login_user(user, remember=form.remember_me.data)

        # Redirect to the page they were trying to access (if any), or the board
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        return redirect(url_for('tasks.board'))

    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    """Log the user out and redirect to login page."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
