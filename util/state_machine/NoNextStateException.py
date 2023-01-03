# -*- coding: utf-8 -*-
from util.state_machine.StateMachine import StateMachine
from util.state_machine.TransitionGroup import TransitionGroup


class NoNextStateException(Exception):
    def __init__(self, state_machine: StateMachine, transition_group: TransitionGroup, *args):
        super().__init__(args)
        self.state_machine = state_machine
        self.transition_group = transition_group
