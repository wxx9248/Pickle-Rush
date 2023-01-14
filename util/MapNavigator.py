import typing

import pygame

from core.object_model.Atlas import Atlas
from core.object_model.Map import Map
from game.atlas.MapAtlas import MapAtlas
from util.PriorityQueue import PriorityQueue


class MapNavigator:
    def __init__(self, source_atlas: Atlas, target_atlas: Atlas, map_atlas: MapAtlas):
        self.__source_atlas = source_atlas
        self.__target_atlas = target_atlas
        self.__map_atlas = map_atlas
        self.__direction_vector = pygame.Vector2()

        self.__source_grid_position = (0, 0)
        self.__source_grid_index = (0, 0)
        self.__target_grid_position = (0, 0)
        self.__target_grid_index = (0, 0)
        self.update_position()

        self.__next_grid_position = self.__source_grid_position

    @property
    def direction_vector(self) -> pygame.Vector2:
        return self.__direction_vector

    def update(self):
        self.update_position()
        if self.__source_grid_position == self.__next_grid_position:
            path = self.construct_path(self.search())
            if len(path) < 1:
                return
            self.__next_grid_position = path[1]
            self.__direction_vector = pygame.Vector2(
                int(self.__next_grid_position[1] - self.__source_grid_position[1]),
                int(self.__next_grid_position[0] - self.__source_grid_position[0])
            )

    def update_position(self):
        self.__source_grid_position = \
            self.__map_atlas.screen_to_grid_position(
                pygame.Vector2(self.__source_atlas.position),
                self.__source_atlas.surface.get_size()
            )
        self.__source_grid_index = (round(self.__source_grid_position.x), round(self.__source_grid_position.y))

        self.__target_grid_position = \
            self.__map_atlas.screen_to_grid_position(
                pygame.Vector2(self.__target_atlas.position),
                self.__target_atlas.surface.get_size()
            )
        self.__target_grid_index = (round(self.__target_grid_position.x), round(self.__target_grid_position.y))

    def search(self):
        # with A* Algorithm
        def cost(p1, p2) -> float:
            (x1, y1) = p1
            (x2, y2) = p2
            return abs(x1 - x2) + abs(y1 - y2)

        def space_neighbor_filter(candidate) -> bool:
            try:
                return self.__map_atlas.map_object.tile_types[candidate[0]][candidate[1]] == Map.TileType.SPACE
            except IndexError:
                return False

        priority_queue = PriorityQueue()

        priority_queue.put(self.__source_grid_index, 0)
        came_from: typing.Dict[typing.Tuple[int, int], typing.Optional[typing.Tuple[int, int]]] = {}
        cost_map: typing.Dict[typing.Tuple[int, int], float] = {self.__source_grid_index: 0}
        came_from[self.__source_grid_index] = None

        while not priority_queue.empty():
            current_grid_index: typing.Tuple[int, int] = priority_queue.get()

            if current_grid_index == self.__target_grid_index:
                break

            candidates = [
                (current_grid_index[0] + 1, current_grid_index[1]),
                (current_grid_index[0] - 1, current_grid_index[1]),
                (current_grid_index[0], current_grid_index[1] + 1),
                (current_grid_index[0], current_grid_index[1] - 1)
            ]

            space_neighbors = [
                candidate
                for candidate in candidates
                if space_neighbor_filter(candidate)
            ]

            for space_neighbor in space_neighbors:
                new_cost = cost_map[current_grid_index] + 1
                if space_neighbor not in cost_map or new_cost < cost_map[space_neighbor]:
                    cost_map[space_neighbor] = new_cost
                    priority = new_cost + cost(space_neighbor, self.__target_grid_index)
                    priority_queue.put(space_neighbor, priority)
                    came_from[space_neighbor] = current_grid_index

        return came_from

    def construct_path(
            self,
            came_from: typing.Dict[typing.Tuple[int, int], typing.Tuple[int, int]]
    ) -> typing.List[typing.Tuple[int, int]]:
        current = self.__target_grid_index
        goal = self.__target_grid_index
        start = self.__source_grid_index

        path: typing.List[typing.Tuple[int, int]] = []
        if goal not in came_from or goal == start:
            # No path was found
            return []

        while current != start:
            path.append(current)
            current = came_from[current]

        path.append(start)
        path.reverse()
        return path
