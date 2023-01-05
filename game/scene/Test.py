# -*- coding: utf-8 -*-
import typing

from asset.AssetObjectFactory import AssetObjectFactory
from core.object_model.Scene import Scene


class Test(Scene):
    def __init__(self, size: typing.Tuple[int, int], asset_object_factory: AssetObjectFactory):
        super().__init__(size, asset_object_factory)
