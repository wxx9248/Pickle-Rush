import typing

from core.object_model.Atlas import Atlas
from core.object_model.Sprite import Sprite
import pygame


class BulletAtlas(Atlas):
    def __init__(self, sprite: Sprite, damage: int = 1, **kwargs):
        super().__init__(sprite, **kwargs)
        self.__damage = damage

    @property
    def damage(self):
        return self.__damage
