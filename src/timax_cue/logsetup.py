"""Sets up logging to the console and to a log file that rotates every day."""

import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parents[2] / "logs"   # <project>/logs
LOG_FILE = LOG_DIR / "timax.log"
HOURS_TO_KEEP = 3


def setup_logging() -> None:
    """Send log messages both to the console and to logs/timax.log.

    Every hour the current file is renamed with the date and hour (e.g.
    timax.log.2026-11-26_13) and a new one starts. Only the last HOURS_TO_KEEP
    old files are kept, so the logs cover at most about 3 hours.
    """
    LOG_DIR.mkdir(exist_ok=True)
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)-7s %(message)s", "%Y-%m-%d %H:%M:%S"
    )

    file_handler = TimedRotatingFileHandler(
        LOG_FILE, when="midnight", backupCount=HOURS_TO_KEEP, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logging.basicConfig(level=logging.INFO, handlers=[file_handler, console_handler])