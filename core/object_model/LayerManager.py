# -*- coding: utf-8 -*-
from __future__ import annotations

import typing

import pygame.surface

from core.object_model.Layer import Layer


class LayerManager:
    def __init__(self):
        self.__layer_dict: typing.Dict[str, Layer] = {}

    def update(self):
        for layer in self.__layer_dict.values():
            layer.update()

    def accept_input_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            [layer.accept_input_event(event) for layer in self.__layer_dict.values()]

    def render(self, surface: pygame.surface.Surface):
        for layer in self.__layer_dict.values():
            layer.render(surface)

    def __setitem__(self, key: str, item: typing.Any):
        self.__layer_dict[key] = item

    def __getitem__(self, key: str):
        item = self.__layer_dict[key]
        return item

    def __repr__(self):
        return repr(self.__layer_dict)

    def __str__(self):
        return str(self.__layer_dict)

    def __len__(self):
        return len(self.__layer_dict)

    def __delitem__(self, key: str):
        del self.__layer_dict[key]

    def __cmp__(self, other: LayerManager):
        return self.__cmp__(other)

    def __contains__(self, item: typing.Any):
        return item in self.__layer_dict

    def __iter__(self):
        return iter(self.__layer_dict)

    def keys(self):
        return self.__layer_dict.keys()

    def values(self):
        return self.__layer_dict.values()

    def items(self):
        return self.__layer_dict.items()
