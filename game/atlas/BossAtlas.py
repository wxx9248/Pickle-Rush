# -*- coding: utf-8 -*-
import typing

import pygame

from asset.AssetObjectFactory import AssetObjectFactory
from core.object_model.Atlas import Atlas
from game.atlas.BacteriaAtlasGravity import BacteriaAtlasGravity
from game.atlas.BulletAtlas import BulletAtlas
from util.PatrolNavigator import PatrolNavigator
from game.atlas.MapAtlas import MapAtlas
from core.object_model.Sprite import Sprite
from core.object_model.Layer import Layer
from core.object_model.TimedState import TimedState
from typing import List


class BossAtlas(Atlas):
    def __init__(self, enemy_list: List, enemy_bullet_list: List, map_atlas: MapAtlas):
        asset_object_factory = AssetObjectFactory()
        super().__init__(asset_object_factory.new_asset_object("asset.sprite.bacteria"))
        self.scale_to((700, 700))
        self.__enemy_list = enemy_list
        self.__bullet_list = enemy_bullet_list
        self.__map_atlas = map_atlas
        self.__hp = 20
        self.__bullet_speed = 5
        self.__fire_cd = TimedState(60 * 1)

        self.__time_elapsed = 0
        self.__prepare_time = 100

    @property
    def hp(self):
        return self.__hp

    @hp.setter
    def hp(self, val):
        self.__hp = val

    def spawn_new_enemy(self):
        bc1 = BacteriaAtlasGravity()
        bc1.position = self.position
        bc1.speed = (-1, -2)
        bc1.map_navigator = PatrolNavigator(bc1, self.__map_atlas, (2, 18))
        self.__enemy_list.append(bc1)

        bc2 = BacteriaAtlasGravity()
        bc2.position = self.position
        bc2.speed = (-5, -3)
        bc2.map_navigator = PatrolNavigator(bc2, self.__map_atlas, (2, 18))
        self.__enemy_list.append(bc2)

    def fire(self):
        img = pygame.Surface((10, 2))
        img.fill(pygame.color.Color("blue"))
        sp = Sprite(img)
        bullet = BulletAtlas(sp)

        fire_vec = pygame.Vector2(-1, 0) * self.__bullet_speed
        bullet.position = tuple(pygame.Vector2(self.position))
        bullet.position_y = int(10.5 * 60)

        bullet.speed = fire_vec
        self.__bullet_list.append(bullet)

    def update(self):
        if self.__time_elapsed < self.__prepare_time:
            self.__time_elapsed += 1
            return

        if len(self.__enemy_list) == 0:
            self.spawn_new_enemy()

        if self.hp < 10 and not self.__fire_cd.activate:
            self.fire()
            self.__fire_cd.reset()
            self.__fire_cd.start()

        self.__fire_cd.update()

    def render(self, surface: pygame.surface.Surface) -> None:
        super().render(surface)
