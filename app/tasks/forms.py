"""
Task Forms (WTForms).

This form handles creating and editing tasks.
It includes all the Notion-like properties: title, description,
status, priority, due date, and tags.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class TaskForm(FlaskForm):
    """Form for creating or editing a task.

    Fields:
        title: The task name (required, max 200 chars)
        description: Optional detailed notes about the task
        status: Which Kanban column the task belongs to
        priority: How important/urgent the task is
        due_date: Optional deadline
        tags: Optional comma-separated labels for categorization
    """
    title = StringField('Title', validators=[
        DataRequired(message='Task title is required.'),
        Length(max=200, message='Title cannot exceed 200 characters.')
    ])

    description = TextAreaField('Description', validators=[
        Optional(),
        Length(max=2000, message='Description cannot exceed 2000 characters.')
    ])

    status = SelectField('Status', choices=[
        ('todo', '📋 To Do'),
        ('in_progress', '🔄 In Progress'),
        ('done', '✅ Done')
    ], validators=[DataRequired()])

    priority = SelectField('Priority', choices=[
        ('low', '🟢 Low'),
        ('medium', '🟡 Medium'),
        ('high', '🔴 High')
    ], validators=[DataRequired()])

    # Optional date field - format must match the HTML date input
    due_date = DateField('Due Date', format='%Y-%m-%d', validators=[Optional()])

    tags = StringField('Tags', validators=[
        Optional(),
        Length(max=200, message='Tags cannot exceed 200 characters.')
    ])

    submit = SubmitField('Save Task')
