# -*- coding: utf-8 -*-
from __future__ import annotations

import enum
import typing


class Map:
    class TileType(enum.IntEnum):
        SPACE = 0
        WALL = 1
        EXIT = 2

    def __init__(self, map_file: typing.Optional[str], *args, **kwargs):
        self.__tile_count: typing.List[int] = [0, 0]
        self.__tile_types: typing.List[typing.List[int]] = [[]]

        if map_file is None:
            self.random(kwargs["tile_count"])
            return

        with open(map_file, "r") as f:
            lines = f.read().split('\n')
            self.__tile_types = [
                [Map.TileType(int(type_id)) for type_id in line.strip(',').split(',')]
                for line in lines if line
            ]
            self.__tile_count[0] = len(self.__tile_types[0])
            self.__tile_count[1] = len(self.__tile_types)

    @property
    def tile_count(self) -> typing.Tuple[int, int]:
        return self.__tile_count[0], self.__tile_count[1]

    @property
    def tile_types(self):
        return self.__tile_types

    def random(self, tile_count: typing.Tuple[int, int]):
        raise NotImplementedError()
