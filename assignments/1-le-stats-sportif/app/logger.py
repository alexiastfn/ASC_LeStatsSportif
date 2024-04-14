"""
Logging module
"""
import logging
from logging.handlers import RotatingFileHandler
import time

class ServerLogger:
    """
    ServerLogger class for implemententing the logging messages
    """
    def __init__(
        self, filename="webserver.log", max_bytes=1024, backup_count=5):

        self.logger = logging.getLogger("ServerLogger")
        self.logger.setLevel(logging.DEBUG)

        self.handler = RotatingFileHandler(f"{filename}", max_bytes, backup_count)
        self.handler.setLevel(logging.INFO)

        formatter = self.formatter()
        self.handler.setFormatter(formatter)
        self.logger.addHandler(self.handler)

    def get_configured_logger(self):
        """ Return a logger instance """
        return self.logger

    def formatter(self):
        """ Formatter for logging messages """

        log_format = (
            "%(asctime)s - %(name)s - %(levelname)s - "
            "%(filename)s:%(lineno)d - %(message)s"
        )

        formatter = logging.Formatter(log_format, datefmt="%Y-%m-%d %H:%M:%S")
        formatter.converter = time.gmtime
        return formatter


server_logger = ServerLogger().get_configured_logger()
