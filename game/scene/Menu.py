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
from game.scene.Test import Test
from util import util


class Menu(Scene):
    def __init__(self, size: typing.Tuple[int, int]):
        super().__init__(size)

        asset_object_factory = AssetObjectFactory()

        # Initialize sprites
        logo_text_sprite: Text = asset_object_factory.new_asset_object("asset.text.menu.logo")
        logo_atlas = Atlas(logo_text_sprite)
        logo_atlas.position_x = util.center(self.size, logo_text_sprite.surface.get_size())[0]
        logo_atlas.position_y = 150

        start_text_sprite: Text = asset_object_factory.new_asset_object("asset.text.menu.start")
        start_text_atlas = Atlas(start_text_sprite)
        start_text_atlas.position_x = util.center(self.size, start_text_sprite.surface.get_size())[0]
        start_text_atlas.position_y = 450

        exit_text_sprite: Text = asset_object_factory.new_asset_object("asset.text.menu.exit")
        exit_text_atlas = Atlas(exit_text_sprite)
        exit_text_atlas.position_x = util.center(self.size, exit_text_sprite.surface.get_size())[0]
        exit_text_atlas.position_y = 550

        cursor_sprite_atlas = MenuSelectorAtlas()
        cursor_sprite_atlas.position_x = 500
        cursor_sprite_atlas.add_anchor(
            (start_text_atlas.position_y - 6, lambda: self.start_game_handler()),
            (exit_text_atlas.position_y - 6, lambda: pygame.event.post(pygame.event.Event(pygame.QUIT)))
        )

        layer = Layer(logo_atlas, start_text_atlas, exit_text_atlas, cursor_sprite_atlas)
        self.layer_manager["menu"] = layer

    def start_game_handler(self):
        event = pygame.event.Event(CustomEventTypes.EVENT_STAGE_CHANGE_SCENE_REQUEST)
        event.scene = Test(self.size)
        pygame.event.post(event)
