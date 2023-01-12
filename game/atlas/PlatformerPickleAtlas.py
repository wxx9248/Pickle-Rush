# -*- coding: utf-8 -*-
import typing

import pygame

from asset.AssetObjectFactory import AssetObjectFactory
from core.object_model.Atlas import Atlas
from core.state_machine.State import State
from core.state_machine.StateMachine import StateMachine
from core.state_machine.TransitionGroup import TransitionGroup
from event.EventDispatcher import EventDispatcher
from game.atlas.PickleAtlas import IdleState, WalkState, WalkRightState, WalkLeftState

class MotionControlEvents:
    EVENT_TOUCH_GROUND = 0

class JumpUpState(WalkState):
    JUMP_SPEED = 8

    def __init__(self, **kwargs):
        super().__init__("jump-up", **kwargs)

    def before_entry(self):
        super().before_entry()
        self.persistent_store["atlas"].speed_y = -self.JUMP_SPEED

    def before_leave(self):
        self.persistent_store["atlas"].speed_y = 0

class JumpUpLeftState(WalkState):
    JUMP_SPEED = 5

    def __init__(self, **kwargs):
        super().__init__("jump-up-left", **kwargs)

    def before_entry(self):
        super().before_entry()
        self.persistent_store["atlas"].speed_y = -self.JUMP_SPEED
        self.persistent_store["atlas"].speed_x = -self.WALK_SPEED

    def before_leave(self):
        self.persistent_store["atlas"].speed_x = 0
        self.persistent_store["atlas"].speed_y = 0


class JumpUpRightState(WalkState):
    JUMP_SPEED = 5

    def __init__(self, **kwargs):
        super().__init__("jump-up-right", **kwargs)

    def before_entry(self):
        super().before_entry()
        self.persistent_store["atlas"].speed_y = -self.JUMP_SPEED
        self.persistent_store["atlas"].speed_x = self.WALK_SPEED

    def before_leave(self):
        self.persistent_store["atlas"].speed_x = 0
        self.persistent_store["atlas"].speed_y = 0


class PlatformerPickleAtlas(Atlas):
    def __init__(self):
        super().__init__()
        asset_object_factory = AssetObjectFactory()
        self["idle"] = asset_object_factory.new_asset_object("asset.sprite.pickle.0")
        self["walking-1"] = asset_object_factory.new_asset_object("asset.sprite.pickle.1")
        self["walking-2"] = asset_object_factory.new_asset_object("asset.sprite.pickle.2")

        self.__state_machine = StateMachine()
        self.__state_machine.add_state(IdleState(atlas=self))
        self.__state_machine.add_state(JumpUpState(atlas=self))
        self.__state_machine.add_state(JumpUpLeftState(atlas=self))
        self.__state_machine.add_state(JumpUpRightState(atlas=self))
        self.__state_machine.add_state(WalkLeftState(atlas=self))
        self.__state_machine.add_state(WalkRightState(atlas=self))
        self.__state_machine.add_transition_group(
            "idle",
            TransitionGroup(
                (self.__state_machine["jump-up"],
                 lambda _, e: e.type == pygame.KEYDOWN and e.key == pygame.K_UP),
                (self.__state_machine["walk-left"],
                 lambda _, e: e.type == pygame.KEYDOWN and e.key == pygame.K_LEFT),
                (self.__state_machine["walk-right"],
                 lambda _, e: e.type == pygame.KEYDOWN and e.key == pygame.K_RIGHT)
            ))

        self.__state_machine.add_transition_group(
            "jump-up",
            TransitionGroup(
                (self.__state_machine["idle"],
                 lambda _, e: e.type == MotionControlEvents.EVENT_TOUCH_GROUND),
                (self.__state_machine["walk-left"],
                 lambda _, e: e.type == pygame.KEYDOWN and e.key == pygame.K_LEFT),
                (self.__state_machine["walk-right"],
                 lambda _, e: e.type == pygame.KEYDOWN and e.key == pygame.K_RIGHT),
            ))
        self.__state_machine.add_transition_group(
            "walk-left",
            TransitionGroup(
                (self.__state_machine["idle"],
                 lambda _, e: e.type == pygame.KEYUP and e.key == pygame.K_LEFT),
                (self.__state_machine["jump-up-left"],
                 lambda _, e: e.type == pygame.KEYDOWN and e.key == pygame.K_UP),
            ))
        self.__state_machine.add_transition_group(
            "walk-right",
            TransitionGroup(
                (self.__state_machine["idle"],
                 lambda _, e: e.type == pygame.KEYUP and e.key == pygame.K_RIGHT),
                (self.__state_machine["jump-up-right"],
                 lambda _, e: e.type == pygame.KEYDOWN and e.key == pygame.K_UP),
            ))

        self.__state_machine.add_transition_group(
            "jump-up-left",
            TransitionGroup(
                (self.__state_machine["idle"],
                 lambda _, e: e.type == MotionControlEvents.EVENT_TOUCH_GROUND)
            )
        )

        self.__state_machine.add_transition_group(
            "jump-up-right",
            TransitionGroup(
                (self.__state_machine["idle"],
                 lambda _, e: e.type == MotionControlEvents.EVENT_TOUCH_GROUND)
            )
        )
        self.__state_machine.start_state = "idle"
        self.__state_machine.reset()

    @property
    def state_machine(self):
        return self.__state_machine

    def update(self):
        super().update()
        self.__state_machine.update()

    def accept_event(self, event: pygame.event.Event):
        self.__state_machine.next(event)
