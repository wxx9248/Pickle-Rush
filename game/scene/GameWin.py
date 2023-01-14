# -*- coding: utf-8 -*-
import typing

import pygame

from asset.AssetObjectFactory import AssetObjectFactory
from core.object_model.Atlas import Atlas
from core.object_model.Layer import Layer
from core.object_model.Scene import Scene
from core.object_model.Text import Text
from event.CustomEventTypes import CustomEventTypes
from game.atlas.MenuSelectorAtlas import MenuSelectorAtlas
from util import util


class GameWin(Scene):
    def __init__(self, size: typing.Tuple[int, int], next_level_scene: typing.Optional[typing.Type[Scene]]):
        super().__init__(size)
        self.__next_level_scene = next_level_scene

        game_win_text_sprite: Text = AssetObjectFactory().new_asset_object("asset.text.game-win")
        game_win_text_atlas = Atlas(game_win_text_sprite)
        game_win_text_atlas.position_x = util.center(self.size, game_win_text_sprite.surface.get_size())[0]
        game_win_text_atlas.position_y = 150

        next_level_text_sprite: Text = AssetObjectFactory().new_asset_object("asset.text.next-level")
        next_level_text_atlas = Atlas(next_level_text_sprite)
        next_level_text_atlas.position = util.center(self.size, next_level_text_sprite.surface.get_size())[0]
        next_level_text_atlas.position_y = 500

        cursor_sprite_atlas = MenuSelectorAtlas()
        cursor_sprite_atlas.position_x = 450
        cursor_sprite_atlas.add_anchor(
            (next_level_text_atlas.position_y - 6, lambda: self.to_next_level()),
        )

        layer = Layer(game_win_text_atlas)
        if next_level_scene:
            layer.add_atlas(next_level_text_atlas)
            layer.add_atlas(cursor_sprite_atlas)

        self.layer_manager["default"] = layer

    def to_next_level(self):
        event = pygame.event.Event(CustomEventTypes.EVENT_STAGE_CHANGE_SCENE_REQUEST)
        event.scene = self.__next_level_scene(self.size)
        pygame.event.post(event)
