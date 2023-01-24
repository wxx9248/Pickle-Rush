# -*- coding: utf-8 -*-
import random
import traceback
import typing

import pygame


def catch_exception_and_print(f: typing.Callable):
    try:
        f()
    except Exception as e:
        traceback.print_exception(e)


def text_render_new_line(cursor: typing.List[int], font_height: int):
    # Carriage return
    cursor[0] = 0
    # Line feed
    cursor[1] += font_height


def text_render_get_font_object(font: str | typing.List[str], font_size: int, bold: bool, italic: bool):
    font_fallback: typing.Optional[str] = None

    if type(font) is str:
        font_fallback = font
        if font_fallback == "default":
            font_fallback = pygame.font.get_default_font()
    elif type(font) is list:
        preferences = [f.lower().replace(' ', '') for f in font]
        available = pygame.font.get_fonts()
        font_fallback = ",".join([a for a in available for p in preferences if a.startswith(p)])
        if len(font_fallback) == 0:
            font_fallback = None

    return pygame.font.SysFont(font_fallback, font_size, bold, italic)


def center(container_size: typing.Tuple[float, float], element_size: typing.Tuple[float, float]) \
        -> typing.Tuple[float, float]:
    return (container_size[0] - element_size[0]) / 2, (container_size[1] - element_size[1]) / 2


def random_color() -> pygame.Color:
    return pygame.Color(random.randint(64, 192), random.randint(64, 192), random.randint(64, 192))


def neighbor_points(point: typing.Tuple[int, int],
                    height: typing.Optional[int] = None,
                    width: typing.Optional[int] = None) -> typing.List[typing.Tuple[int, int]]:
    candidates = [(point[0] - 1, point[1]),
                  (point[0] + 1, point[1]),
                  (point[0], point[1] - 1),
                  (point[0], point[1] + 1)]

    if height is not None and width is not None:
        return [(i, j)
                for (i, j) in candidates
                if 0 <= i < height and 0 <= j < width]

    return candidates


def extended_neighbor_points(point: typing.Tuple[int, int],
                             height: typing.Optional[int] = None,
                             width: typing.Optional[int] = None) -> typing.List[typing.Tuple[int, int]]:
    candidates = [(point[0] - 1, point[1]),
                  (point[0] + 1, point[1]),
                  (point[0], point[1] - 1),
                  (point[0], point[1] + 1),
                  (point[0] - 1, point[1] - 1),
                  (point[0] + 1, point[1] + 1),
                  (point[0] + 1, point[1] - 1),
                  (point[0] - 1, point[1] + 1)]
    if height is not None and width is not None:
        return [(i, j)
                for (i, j) in candidates
                if 0 <= i < height and 0 <= j < width]

    return candidates


def point_distance_squared(start: typing.Tuple[int, int], end: typing.Tuple[int, int]):
    return (end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2
