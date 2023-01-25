# -*- coding: utf-8 -*-
import typing

import pygame.sprite

from core.object_model.Atlas import Atlas
from typing import List


class Layer:
    def __init__(self, *args: Atlas):
        self.__atlases: typing.List[Atlas] = [*args]

    def set_atlas_list(self, val: List[Atlas]):
        self.__atlases = val

    def del_atlas(self, atlas: Atlas):
        self.__atlases.remove(atlas)

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
