"""Logger configuration settings."""

import os
from pathlib import Path
from typing import Final

# Project root directory
PROJECT_ROOT: Final[Path] = Path(__file__).parent.parent

# Log directory
LOG_DIR: Final[Path] = PROJECT_ROOT / "logs"

# Log file paths
LOG_FILE: Final[Path] = LOG_DIR / "app.log"
ERROR_LOG_FILE: Final[Path] = LOG_DIR / "error.log"
JSON_LOG_FILE: Final[Path] = LOG_DIR / "app.json.log"

# Log levels
DEFAULT_LOG_LEVEL: Final[str] = os.getenv("LOG_LEVEL", "DEBUG")
FILE_LOG_LEVEL: Final[str] = os.getenv("FILE_LOG_LEVEL", "DEBUG")
CONSOLE_LOG_LEVEL: Final[str] = os.getenv("CONSOLE_LOG_LEVEL", "DEBUG")

# Log formats (with milliseconds)
CONSOLE_FORMAT: Final[str] = (
    "%(log_color)s%(asctime)s.%(msecs)03d [%(levelname)-8s] %(name)s: %(message)s"
)
FILE_FORMAT: Final[str] = (
    "%(asctime)s.%(msecs)03d [%(levelname)-8s] %(name)s:%(lineno)d - %(message)s"
)
JSON_FORMAT: Final[str] = "%(asctime)s.%(msecs)03d %(name)s %(levelname)s %(message)s"

# Enhanced format that can show extra fields when available
ENHANCED_FORMAT: Final[str] = (
    "%(asctime)s.%(msecs)03d [%(levelname)-8s] %(name)s:%(lineno)d - %(message)s%(extra_info)s"
)

# Date format (with milliseconds)
DATE_FORMAT: Final[str] = "%Y-%m-%d %H:%M:%S"

# File rotation settings
MAX_LOG_SIZE: Final[int] = 10 * 1024 * 1024  # 10MB
BACKUP_COUNT: Final[int] = 5

# Environment settings
IS_PRODUCTION: Final[bool] = os.getenv("ENVIRONMENT", "development") == "production"
USE_JSON_FORMAT: Final[bool] = (
    os.getenv("USE_JSON_FORMAT", "false").lower() == "true" or IS_PRODUCTION
)

# Colorlog color configuration
LOG_COLORS: Final[dict[str, str]] = {
    "DEBUG": "cyan",
    "INFO": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "red,bg_white",
}
