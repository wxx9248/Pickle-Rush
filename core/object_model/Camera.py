from typing import Tuple

import pygame

from core.object_model.Atlas import Atlas


class Camera:
    def __init__(self, size: Tuple[int, int], target: Atlas = None,
                 world_size: Tuple[int, int] = None):
        self.__ONLY_TRACK_X = True
        self.__center_pox = pygame.Vector2()
        self.__target: Atlas = target
        self.__size = size
        self.__size_x = size[0] if size else None
        self.__size_y = size[1] if size else None
        self.__world_size = world_size
        self.__world_size_x = world_size[0] if world_size else None
        self.__world_size_y = world_size[1] if world_size else None
        self.__move_boundary_x = None
        self.__move_boundary_y = None
        self.update_move_boundary()

    def get_render_params(self) -> tuple[int, ...]:
        x, y = 0, 0
        if self.__target and self.__world_size:
            x = min(max(int(self.__target.position_x - self.__size_x / 2), 0),
                    self.__move_boundary_x)
            y = min(max(int(self.__target.position_y - self.__size_y / 2), 0),
                    self.__move_boundary_y)
        elif self.__target:
            x = max(int(self.__target.position_x - self.__size_x / 2), 0)
            y = max(int(self.__target.position_y - self.__size_y / 2), 0)
        width, height = self.__size
        if self.ONLY_TRACK_X:
            y = 0
        return tuple([x, y, width, height])

    @property
    def world_size(self):
        return self.world_size

    @world_size.setter
    def world_size(self, val: Tuple[int, int]):
        self.__world_size = val
        self.__world_size_x = val[0]
        self.__world_size_y = val[1]

    def update_move_boundary(self):
        if self.__world_size_x and self.__world_size_y:
            self.__move_boundary_x = self.__world_size_x - self.__size_x
            if self.ONLY_TRACK_X:
                self.__move_boundary_y = 0
            else:
                self.__move_boundary_y = self.__world_size_y - self.__size_y

    @property
    def ONLY_TRACK_X(self):
        return self.__ONLY_TRACK_X

    @ONLY_TRACK_X.setter
    def ONLY_TRACK_X(self, value: bool):
        self.__ONLY_TRACK_X = value
