# -*- coding: utf-8 -*-
import pygame.display

from core.BaseThread import BaseThread
from event.EventDispatcher import EventDispatcher


class GraphicThread(BaseThread):
    def __init__(self, event_dispatcher: EventDispatcher):
        super().__init__(event_dispatcher)

    def run(self):
        try:
            screen = pygame.display.set_mode((600, 600))
            while self.running:
                pygame.display.update()
        except BaseException as e:
            self.exception = e
            self.stop()
