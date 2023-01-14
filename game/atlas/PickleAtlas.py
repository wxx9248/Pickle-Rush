# -*- coding: utf-8 -*-
import math

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
    WALK_SPEED = 3
    DIAGONAL_WALK_SPEED = math.sqrt(2) / 2 * WALK_SPEED

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


class WalkNorthState(WalkState):
    def __init__(self, **kwargs):
        super().__init__("walk-north", **kwargs)

    def before_entry(self):
        super().before_entry()
        self.persistent_store["atlas"].speed_y = -WalkState.WALK_SPEED

    def before_leave(self):
        self.persistent_store["atlas"].speed_y = 0


class WalkSouthState(WalkState):
    def __init__(self, **kwargs):
        super().__init__("walk-south", **kwargs)

    def before_entry(self):
        super().before_entry()
        self.persistent_store["atlas"].speed_y = WalkState.WALK_SPEED

    def before_leave(self):
        self.persistent_store["atlas"].speed_y = 0


class WalkWestState(WalkState):
    def __init__(self, **kwargs):
        super().__init__("walk-west", **kwargs)

    def before_entry(self):
        super().before_entry()
        self.persistent_store["atlas"].speed_x = -WalkState.WALK_SPEED

    def before_leave(self):
        self.persistent_store["atlas"].speed_x = 0


class WalkEastState(WalkState):
    def __init__(self, **kwargs):
        super().__init__("walk-east", **kwargs)

    def before_entry(self):
        super().before_entry()
        self.persistent_store["atlas"].speed_x = WalkState.WALK_SPEED

    def before_leave(self):
        self.persistent_store["atlas"].speed_x = 0


class WalkNorthWestState(WalkState):
    def __init__(self, **kwargs):
        super().__init__("walk-north-west", **kwargs)

    def before_entry(self):
        super().before_entry()
        self.persistent_store["atlas"].speed_x = -WalkState.DIAGONAL_WALK_SPEED
        self.persistent_store["atlas"].speed_y = -WalkState.DIAGONAL_WALK_SPEED

    def before_leave(self):
        self.persistent_store["atlas"].speed_x = 0
        self.persistent_store["atlas"].speed_y = 0


class WalkNorthEastState(WalkState):
    def __init__(self, **kwargs):
        super().__init__("walk-north-east", **kwargs)

    def before_entry(self):
        super().before_entry()
        self.persistent_store["atlas"].speed_x = WalkState.DIAGONAL_WALK_SPEED
        self.persistent_store["atlas"].speed_y = -WalkState.DIAGONAL_WALK_SPEED

    def before_leave(self):
        self.persistent_store["atlas"].speed_x = 0
        self.persistent_store["atlas"].speed_y = 0


class WalkSouthWestState(WalkState):
    def __init__(self, **kwargs):
        super().__init__("walk-south-west", **kwargs)

    def before_entry(self):
        super().before_entry()
        self.persistent_store["atlas"].speed_x = -WalkState.DIAGONAL_WALK_SPEED
        self.persistent_store["atlas"].speed_y = WalkState.DIAGONAL_WALK_SPEED

    def before_leave(self):
        self.persistent_store["atlas"].speed_x = 0
        self.persistent_store["atlas"].speed_y = 0


class WalkSouthEastState(WalkState):
    def __init__(self, **kwargs):
        super().__init__("walk-south-east", **kwargs)

    def before_entry(self):
        super().before_entry()
        self.persistent_store["atlas"].speed_x = WalkState.DIAGONAL_WALK_SPEED
        self.persistent_store["atlas"].speed_y = WalkState.DIAGONAL_WALK_SPEED

    def before_leave(self):
        self.persistent_store["atlas"].speed_x = 0
        self.persistent_store["atlas"].speed_y = 0


class PickleAtlas(Atlas):
    def __init__(self):
        super().__init__()
        asset_object_factory = AssetObjectFactory()
        self["idle"] = asset_object_factory.new_asset_object("asset.sprite.pickle.0")
        self["walking-1"] = asset_object_factory.new_asset_object("asset.sprite.pickle.1")
        self["walking-2"] = asset_object_factory.new_asset_object("asset.sprite.pickle.2")

        self.__state_machine = StateMachine()
        self.__state_machine.add_state(IdleState(atlas=self))
        self.__state_machine.add_state(WalkNorthState(atlas=self))
        self.__state_machine.add_state(WalkSouthState(atlas=self))
        self.__state_machine.add_state(WalkWestState(atlas=self))
        self.__state_machine.add_state(WalkEastState(atlas=self))
        self.__state_machine.add_state(WalkNorthWestState(atlas=self))
        self.__state_machine.add_state(WalkNorthEastState(atlas=self))
        self.__state_machine.add_state(WalkSouthWestState(atlas=self))
        self.__state_machine.add_state(WalkSouthEastState(atlas=self))
        self.__state_machine.add_transition_group(
            "idle",
            TransitionGroup(
                (self.__state_machine["walk-north"],
                 lambda _, e: e.type == pygame.KEYDOWN and e.key == pygame.K_UP),
                (self.__state_machine["walk-south"],
                 lambda _, e: e.type == pygame.KEYDOWN and e.key == pygame.K_DOWN),
                (self.__state_machine["walk-west"],
                 lambda _, e: e.type == pygame.KEYDOWN and e.key == pygame.K_LEFT),
                (self.__state_machine["walk-east"],
                 lambda _, e: e.type == pygame.KEYDOWN and e.key == pygame.K_RIGHT)
            ))
        self.__state_machine.add_transition_group(
            "walk-north",
            TransitionGroup(
                (self.__state_machine["idle"],
                 lambda _, e: e.type == pygame.KEYUP and e.key == pygame.K_UP),
                (self.__state_machine["walk-north-west"],
                 lambda _, e: e.type == pygame.KEYDOWN and e.key == pygame.K_LEFT),
                (self.__state_machine["walk-north-east"],
                 lambda _, e: e.type == pygame.KEYDOWN and e.key == pygame.K_RIGHT)
            ))
        self.__state_machine.add_transition_group(
            "walk-south",
            TransitionGroup(
                (self.__state_machine["idle"],
                 lambda _, e: e.type == pygame.KEYUP and e.key == pygame.K_DOWN),
                (self.__state_machine["walk-south-west"],
                 lambda _, e: e.type == pygame.KEYDOWN and e.key == pygame.K_LEFT),
                (self.__state_machine["walk-south-east"],
                 lambda _, e: e.type == pygame.KEYDOWN and e.key == pygame.K_RIGHT)
            ))
        self.__state_machine.add_transition_group(
            "walk-west",
            TransitionGroup(
                (self.__state_machine["idle"],
                 lambda _, e: e.type == pygame.KEYUP and e.key == pygame.K_LEFT),
                (self.__state_machine["walk-north-west"],
                 lambda _, e: e.type == pygame.KEYDOWN and e.key == pygame.K_UP),
                (self.__state_machine["walk-south-west"],
                 lambda _, e: e.type == pygame.KEYDOWN and e.key == pygame.K_DOWN)
            ))
        self.__state_machine.add_transition_group(
            "walk-east",
            TransitionGroup(
                (self.__state_machine["idle"],
                 lambda _, e: e.type == pygame.KEYUP and e.key == pygame.K_RIGHT),
                (self.__state_machine["walk-north-east"],
                 lambda _, e: e.type == pygame.KEYDOWN and e.key == pygame.K_UP),
                (self.__state_machine["walk-south-east"],
                 lambda _, e: e.type == pygame.KEYDOWN and e.key == pygame.K_DOWN)
            ))

        self.__state_machine.add_transition_group(
            "walk-north-west",
            TransitionGroup(
                (self.__state_machine["walk-north"],
                 lambda _, e: e.type == pygame.KEYUP and e.key == pygame.K_LEFT),
                (self.__state_machine["walk-west"],
                 lambda _, e: e.type == pygame.KEYUP and e.key == pygame.K_UP)
            ))

        self.__state_machine.add_transition_group(
            "walk-north-east",
            TransitionGroup(
                (self.__state_machine["walk-north"],
                 lambda _, e: e.type == pygame.KEYUP and e.key == pygame.K_RIGHT),
                (self.__state_machine["walk-east"],
                 lambda _, e: e.type == pygame.KEYUP and e.key == pygame.K_UP)
            ))

        self.__state_machine.add_transition_group(
            "walk-south-west",
            TransitionGroup(
                (self.__state_machine["walk-south"],
                 lambda _, e: e.type == pygame.KEYUP and e.key == pygame.K_LEFT),
                (self.__state_machine["walk-west"],
                 lambda _, e: e.type == pygame.KEYUP and e.key == pygame.K_DOWN)
            ))

        self.__state_machine.add_transition_group(
            "walk-south-east",
            TransitionGroup(
                (self.__state_machine["walk-south"],
                 lambda _, e: e.type == pygame.KEYUP and e.key == pygame.K_RIGHT),
                (self.__state_machine["walk-east"],
                 lambda _, e: e.type == pygame.KEYUP and e.key == pygame.K_DOWN)
            ))

        self.__state_machine.start_state = "idle"
        self.__state_machine.reset()

    def update(self):
        super().update()
        self.__state_machine.update()

    def accept_event(self, event: pygame.event.Event):
        self.__state_machine.next(event)
