# Contributing Guide

Thank you for your interest in contributing to the Cyclist Database project! This guide outlines how to contribute effectively.

## How to Contribute

### Reporting Issues

- Use the [GitHub Issues](https://github.com/datadutch/cyclist-database/issues) page to report bugs or suggest features.
- Include:
  - A clear title and description.
  - Steps to reproduce (for bugs).
  - Expected vs. actual behavior.

### Submitting Pull Requests

1. **Fork the repository** and clone your fork.
2. **Create a branch** for your feature/fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
   **Note**: Never commit or push directly to `main`. Always use a feature branch.
3. **Make changes** and commit them:
   ```bash
   git commit -m "Add feature: your feature description"
   ```
4. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
5. **Open a Pull Request** (PR) to the `main` branch of the original repository.

## Coding Standards

### Python

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) guidelines.
- Use descriptive variable and function names.
- Include docstrings for functions and classes.

### Commits

- Use clear, concise commit messages.
- Prefix commits with:
  - `feat`: New feature.
  - `fix`: Bug fix.
  - `docs`: Documentation changes.
  - `refactor`: Code refactoring.
  - `chore`: Maintenance tasks.

### Testing

- Ensure your changes do not break existing functionality.
- Add tests for new features if applicable.

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/datadutch/cyclist-database.git
   ```
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Review Process

- PRs will be reviewed by maintainers.
- Address feedback promptly.
- Once approved, your changes will be merged.

## License

By contributing, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).
