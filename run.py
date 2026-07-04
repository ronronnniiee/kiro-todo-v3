"""
Entry point to run the Flask application.

Usage:
    python run.py

This starts the Flask development server on http://localhost:5000
You can view your Kanban board by opening that URL in your browser.
"""
from app import create_app

# Create the Flask application using our app factory
app = create_app()

if __name__ == '__main__':
    # debug=True enables auto-reload when you change code (great for development!)
    app.run(debug=True)
