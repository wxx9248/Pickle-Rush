# -*- coding: utf-8 -*-
import typing

import pygame.surface

from core.object_model.Map import Map
from core.object_model.Sprite import Sprite


class TileSprite(Sprite):
    def __init__(self, tile_type: Map.TileType, tile_size: int, sprite: typing.Optional[Sprite] = None):
        surface = pygame.surface.Surface((tile_size, tile_size), pygame.SRCALPHA).convert_alpha()
        if sprite is not None:
            surface = pygame.transform.scale(sprite.surface, (tile_size, tile_size)).convert_alpha()
        super().__init__(surface)
