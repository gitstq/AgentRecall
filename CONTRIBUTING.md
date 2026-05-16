# Contributing to AgentRecall 🧠

Thank you for your interest in contributing to AgentRecall! This document provides guidelines for contributing.

## Development Setup

```bash
# Clone the repository
git clone https://github.com/gitstq/AgentRecall.git
cd AgentRecall

# Install in development mode
pip install -e .

# Run tests
python -m pytest tests/ -v
```

## Code Style

- Follow PEP 8 conventions
- Use type hints where possible
- Keep functions focused and small
- Add docstrings to all public functions and classes
- Maximum line length: 100 characters

## Commit Messages

Follow the Angular commit convention:

- `feat: add new feature`
- `fix: fix a bug`
- `docs: update documentation`
- `refactor: code refactoring`
- `test: add or update tests`
- `chore: maintenance tasks`

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Issue Reporting

When reporting issues, please include:

- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages (if any)

## License

By contributing to AgentRecall, you agree that your contributions will be licensed under the MIT License.
