# -*- coding: utf-8 -*-
import logging
import threading
import typing

import pygame

from event.EventDispatcher import EventDispatcher
from event.EventHandler import EventHandler


class BaseThread(threading.Thread):
    def __init__(self, event_dispatcher: EventDispatcher):
        super().__init__(name=self.__class__.__name__)
        self.__logger = logging.getLogger(self.name)
        self.__event_dispatcher = event_dispatcher
        self.__running = True
        self.__exception: typing.Optional[BaseException] = None

        self.__event_handler_quit = EventHandler("quit", lambda _: self.stop())
        self.__event_dispatcher.register(pygame.QUIT, self.name, self.__event_handler_quit)

    @property
    def logger(self):
        return self.__logger

    @property
    def event_dispatcher(self):
        return self.__event_dispatcher

    @property
    def exception(self):
        return self.__exception

    @exception.setter
    def exception(self, value):
        self.__exception = value

    @property
    def running(self):
        return self.__running

    def join(self, timeout: float | None = None) -> None:
        super().join(timeout)
        if self.__exception is not None:
            raise self.__exception

    def stop(self):
        self.__running = False

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.__class__.__name__
