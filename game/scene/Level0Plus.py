# -*- coding: utf-8 -*-
import typing

import pygame

from asset.AssetObjectFactory import AssetObjectFactory
from core.object_model.Layer import Layer
from core.object_model.Map import Map
from core.object_model.Scene import Scene
from event.CustomEventTypes import CustomEventTypes
from game.atlas.BacteriaAtlas import BacteriaAtlas
from game.atlas.MapAtlas import MapAtlas
from game.atlas.PickleAtlas import PickleAtlas
from game.scene.GameLost import GameLost
from game.scene.GameWin import GameWin
from game.scene.Level1 import Level1
from util import util
from util.MapNavigator import MapNavigator


class Level0Plus(Scene):
    def __init__(self, size: typing.Tuple[int, int]):
        super().__init__(size)

        self.background["background"] = AssetObjectFactory().new_asset_object("asset.sprite.level.0.plus.background")

        texture_dict = {
            Map.TileType.SPACE: AssetObjectFactory().new_asset_object("asset.sprite.level.0.tile.soil"),
            Map.TileType.WALL: AssetObjectFactory().new_asset_object("asset.sprite.level.0.tile.wall"),
            Map.TileType.EXIT: AssetObjectFactory().new_asset_object("asset.sprite.level.0.tile.exit"),
            Map.TileType.START: AssetObjectFactory().new_asset_object("asset.sprite.level.0.tile.spawn")
        }

        self.__map_atlas = \
            MapAtlas(AssetObjectFactory().new_asset_object("asset.map.random", tile_count=(17, 23)), texture_dict)
        self.__map_atlas.position = util.center(
            size,
            self.__map_atlas[self.__map_atlas.current_sprite_key].surface.get_size()
        )
        map_layer = Layer(self.__map_atlas)

        self.__pickle_atlas = PickleAtlas()
        self.__pickle_atlas.scale = (0.025, 0.025)
        self.__pickle_atlas.position = self.__map_atlas.grid_to_screen_position(
            pygame.Vector2(self.__map_atlas.map_object.start_point), None
        )

        entity_layer = Layer(self.__pickle_atlas)

        self.__bacteria_atlas_position = (
            (BacteriaAtlas(), (1, 1)),
            (BacteriaAtlas(), (15, 1)),
            (BacteriaAtlas(), (1, 21)),
            (BacteriaAtlas(), (15, 21)),
            (BacteriaAtlas(), self.__map_atlas.map_object.exit_point)
        )
        for (bacteria_atlas, position) in self.__bacteria_atlas_position:
            bacteria_atlas.scale = (0.025, 0.025)
            bacteria_atlas.position = self.__map_atlas.grid_to_screen_position(
                pygame.Vector2(position), bacteria_atlas.surface.get_size()
            )
            bacteria_atlas.map_navigator = MapNavigator(bacteria_atlas, self.__pickle_atlas, self.__map_atlas)
            entity_layer.add_atlas(bacteria_atlas)

        self.layer_manager["map"] = map_layer
        self.layer_manager["entity"] = entity_layer

    def update(self):
        pickle_position = self.__pickle_atlas.position
        super().update()

        collide_bacteria = any([self.__pickle_atlas.collides_atlas(bacteria_atlas)
                                for (bacteria_atlas, _) in self.__bacteria_atlas_position])
        if collide_bacteria:
            event = pygame.event.Event(CustomEventTypes.EVENT_STAGE_CHANGE_SCENE_REQUEST)
            event.scene = GameLost(self.size, self.__class__)
            pygame.event.post(event)

        collide_wall = self.__pickle_atlas.collides_mask(
            self.__map_atlas.wall_mask,
            pygame.Vector2(self.__map_atlas.position) - pygame.Vector2(self.__pickle_atlas.position)
        )
        if collide_wall:
            self.__pickle_atlas.speed = (0, 0)
            self.__pickle_atlas.position = pickle_position
            return

        collide_exit = self.__pickle_atlas.collides_mask(
            self.__map_atlas.exit_mask,
            pygame.Vector2(self.__map_atlas.position) - pygame.Vector2(self.__pickle_atlas.position)
        )
        if collide_exit:
            event = pygame.event.Event(CustomEventTypes.EVENT_STAGE_CHANGE_SCENE_REQUEST)
            event.scene = GameWin(self.size, Level1)
            pygame.event.post(event)
