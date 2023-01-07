# -*- coding: utf-8 -*-
import logging

import pygame
from pygame import Rect
from typing import Tuple
from core.object_model.Atlas import Atlas
from core.object_model.Sprite import Sprite

class TileType:
    SPACE = 0
    WALL = 1
    EXIT = 2

class TileAtlas(Atlas):
    def __init__(self, tile_type: int, position: Tuple[int, int], block_size: int,
                 *groups: pygame.sprite.AbstractGroup):
        self.__logger = logging.getLogger(self.__class__.__name__)

        tile_surface = pygame.Surface((block_size, block_size))

        if tile_type == TileType.SPACE:
            tile_surface.fill((255, 255, 255))
        elif tile_type == TileType.WALL:
            tile_surface.fill((255, 0, 0))
        elif tile_type == TileType.EXIT:
            tile_surface.fill((0, 255, 0))

        tile_sprite = Sprite(tile_surface, *groups)

        super().__init__(tile_sprite)

        self.__tile_type = tile_type
        self.__block_size = block_size
        self.__nominal_pos_x = position[0]
        self.__nominal_pos_y = position[1]
        self.position_x = self.__nominal_pos_x * block_size
        self.position_y = self.__nominal_pos_y * block_size

        self.rect = pygame.Rect(self.position_x, self.position_y, self.__block_size,
                                self.__block_size)

    @property
    def tile_type(self) -> int:
        return self.__tile_type

    def render(self, surface: pygame.surface.Surface):
        super(TileAtlas, self).render(surface)
        # if self.__tile_type == "1":
            # pygame.draw.rect(surface, (0, 255, 0), self.rect, 5, 1)
