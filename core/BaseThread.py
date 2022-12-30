# -*- coding: utf-8 -*-
import logging
import threading


class BaseThread(threading.Thread):
    def __init__(self):
        super().__init__(name=self.__class__.__name__)
        self.__logger = logging.getLogger(self.name)
        self.__running = True

    @property
    def logger(self) -> logging.Logger:
        return self.__logger

    @property
    def running(self) -> bool:
        return self.__running

    def stop(self):
        self.__running = False

    def __repr__(self) -> str:
        return self.__class__.__name__

    def __str__(self) -> str:
        return self.__class__.__name__
