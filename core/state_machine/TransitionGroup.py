# -*- coding: utf-8 -*-
from __future__ import annotations

import typing

from core.state_machine.State import State
from core.state_machine.StateMachine import ExciterType


class TransitionGroup:
    def __init__(self, source_state: State, *args: ConnectionType):
        self.__source_state: State = source_state
        self.__destination_predicate_dict: typing.Dict[State, PredicateType] = \
            {destination_state: predicate for destination_state, predicate in args}

    @property
    def source_state(self):
        return self.__source_state

    def add_connection(self, connection: ConnectionType):
        self.__destination_predicate_dict[connection[0]] = connection[1]

    def remove_connection(self, destination_state: State):
        del self.__destination_predicate_dict[destination_state]

    def get_all_destinations(self):
        return self.__destination_predicate_dict.keys()

    def get_possible_destinations(self, exciter: ExciterType):
        return [state for state, predicate in self.__destination_predicate_dict.items() if predicate(self, exciter)]

    def __repr__(self):
        return repr(self.__destination_predicate_dict)

    def __str__(self):
        return str(self.__destination_predicate_dict)

    def __len__(self):
        return len(self.__destination_predicate_dict)

    def __contains__(self, item: State):
        return item in self.__destination_predicate_dict

    def __iter__(self):
        return iter(self.__destination_predicate_dict)

    def keys(self):
        return self.__destination_predicate_dict.keys()

    def values(self):
        return self.__destination_predicate_dict.values()

    def items(self):
        return self.__destination_predicate_dict.items()


PredicateType: typing.TypeAlias = typing.Callable[[TransitionGroup, ExciterType], bool]
ConnectionType: typing.TypeAlias = typing.Tuple[State, PredicateType]
