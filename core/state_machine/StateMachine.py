# -*- coding: utf-8 -*-
from __future__ import annotations

import typing

from core.state_machine.NoNextStateException import NoNextStateException

if typing.TYPE_CHECKING:
    from core.state_machine.TransitionGroup import TransitionGroup
    from core.state_machine.State import State

ExciterType: typing.TypeAlias = typing.Any


class StateMachine:
    def __init__(self):
        self.__state_dict: typing.Dict[str, State] = {}
        self.__transition_group_dict: typing.Dict[str, TransitionGroup] = {}
        self.__start_state: typing.Optional[State] = None
        self.__current_state: typing.Optional[State] = None
        self.__end_state: typing.Optional[State] = None

    @property
    def all_states(self) -> typing.List[State]:
        return list(self.__state_dict.values())

    @property
    def all_transition_groups(self) -> typing.List[TransitionGroup]:
        return list(self.__transition_group_dict.values())

    @property
    def start_state(self):
        return self.__start_state

    @start_state.setter
    def start_state(self, value: State | str):
        if type(value) is str:
            self.__start_state = self.__state_dict[value]
            return

        self.__start_state = value
        if value.identifier not in self.__state_dict:
            self.__state_dict[value.identifier] = value

    @property
    def current_state(self):
        return self.__current_state

    @current_state.setter
    def current_state(self, value: State | str):
        if type(value) is str:
            self.__current_state = self.__state_dict[value]
            return

        self.__current_state = value
        if value.identifier not in self.__state_dict:
            self.__state_dict[value.identifier] = value

    @property
    def end_state(self):
        return self.__end_state

    @end_state.setter
    def end_state(self, value: State | str):
        if type(value) is str:
            self.__end_state = self.__state_dict[value]
            return

        self.__end_state = value
        if value.identifier not in self.__state_dict:
            self.__state_dict[value.identifier] = value

    @property
    def halted(self) -> bool:
        if self.__current_state is None:
            return True
        if self.__end_state is None:
            return False
        return self.__current_state == self.end_state

    def remove_state(self, state: State | str):
        if type(state) is not State:
            state = self.__state_dict[state]

        # Remove state and corresponding transition group from dictionary
        del self.__state_dict[state.identifier]
        del self.__transition_group_dict[state.identifier]

        # Remove all connections where the target state is a destination in each transition group
        [transition_group.remove_connection(state)
         for transition_group in self.__transition_group_dict.values()
         if state in transition_group]

        # Remove other references if necessary
        if self.__start_state == state:
            self.__start_state = None
        if self.__current_state == state:
            self.__current_state = None
        if self.__end_state == state:
            self.__end_state = None

    def register_transition_group(self, source_state: State | str, transition: TransitionGroup):
        if type(source_state) is not State:
            source_state = self.__state_dict[source_state]
        self.__transition_group_dict[source_state.identifier] = transition

    def remove_transition_group(self, source_state: State | str):
        if type(source_state) is not State:
            state = self.__state_dict[source_state]

        del self.__transition_group_dict[source_state.identifier]

    def reset(self, reset_state=False):
        self.__current_state = self.__start_state
        if reset_state:
            [state.reset() for state in self.__state_dict.values()]

    def next(self, exciter: ExciterType):
        if self.halted:
            return

        next_state_list = \
            self.__transition_group_dict[self.__current_state.identifier].get_possible_destinations(exciter)

        if len(next_state_list) == 0:
            raise NoNextStateException(self, self.__transition_group_dict[self.__current_state.identifier])

        self.__current_state = self.resolve_next_state_list(next_state_list)

    def resolve_next_state_list(self, next_state_list: typing.List[State]) -> State:
        if len(next_state_list) > 1:
            raise NotImplementedError("Cannot resolve multiple next states")
        return next_state_list[0]

    def update(self):
        if self.halted:
            return
        self.__current_state.update()

    def __getitem__(self, key: str):
        item = self.__state_dict[key]
        return item

    def __repr__(self):
        return repr(self.__state_dict)

    def __str__(self):
        return str(self.__state_dict)

    def __len__(self):
        return len(self.__state_dict)

    def __cmp__(self, other: StateMachine):
        return self.__cmp__(other)

    def __contains__(self, item: typing.Any):
        return item in self.__state_dict

    def __iter__(self):
        return iter(self.__state_dict)

    def keys(self):
        return self.__state_dict.keys()

    def values(self):
        return self.__state_dict.values()

    def items(self):
        return self.__state_dict.items()


class NoNextStateException(Exception):
    def __init__(self, state_machine: StateMachine, transition_group: TransitionGroup, *args):
        super().__init__(args)
        self.state_machine = state_machine
        self.transition_group = transition_group
