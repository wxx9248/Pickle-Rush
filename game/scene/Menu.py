# -*- coding: utf-8 -*-
import typing

from asset.AssetObjectFactory import AssetObjectFactory
from core.Atlas import Atlas
from core.Layer import Layer
from core.Scene import Scene


class Menu(Scene):
    def __init__(self, size: typing.Tuple[int, int], asset_object_factory: AssetObjectFactory):
        super().__init__(size)

        logo = asset_object_factory.new_asset_object("asset.text.menu.logo")
        atlas = Atlas()
        atlas["logo"] = logo
        atlas.position = (100, 100)
        atlas.current_sprite_key = "logo"

        layer = Layer(atlas)
        self.layer_manager["menu"] = layer
