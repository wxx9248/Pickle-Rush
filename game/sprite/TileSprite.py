# -*- coding: utf-8 -*-
import pygame.surface

from core.object_model.Map import Map
from core.object_model.Sprite import Sprite


class TileSprite(Sprite):
    def __init__(self, tile_type: Map.TileType, tile_size: int):
        surface = pygame.surface.Surface((tile_size, tile_size)).convert_alpha()
        if tile_type == Map.TileType.SPACE:
            surface.fill(pygame.color.Color("white"))
        elif tile_type == Map.TileType.WALL:
            surface.fill(pygame.color.Color("red"))
        elif tile_type == Map.TileType.EXIT:
            surface.fill(pygame.color.Color("green"))
        elif tile_type == Map.TileType.START:
            surface.fill(pygame.color.Color("blue"))
        super().__init__(surface)
