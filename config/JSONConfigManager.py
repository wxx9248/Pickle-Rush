# -*- coding: utf-8 -*-
import json

from config import AbstractConfigManager
from config.ReactiveConfigNode import ReactiveConfigNode


class Serializer(AbstractConfigManager.Serializer):
    def __init__(self, indent=4):
        self.__indent = 4

    @property
    def indent(self):
        return self.__indent

    def serialize(self, config_node:  ReactiveConfigNode) -> str:
        return json.dumps(config_node, indent=self.indent)

    def deserialize(self, config_string: str) -> ReactiveConfigNode:
        return json.loads(config_string, object_hook=lambda d: self.object_hook(d))

    def object_hook(self, config_node: ReactiveConfigNode | dict) -> ReactiveConfigNode:
        return ReactiveConfigNode(config_node)


class JSONConfigManager(AbstractConfigManager.AbstractConfigManager):
    def __init__(
            self,
            file_path: str,
            binding_mode=AbstractConfigManager.AbstractConfigManager.BindingMode.DOUBLE
    ):
        super().__init__(Serializer(), file_path, binding_mode)
