# -*- coding: utf-8 -*-
import typing

import pygame.mixer

from core.LayerManager import LayerManager
from core.Sound import Sound


class Scene:
    def __init__(self):
        self.__background_music = None

        self.__layer_manager = LayerManager()
        self.__sound_fx_dict: typing.Dict[str, Sound] = {}
        self.__background_music_channel: pygame.mixer.Channel = pygame.mixer.Channel(0)

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
    def background_music(self):
        return self.__background_music

    @background_music.setter
    def background_music(self, value: Sound):
        self.__background_music = value

    def update(self):
        self.__layer_manager.update()

    def render(self, surface: pygame.surface.Surface):
        self.__layer_manager.render(surface)
