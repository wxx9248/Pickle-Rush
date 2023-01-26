# -*- coding: utf-8 -*-
import typing

import pygame.event

from asset.AssetObjectFactory import AssetObjectFactory
from core.object_model.Atlas import Atlas
from core.object_model.Layer import Layer
from core.object_model.Scene import Scene
from core.object_model.Sprite import Sprite
from event.CustomEventTypes import CustomEventTypes
from game.atlas.MenuSelectorAtlas import MenuSelectorAtlas
from game.scene import Menu
from util import util


class GameLost(Scene):
    def __init__(self, size: typing.Tuple[int, int], retry_scene: typing.Optional[typing.Type[Scene]]):
        super().__init__(size)
        self.__retry_scene = retry_scene

        self.background = Atlas(AssetObjectFactory().new_asset_object("asset.sprite.menu.background"))
        self.background.scale_to(size)

        game_lost_text_sprite: Sprite = AssetObjectFactory().new_asset_object("asset.sprite.game-lost")
        game_lost_text_atlas = Atlas(game_lost_text_sprite)
        game_lost_text_atlas.position_x = util.center(self.size, game_lost_text_atlas.surface.get_size())[0]
        game_lost_text_atlas.position_y = 100

        retry_text_sprite: Sprite = AssetObjectFactory().new_asset_object("asset.sprite.retry")
        retry_text_atlas = Atlas(retry_text_sprite)
        retry_text_atlas.scale = (0.6, 0.6)
        retry_text_atlas.position_x = util.center(self.size, retry_text_atlas.surface.get_size())[0]
        retry_text_atlas.position_y = 450

        back_to_menu_text_sprite: Sprite = AssetObjectFactory().new_asset_object("asset.sprite.back-to-menu")
        back_to_menu_text_atlas = Atlas(back_to_menu_text_sprite)
        back_to_menu_text_atlas.scale = (0.6, 0.6)
        back_to_menu_text_atlas.position_x = util.center(self.size, back_to_menu_text_atlas.surface.get_size())[0]
        back_to_menu_text_atlas.position_y = 550

        cursor_sprite_atlas = MenuSelectorAtlas()
        cursor_sprite_atlas.scale = (0.04, 0.04)
        cursor_sprite_atlas.position_x = 400
        cursor_sprite_atlas.add_anchor(
            (retry_text_atlas.position_y - 6, lambda: self.retry()),
            (back_to_menu_text_atlas.position_y + 4, lambda: self.back_to_menu())
        )

        layer = Layer(game_lost_text_atlas, retry_text_atlas, back_to_menu_text_atlas, cursor_sprite_atlas)
        self.layer_manager["default"] = layer

    def retry(self):
        event = pygame.event.Event(CustomEventTypes.EVENT_STAGE_CHANGE_SCENE_REQUEST)
        event.scene = self.__retry_scene(self.size)
        pygame.event.post(event)

    def back_to_menu(self):
        event = pygame.event.Event(CustomEventTypes.EVENT_STAGE_CHANGE_SCENE_REQUEST)
        event.scene = Menu.Menu(self.size)
        pygame.event.post(event)
