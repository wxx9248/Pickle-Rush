# -*- coding: utf-8 -*-
import queue
import typing

import pygame

from core.Stage import Stage
from core.SubsystemThread import SubsystemThread
from event.EventDispatcher import EventDispatcher

RenderQueueType: typing.TypeAlias = queue.Queue[typing.List[pygame.surface.Surface]]


class GameThread(SubsystemThread):
    def __init__(self, global_event_dispatcher: EventDispatcher, stage: Stage):
        super().__init__(global_event_dispatcher)

        self.__stage = stage
        stage.before_scene_change = lambda: self.pause()
        stage.after_scene_change = lambda: self.resume()

    def loop(self):
        self.local_event_dispatcher.dispatch(self.event_queue.get())
        self.__stage.scene.update()
