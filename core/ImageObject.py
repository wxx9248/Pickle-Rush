# -*- coding: utf-8 -*-
import pygame.sprite


class ImageObject(pygame.sprite.DirtySprite):
    def __init__(self, image: pygame.surface.Surface, *groups: pygame.sprite.AbstractGroup):
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect()
