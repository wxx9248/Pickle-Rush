# -*- coding: utf-8 -*-
import queue

import pygame

from core.BaseThread import BaseThread
from event.CustomEventTypes import CustomEventTypes
from event.EventDispatcher import EventDispatcher
from event.EventHandler import EventHandler
from event.LocalEventDispatcher import LocalEventDispatcher
from event.LocalEventReceiver import LocalEventReceiver


class SubsystemThread(BaseThread):
    def __init__(self, global_event_dispatcher: EventDispatcher, paused=False):
        super().__init__(paused)
        self.__event_queue = queue.Queue()
        self.__local_event_receiver = LocalEventReceiver(self.__event_queue)
        self.__local_event_dispatcher = LocalEventDispatcher(global_event_dispatcher, self.__local_event_receiver)

        self.__event_handler_quit = EventHandler("quit", lambda _: self.stop())
        self.__local_event_dispatcher.register(pygame.QUIT, self.name, self.__event_handler_quit)

    @property
    def event_queue(self) -> queue.Queue[pygame.event.Event]:
        return self.__event_queue

    @property
    def local_event_dispatcher(self) -> LocalEventDispatcher:
        return self.__local_event_dispatcher

    def loop(self):
        self.__local_event_dispatcher.dispatch(self.event_queue.get())

    def on_exception(self, exception):
        self.logger.debug("Posting thread exception event")
        exception_event = pygame.event.Event(CustomEventTypes.EVENT_THREAD_EXCEPTION)
        exception_event.thread = self.name
        exception_event.exception = exception
        pygame.event.post(exception_event)
