# -*- coding: utf-8 -*-
import json

from config.serializer.IConfigSerializer import IConfigSerializer


class JSONConfigSerializer(IConfigSerializer):
    def __init__(self, indent=4):
        self.__indent = 4

    @property
    def indent(self):
        return self.__indent

    def serialize(self, config_dict: dict) -> str:
        return json.dumps(config_dict, indent=self.indent)

    def deserialize(self, config_string: str) -> dict:
        return json.loads(config_string)
