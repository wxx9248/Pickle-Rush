# -*- coding: utf-8 -*-
import typing

from asset.AssetObjectFactory import AssetObjectFactory
from core.object_model.Atlas import Atlas
from core.object_model.Layer import Layer
from core.object_model.Scene import Scene
from core.object_model.Text import Text
from util import util


class Menu(Scene):
    def __init__(self, size: typing.Tuple[int, int], asset_object_factory: AssetObjectFactory):
        super().__init__(size)

        logo_text: Text = asset_object_factory.new_asset_object("asset.text.menu.logo")
        logo_atlas = Atlas()
        logo_atlas["logo"] = logo_text
        logo_atlas.position_x = util.center(self.size, logo_text.surface.get_size())[0]
        logo_atlas.position_y = 150
        logo_atlas.current_sprite_key = "logo"

        start_text: Text = asset_object_factory.new_asset_object("asset.text.menu.start")
        start_text_atlas = Atlas()
        start_text_atlas["start"] = start_text
        start_text_atlas.position_x = util.center(self.size, start_text.surface.get_size())[0]
        start_text_atlas.position_y = 450
        start_text_atlas.current_sprite_key = "start"

        exit_text: Text = asset_object_factory.new_asset_object("asset.text.menu.exit")
        exit_text_atlas = Atlas()
        exit_text_atlas["exit"] = exit_text
        exit_text_atlas.position_x = util.center(self.size, exit_text.surface.get_size())[0]
        exit_text_atlas.position_y = 550
        exit_text_atlas.current_sprite_key = "exit"

        layer = Layer(logo_atlas, start_text_atlas, exit_text_atlas)
        self.layer_manager["menu"] = layer
