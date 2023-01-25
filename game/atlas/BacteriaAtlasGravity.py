# -*- coding: utf-8 -*-
import typing

import pygame

from asset.AssetObjectFactory import AssetObjectFactory
from core.object_model.Atlas import Atlas
from util.MapNavigator import MapNavigator


class BacteriaAtlasGravity(Atlas):
    G = 0.1

    def __init__(self):
        asset_object_factory = AssetObjectFactory()
        super().__init__(asset_object_factory.new_asset_object("asset.sprite.bacteria"))
        self.scale_to((60, 60))

        self.__first_touch_ground = False
        self.__map_navigator: typing.Optional[MapNavigator] = None
        self.__speed = 2
        self.__hp = 1
        self.__damage = 1
        self.acceleration_y = self.G

    @property
    def first_touch_ground(self):
        return self.__first_touch_ground

    @first_touch_ground.setter
    def first_touch_ground(self, val: bool):
        self.__first_touch_ground = val

    @property
    def map_navigator(self):
        return self.__map_navigator

    @map_navigator.setter
    def map_navigator(self, value: typing.Optional[MapNavigator]):
        self.__map_navigator = value

    @property
    def hp(self):
        return self.__hp

    @hp.setter
    def hp(self, val):
        self.__hp = val

    @property
    def damage(self):
        return self.__damage

    # after first touch ground.
    # this atlas will only move by directly position change.
    def update(self) -> None:
        if not self.__first_touch_ground:
            super().update()
            return

        if self.__map_navigator:
            self.__map_navigator.update()
            self.position += (self.__map_navigator.direction_vector * self.__speed)

    def render(self, surface: pygame.surface.Surface) -> None:
        super().render(surface)
