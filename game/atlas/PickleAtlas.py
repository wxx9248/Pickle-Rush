# -*- coding: utf-8 -*-
import typing

import pygame

from core.object_model.Atlas import Atlas
from core.object_model.Sprite import Sprite
from core.state_machine.StateMachine import StateMachine


class PickleAtlas(Atlas):
    def __init__(self, default_sprite: typing.Optional[Sprite] = None):
        super().__init__(default_sprite)
        self.__state_machine = StateMachine()

    def update(self):
        pass

    def accept_input_event(self, event: pygame.event.Event):
        pass
