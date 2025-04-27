```markdown
# RICEWEARE.COM Parser

This project is a web parser for RICEWEARE.COM. Follow the instructions below to set up and run the application.

## Prerequisites

- Python 3.x
- PostgreSQL installed and running
- `pip` package manager

## Installation

1. **Clone the repository**:
   ```bash
   git clone git@github.com:keyerror-0/Networks.git
   cd lab4
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Linux/macOS
   # For Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Database Setup

1. **Create a PostgreSQL database** (via `psql` or a GUI tool like pgAdmin):
   ```sql
   CREATE DATABASE riceweare_parser;
   ```

2. **Configure environment variables**:
   - Create a `.env` file in the project root.
   - Add the following variables (replace placeholders with your values):
     ```ini
     DB_USER=your_postgres_username
     DB_PASSWORD=your_postgres_password
     DB_HOST=localhost  # or your database host
     DB_PORT=5432       # default PostgreSQL port
     DB_NAME=riceweare_parser
     FLASK_APP=parse.py
     ```

## Initialize the Database

1. **Run database migrations**:
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

## Run the Application

```bash
flask run
```

The application will be available at `http://localhost:5000`.

---

**Note**: Ensure PostgreSQL is running before starting the app. Keep the virtual environment activated while using the application.
```