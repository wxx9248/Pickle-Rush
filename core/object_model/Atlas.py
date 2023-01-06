# -*- coding: utf-8 -*-
from __future__ import annotations

import typing

import pygame

from core.object_model.Sprite import Sprite


class Atlas:
    def __init__(self, default_sprite: typing.Optional[Sprite] = None):
        self.__sprite_dict: typing.Dict[str, Sprite] = {}
        self.__cached_sprite_surfaces: typing.Dict[str, pygame.surface.Surface] = {}
        self.__current_sprite_key: typing.Optional[str] = None

        self.__position = pygame.Vector2(0, 0)
        self.__speed = pygame.Vector2(0, 0)
        self.__acceleration = pygame.Vector2(0, 0)
        self.__opacity: int = 255
        self.__scale = pygame.Vector2(1, 1)

        if default_sprite is not None:
            self["default"] = default_sprite
            self.current_sprite_key = "default"

    @property
    def position(self) -> typing.Tuple[float, float]:
        return self.__position.x, self.__position.y

    @property
    def position_int(self) -> typing.Tuple[int, int]:
        return int(self.__position.x), int(self.__position.y)

    @position.setter
    def position(self, value: typing.Tuple[float, float]):
        self.__position.update(value)

    @property
    def position_x(self) -> float:
        return self.__position.x

    @position_x.setter
    def position_x(self, value: float):
        self.__position.x = value

    @property
    def position_y(self) -> float:
        return self.__position.y

    @position_y.setter
    def position_y(self, value: float):
        self.__position.y = value

    @property
    def speed(self) -> typing.Tuple[float, float]:
        return self.__speed.x, self.__speed.y

    @speed.setter
    def speed(self, value: typing.Tuple[float, float]):
        self.__speed.update(value)

    @property
    def speed_x(self) -> float:
        return self.__speed.x

    @speed_x.setter
    def speed_x(self, value: float):
        self.__speed.x = value

    @property
    def speed_y(self) -> float:
        return self.__speed.y

    @speed_y.setter
    def speed_y(self, value: float):
        self.__speed.y = value

    @property
    def acceleration(self):
        return self.__acceleration.x, self.__acceleration.y

    @acceleration.setter
    def acceleration(self, value: typing.Tuple[float, float]):
        self.__acceleration.update(value)

    @property
    def acceleration_x(self) -> float:
        return self.__acceleration.x

    @acceleration_x.setter
    def acceleration_x(self, value: float):
        self.__acceleration.x = value

    @property
    def acceleration_y(self) -> float:
        return self.__acceleration.y

    @acceleration_y.setter
    def acceleration_y(self, value: float):
        self.__acceleration.y = value

    @property
    def opacity(self):
        return self.__opacity

    @opacity.setter
    def opacity(self, value: int):
        if value > 255:
            value = 255
        if value < 0:
            value = 0
        self.__opacity = value
        self.update_surface_cache_opacity()

    @property
    def scale(self):
        return self.__scale.x, self.__scale.y

    @scale.setter
    def scale(self, value: typing.Tuple[float, float]):
        self.__scale.update(value)
        self.update_surface_cache_scale()

    @property
    def scale_x(self) -> float:
        return self.__scale.x

    @scale_x.setter
    def scale_x(self, value: float):
        self.__scale.x = value
        self.update_surface_cache_scale()

    @property
    def scale_y(self) -> float:
        return self.__scale.y

    @scale_y.setter
    def scale_y(self, value: float):
        self.__scale.y = value
        self.update_surface_cache_scale()

    @property
    def current_sprite_key(self) -> typing.Optional[str]:
        return self.__current_sprite_key

    @current_sprite_key.setter
    def current_sprite_key(self, value: typing.Optional[str]):
        self.__current_sprite_key = value
        if self.__current_sprite_key is None:
            self.__current_sprite_surface = None
            return
        self.__current_sprite_surface = self.__cached_sprite_surfaces[self.__current_sprite_key]

    def update_surface_cache_scale(self, key: typing.Optional[str] = None):
        iterable = self.__sprite_dict
        if key is not None:
            iterable = {key: self.__sprite_dict[key]}

        for key, sprite in iterable.items():
            self.__cached_sprite_surfaces[key] = pygame.transform.scale(
                sprite.surface,
                (self.__scale.x * sprite.surface.get_width(), self.__scale.y * sprite.surface.get_height())
            )

    def update_surface_cache_opacity(self, key: typing.Optional[str] = None):
        iterable = self.__cached_sprite_surfaces.values()
        if key is not None:
            iterable = [self.__cached_sprite_surfaces[key]]

        for sprite in iterable:
            sprite.set_alpha(self.__opacity)

    def update_surface_cache(self, key: typing.Optional[str] = None):
        self.update_surface_cache_scale(key)
        self.update_surface_cache_opacity(key)

    def render(self, surface: pygame.surface.Surface):
        if self.__current_sprite_surface is None:
            return
        self.__speed += self.__acceleration
        self.__position += self.__speed

        surface.blit(self.__current_sprite_surface, self.position_int)

    def update(self):
        pass

    def accept_input_event(self, event: pygame.event.Event):
        pass

    def __setitem__(self, key: str, item: Sprite):
        self.__sprite_dict[key] = item
        self.update_surface_cache(key)

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
        del self.__cached_sprite_surfaces[key]
        if self.__current_sprite_key == key:
            self.current_sprite_key = None

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
