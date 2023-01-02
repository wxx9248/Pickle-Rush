# -*- coding: utf-8 -*-

from asset.AssetObjectFactory import AssetObjectFactory
from core.Atlas import Atlas
from core.Layer import Layer
from core.Scene import Scene


class Menu(Scene):
    def __init__(self, asset_object_factory: AssetObjectFactory):
        super().__init__()

        logo = asset_object_factory.new_asset_object("asset.text.menu.logo")
        atlas = Atlas()
        atlas["logo"] = logo
        atlas.position = (100, 100)
        atlas.current_sprite_key = "logo"

        layer = Layer(atlas)
        self.layer_manager["menu"] = layer

        # TODO: Atlas: locking mechanism
        # TODO: state machine; add interface to Atlas for accepting state machine events
        # TODO: input handling
