# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import logging

class CustomFormatter(logging.Formatter):
    """ Custom logger """

    grey = "\x1b[36;20m"
    black = "\x1b[30;20m"
    normal = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    file = reset + grey + " (%(filename)s:%(lineno)d)" + reset
    format = "[%(levelname).1s %(asctime)s] %(message)s" + file
    FORMATS = {
        logging.DEBUG: normal + format,
        logging.INFO: black + format,
        logging.WARNING: yellow + format,
        logging.ERROR: red + format,
        logging.CRITICAL: bold_red + format }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%H:%M:%S")
        return formatter.format(record)


log = logging.getLogger("GSP")
log.setLevel(logging.WARNING)

_handler = logging.StreamHandler()
_handler.setLevel(logging.DEBUG)
_handler.setFormatter(CustomFormatter())
log.addHandler(_handler)
