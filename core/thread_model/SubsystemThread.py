# -*- coding: utf-8 -*-

import pygame

from core.thread_model.BaseThread import BaseThread
from event.CustomEventTypes import CustomEventTypes
from event.EventDispatcher import EventDispatcher
from event.EventHandler import EventHandler
from event.LocalEventDispatcher import LocalEventDispatcher


class SubsystemThread(BaseThread):
    def __init__(self, global_event_dispatcher: EventDispatcher, paused=False):
        super().__init__(paused)
        self.__local_event_dispatcher = LocalEventDispatcher(self.name, global_event_dispatcher)

        self.__event_handler_quit = EventHandler("quit", lambda _: self.stop())
        self.__local_event_dispatcher.register(pygame.QUIT, "default", self.__event_handler_quit)

    @property
    def local_event_dispatcher(self) -> LocalEventDispatcher:
        return self.__local_event_dispatcher

    def loop(self):
        self.__local_event_dispatcher.dispatch()

    def on_exception(self, exception):
        self.logger.debug("Posting thread exception event")
        exception_event = pygame.event.Event(CustomEventTypes.EVENT_THREAD_EXCEPTION)
        exception_event.thread = self.name
        exception_event.exception = exception
        pygame.event.post(exception_event)
