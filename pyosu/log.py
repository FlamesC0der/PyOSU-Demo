import logging


class LoggingFormatter(logging.Formatter):
    black = "\x1b[30m"
    FAIL = "\033[91m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    blue = "\x1b[34m"
    gray = "\x1b[38m"
    reset = "\x1b[0m"

    format = "[%(asctime)s] %(levelname)-8s | %(module)-8s | %(message)s"

    FORMATS = {
        logging.DEBUG: gray + format + reset,
        logging.INFO: blue + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: FAIL + format + reset,
    }

    def format(self, record):
        formatter = logging.Formatter(self.FORMATS.get(record.levelno))
        return formatter.format(record)


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(LoggingFormatter())
file_handler = logging.FileHandler(
    filename=f"Logs/core_log.log",
    mode="w",
)
file_handler.setFormatter(
    logging.Formatter("[%(asctime)s] %(levelname)-8s | %(module)-8s | %(message)s")
)

logger.addHandler(console_handler)
logger.addHandler(file_handler)