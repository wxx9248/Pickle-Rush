# -*- coding: utf-8 -*-
import typing

import pygame

from asset.AssetObjectFactory import AssetObjectFactory
from core.object_model.Atlas import Atlas
from core.object_model.Layer import Layer
from core.object_model.Scene import Scene
from core.object_model.Sprite import Sprite
from core.object_model.Text import Text
from event.CustomEventTypes import CustomEventTypes
from game.scene import Menu
from util import util


class Help(Scene):
    def __init__(self, size: typing.Tuple[int, int]):
        super().__init__(size)

        asset_object_factory = AssetObjectFactory()

        self.background = Atlas(asset_object_factory.new_asset_object("asset.sprite.menu.background"))
        self.background.scale_to(size)

        back_text: Text = asset_object_factory.new_asset_object("asset.text.help.back-hint")
        back_text_atlas = Atlas(back_text)

        help_manual_sprite: Sprite = asset_object_factory.new_asset_object("asset.sprite.help-manual")
        help_manual_atlas = Atlas(help_manual_sprite)
        help_manual_atlas.scale = (0.6, 0.6)
        help_manual_atlas.position = util.center(self.size, help_manual_atlas.surface.get_size())

        layer = Layer(back_text_atlas, help_manual_atlas)
        self.layer_manager["help"] = layer

    def back_to_menu(self):
        event = pygame.event.Event(CustomEventTypes.EVENT_STAGE_CHANGE_SCENE_REQUEST)
        event.scene = Menu.Menu(self.size)
        pygame.event.post(event)

    def accept_event(self, event: pygame.event.Event):
        super().accept_event(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.back_to_menu()
