# -*- coding: utf-8 -*-
import typing

from core.object_model.Layer import Layer
from core.object_model.Scene import Scene
from game.atlas.PickleAtlas import PickleAtlas


class Test(Scene):
    def __init__(self, size: typing.Tuple[int, int]):
        super().__init__(size)

        self.pickle_atlas = PickleAtlas()
        self.pickle_atlas.scale = (0.2, 0.2)

        layer = Layer(self.pickle_atlas)

        self.layer_manager["test"] = layer

    def update(self):
        self.pickle_atlas.update()
