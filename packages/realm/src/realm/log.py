import logging

from colorama import Fore


class ColorFormatter(logging.Formatter):
    grey = Fore.LIGHTBLACK_EX
    yellow = Fore.YELLOW
    red = Fore.RED
    reset = Fore.RESET
    format = "%(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def __create_logger():
    import logging

    logger = logging.getLogger("realm")
    handler = logging.StreamHandler()
    handler.setFormatter(ColorFormatter())
    logger.addHandler(handler)
    return logger


logger = __create_logger()
