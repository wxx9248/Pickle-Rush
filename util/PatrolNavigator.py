from typing import Tuple

import pygame

from core.object_model.Atlas import Atlas
from game.atlas.MapAtlas import MapAtlas


class PatrolNavigator:
    def __init__(self, source_atlas: Atlas, map_atlas: MapAtlas, patrol_x_grid_range: Tuple[int, int]):
        self.__source_atlas = source_atlas
        self.__map_atlas = map_atlas
        self.__x_range = patrol_x_grid_range
        self.__direction_vector = pygame.Vector2(1, 0)
        self.__source_grid_position = (0, 0)
        self.__source_grid_index = (0, 0)
        self.update_position()

    @property
    def direction_vector(self):
        return self.__direction_vector

    def update_position(self):
        self.__source_grid_position = \
            self.__map_atlas.screen_to_grid_position(
                pygame.Vector2(self.__source_atlas.position),
                self.__source_atlas.surface.get_size()
            )
        self.__source_grid_index = (
            round(self.__source_grid_position.x), round(self.__source_grid_position.y))

    def update(self):
        self.update_position()
        if self.__x_range[0] < self.__source_grid_position[1] < self.__x_range[1]:
            pass
        else:
            self.__direction_vector = - self.__direction_vector
