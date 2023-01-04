# -*- coding: utf-8 -*-
import typing

import pygame.mixer

from core.object_model.Atlas import Atlas
from core.object_model.LayerManager import LayerManager
from core.object_model.Sound import Sound
from core.object_model.Sprite import Sprite


class Scene:
    def __init__(self, size: typing.Tuple[int, int]):
        self.__size = size

        default_background_surface = pygame.surface.Surface(size)
        default_background_surface.fill(pygame.Color("black"))
        self.__background: Atlas = Atlas()
        self.__background["default-background"] = Sprite(default_background_surface)
        self.__background.current_sprite_key = "default-background"

        self.__background_music: typing.Optional[Sound] = None

        self.__layer_manager = LayerManager()
        self.__sound_fx_dict: typing.Dict[str, Sound] = {}
        self.__background_music_channel: pygame.mixer.Channel = pygame.mixer.Channel(0)

    @property
    def size(self):
        return self.__size

    @property
    def layer_manager(self):
        return self.__layer_manager

    @property
    def sound_fx_dict(self):
        return self.__sound_fx_dict

    @property
    def background_music_channel(self):
        return self.__background_music_channel

    @property
    def background(self):
        return self.__background

    @background.setter
    def background(self, value: Atlas):
        self.__background = value

    @property
    def background_music(self):
        return self.__background_music

    @background_music.setter
    def background_music(self, value: Sound):
        self.__background_music = value

    def update(self):
        self.__layer_manager.update()

    def render(self, surface: pygame.surface.Surface):
        self.__background.render(surface)
        self.__layer_manager.render(surface)

    def accept_input_event(self, event: pygame.event.Event):
        pass
