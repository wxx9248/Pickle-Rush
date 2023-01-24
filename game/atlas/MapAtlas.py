# -*- coding: utf-8 -*-
import typing

import pygame.surface

from core.object_model.Atlas import Atlas
from core.object_model.Map import Map
from core.object_model.Sprite import Sprite
from game.sprite.TileSprite import TileSprite
from util import util


class MapAtlas(Atlas):
    def __init__(self, map_object: Map, tile_size: int = 40, **kwargs):
        self.__map_object = map_object
        self.__tile_sprite_dict: typing.Dict[Map.TileType, Sprite] = {}

        # TODO: Use pictures for tiles instead of TileSprite
        self.__tile_size = tile_size
        self.__tile_sprite_dict[Map.TileType.SPACE] = TileSprite(Map.TileType.SPACE, self.__tile_size)
        self.__tile_sprite_dict[Map.TileType.WALL] = TileSprite(Map.TileType.WALL, self.__tile_size)
        self.__tile_sprite_dict[Map.TileType.EXIT] = TileSprite(Map.TileType.EXIT, self.__tile_size)
        self.__tile_sprite_dict[Map.TileType.DEAD] = TileSprite(Map.TileType.DEAD, self.__tile_size)
        self.__tile_sprite_dict[Map.TileType.START] = TileSprite(Map.TileType.START, self.__tile_size)

        surface = pygame.surface.Surface(
            (self.__tile_size * map_object.tile_count[1],
             self.__tile_size * map_object.tile_count[0])).convert_alpha()

        [surface.blit(self.__tile_sprite_dict[tile_type].surface,
                      (j * self.__tile_size, i * self.__tile_size))
         for i, row in enumerate(self.__map_object.tile_types)
         for j, tile_type in enumerate(row)]

        super().__init__(Sprite(surface), **kwargs)

        # Generating masks
        mask_surface = pygame.surface.Surface(surface.get_size(), depth=8)
        mask_surface.set_colorkey(pygame.color.Color("white"))

        tile_mask_surface = pygame.surface.Surface((self.__tile_size, self.__tile_size), depth=8)
        tile_mask_surface.fill(pygame.color.Color("black"))

        mask_surface.fill(pygame.color.Color("white"))
        [mask_surface.blit(tile_mask_surface, (j * self.__tile_size, i * self.__tile_size))
         for i, row in enumerate(self.__map_object.tile_types)
         for j, tile_type in enumerate(row)
         if tile_type == Map.TileType.WALL]
        self.__wall_mask = pygame.mask.from_surface(mask_surface)

        mask_surface.fill(pygame.color.Color("white"))
        [mask_surface.blit(tile_mask_surface, (j * self.__tile_size, i * self.__tile_size))
         for i, row in enumerate(self.__map_object.tile_types)
         for j, tile_type in enumerate(row)
         if tile_type == Map.TileType.EXIT]
        self.__exit_mask = pygame.mask.from_surface(mask_surface)

        mask_surface.fill(pygame.color.Color("white"))
        [mask_surface.blit(tile_mask_surface, (j * self.__tile_size, i * self.__tile_size))
         for i, row in enumerate(self.__map_object.tile_types)
         for j, tile_type in enumerate(row)
         if tile_type == Map.TileType.DEAD]
        self.__dead_mask = pygame.mask.from_surface(mask_surface)

    @property
    def map_object(self):
        return self.__map_object

    @property
    def wall_mask(self):
        return self.__wall_mask

    @property
    def exit_mask(self):
        return self.__exit_mask

    @property
    def dead_mask(self):
        return self.__dead_mask

    # for debug use only
    def render(self, surface: pygame.surface.Surface):
        super().render(surface)
        if self.SHOW_COLLIDE_BODY:
            c_comp = self.wall_mask.connected_components()
            for comp in c_comp:
                outline = comp.outline(10)
                outline = [(t[0] + self.position_x, t[1] + self.position_y) for t in outline]
                pygame.draw.lines(surface, (0, 0, 255), True, outline, 3)

    def grid_to_screen_position(self, grid_position: pygame.Vector2,
                                element_size: typing.Optional[
                                    typing.Tuple[int, int]]) -> pygame.Vector2:
        position = grid_position * self.__tile_size
        position = pygame.Vector2(position.x * self.scale_x, position.y * self.scale_y)
        if element_size:
            position += pygame.Vector2(
                util.center((self.__tile_size, self.__tile_size), element_size))
        position = pygame.Vector2(position.y, position.x)
        position += pygame.Vector2(self.position)
        return position

    def screen_to_grid_position(self, screen_position: pygame.Vector2,
                                element_size: typing.Optional[
                                    typing.Tuple[int, int]]) -> pygame.Vector2:
        position = screen_position - pygame.Vector2(self.position)
        position = pygame.Vector2(position.y, position.x)
        position = pygame.Vector2(position.x / self.scale_x, position.y / self.scale_y)
        if element_size:
            position -= pygame.Vector2(
                util.center((self.__tile_size, self.__tile_size), element_size))
        position /= self.__tile_size
        return position
