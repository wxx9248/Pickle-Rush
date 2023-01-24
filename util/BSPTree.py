# -*- coding: utf-8 -*-

from __future__ import annotations

import random
import typing

import pygame

from core.object_model import Map


class Node:
    def __init__(self, rect: pygame.Rect, left: typing.Optional[Node], right: typing.Optional[Node]):
        self.__rect = rect
        self.__room_rect: typing.Optional[pygame.Rect] = None
        self.__left = left
        self.__right = right

    @property
    def rect(self):
        return self.__rect

    @property
    def room_rect(self):
        return self.__room_rect

    @room_rect.setter
    def room_rect(self, value):
        if self.is_leaf or value is None:
            self.__room_rect = value
            return
        raise ValueError("Try to assign a room to a non-leaf node")

    @property
    def left(self):
        return self.__left

    @property
    def right(self):
        return self.__right

    @left.setter
    def left(self, value):
        self.__room_rect = None
        self.__left = value

    @right.setter
    def right(self, value):
        self.__room_rect = None
        self.__right = value

    @property
    def is_leaf(self) -> bool:
        return self.__left is None and self.__right is None

    def __repr__(self):
        return repr(self.__rect)

    def __str__(self):
        return str(self.__rect)


class BSPTree:
    def __init__(self, root_rect: pygame.Rect):
        self.__root_node = Node(root_rect, None, None)

    @property
    def root_node(self):
        return self.__root_node

    def random(
            self,
            max_depth: int = 8,
            min_depth: int = 5,
            min_parent_width: int = 3,
            min_parent_height: int = 3,
            stop_threshold: float = 0.15,
            split_bias: float = 0.35):

        self.__root_node.left = None
        self.__root_node.right = None

        def recurse(parent_node: Node, parent_direction: bool, current_depth: int):
            if current_depth > max_depth:
                return
            if current_depth >= min_depth and random.random() < stop_threshold:
                return

            (parent_width, parent_height) = parent_node.rect.size
            if parent_height <= min_parent_height and parent_width <= min_parent_height:
                return
            elif parent_height <= min_parent_height and parent_width > min_parent_width:
                split_vertical = True
            elif parent_height > min_parent_height and parent_width <= min_parent_width:
                split_vertical = False
            else:
                split_vertical = not parent_direction

            if split_vertical:
                split_offset = round(random.uniform(split_bias, 1 - split_bias) * parent_width)
                parent_node.left = Node(
                    pygame.Rect(parent_node.rect.x, parent_node.rect.y,
                                split_offset, parent_height),
                    None, None)
                parent_node.right = Node(
                    pygame.Rect(parent_node.rect.x + split_offset, parent_node.rect.y,
                                parent_width - split_offset, parent_height),
                    None, None
                )
            else:
                split_offset = round(random.uniform(split_bias, 1 - split_bias) * parent_height)
                parent_node.left = Node(
                    pygame.Rect(parent_node.rect.x, parent_node.rect.y,
                                parent_width, split_offset),
                    None, None
                )
                parent_node.right = Node(
                    pygame.Rect(parent_node.rect.x, parent_node.rect.y + split_offset,
                                parent_width, parent_height - split_offset),
                    None, None
                )

            recurse(parent_node.left, split_vertical, current_depth + 1)
            recurse(parent_node.right, split_vertical, current_depth + 1)

        recurse(self.__root_node, random.random() < 0.5, 1)

    def dfs_preorder_iterator(self) -> typing.Optional[typing.Iterator[Node]]:
        stack = []
        current = self.__root_node

        while len(stack) or current is not None:
            if current is not None:
                yield current
                stack.append(current)
                current = current.left
            else:
                current = stack.pop()
                current = current.right

    def generate_rooms(self, min_width: int = 1, min_height: int = 1):
        (root_x, root_y, root_width, root_height) = (self.__root_node.rect.x, self.__root_node.rect.y,
                                                     self.__root_node.rect.width, self.__root_node.rect.height)
        for node in self.dfs_preorder_iterator():
            node.room_rect = None
            if not node.is_leaf:
                continue
            (x, y, width, height) = (node.rect.x, node.rect.y, node.rect.width, node.rect.height)

            if width < min_width or height < min_height:
                continue

            room_width = random.randint(min_width, width)
            room_height = random.randint(min_height, height)
            room_x = random.randint(x, x + width - room_width)
            room_y = random.randint(y, y + height - room_height)

            node.room_rect = pygame.Rect(x, y, room_width, room_height)

    def to_map_tiles(self) -> typing.List[typing.List[Map.Map.TileType]]:
        (root_x, root_y, root_width, root_height) = (self.__root_node.rect.x, self.__root_node.rect.y,
                                                     self.__root_node.rect.width, self.__root_node.rect.height)

        map_tiles = [[Map.Map.TileType.SPACE for _ in range(root_width)] for _ in range(root_height)]

        for node in self.dfs_preorder_iterator():
            if node.room_rect is None:
                continue

            (x, y, width, height) = (node.room_rect.x, node.room_rect.y,
                                     node.room_rect.width, node.room_rect.height)

            for i in range(height):
                for j in range(width):
                    map_tiles[root_y + y + i][root_x + x + j] = Map.Map.TileType.WALL

        return map_tiles
