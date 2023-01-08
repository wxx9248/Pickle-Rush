# -*- coding: utf-8 -*-
from __future__ import annotations

import typing


class State:
    def __init__(self, identifier: str, **kwargs):
        self.__identifier = identifier
        self.__persistent_store: typing.Dict = kwargs
        self.__store: typing.Dict = {}
        self.__volatile_store: typing.Dict = {}

    @property
    def identifier(self):
        return self.__identifier

    @property
    def persistent_store(self):
        return self.__persistent_store

    @property
    def store(self):
        return self.__store

    @property
    def volatile_store(self):
        return self.__volatile_store

    def reset(self):
        self.__volatile_store.clear()
        self.__store.clear()

    def before_entry(self):
        pass

    def before_leave(self):
        pass

    def update(self):
        pass

    def __hash__(self):
        return hash(self.__identifier)

    def __eq__(self, other: State):
        return self.__identifier == other.__identifier
