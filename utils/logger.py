from pathlib import Path
import logging


class LoggerFactory:
    """Creates module-specific loggers that write log files under data/."""

    PROJECT_ROOT = Path(__file__).resolve().parents[1]
    LOG_DIR = PROJECT_ROOT / "data"

    @classmethod
    def get_logger(cls, logger_name: str, log_file_name: str) -> logging.Logger:
        cls.LOG_DIR.mkdir(parents=True, exist_ok=True)

        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)
        logger.propagate = False

        expected_path = str(cls.LOG_DIR / log_file_name)
        already_configured = any(
            isinstance(handler, logging.FileHandler)
            and getattr(handler, "baseFilename", None) == expected_path
            for handler in logger.handlers
        )

        if not already_configured:
            handler = logging.FileHandler(expected_path, encoding="utf-8")
            handler.setFormatter(logging.Formatter(
                "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
            ))
            logger.addHandler(handler)

        return logger
