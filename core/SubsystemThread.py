# -*- coding: utf-8 -*-
import queue
import typing

import pygame

from core.BaseThread import BaseThread
from event.CustomEventTypes import CustomEventTypes
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
    def event_queue(self) -> queue.Queue[pygame.event.Event]:
        return self.__event_queue

    @property
    def local_event_dispatcher(self) -> LocalEventDispatcher:
        return self.__local_event_dispatcher

    @property
    def exception(self) -> typing.Optional[Exception]:
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
            self.logger.error("Thread exception occurred")
            self.exception = e

            self.logger.debug("Posting thread exception event")
            exception_event = pygame.event.Event(CustomEventTypes.EVENT_THREAD_EXCEPTION)
            exception_event.thread = self.name
            exception_event.exception = e
            pygame.event.post(exception_event)

            self.logger.debug("Stopping thread")
            self.stop()

    def join(self, timeout: float | None = None):
        super().join(timeout)
        if self.__exception is not None:
            raise self.__exception
