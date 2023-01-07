# -*- coding: utf-8 -*-
import typing

import pygame.surface

from asset.AssetObjectFactory import AssetObjectFactory
from core.object_model.Scene import Scene
from core.object_model.Layer import Layer
from core.object_model.Atlas import Atlas
from core.object_model.Map import Map
from core.object_model.Sprite import Sprite
from game.atlas.PickleAtlas import PickleAtlas
from game.atlas.BacteriaAtlas import BacteriaAtlas


class Level0(Scene):
    def __init__(self, size: typing.Tuple[int, int], asset_object_factory: AssetObjectFactory):
        super().__init__(size, asset_object_factory)

        pygame.key.set_repeat(1, 50)

        map_obj: Map = asset_object_factory.new_asset_object("asset.map.level.1")
        self.map_obj = map_obj

        map_atlas = list(map_obj.map_wall_atlas_dict.values())
        map_wall_layer = Layer(*map_atlas)

        bg_surface = pygame.Surface(self.size)
        bg_surface.fill((255, 255, 255))
        bg_layer = Layer(Atlas(Sprite(bg_surface)))

        pickle_atlas = PickleAtlas(self)
        pickle_atlas.position = (500, 500)

        self.attached_instances["pickle_atlas"] = pickle_atlas

        bacteria_atlas = BacteriaAtlas(self)
        bacteria_atlas.position = (40, 40)

        entity_layer = Layer(pickle_atlas, bacteria_atlas)

        print(bacteria_atlas.reconstruct_path(bacteria_atlas.a_star_search()))

        self.layer_manager["background"] = bg_layer
        self.layer_manager["map_wall"] = map_wall_layer
        self.layer_manager["entity"] = entity_layer
