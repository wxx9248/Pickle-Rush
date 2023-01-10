# -*- coding: utf-8 -*-
import logging
import heapq
from typing import Optional, Dict, Tuple, Union
import pygame
from typing import Tuple
from core.object_model.Atlas import Atlas
from asset.AssetObjectFactory import AssetObjectFactory
from core.object_model.Map import Map
from core.object_model.Scene import Scene
from game.scene.GameLost import GameLost

from event.CustomEventTypes import CustomEventTypes


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


class BacteriaAtlas(Atlas):
    def __init__(self, scene: Scene):
        ao = AssetObjectFactory()
        super().__init__(ao.new_asset_object("asset.sprite.bacteria"))

        self.__logger = logging.getLogger(self.__class__.__name__)
        self.__scene = scene
        self.__map_obj: Map = scene.map_obj
        self.__sprite_size = pygame.Vector2(32, 32)
        self.__step_size = 2
        self.current_sprite_key = "default"
        self.grid_pos = self.get_grid_pos()
        self.__pickle_instance = self.__scene.attached_instances["pickle_atlas"]
        self.rect = pygame.Rect(self.position_x, self.position_y, self.__sprite_size.x,
                                self.__sprite_size.y)

        self.__moving_flag = False
        self.__next_grid_pos = self.grid_pos

    def get_grid_pos(self) -> Tuple[int, int]:
        return self.__map_obj.to_grid_position(pygame.Vector2(self.position))

    def get_next_pos(self) -> Union[Tuple[int, int], str]:
        came_from = self.a_star_search()
        path = self.reconstruct_path(came_from)
        wall_dict = self.__map_obj.map_wall_atlas_dict
        if len(path) == 0:
            return "STOP"
        if wall_dict[path[1]].tile_type == TileType.WALL:
            return "STOP"

        next_pos = path[1]
        return next_pos

    def update_position(self) -> None:
        self.rect.x = self.position_x
        self.rect.y = self.position_y
        self.grid_pos = self.get_grid_pos()

        if not self.__moving_flag:
            next_pos = self.get_next_pos()
            if next_pos != "STOP":
                self.__next_grid_pos = next_pos
                self.__moving_flag = True

    def check_if_overtake(self) -> bool:
        return self.grid_pos == self.__pickle_instance.grid_pos

    def update(self) -> None:
        self.update_position()
        for _ in range(self.__step_size):
            self.move_to_next_pos()
        if self.check_if_overtake():
            event = pygame.event.Event(CustomEventTypes.EVENT_STAGE_CHANGE_SCENE_REQUEST)
            event.scene = GameLost(self.__scene.size, self.__scene.asset_object_factory)
            pygame.event.post(event)

    def render(self, surface: pygame.surface.Surface) -> None:
        super(BacteriaAtlas, self).render(surface)
        # pygame.draw.rect(surface, (0, 255, 0), self.rect, 5, 1)

    def check_collide_with_wall(self) -> bool:
        for pos, tile_atlas in self.__map_obj.map_wall_atlas_dict.items():
            if tile_atlas.tile_type == TileType.WALL and self.rect.colliderect(tile_atlas.rect):
                return True
        return False

    # moving to next position's center point
    # this can prevent get stuck
    def move_to_next_pos(self) -> None:
        def norm(n):
            if n > 0:
                return 1
            if n < 0:
                return -1
            if n == 0:
                return 0

        block_size = self.__scene.map_obj.tile_size
        center_pos = pygame.Vector2(self.rect.center)
        next_center_pos = pygame.Vector2(self.__next_grid_pos[0] * block_size + block_size / 2,
                                         self.__next_grid_pos[1] * block_size + block_size / 2)
        moving_vec = next_center_pos - center_pos

        if abs(moving_vec.x) <= 1 and abs(moving_vec.y) <= 1:
            self.__moving_flag = False
            return

        moving_vec.x = norm(moving_vec.x)
        moving_vec.y = norm(moving_vec.y)

        if abs(moving_vec.x) > abs(moving_vec.y):
            moving_vec.y = 0
        else:
            moving_vec.x = 0

        self.position += moving_vec
        self.update_position()
        if self.check_collide_with_wall():
            self.position -= moving_vec
        self.update_position()

    def a_star_search(self) -> Dict[Tuple[int, int], Tuple[int, int]]:
        def cost_func(p1, p2) -> float:
            (x1, y1) = p1
            (x2, y2) = p2
            return abs(x1 - x2) + abs(y1 - y2)

        open_list = PriorityQueue()
        start = self.__map_obj.to_grid_position(pygame.Vector2(self.position))
        goal = self.__map_obj.to_grid_position(
            pygame.Vector2(self.__pickle_instance.position))
        open_list.put(start, 0)
        came_from: dict[Tuple[int, int], Optional[Tuple[int, int]]] = {}
        cost_map: dict[Tuple[int, int], float] = {start: 0}
        came_from[start] = None

        while not open_list.empty():
            curr: Tuple[int, int] = open_list.get()

            if curr == goal:
                break

            neighbors = []
            next_candis = [(curr[0] + 1, curr[1]),
                           (curr[0] - 1, curr[1]),
                           (curr[0], curr[1] + 1),
                           (curr[0], curr[1] - 1)]

            for next_candi in next_candis:
                if self.__map_obj.map_wall_atlas_dict[next_candi].tile_type == TileType.SPACE:
                    neighbors.append(next_candi)

            for next_neighbor in neighbors:
                new_cost = cost_map[curr] + 1
                if next_neighbor not in cost_map or new_cost < cost_map[next_neighbor]:
                    cost_map[next_neighbor] = new_cost
                    priority = new_cost + cost_func(self.position, self.__pickle_instance.position)
                    open_list.put(next_neighbor, priority)
                    came_from[next_neighbor] = curr

        return came_from

    def reconstruct_path(self, came_from: dict[Tuple[int, int], Tuple[int, int]],
                         ) -> list[Tuple[int, int]]:

        current: Tuple[int, int] = self.__pickle_instance.grid_pos
        goal: Tuple[int, int] = self.__pickle_instance.grid_pos
        start = self.grid_pos

        path: list[Tuple[int, int]] = []
        if goal not in came_from or goal == start:  # no path was found
            return []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)  # optional
        path.reverse()  # optional
        return path
