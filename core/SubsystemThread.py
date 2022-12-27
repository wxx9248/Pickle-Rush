# -*- coding: utf-8 -*-
import queue
import typing

import pygame

from core.BaseThread import BaseThread
from event.EventDispatcher import EventDispatcher
from event.EventHandler import EventHandler
from event.LocalEventDispatcher import LocalEventDispatcher
from event.LocalEventReceiver import LocalEventReceiver


class SubsystemThread(BaseThread):
    def __init__(self, global_event_dispatcher: EventDispatcher):
        super().__init__()
        self.__event_queue = queue.Queue()
        self.__local_event_receiver = LocalEventReceiver(self.__event_queue)
        self.__local_event_dispatcher = LocalEventDispatcher(global_event_dispatcher, self.__local_event_receiver)

        self.__exception: typing.Optional[BaseException] = None

        self.__event_handler_quit = EventHandler("quit", lambda _: self.stop())
        self.__local_event_dispatcher.register(pygame.QUIT, self.name, self.__event_handler_quit)

    @property
    def event_queue(self):
        return self.__event_queue

    @property
    def local_event_dispatcher(self):
        return self.__local_event_dispatcher

    @property
    def exception(self):
        return self.__exception

    @exception.setter
    def exception(self, value):
        self.__exception = value

    def before_looper(self):
        pass

    def after_looper(self):
        pass

    def looper(self):
        while self.running:
            self.local_event_dispatcher.dispatch(self.event_queue.get())

    def run(self):
        try:
            self.before_looper()
            self.looper()
            self.after_looper()
        except BaseException as e:
            self.logger.error("Thread exception occurred. Stopping")
            self.exception = e
            self.stop()

    def join(self, timeout: float | None = None) -> None:
        super().join(timeout)
        if self.__exception is not None:
            raise self.__exception

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.__class__.__name__
