# -*- coding: utf-8 -*-
import queue
import typing

import pygame

from core.SubsystemThread import SubsystemThread
from event.EventDispatcher import EventDispatcher

RenderQueueType: typing.TypeAlias = queue.Queue[typing.List[pygame.Rect]]


class GameThread(SubsystemThread):
    def __init__(self, global_event_dispatcher: EventDispatcher, display_surface: pygame.surface.Surface):
        super().__init__(global_event_dispatcher)
        self.__display_surface = display_surface
        self.__render_queue: RenderQueueType = queue.Queue()

    @property
    def render_queue(self) -> RenderQueueType:
        return self.__render_queue

    def looper(self):
        while self.running:
            not self.event_queue.empty() and self.local_event_dispatcher.dispatch(self.event_queue.get())
