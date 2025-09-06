#!/usr/bin/env python3

import argparse

from src.__version__ import __version__
from src.demo import Demo
from src.logger import get_logger


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        prog="python-template",
        description="Python Template Application with Demo Functionality",
        epilog="Without arguments, the application will simply start and finish.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--demo", action="store_true", help="Run demonstration of application features"
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show program version",
    )

    return parser


def main() -> None:
    """Main application entry point."""
    parser = create_parser()
    args = parser.parse_args()

    logger = get_logger("main")

    logger.info("Application started")

    if args.demo:
        logger.info("Running demo mode...")
        demo = Demo()
        demo.run()

    logger.info("Application finished")


if __name__ == "__main__":
    main()
