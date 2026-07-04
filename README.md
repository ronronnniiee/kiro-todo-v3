# 📋 Kanban Task Manager

A personal, Notion-inspired Kanban task manager built with **Flask** and **PostgreSQL**. Organize your tasks in a beautiful drag-and-drop board with To Do, In Progress, and Done columns.

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Flask](https://img.shields.io/badge/Flask-3.1-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- **🔐 User Authentication** — Register, login, and logout with secure password hashing
- **📋 Kanban Board** — Three columns (To Do, In Progress, Done) to visualize your workflow
- **🖱️ Drag & Drop** — Move tasks between columns with smooth drag-and-drop (powered by SortableJS)
- **📝 Rich Task Properties** — Title, description, priority, due dates, and tags
- **🎨 Clean UI** — Notion-inspired minimal design with Bootstrap 5
- **🔒 Personal Tasks** — Each user only sees their own tasks
- **📱 Responsive** — Works on desktop, tablet, and mobile

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Flask | Python web framework |
| PostgreSQL | Database |
| Flask-SQLAlchemy | ORM (database interactions) |
| Flask-Login | User session management |
| Flask-WTF | Form handling & CSRF protection |
| Flask-Migrate | Database migrations |
| Bootstrap 5 | CSS framework |
| SortableJS | Drag-and-drop library |

## 📦 Prerequisites

Before you start, make sure you have these installed:

1. **Python 3.9+** — [Download Python](https://www.python.org/downloads/)
2. **PostgreSQL** — [Download PostgreSQL](https://www.postgresql.org/download/)
3. **pip** — Python package manager (comes with Python)

To check if you have them installed, run:
```bash
python --version
psql --version
```

## 🚀 Quick Start Guide

Follow these steps to get the app running on your computer:

### Step 1: Clone or Download the Project

```bash
cd kanban-task-manager
```

### Step 2: Create a Virtual Environment

A virtual environment keeps this project's packages separate from other Python projects.

```bash
# Create the virtual environment
python -m venv venv

# Activate it:
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

You'll know it's activated when you see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Create the PostgreSQL Database

Open a terminal and run:

```bash
# Log into PostgreSQL (you might need to use your postgres password)
psql -U postgres

# Create the database
CREATE DATABASE kanban_tasks;

# Exit psql
\q
```

**If your PostgreSQL has a different username/password**, update the connection string in `config.py`:
```python
SQLALCHEMY_DATABASE_URI = 'postgresql://YOUR_USERNAME:YOUR_PASSWORD@localhost:5432/kanban_tasks'
```

### Step 5: Initialize the Database

Flask-Migrate creates the database tables from our Python models:

```bash
# Initialize migrations (only needed once)
flask db init

# Generate migration files from our models
flask db migrate -m "Initial migration - create user and task tables"

# Apply the migration (creates the actual tables)
flask db upgrade
```

### Step 6: Run the Application

```bash
python run.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Step 7: Open in Browser

Go to **http://localhost:5000** in your web browser.

1. Click **Register** to create an account
2. Log in with your new account
3. Click **+ New Task** to create your first task
4. Drag tasks between columns to update their status!

## 📁 Project Structure

```
kanban-task-manager/
├── app/                        # Main application package
│   ├── __init__.py            # App factory (creates & configures the app)
│   ├── models.py              # Database models (User, Task)
│   ├── auth/                  # Authentication blueprint
│   │   ├── __init__.py       # Blueprint setup
│   │   ├── routes.py         # Login/register/logout routes
│   │   └── forms.py          # WTForms for auth
│   ├── tasks/                 # Tasks blueprint
│   │   ├── __init__.py       # Blueprint setup
│   │   ├── routes.py         # CRUD routes + AJAX status update
│   │   └── forms.py          # WTForms for tasks
│   ├── templates/             # HTML templates (Jinja2)
│   │   ├── base.html         # Base layout (navbar, styles)
│   │   ├── auth/             # Auth pages
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── tasks/            # Task pages
│   │   │   ├── board.html    # Kanban board view
│   │   │   ├── task_form.html # Create/edit form
│   │   │   └── _task_card.html # Reusable task card
│   │   └── errors/           # Error pages
│   │       ├── 404.html
│   │       └── 500.html
│   └── static/               # Static files
│       └── js/
│           └── board.js      # Drag-and-drop logic
├── config.py                  # Configuration settings
├── requirements.txt           # Python dependencies
├── run.py                     # Entry point (start here!)
└── README.md                  # You are here!
```

## 🧠 How It Works (For Beginners)

### The App Factory Pattern
Flask uses a "factory" function (`create_app()` in `app/__init__.py`) to build the app. This pattern:
- Keeps code organized
- Makes testing easier
- Prevents circular imports

### Blueprints
The app is split into **blueprints** — think of them as mini-apps:
- `auth` blueprint: handles login/register/logout
- `tasks` blueprint: handles everything task-related

### Database Models
Instead of writing SQL directly, we use **SQLAlchemy ORM** — Python classes that represent database tables. Changes to these classes can be applied using `flask db migrate` and `flask db upgrade`.

### Drag-and-Drop
When you drag a task to a new column:
1. SortableJS detects the drop event
2. JavaScript sends an AJAX PATCH request with the new status
3. Flask updates the database
4. If it fails, the card snaps back to its original column

## 🔧 Configuration

You can configure the app using environment variables:

| Variable | Default | Description |
|---|---|---|
| `SECRET_KEY` | `dev-secret-key-change-in-production` | Session encryption key |
| `DATABASE_URL` | `postgresql://postgres:postgres@localhost:5432/kanban_tasks` | Database connection |

Example:
```bash
export SECRET_KEY="your-super-secret-random-string"
export DATABASE_URL="postgresql://myuser:mypass@localhost:5432/kanban_tasks"
```

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"
Make sure your virtual environment is activated:
```bash
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### "FATAL: password authentication failed"
Update the database URI in `config.py` with your PostgreSQL credentials.

### "FATAL: database 'kanban_tasks' does not exist"
Create the database first:
```bash
psql -U postgres -c "CREATE DATABASE kanban_tasks;"
```

### "ImportError: cannot import name 'create_app'"
Make sure you're running from the project root directory (where `run.py` is).

### Port 5000 already in use
Another app is using port 5000. Either stop it, or run Flask on a different port:
```bash
flask run --port 5001
```

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

Made with ❤️ as a learning project. Happy coding! 🎉
