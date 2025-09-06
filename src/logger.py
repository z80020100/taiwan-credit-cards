"""Professional logging setup with console and file output."""

import logging
import logging.handlers
import sys
import time
from collections.abc import Callable, Generator, MutableMapping
from contextlib import contextmanager
from functools import wraps
from pathlib import Path
from typing import Any, TypeVar, cast

import colorlog
from pythonjsonlogger import jsonlogger

from . import config

# Type variables
F = TypeVar("F", bound=Callable[..., Any])

# Global logger cache
_loggers: dict[str, logging.Logger] = {}


class ColoredConsoleHandler(colorlog.StreamHandler):
    """Enhanced colored console handler with better formatting."""

    def __init__(self, stream: Any = None) -> None:
        super().__init__(stream or sys.stdout)
        self.setFormatter(
            colorlog.ColoredFormatter(
                config.CONSOLE_FORMAT,
                datefmt=config.DATE_FORMAT,
                log_colors=config.LOG_COLORS,
                secondary_log_colors={},
                style="%",
            )
        )


class JsonFileHandler(logging.handlers.RotatingFileHandler):
    """JSON formatted rotating file handler."""

    def __init__(self, filename: str | Path) -> None:
        super().__init__(
            filename=str(filename),
            maxBytes=config.MAX_LOG_SIZE,
            backupCount=config.BACKUP_COUNT,
            encoding="utf-8",
        )
        self.setFormatter(
            jsonlogger.JsonFormatter(config.JSON_FORMAT, datefmt=config.DATE_FORMAT)
        )


class StandardFileHandler(logging.handlers.RotatingFileHandler):
    """Standard formatted rotating file handler."""

    def __init__(self, filename: str | Path) -> None:
        super().__init__(
            filename=str(filename),
            maxBytes=config.MAX_LOG_SIZE,
            backupCount=config.BACKUP_COUNT,
            encoding="utf-8",
        )
        self.setFormatter(
            logging.Formatter(config.FILE_FORMAT, datefmt=config.DATE_FORMAT)
        )


def setup_logger(
    name: str = "app",
    level: str | int = config.DEFAULT_LOG_LEVEL,
    console_level: str | int = config.CONSOLE_LOG_LEVEL,
    file_level: str | int = config.FILE_LOG_LEVEL,
    enable_console: bool = True,
    enable_file: bool = True,
    enable_error_file: bool = True,
    enable_json_file: bool = True,
) -> logging.Logger:
    """
    Set up a logger with console and file handlers.

    Args:
        name: Logger name
        level: Overall logger level
        console_level: Console handler level
        file_level: File handler level
        enable_console: Enable console output
        enable_file: Enable file logging
        enable_error_file: Enable separate error file logging
        enable_json_file: Enable JSON format file logging

    Returns:
        Configured logger instance
    """
    if name in _loggers:
        return _loggers[name]

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Ensure log directory exists
    config.LOG_DIR.mkdir(exist_ok=True)

    # Console handler
    if enable_console:
        console_handler = ColoredConsoleHandler()
        console_handler.setLevel(console_level)
        logger.addHandler(console_handler)

    # Standard file handler (human-readable)
    if enable_file:
        file_handler = StandardFileHandler(config.LOG_FILE)
        file_handler.setLevel(file_level)
        logger.addHandler(file_handler)

    # JSON file handler (machine-readable with extra data)
    if enable_json_file:
        json_handler = JsonFileHandler(config.JSON_LOG_FILE)
        json_handler.setLevel(file_level)
        logger.addHandler(json_handler)

    # Error file handler (always uses standard format for readability)
    if enable_error_file:
        error_handler = StandardFileHandler(config.ERROR_LOG_FILE)
        error_handler.setLevel(logging.ERROR)
        logger.addHandler(error_handler)

    # Prevent duplicate logs
    logger.propagate = False

    # Cache the logger
    _loggers[name] = logger

    return logger


def get_logger(name: str = "app") -> logging.Logger:
    """
    Get or create a logger instance.

    Args:
        name: Logger name

    Returns:
        Logger instance
    """
    if name not in _loggers:
        return setup_logger(name)
    return _loggers[name]


def log_execution_time(logger: logging.Logger | None = None) -> Callable[[F], F]:
    """
    Decorator to log function execution time.

    Args:
        logger: Logger instance to use. If None, uses default logger.

    Returns:
        Decorated function
    """

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            log = logger or get_logger()
            start_time = time.time()

            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                log.info(
                    f"{func.__name__} completed in {execution_time:.4f}s",
                    extra={
                        "function": func.__name__,
                        "execution_time": execution_time,
                        "status": "success",
                    },
                )
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                log.error(
                    f"{func.__name__} failed after {execution_time:.4f}s: {e}",
                    extra={
                        "function": func.__name__,
                        "execution_time": execution_time,
                        "status": "error",
                        "error": str(e),
                    },
                    exc_info=True,
                )
                raise

        return cast(F, wrapper)

    return decorator


@contextmanager
def log_context(
    logger: logging.Logger | None = None, **context: Any
) -> Generator[logging.Logger]:
    """
    Context manager for adding extra context to log messages.

    Args:
        logger: Logger instance to use. If None, uses default logger.
        **context: Additional context to add to log messages.

    Yields:
        Logger with context
    """
    log = logger or get_logger()

    # Create a new logger adapter with context
    class ContextAdapter(logging.LoggerAdapter):
        def process(
            self, msg: str, kwargs: MutableMapping[str, Any]
        ) -> tuple[str, MutableMapping[str, Any]]:
            if "extra" not in kwargs:
                kwargs["extra"] = {}
            kwargs["extra"].update(self.extra)
            return msg, kwargs

    context_logger = ContextAdapter(log, context)
    yield cast(logging.Logger, context_logger)


# Default logger instance
default_logger = get_logger("default")


# Convenience functions using default logger
def debug(msg: str, *args: Any, **kwargs: Any) -> None:
    """Log debug message."""
    default_logger.debug(msg, *args, **kwargs)


def info(msg: str, *args: Any, **kwargs: Any) -> None:
    """Log info message."""
    default_logger.info(msg, *args, **kwargs)


def warning(msg: str, *args: Any, **kwargs: Any) -> None:
    """Log warning message."""
    default_logger.warning(msg, *args, **kwargs)


def error(msg: str, *args: Any, **kwargs: Any) -> None:
    """Log error message."""
    default_logger.error(msg, *args, **kwargs)


def critical(msg: str, *args: Any, **kwargs: Any) -> None:
    """Log critical message."""
    default_logger.critical(msg, *args, **kwargs)
