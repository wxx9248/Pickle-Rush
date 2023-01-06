# -*- coding: utf-8 -*-
import pygame.sprite


class Sprite(pygame.sprite.Sprite):
    def __init__(self, image: pygame.surface.Surface, *groups: pygame.sprite.AbstractGroup):
        super().__init__(*groups)
        self.image = image.convert_alpha()
        self.rect = self.image.get_rect()

    @property
    def surface(self):
        return self.image
