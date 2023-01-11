# -*- coding: utf-8 -*-
import typing

import pygame

from asset.AssetObjectFactory import AssetObjectFactory
from core.object_model.Atlas import Atlas
from core.object_model.Sprite import Sprite

AnchorType: typing.TypeAlias = typing.Tuple[float, typing.Callable]


class MenuSelectorAtlas(Atlas):
    def __init__(self):
        super().__init__(AssetObjectFactory().new_asset_object("asset.text.menu.cursor"))
        self.__anchors: typing.List[AnchorType] = []
        self.__current_anchor_index = -1

    def add_anchor(self, *anchors: AnchorType):
        self.__anchors.extend(anchors)
        if len(self.__anchors) and self.__current_anchor_index < 0:
            self.__current_anchor_index = 0

    def render(self, surface: pygame.surface.Surface):
        if self.__current_anchor_index < 0:
            return
        super().render(surface)

    def update(self):
        super().update()
        if self.__current_anchor_index < 0:
            return
        self.position_y = self.__anchors[self.__current_anchor_index][0]

    def accept_event(self, event: pygame.event.Event):
        if self.__current_anchor_index < 0:
            return

        if event.key == pygame.K_RETURN:
            self.__anchors[self.__current_anchor_index][1]()

        if event.key == pygame.K_UP and self.__current_anchor_index > 0:
            self.__current_anchor_index -= 1
        elif event.key == pygame.K_DOWN and self.__current_anchor_index < len(self.__anchors) - 1:
            self.__current_anchor_index += 1
