"""Logger demonstration module with various examples."""

import time

from .logger import get_logger, log_context, log_execution_time


class LoggerDemo:
    """Professional logger demonstration class."""

    def __init__(self) -> None:
        """Initialize the logger demo."""
        self.logger = get_logger("logger_demo")

    @log_execution_time()
    def _slow_operation(self) -> str:
        """Simulate a slow operation to demonstrate performance logging."""
        time.sleep(0.1)
        return "Operation completed successfully"

    @log_execution_time()
    def _error_operation(self) -> None:
        """Simulate an error to demonstrate error logging."""
        raise ValueError("This is a test error for demonstration")

    def basic_logging(self) -> None:
        """Demonstrate basic logging levels."""
        self.logger.info("=== Basic Logging Demo ===")
        self.logger.debug("Debug message")
        self.logger.info("Info message")
        self.logger.warning("Warning message")
        self.logger.error("Error message")
        self.logger.critical("Critical message")

    def structured_logging(self) -> None:
        """Demonstrate structured logging with extra data."""
        self.logger.info("=== Structured Logging Demo ===")
        self.logger.info("Message with extra data", extra={"data": 0})

    def performance_logging(self) -> None:
        """Demonstrate performance logging with decorators."""
        self.logger.info("=== Performance Logging Demo ===")
        result = self._slow_operation()
        self.logger.info(f"Demo operation completed: {result}")

    def error_logging(self) -> None:
        """Demonstrate error logging with exception handling."""
        self.logger.info("=== Error Logging Demo ===")
        try:
            self._error_operation()
        except ValueError as e:
            self.logger.error(f"Caught expected error: {e}", exc_info=True)

    def context_logging(self) -> None:
        """Demonstrate context logging for related operations."""
        self.logger.info("=== Context Logging Demo ===")
        with log_context(self.logger, context_data=0) as ctx_logger:
            ctx_logger.info("Example message with context")

    def run(self) -> None:
        """Run all individual demo methods."""
        self.logger.info("Logger Demo Started")

        self.basic_logging()
        self.structured_logging()
        self.performance_logging()
        self.error_logging()
        self.context_logging()

        self.logger.info("Logger Demo Completed")


class Demo:
    """Main demo class to manage different module demonstrations."""

    def __init__(self) -> None:
        """Initialize the demo manager."""
        self.logger_demo = LoggerDemo()

    def run(self) -> None:
        """Run all module demos."""
        self.logger_demo.run()
