# -*- coding: utf-8 -*-
import typing

import pygame.surface

from core.object_model.Atlas import Atlas
from core.object_model.Map import Map
from core.object_model.Sprite import Sprite
from game.sprite.TileSprite import TileSprite


class MapAtlas(Atlas):
    def __init__(self, map_object: Map):
        self.__map_object = map_object
        self.__tile_sprite_dict: typing.Dict[Map.TileType, Sprite] = {}

        # TODO: Use pictures for tiles instead of TileSprite
        self.__tile_size = 40
        self.__tile_sprite_dict[Map.TileType.SPACE] = TileSprite(Map.TileType.SPACE, self.__tile_size)
        self.__tile_sprite_dict[Map.TileType.WALL] = TileSprite(Map.TileType.WALL, self.__tile_size)
        self.__tile_sprite_dict[Map.TileType.EXIT] = TileSprite(Map.TileType.EXIT, self.__tile_size)

        surface = pygame.surface.Surface(
            (self.__tile_size * map_object.tile_count[0], self.__tile_size * map_object.tile_count[1])).convert_alpha()

        [surface.blit(self.__tile_sprite_dict[tile_type].surface, (i * self.__tile_size, j * self.__tile_size))
         for j, row in enumerate(self.__map_object.tile_types)
         for i, tile_type in enumerate(row)]

        super().__init__(Sprite(surface))

        # Generating masks
        mask_surface = pygame.surface.Surface(surface.get_size(), depth=8)
        mask_surface.set_colorkey(pygame.color.Color("white"))

        tile_mask_surface = pygame.surface.Surface((self.__tile_size, self.__tile_size), depth=8)
        tile_mask_surface.fill(pygame.color.Color("black"))

        mask_surface.fill(pygame.color.Color("white"))
        [mask_surface.blit(tile_mask_surface, (i * self.__tile_size, j * self.__tile_size))
         for j, row in enumerate(self.__map_object.tile_types)
         for i, tile_type in enumerate(row)
         if tile_type == Map.TileType.WALL]
        self.__wall_mask = pygame.mask.from_surface(mask_surface)

        mask_surface.fill(pygame.color.Color("white"))
        [mask_surface.blit(tile_mask_surface, (i * self.__tile_size, j * self.__tile_size))
         for j, row in enumerate(self.__map_object.tile_types)
         for i, tile_type in enumerate(row)
         if tile_type == Map.TileType.EXIT]
        self.__exit_mask = pygame.mask.from_surface(mask_surface)

    @property
    def wall_mask(self):
        return self.__wall_mask

    @property
    def exit_mask(self):
        return self.__exit_mask

    def to_screen_position(self, grid_position: pygame.Vector2) -> pygame.Vector2:
        position = grid_position * self.__tile_size
        position = pygame.Vector2(position.x * self.scale_x, position.y * self.scale_y)
        return position + pygame.Vector2(self.position)
