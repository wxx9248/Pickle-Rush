# -*- coding: utf-8 -*-
import typing

import pygame.surface

from core.object_model.Scene import Scene


class Stage:
    def __init__(self, surface: pygame.surface.Surface):
        self.__surface = surface
        self.__scene: typing.Optional[Scene] = None
        self.__before_scene_change: typing.Callable[[None], None] = lambda: None
        self.__after_scene_change: typing.Callable[[None], None] = lambda: None

    @property
    def before_scene_change(self):
        return self.__before_scene_change

    @before_scene_change.setter
    def before_scene_change(self, value):
        self.__before_scene_change = value

    @property
    def after_scene_change(self):
        return self.__after_scene_change

    @after_scene_change.setter
    def after_scene_change(self, value):
        self.__after_scene_change = value

    @property
    def scene(self):
        return self.__scene

    @scene.setter
    def scene(self, value: Scene):
        self.__before_scene_change()
        self.__scene = value
        self.__after_scene_change()

    def set_scene(self, scene: Scene):
        self.scene = scene

    def accept_event(self, event: pygame.event.Event):
        self.__scene.accept_event(event)
