# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python 3.13 project template with pre-configured code formatting and development tools, featuring a professional logging system with CLI interface.

## Development Commands

### Setup
```bash
uv sync                              # Install dependencies using uv package manager
uv run pre-commit install           # Install pre-commit hooks for automated quality checks
```

### Running the Application
```bash
uv run python main.py               # Run main application
uv run python main.py --demo        # Run with demo functionality (showcases logging features)
uv run python main.py --version     # Show version
```

### Code Quality and Linting
```bash
uv run ruff check .                 # Check for linting issues
uv run ruff check --fix .           # Auto-fix linting issues
uv run ruff format .                # Format code with Ruff (primary formatter)
uv run mypy .                       # Run type checking (strict mode)
uv run isort .                      # Sort imports (Black-compatible)
uv run black .                      # Format with Black (fallback option)
```

### Combined Quality Check (Recommended)
```bash
uv run ruff check --fix . && uv run mypy . && uv run ruff format .
```

## Project Architecture

### Core Structure
- **main.py**: Application entry point with CLI argument parsing using `argparse`
- **src/**: Main package directory containing all application modules
- **src/__version__.py**: Dynamic version management using `importlib.metadata`
- **src/config.py**: Centralized logging configuration and settings
- **src/logger.py**: Professional logging system with multiple output formats
- **src/demo.py**: Demonstration module showcasing logging capabilities

### Logging System
The project features a comprehensive logging system with:
- **Multiple handlers**: Console (colored), standard file, JSON file, and error-specific file
- **Rotating logs**: Automatic log rotation (10MB max, 5 backups)
- **Structured logging**: Support for JSON format with extra context data
- **Decorators**: `@log_execution_time` for performance monitoring
- **Context managers**: `log_context()` for adding contextual information
- **Environment-aware**: Configurable log levels via environment variables

### Configuration Management
- **Environment-based**: Logging levels configurable via `LOG_LEVEL`, `FILE_LOG_LEVEL`, `CONSOLE_LOG_LEVEL`
- **Production mode**: Automatic JSON logging in production environment
- **Centralized settings**: All configuration constants in `src/config.py`

## Code Quality Configuration

### Tool Stack
- **Ruff**: Modern Python linter and formatter (primary)
- **MyPy**: Static type checking with strict configuration
- **Black**: Code formatter (fallback, Ruff preferred)
- **isort**: Import sorting with Black compatibility
- **Pre-commit hooks**: Automated code quality checks before commits

### Ruff Configuration (pyproject.toml)
- Line length: 88 characters (Black-compatible)
- Target: Python 3.13
- Enabled rules: pycodestyle (E,W), pyflakes (F), isort (I), flake8-bugbear (B), flake8-comprehensions (C4), pyupgrade (UP)
- Double quotes, space indentation, auto-formatting

### MyPy Configuration
- Strict type checking enabled (`disallow_untyped_defs`, `disallow_incomplete_defs`)
- Warnings for unused imports, redundant casts, unreachable code
- Python 3.13 target with comprehensive error detection

### Pre-commit Hooks
Automatically runs before commits:
- Code formatting (Ruff, Black fallback)
- Import sorting (isort)
- Type checking (MyPy)
- File cleanup (trailing whitespace, newlines)
- YAML validation and large file detection

### Dependencies
- **Runtime**: `colorlog`, `python-json-logger`
- **Development**: `ruff`, `mypy`, `black`, `isort`, `pre-commit`

## Development Patterns

### Version Management
Version is dynamically retrieved using `importlib.metadata.version()` from package metadata, not hardcoded.

### Logging Usage
- Use `get_logger(__name__)` or `get_logger("module_name")` to create module-specific loggers
- Leverage `@log_execution_time()` decorator for performance-critical functions
- Use structured logging with `extra={}` parameter for machine-readable logs
- Employ `log_context()` for operations requiring shared context

### CLI Structure
The application uses `argparse` with proper help text, version handling, and modular command structure suitable for extension.

## Project Structure
```
.
├── .pre-commit-config.yaml    # Pre-commit configuration
├── .vscode/settings.json      # VS Code settings for development
├── main.py                    # Main application entry point
├── pyproject.toml             # Project configuration and dependencies
├── uv.lock                    # Dependency lock file
├── README.md                  # Project documentation
├── CLAUDE.md                  # This file
└── src/                       # Main package directory
    ├── __init__.py            # Package initialization
    ├── __version__.py         # Dynamic version management
    ├── config.py             # Logging and app configuration
    ├── logger.py             # Professional logging system
    └── demo.py               # Feature demonstrations
```

## Contributing Guidelines

1. **Code Quality**: Ensure all pre-commit hooks pass
2. **Type Safety**: Add type annotations to all functions (MyPy strict mode)
3. **Code Style**: Follow Ruff/Black formatting (88-character line length)
4. **Import Organization**: Use isort with Black profile
5. **Testing**: Test changes before committing
6. **Quality Check**: Run `uv run ruff check . && uv run mypy .` before commits

## Requirements

- **Python 3.13+**
- **uv**: Modern Python package manager for dependency management
- **VS Code**: Recommended IDE with Black Formatter extension
