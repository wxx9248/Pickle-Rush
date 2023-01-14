# -*- coding: utf-8 -*-
import typing

import pygame.sprite

from core.object_model.Atlas import Atlas


class Layer:
    def __init__(self, *args: Atlas):
        self.__atlases: typing.List[Atlas] = [*args]

    def add_atlas(self, atlas: Atlas):
        self.__atlases.append(atlas)

    def update(self):
        for atlas in self.__atlases:
            atlas.update()

    def render(self, surface: pygame.surface.Surface):
        for atlas in self.__atlases:
            atlas.render(surface)

    def accept_event(self, event: pygame.event.Event):
        for atlas in self.__atlases:
            atlas.accept_event(event)
