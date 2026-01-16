import logging
import os
from logging.handlers import RotatingFileHandler


def configure_logging(app):
    level_str = os.environ.get("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_str, logging.INFO)

    app.logger.setLevel(level)

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)
    app.logger.addHandler(ch)

    # Optional file logging
    log_file = os.environ.get("LOG_FILE", "").strip()
    if log_file:
        fh = RotatingFileHandler(log_file, maxBytes=2_000_000, backupCount=3)
        fh.setLevel(level)
        fh.setFormatter(formatter)
        app.logger.addHandler(fh)

    # Reduce werkzeug noise
    logging.getLogger("werkzeug").setLevel(logging.WARNING)
