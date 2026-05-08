# Setup Guide

This guide covers the setup and installation of the Cyclist Database project.

## Prerequisites

- **Python**: 3.14.4 or later (recommended).
- **Database**: SQLite (default) or your preferred database.
- **Git**: For version control.

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/datadutch/cyclist-database.git
cd cyclist-database
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
```

- **Activate the environment**:
  - **macOS/Linux**: `source venv/bin/activate`
  - **Windows**: `venv\Scripts\activate`

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` does not exist, create it and list all dependencies:

```bash
echo "sqlite3" > requirements.txt
pip install -r requirements.txt
```

### 4. Configure the Database

By default, the project uses SQLite. To use a different database:

1. Install the appropriate driver (e.g., `psycopg2` for PostgreSQL).
2. Update the database configuration in `config.py` (if applicable).

### 5. Run the Application

```bash
python main.py
```

## Verification

- Check the Python version:
  ```bash
  python --version
  ```
- Verify dependencies:
  ```bash
  pip list
  ```

## Troubleshooting

- **Python not found**: Ensure Python 3.14+ is installed and in your `PATH`.
- **Dependency errors**: Run `pip install --upgrade pip` and retry.
- **Database issues**: Check permissions and ensure the database file is writable.
