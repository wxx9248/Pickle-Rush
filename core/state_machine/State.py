# -*- coding: utf-8 -*-
from __future__ import annotations

import typing


class State:
    def __init__(self, identifier: str, updater: typing.Callable[[State], None]):
        self.__identifier = identifier
        self.__updater = updater
        self.__store: typing.Dict = {}

    @property
    def identifier(self):
        return self.__identifier

    @property
    def updater(self):
        return self.__updater

    @property
    def store(self):
        return self.__store

    def reset(self):
        self.__store = {}

    def update(self):
        self.__updater(self)

    def __hash__(self):
        return hash(self.__identifier)

    def __eq__(self, other: State):
        return self.__identifier == other.__identifier
