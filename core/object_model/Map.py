# -*- coding: utf-8 -*-
from __future__ import annotations

import enum
import random
import typing

import pygame

from util import util
from util.BSPTree import BSPTree
from util.PriorityQueue import PriorityQueue


class Map:
    class TileType(enum.IntEnum):
        SPACE = 0
        WALL = 1
        EXIT = 2
        DEAD = 3
        START = 4

    def __init__(self, map_file: typing.Optional[str], *args, **kwargs):
        self.__tile_count: typing.List[int] = [0, 0]
        self.__tile_types: typing.List[typing.List[int]] = [[]]
        self.__start_point: typing.Tuple[int, int] = (0, 0)
        self.__exit_point: typing.Tuple[int, int] = (0, 0)

        if map_file is None:
            self.random(kwargs["tile_count"])
            return

        with open(map_file, "r") as f:
            lines = f.read().split('\n')
            self.__tile_types = [
                [Map.TileType(int(type_id)) for type_id in line.strip(',').split(',')]
                for line in lines if line
            ]
            self.__tile_count[0] = len(self.__tile_types)
            self.__tile_count[1] = len(self.__tile_types[0])

            for i in range(self.__tile_count[0]):
                for j in range(self.__tile_count[1]):
                    if self.__tile_types[i][j] == Map.TileType.START:
                        self.__start_point = (i, j)
                    if self.__tile_types[i][j] == Map.TileType.EXIT:
                        self.__exit_point = (i, j)

    @property
    def tile_count(self) -> typing.Tuple[int, int]:
        return self.__tile_count[0], self.__tile_count[1]

    @property
    def tile_types(self):
        return self.__tile_types

    @property
    def start_point(self):
        return self.__start_point

    @property
    def exit_point(self):
        return self.__exit_point

    def random(self, tile_count: typing.Tuple[int, int]):
        self.__tile_count = list(tile_count)
        self.bsp_random()
        self.set_wall()
        self.set_terminals()
        self.make_paths()

    def bsp_random(self):
        bsp_tree = BSPTree(pygame.Rect((0, 0), (self.__tile_count[1], self.__tile_count[0])))
        bsp_tree.random()
        bsp_tree.generate_rooms()
        self.__tile_types = bsp_tree.to_map_tiles()

    def set_wall(self):
        (height, width) = (self.__tile_count[0], self.__tile_count[1])
        candidates = [(i, j)
                      for i in range(height)
                      for j in range(width)
                      if i * j * (height - i - 1) * (width - j - 1) == 0]
        for (i, j) in candidates:
            self.__tile_types[i][j] = Map.TileType.WALL

    def set_terminals(self):
        (height, width) = (self.__tile_count[0], self.__tile_count[1])

        # Set starting point
        self.__start_point = (height // 2, width // 2)
        self.__tile_types[self.__start_point[0]][self.__start_point[1]] = Map.TileType.START

        # Set exit
        candidates = {(i, j)
                      for i in range(height)
                      for j in range(width)
                      if i * j * (height - i - 1) * (width - j - 1) == 0
                      and (i * (height - i - 1) != 0 or j * (width - j - 1) != 0)}

        while True:
            # No blocker before the exit tile
            (i, j) = random.choice(list(candidates))
            if i == 0 and self.__tile_types[i + 1][j] == Map.TileType.WALL \
                    or j == 0 and self.__tile_types[i][j + 1] == Map.TileType.WALL \
                    or (height - i - 1) == 0 and self.__tile_types[i - 1][j] == Map.TileType.WALL \
                    or (width - j - 1) == 0 and self.__tile_types[i][j - 1] == Map.TileType.WALL:
                candidates.remove((i, j))
            else:
                break

        self.__tile_types[i][j] = Map.TileType.EXIT
        self.__exit_point = (i, j)

    def make_paths(self):
        (height, width) = (self.__tile_count[0], self.__tile_count[1])
        candidates = [(1, 1), (1, width - 2), (height - 2, 1), (height - 2, width - 2), self.__exit_point]

        # Check connectivity: Dijkstra
        dijkstra_map = self.generate_dijkstra_map()
        unreachable_points = [candidate for candidate in candidates if dijkstra_map[candidate[0]][candidate[1]] is None]
        [self.make_path(self.__start_point, point, point == self.__exit_point) for point in unreachable_points]

    def make_path(self, start: typing.Tuple[int, int], end: typing.Tuple[int, int], end_on_border: bool = False):
        stack = [start]
        visited = {start}
        while len(stack):
            point = stack[-1]
            if point == end:
                break

            neighbors = set(util.neighbor_points(point, self.__tile_count[0], self.__tile_count[1]))
            unvisited_neighbors = neighbors - visited
            if len(unvisited_neighbors) == 0:
                stack.pop()
                continue

            if end_on_border and end in util.extended_neighbor_points(point):
                break

            neighbor = min(unvisited_neighbors, key=lambda p: util.point_distance_squared(p, end))

            if self.__tile_types[neighbor[0]][neighbor[1]] != Map.TileType.START \
                    or self.__tile_types[neighbor[0]][neighbor[1]] != Map.TileType.SPACE:
                self.__tile_types[neighbor[0]][neighbor[1]] = Map.TileType.SPACE

            stack.append(neighbor)
            visited.add(neighbor)

    def generate_dijkstra_map(self, root: typing.Optional[typing.Tuple[int, int]] = None) \
            -> typing.List[typing.List[typing.Optional[int]]]:
        if root is None:
            root = self.__start_point

        dijkstra_map: typing.List[typing.List[typing.Optional[int]]] = [[None for _ in row]
                                                                        for row in self.__tile_types]
        dijkstra_map[root[0]][root[1]] = 0

        frontier = PriorityQueue()
        frontier.push(root, dijkstra_map[root[0]][root[1]])
        while not frontier.empty():
            value, point = frontier.pop()
            neighbors = util.neighbor_points(point, self.__tile_count[0], self.__tile_count[1])
            space_neighbors = [(i, j)
                               for (i, j) in neighbors
                               if self.__tile_types[i][j] == Map.TileType.SPACE
                               or self.__tile_types[i][j] == Map.TileType.START]
            unvisited_space_neighbors = [(i, j)
                                         for (i, j) in space_neighbors
                                         if dijkstra_map[i][j] is None]

            for space_neighbor in unvisited_space_neighbors:
                new_value = value + 1
                dijkstra_map[space_neighbor[0]][space_neighbor[1]] = new_value
                frontier.push(space_neighbor, new_value)

        return dijkstra_map
