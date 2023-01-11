# -*- coding: utf-8 -*-
import pygame.mixer


class Sound(pygame.mixer.Sound):
    def __init__(self, file, *args, **kwargs):
        super().__init__(file)
