import os
from logging.handlers import RotatingFileHandler
import logging


class mytinylog:

    def __init__(self, name, path, dev_out, level='info'):
        levels = {'debug': logging.DEBUG,
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR,
            'critical': logging.CRITICAL}
        self.__name__ = name
        self.__path__ = os.path.abspath(path)
        if not os.path.exists(self.__path__):
            os.makedirs(self.__path__)
        self.log = logging.getLogger(name)
        self.log_file = '%s.log' % os.path.join(self.__path__, self.__name__)
        formatter = logging.Formatter(
            self.__name__ + ': %(levelname)s : %(asctime)s : %(message)s')
        fileHandler = RotatingFileHandler(
            self.log_file, mode='a', maxBytes=1e6, backupCount=5)
        fileHandler.setFormatter(formatter)
        streamHandler = logging.StreamHandler(dev_out)
        streamHandler.setFormatter(formatter)
        self.log.setLevel(levels[level])
        self.log.addHandler(fileHandler)
        self.log.addHandler(streamHandler)
