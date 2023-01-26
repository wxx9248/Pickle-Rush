# -*- coding: utf-8 -*-
import typing

import pygame.event

from asset.AssetObjectFactory import AssetObjectFactory
from core.object_model.Atlas import Atlas
from core.object_model.Layer import Layer
from core.object_model.Scene import Scene
from core.object_model.Sprite import Sprite
from core.object_model.Text import Text
from event.CustomEventTypes import CustomEventTypes
from game.atlas.MenuSelectorAtlas import MenuSelectorAtlas
from game.scene.GameLost import GameLost
from game.scene.GameWin import GameWin
from game.scene.Level0 import Level0
from game.scene.Level1 import Level1
from game.scene.Level2 import Level2
from util import util


class Menu(Scene):
    def __init__(self, size: typing.Tuple[int, int]):
        super().__init__(size)

        asset_object_factory = AssetObjectFactory()

        self.background = Atlas(asset_object_factory.new_asset_object("asset.sprite.menu.background"))
        self.background.scale_to(size)

        # Initialize sprites
        logo_text_sprite: Sprite = asset_object_factory.new_asset_object("asset.sprite.menu.logo")
        logo_atlas = Atlas(logo_text_sprite)
        logo_atlas.position_x = util.center(self.size, logo_atlas.surface.get_size())[0]
        logo_atlas.position_y = 100

        start_text_sprite: Sprite = asset_object_factory.new_asset_object("asset.sprite.menu.start")
        start_text_atlas = Atlas(start_text_sprite)
        start_text_atlas.scale = (0.8, 0.8)
        start_text_atlas.position_x = util.center(self.size, start_text_atlas.surface.get_size())[0]
        start_text_atlas.position_y = 425

        exit_text_sprite: Sprite = asset_object_factory.new_asset_object("asset.sprite.menu.exit")
        exit_text_atlas = Atlas(exit_text_sprite)
        exit_text_atlas.scale = (0.8, 0.8)
        exit_text_atlas.position_x = util.center(self.size, exit_text_atlas.surface.get_size())[0]
        exit_text_atlas.position_y = 525

        cursor_sprite_atlas = MenuSelectorAtlas()
        cursor_sprite_atlas.scale = (0.04, 0.04)
        cursor_sprite_atlas.position_x = 475
        cursor_sprite_atlas.add_anchor(
            (start_text_atlas.position_y + 7, lambda: self.start_game()),
            (exit_text_atlas.position_y + 7, lambda: pygame.event.post(pygame.event.Event(pygame.QUIT)))
        )

        layer = Layer(logo_atlas, start_text_atlas, exit_text_atlas, cursor_sprite_atlas)
        self.layer_manager["menu"] = layer

    def start_game(self):
        event = pygame.event.Event(CustomEventTypes.EVENT_STAGE_CHANGE_SCENE_REQUEST)
        event.scene = Level1(self.size)
        pygame.event.post(event)
