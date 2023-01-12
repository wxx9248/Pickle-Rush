import pygame
from core.object_model.Atlas import Atlas
from typing import Tuple


class Camera:
    def __init__(self, size: Tuple[int, int], target: Atlas = None):
        self.__ONLY_TRACK_X = True
        self.__center_pox = pygame.Vector2()
        self.__target: Atlas = target
        self.__size = size
        self.__size_x = size[0]
        self.__size_y = size[1]

    def get_render_params(self) -> tuple[int, ...]:
        x = int(self.__target.position_x - self.__size_x / 2)
        y = int(self.__target.position_y - self.__size_y / 2)
        width, height = self.__size
        if self.ONLY_TRACK_X:
            y = 0
        return tuple([x, y, width, height])

    @property
    def ONLY_TRACK_X(self):
        return self.__ONLY_TRACK_X

    @ONLY_TRACK_X.setter
    def ONLY_TRACK_X(self, value: bool):
        self.__ONLY_TRACK_X = value
