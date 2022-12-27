# -*- coding: utf-8 -*-
import pygame.display

from core.SubsystemThread import SubsystemThread
from event.EventDispatcher import EventDispatcher


class GraphicThread(SubsystemThread):
    def __init__(self, global_event_dispatcher: EventDispatcher):
        super().__init__(global_event_dispatcher)

    def looper(self):
        screen = pygame.display.set_mode((600, 600))
        while self.running:
            not self.event_queue.empty() and self.local_event_dispatcher.dispatch(self.event_queue.get())
            pygame.display.update()
