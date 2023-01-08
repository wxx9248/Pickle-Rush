# -*- coding: utf-8 -*-

import pygame

from asset.AssetObjectFactory import AssetObjectFactory
from core.object_model.Atlas import Atlas
from core.state_machine.State import State
from core.state_machine.StateMachine import StateMachine
from core.state_machine.TransitionGroup import TransitionGroup


class IdleState(State):
    def __init__(self, **kwargs):
        super().__init__("idle", **kwargs)

    def before_entry(self):
        self.persistent_store["atlas"].current_sprite_key = "idle"


class WalkState(State):
    def before_entry(self):
        self.volatile_store["counter"] = 0

    def update(self):
        counter = self.volatile_store["counter"]
        divided_counter = counter // 10
        if divided_counter % 2:
            self.persistent_store["atlas"].current_sprite_key = "walking-2"
        else:
            self.persistent_store["atlas"].current_sprite_key = "walking-1"

        if counter > 1000:
            self.volatile_store["counter"] = 0
            return
        self.volatile_store["counter"] += 1


class WalkUpState(WalkState):
    def __init__(self, **kwargs):
        super().__init__("walk-up", **kwargs)

    def before_entry(self):
        super().before_entry()
        self.persistent_store["atlas"].speed_y = -1

    def before_leave(self):
        self.persistent_store["atlas"].speed_y = 0


class WalkDownState(WalkState):
    def __init__(self, **kwargs):
        super().__init__("walk-down", **kwargs)

    def before_entry(self):
        super().before_entry()
        self.persistent_store["atlas"].speed_y = 1

    def before_leave(self):
        self.persistent_store["atlas"].speed_y = 0


class WalkLeftState(WalkState):
    def __init__(self, **kwargs):
        super().__init__("walk-left", **kwargs)

    def before_entry(self):
        super().before_entry()
        self.persistent_store["atlas"].speed_x = -1

    def before_leave(self):
        self.persistent_store["atlas"].speed_x = 0


class WalkRightState(WalkState):
    def __init__(self, **kwargs):
        super().__init__("walk-right", **kwargs)

    def before_entry(self):
        super().before_entry()
        self.persistent_store["atlas"].speed_x = 1

    def before_leave(self):
        self.persistent_store["atlas"].speed_x = 0


class PickleAtlas(Atlas):
    def __init__(self):
        super().__init__()
        asset_object_factory = AssetObjectFactory()
        self["idle"] = asset_object_factory.new_asset_object("asset.sprite.pickle.0")
        self["walking-1"] = asset_object_factory.new_asset_object("asset.sprite.pickle.1")
        self["walking-2"] = asset_object_factory.new_asset_object("asset.sprite.pickle.2")

        self.__state_machine = StateMachine()
        self.__state_machine.add_state(IdleState(atlas=self))
        self.__state_machine.add_state(WalkUpState(atlas=self))
        self.__state_machine.add_state(WalkDownState(atlas=self))
        self.__state_machine.add_state(WalkLeftState(atlas=self))
        self.__state_machine.add_state(WalkRightState(atlas=self))
        self.__state_machine.start_state = "idle"
        self.__state_machine.reset()
        self.__state_machine.add_transition_group(
            "idle",
            TransitionGroup(
                (self.__state_machine["walk-up"], lambda _, e: e.type == pygame.KEYDOWN and e.key == pygame.K_UP),
                (self.__state_machine["walk-down"], lambda _, e: e.type == pygame.KEYDOWN and e.key == pygame.K_DOWN),
                (self.__state_machine["walk-left"], lambda _, e: e.type == pygame.KEYDOWN and e.key == pygame.K_LEFT),
                (self.__state_machine["walk-right"], lambda _, e: e.type == pygame.KEYDOWN and e.key == pygame.K_RIGHT)
            ))
        self.__state_machine.add_transition_group(
            "walk-up",
            TransitionGroup(
                (self.__state_machine["idle"], lambda _, e: e.type == pygame.KEYUP and e.key == pygame.K_UP)
            ))
        self.__state_machine.add_transition_group(
            "walk-down",
            TransitionGroup(
                (self.__state_machine["idle"], lambda _, e: e.type == pygame.KEYUP and e.key == pygame.K_DOWN)
            ))
        self.__state_machine.add_transition_group(
            "walk-left",
            TransitionGroup(
                (self.__state_machine["idle"], lambda _, e: e.type == pygame.KEYUP and e.key == pygame.K_LEFT)
            ))
        self.__state_machine.add_transition_group(
            "walk-right",
            TransitionGroup(
                (self.__state_machine["idle"], lambda _, e: e.type == pygame.KEYUP and e.key == pygame.K_RIGHT)
            ))

    def update(self):
        self.__state_machine.update()

    def accept_input_event(self, event: pygame.event.Event):
        self.__state_machine.next(event)
