# -*- coding: utf-8 -*-
import typing
from typing import Optional, Dict
from typing import Tuple

import pygame

from asset.AssetObjectFactory import AssetObjectFactory
from core.object_model.Atlas import Atlas
from util.MapNavigator import MapNavigator
from util.PriorityQueue import PriorityQueue


class BacteriaAtlas(Atlas):
    def __init__(self):
        asset_object_factory = AssetObjectFactory()
        super().__init__(asset_object_factory.new_asset_object("asset.sprite.bacteria"))

        self.__map_navigator: typing.Optional[MapNavigator] = None
        self.__speed = 2

    @property
    def map_navigator(self):
        return self.__map_navigator

    @map_navigator.setter
    def map_navigator(self, value: typing.Optional[MapNavigator]):
        self.__map_navigator = value

    def update(self) -> None:
        super().update()
        if self.__map_navigator:
            self.__map_navigator.update()
            self.position += (self.__map_navigator.direction_vector * self.__speed)

    def render(self, surface: pygame.surface.Surface) -> None:
        super().render(surface)

