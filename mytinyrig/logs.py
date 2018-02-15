import os
from logging.handlers import RotatingFileHandler
import logging

class log:

    def __init__(self, name, path, level=logging.INFO):
        self.__name__ = name
        self.__path__ = os.path.join(path, self.__name__)
        if not os.path.exists(self.__path__):
            os.makedirs(self.__path__)
        self.log = logging.getLogger(name)
        self.log_file = '%s.log' % self.__path__
        formatter = logging.Formatter(
            '%(levelname)s : %(asctime)s : %(message)s')
        fileHandler = RotatingFileHandler(
            self.log_file, mode='a', maxBytes=1e6, backupCount=5)
        fileHandler.setFormatter(formatter)
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)
        self.log.setLevel(level)
        self.log.addHandler(fileHandler)
        self.log.addHandler(streamHandler)
