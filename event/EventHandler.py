# -*- coding: utf-8 -*-
from __future__ import annotations

import typing

import pygame

HandlerCallable: typing.TypeAlias = typing.Callable[[pygame.event.Event], None]


class EventHandler:
    def __init__(self, identifier: str, callback: HandlerCallable):
        self.__identifier = identifier
        self.__callable = callback

    @property
    def identifier(self):
        return self.__identifier

    def handle(self, event: pygame.event.Event):
        self.__callable(event)

    def __eq__(self, other: EventHandler):
        return self.__identifier == other.__identifier

    def __hash__(self):
        return hash(self.__identifier)
