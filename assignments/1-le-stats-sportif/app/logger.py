import logging
from logging.handlers import RotatingFileHandler
import time


class ServerLogger:
    def __init__(
        self, filename="webserver.log", maxBytes=1024, backupCount=5):

        self.logger = logging.getLogger("ServerLogger")
        self.logger.setLevel(logging.DEBUG)

        self.handler = RotatingFileHandler(f"{filename}", maxBytes, backupCount)
        self.handler.setLevel(logging.INFO)

        formatter = self.formatter()
        self.handler.setFormatter(formatter)
        self.logger.addHandler(self.handler)

    def getConfiguredLogger(self):
        return self.logger

    def formatter(self):

        log_format = (
            "%(asctime)s - %(name)s - %(levelname)s - "
            "%(filename)s:%(lineno)d - %(message)s"
        )

        formatter = logging.Formatter(log_format, datefmt="%Y-%m-%d %H:%M:%S")
        formatter.converter = time.gmtime
        return formatter


server_logger = ServerLogger().getConfiguredLogger()
