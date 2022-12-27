# -*- coding: utf-8 -*-

import pygame

from core.BaseThread import BaseThread
from event.EventDispatcher import EventDispatcher
from event.EventHandler import EventHandler


class EventDispatchThread(BaseThread):
    def __init__(self, global_event_dispatcher: EventDispatcher):
        super().__init__()
        self.__global_event_dispatcher = global_event_dispatcher
        self.__event_handler_quit = EventHandler("quit", lambda _: self.stop())
        self.__global_event_dispatcher.register(pygame.QUIT, self.name, self.__event_handler_quit)

    def run(self):
        while self.running:
            self.__global_event_dispatcher.dispatch_all(pygame.event.get())
