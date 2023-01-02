# -*- coding: utf-8 -*-
from __future__ import annotations

import typing

import pygame

from core.Sprite import Sprite


class Atlas:
    MOVEMENT_UNIT = 1

    def __init__(self):
        self.__sprite_dict: typing.Dict[str, Sprite] = {}
        self.__current_sprite: typing.Optional[Sprite] = None
        self.__current_sprite_key: typing.Optional[str] = None
        self.__position: typing.List[int, int] = [0, 0]
        self.__speed = pygame.Vector2(0, 0)
        self.__acceleration = pygame.Vector2(0, 0)

    @property
    def position(self) -> typing.Tuple[int, int]:
        return self.__position[0], self.__position[1]

    @position.setter
    def position(self, value: typing.Tuple[int, int]):
        self.__position[0] = value[0]
        self.__position[1] = value[1]

    @property
    def speed(self) -> typing.Tuple[float, float]:
        return self.__speed.x, self.__speed.y

    @speed.setter
    def speed(self, value: typing.Tuple[float, float]):
        self.__speed.update(value)

    @property
    def acceleration(self):
        return self.__acceleration.x, self.__acceleration.y

    @acceleration.setter
    def acceleration(self, value: typing.Tuple[float, float]):
        self.__acceleration.update(value)

    @property
    def current_sprite_key(self) -> typing.Optional[str]:
        return self.__current_sprite_key

    @current_sprite_key.setter
    def current_sprite_key(self, value: typing.Optional[str]):
        self.__current_sprite_key = value
        if self.__current_sprite_key is None:
            self.__current_sprite = None
            return
        self.__current_sprite = self.__sprite_dict[self.__current_sprite_key]

    def render(self, surface: pygame.surface.Surface):
        if self.__current_sprite is None:
            return
        surface.blit(self.__current_sprite.surface, self.__position)

    def update(self):
        pass

    def __setitem__(self, key: str, item: typing.Any):
        self.__sprite_dict[key] = item

    def __getitem__(self, key: str):
        item = self.__sprite_dict[key]
        return item

    def __repr__(self):
        return repr(self.__sprite_dict)

    def __str__(self):
        return str(self.__sprite_dict)

    def __len__(self):
        return len(self.__sprite_dict)

    def __delitem__(self, key: str):
        del self.__sprite_dict[key]

    def __cmp__(self, other: Atlas):
        return self.__cmp__(other)

    def __contains__(self, item: typing.Any):
        return item in self.__sprite_dict

    def __iter__(self):
        return iter(self.__sprite_dict)

    def keys(self):
        return self.__sprite_dict.keys()

    def values(self):
        return self.__sprite_dict.values()

    def items(self):
        return self.__sprite_dict.items()
