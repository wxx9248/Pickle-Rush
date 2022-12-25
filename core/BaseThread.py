# -*- coding: utf-8 -*-
import logging
import threading

import pygame

from core.EventDispatcher import EventDispatcher


class BaseThread(threading.Thread):
    def __init__(self):
        super().__init__(name=self.__class__.__name__)
        self.__logger = logging.getLogger(self.name)
        self.__event_dispatcher = EventDispatcher()
        self.__running = True

        self.__event_dispatcher.register(pygame.QUIT, lambda _: self.stop())

    @property
    def logger(self):
        return self.__logger

    @property
    def event_dispatcher(self):
        return self.__event_dispatcher

    @property
    def running(self):
        return self.__running

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.__class__.__name__

    def stop(self):
        self.__running = False
