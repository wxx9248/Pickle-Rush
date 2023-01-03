# -*- coding: utf-8 -*-
from __future__ import annotations

import typing

from core.state_machine.State import State
from core.state_machine.StateMachine import ExciterType


class TransitionGroup:
    def __init__(self, *args: ConnectionType):
        self.__connection_dict: typing.Dict[State, PredicateType] = \
            {destination_state: predicate for destination_state, predicate in args}

    def add_connection(self, connection: ConnectionType):
        self.__connection_dict[connection[0]] = connection[1]

    def remove_connection(self, destination_state: State):
        del self.__connection_dict[destination_state]

    def get_all_destinations(self):
        return self.__connection_dict.keys()

    def get_possible_destinations(self, exciter: ExciterType):
        return [state for state, predicate in self.__connection_dict.items() if predicate(self, exciter)]

    def __repr__(self):
        return repr(self.__connection_dict)

    def __str__(self):
        return str(self.__connection_dict)

    def __len__(self):
        return len(self.__connection_dict)

    def __contains__(self, item: State):
        return item in self.__connection_dict

    def __iter__(self):
        return iter(self.__connection_dict)

    def keys(self):
        return self.__connection_dict.keys()

    def values(self):
        return self.__connection_dict.values()

    def items(self):
        return self.__connection_dict.items()


PredicateType: typing.TypeAlias = typing.Callable[[TransitionGroup, ExciterType], bool]
ConnectionType: typing.TypeAlias = typing.Tuple[State, PredicateType]
