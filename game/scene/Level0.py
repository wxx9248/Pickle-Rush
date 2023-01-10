# -*- coding: utf-8 -*-
import typing

import pygame.surface

from asset.AssetObjectFactory import AssetObjectFactory
from core.object_model.Layer import Layer
from core.object_model.Scene import Scene
from core.object_model.Sprite import Sprite
from game.atlas.MapAtlas import MapAtlas
from game.atlas.PickleAtlas import PickleAtlas
from util import util


class Level0(Scene):
    def __init__(self, size: typing.Tuple[int, int]):
        super().__init__(size)

        background_surface = pygame.Surface(self.size).convert_alpha()
        background_surface.fill(pygame.Color("white"))
        self.background["background"] = Sprite(background_surface)

        self.__map_atlas = MapAtlas(AssetObjectFactory().new_asset_object("asset.map.level.0"))
        self.__map_atlas.position = util.center(
            size,
            self.__map_atlas[self.__map_atlas.current_sprite_key].surface.get_size()
        )
        map_layer = Layer(self.__map_atlas)

        self.__pickle_atlas = PickleAtlas()
        self.__pickle_atlas.position = self.__map_atlas.to_screen_position(pygame.Vector2(10, 10))
        self.__pickle_atlas.scale = (0.025, 0.025)

        # bacteria_atlas = BacteriaAtlas(self)
        # bacteria_atlas.position = (40, 40)

        entity_layer = Layer(self.__pickle_atlas)

        # print(bacteria_atlas.reconstruct_path(bacteria_atlas.a_star_search()))

        self.layer_manager["map"] = map_layer
        self.layer_manager["entity"] = entity_layer

    def update(self):
        pickle_position = self.__pickle_atlas.position
        super().update()

        collide_wall = self.__pickle_atlas.collides_mask(
            self.__map_atlas.wall_mask,
            pygame.Vector2(self.__map_atlas.position) - pygame.Vector2(self.__pickle_atlas.position)
        )

        if collide_wall is not None:
            print(collide_wall)
            self.__pickle_atlas.speed = (0, 0)
            self.__pickle_atlas.position = pickle_position

