# -*- coding: utf-8 -*-

import pygame

from asset.AssetObjectFactory import AssetObjectFactory
from config.ConfigManager import ConfigManager
from core.object_model.Atlas import Atlas
from core.state_machine.State import State
from core.state_machine.StateMachine import StateMachine
from core.state_machine.TransitionGroup import TransitionGroup
from event.CustomEventTypes import CustomEventTypes
from game.atlas.PickleAtlas import WalkState
from game.atlas.BulletAtlas import BulletAtlas
from core.object_model.TimedState import TimedState
from typing import Dict, List


class IdleStateHorizontal(State):
    def __init__(self, **kwargs):
        super().__init__("idle", **kwargs)

    def before_entry(self):
        self.persistent_store["atlas"].current_sprite_key = "idle"


class WalkLeftState(WalkState):
    def __init__(self, **kwargs):
        super().__init__("walk-left", **kwargs)

    def before_entry(self):
        super().before_entry()
        self.persistent_store["atlas"].speed_x = -WalkState.WALK_SPEED
        self.persistent_store["atlas"].direction = "left"

    def before_leave(self):
        self.persistent_store["atlas"].speed_x = 0


class WalkRightState(WalkState):
    def __init__(self, **kwargs):
        super().__init__("walk-right", **kwargs)

    def before_entry(self):
        super().before_entry()
        self.persistent_store["atlas"].speed_x = WalkState.WALK_SPEED
        self.persistent_store["atlas"].direction = "right"

    def before_leave(self):
        self.persistent_store["atlas"].speed_x = 0


class IdleStateVertical(State):
    def __init__(self, **kwargs):
        super().__init__("idle", **kwargs)


class JumpUpState(State):
    # Acceleration when jumping up
    A = 5

    def __init__(self, **kwargs):
        super().__init__("jump-up", **kwargs)

    def before_entry(self):
        self.volatile_store["accelerated"] = False

    def update(self):
        if self.volatile_store["accelerated"]:
            return

        self.persistent_store["atlas"].speed_y -= JumpUpState.A
        self.volatile_store["accelerated"] = True


class MidAirState(State):
    def __init__(self, **kwargs):
        super().__init__("mid-air", **kwargs)


class PickleAtlasGravity(Atlas):
    # Gravitational acceleration
    G = 0.1

    def __init__(self, bullet_list: List[BulletAtlas] = None):
        super().__init__()
        asset_object_factory = AssetObjectFactory()
        self["idle"] = asset_object_factory.new_asset_object("asset.sprite.pickle.0")
        self["walking-1"] = asset_object_factory.new_asset_object("asset.sprite.pickle.1")
        self["walking-2"] = asset_object_factory.new_asset_object("asset.sprite.pickle.2")

        config_manager = ConfigManager()
        self.__debug = config_manager.get("config.debug")

        if bullet_list is None:
            bullet_list = []
        self.__bullet_list = bullet_list

        # used for specifying firing direction for now
        self.direction = "right"

        self.__hp = 5

        self.__state_machine_horizontal = StateMachine()
        self.__state_machine_horizontal.add_state(IdleStateHorizontal(atlas=self))
        self.__state_machine_horizontal.add_state(WalkLeftState(atlas=self))
        self.__state_machine_horizontal.add_state(WalkRightState(atlas=self))
        self.__state_machine_horizontal.add_transition_group(
            "idle",
            TransitionGroup(
                (self.__state_machine_horizontal["walk-left"],
                 lambda _, e: e.type == pygame.KEYDOWN and e.key == pygame.K_LEFT),
                (self.__state_machine_horizontal["walk-right"],
                 lambda _, e: e.type == pygame.KEYDOWN and e.key == pygame.K_RIGHT)
            ))
        self.__state_machine_horizontal.add_transition_group(
            "walk-left",
            TransitionGroup(
                (self.__state_machine_horizontal["idle"],
                 lambda _, e: e.type == pygame.KEYUP and e.key == pygame.K_LEFT)
            ))
        self.__state_machine_horizontal.add_transition_group(
            "walk-right",
            TransitionGroup(
                (self.__state_machine_horizontal["idle"],
                 lambda _, e: e.type == pygame.KEYUP and e.key == pygame.K_RIGHT)
            ))

        self.__state_machine_horizontal.start_state = "idle"
        self.__state_machine_horizontal.reset()

        self.__state_machine_vertical = StateMachine()
        self.__state_machine_vertical.add_state(IdleStateVertical(atlas=self))
        self.__state_machine_vertical.add_state(JumpUpState(atlas=self))
        self.__state_machine_vertical.add_state(MidAirState(atlas=self))
        self.__state_machine_vertical.add_transition_group(
            "idle",
            TransitionGroup(
                (self.__state_machine_vertical["jump-up"],
                 lambda _, e: e.type == pygame.KEYDOWN and e.key == pygame.K_UP)
            ))
        self.__state_machine_vertical.add_transition_group(
            "jump-up",
            TransitionGroup(
                (self.__state_machine_vertical["mid-air"], lambda _, e: True)
            ))
        self.__state_machine_vertical.add_transition_group(
            "mid-air",
            TransitionGroup(
                (self.__state_machine_vertical["idle"],
                 lambda _, e: e.type == CustomEventTypes.EVENT_LEVEL_1_COLLIDE_FLOOR)
            ))
        self.__state_machine_vertical.start_state = "idle"
        self.__state_machine_vertical.reset()

        self.acceleration_y = PickleAtlasGravity.G
        self.__bullet_speed = 5

        self.__invincible = TimedState(60 * 2)

    def hit(self, damage):
        if not self.__invincible.activate:
            self.__hp -= damage
            self.__invincible.start()

    @property
    def hp(self):
        return self.__hp

    @hp.setter
    def hp(self, val):
        self.__hp = val

    def fire(self):
        bullet = BulletAtlas()
        fire_vec = (0, 0)
        r_side_offset = pygame.Vector2(self.surface.get_size())
        r_side_offset.y /= 2
        l_side_offset = pygame.Vector2(-r_side_offset.x, r_side_offset.y)
        if self.direction == "left":
            fire_vec = pygame.Vector2(-1, 0) * self.__bullet_speed
            bullet.position = tuple(pygame.Vector2(self.position) + l_side_offset)
        elif self.direction == "right":
            fire_vec = pygame.Vector2(1, 0) * self.__bullet_speed
            bullet.position = tuple(pygame.Vector2(self.position) + r_side_offset)
        bullet.speed = fire_vec
        self.__bullet_list.append(bullet)

    def update(self):
        super().update()
        self.__state_machine_horizontal.update()
        self.__state_machine_vertical.update()
        self.__invincible.update()

    def accept_event(self, event: pygame.event.Event):
        self.__state_machine_horizontal.next(event)
        self.__state_machine_vertical.next(event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            self.fire()
