# Usage Guide

This document explains how to use the Cyclist Database project.

## Running the Application

### Basic Usage

1. **Start the application**:
   ```bash
   python main.py
   ```

2. **Interactive Mode**:
   - Follow the on-screen prompts to add, view, or update cyclist records.

### Command-Line Arguments

The application supports the following arguments:

| Argument | Description | Example |
|----------|-------------|---------|
| `--help` | Show help message | `python main.py --help` |
| `--version` | Show version | `python main.py --version` |
| `--db-path` | Specify database path | `python main.py --db-path /path/to/db.sqlite` |

### Examples

1. **Run with a custom database path**:
   ```bash
   python main.py --db-path /tmp/cyclist.db
   ```

2. **View help**:
   ```bash
   python main.py --help
   ```

## Database Operations

### Adding a Cyclist

1. Select the "Add Cyclist" option from the menu.
2. Enter the cyclist details (name, age, team, etc.).
3. Confirm the entry.

### Querying Cyclists

1. Select the "Query Cyclists" option.
2. Choose a filter (e.g., by team, age range).
3. View the results.

### Updating Records

1. Select the "Update Cyclist" option.
2. Search for the cyclist by ID or name.
3. Edit the fields and save.

## Advanced Usage

### Batch Operations

To perform batch operations (e.g., importing from CSV):

```bash
python scripts/import_csv.py --input data/cyclists.csv
```

### Exporting Data

Export data to CSV:

```bash
python scripts/export_csv.py --output data/export.csv
```

## Notes

- Ensure the database file is writable.
- Backup the database before performing bulk operations.
