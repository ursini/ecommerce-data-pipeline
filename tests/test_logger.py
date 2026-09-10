from pathlib import Path

from src.utils.logger import get_logger, LOG_FILE


def test_logger_returns_logger():
    logger = get_logger("test_logger")

    assert logger.name == "test_logger"
    assert logger.level == 20


def test_logger_creates_log_file():
    logger = get_logger("test_file_logger")

    logger.info("Test log message")

    assert Path(LOG_FILE).exists()


def test_logger_has_handlers():
    logger = get_logger("test_handlers_logger")

    assert len(logger.handlers) >= 1