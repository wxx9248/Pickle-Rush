# -*- coding: utf-8 -*-
import typing

from asset.AssetObjectFactory import AssetObjectFactory
from core.object_model.Atlas import Atlas
from core.object_model.Layer import Layer
from core.object_model.Scene import Scene
from game.atlas.PickleAtlas import PickleAtlas


class Test(Scene):
    def __init__(self, size: typing.Tuple[int, int], asset_object_factory: AssetObjectFactory):
        super().__init__(size, asset_object_factory)

        pickle_sprite_0 = asset_object_factory.new_asset_object("asset.sprite.pickle.0")
        pickle_sprite_1 = asset_object_factory.new_asset_object("asset.sprite.pickle.1")
        pickle_sprite_2 = asset_object_factory.new_asset_object("asset.sprite.pickle.2")

        self.logo_atlas = PickleAtlas()
        self.logo_atlas.scale = (0.5, 0.5)
        self.logo_atlas.opacity = 100
        self.logo_atlas["pickle-0"] = pickle_sprite_0
        self.logo_atlas["pickle-1"] = pickle_sprite_1
        self.logo_atlas["pickle-2"] = pickle_sprite_2
        self.logo_atlas.current_sprite_key = "pickle-0"

        layer = Layer(self.logo_atlas)

        self.layer_manager["test"] = layer

        self.counter = 0

    def update(self):
        self.logo_atlas.current_sprite_key = f"pickle-{self.counter}"
        self.counter += 1
        self.counter %= 3
