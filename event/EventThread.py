# -*- coding: utf-8 -*-
import pygame

from core.BaseThread import BaseThread
from event.EventDispatcher import EventDispatcher


class EventThread(BaseThread):
    def __init__(self, event_dispatcher: EventDispatcher):
        super().__init__(event_dispatcher)

    def run(self):
        while self.running:
            self.event_dispatcher.dispatch_all(pygame.event.get())
