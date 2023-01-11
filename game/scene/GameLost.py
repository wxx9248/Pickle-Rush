# -*- coding: utf-8 -*-
import typing

import pygame.event

from asset.AssetObjectFactory import AssetObjectFactory
from core.object_model.Atlas import Atlas
from core.object_model.Layer import Layer
from core.object_model.Scene import Scene
from core.object_model.Text import Text
from event.CustomEventTypes import CustomEventTypes
from game.atlas.MenuSelectorAtlas import MenuSelectorAtlas
from util import util


class GameLost(Scene):
    def __init__(self, size: typing.Tuple[int, int]):
        super().__init__(size)

        # Initialize sprites
        text_sprite: Text = AssetObjectFactory().new_asset_object("asset.text.gamelost.text")
        text_atlas = Atlas(text_sprite)
        text_atlas.position_x = util.center(self.size, text_sprite.surface.get_size())[0]
        text_atlas.position_y = 150

        layer = Layer(text_atlas)
        self.layer_manager["default"] = layer
