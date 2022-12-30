# -*- coding: utf-8 -*-
import pygame.sprite


class SceneObject(pygame.sprite.LayeredDirty):
    def __init__(self, *sprites: pygame.sprite.DirtySprite, **kwargs):
        super().__init__(*sprites, **kwargs)
