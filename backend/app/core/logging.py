import logging
import sys


def configure_logging() -> None:
    """Configure application logging using Python's standard logging module."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout,
    )


def get_logger(name: str = "ai-testpilot") -> logging.Logger:
    return logging.getLogger(name)
