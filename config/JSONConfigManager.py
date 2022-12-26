# -*- coding: utf-8 -*-
import json
import typing

from config import AbstractConfigManager
from config.ReactiveConfigNode import ReactiveConfigNode


def deserialize_object_hook(config_node: ReactiveConfigNode | dict) -> ReactiveConfigNode:
    return ReactiveConfigNode(config_node)


class JSONDecoder(json.JSONDecoder):
    def __init__(self, *, parse_float=None,
                 parse_int=None, parse_constant=None, strict=True,
                 object_pairs_hook=None):
        super().__init__(object_hook=deserialize_object_hook, parse_float=parse_float, parse_int=parse_int,
                         parse_constant=parse_constant, strict=strict, object_pairs_hook=object_pairs_hook)


class JSONEncoder(json.JSONEncoder):
    def __init__(self, *, skipkeys=False, ensure_ascii=True,
                 check_circular=True, allow_nan=True, sort_keys=False,
                 indent=None, separators=None, default=None):
        super().__init__(skipkeys=skipkeys, ensure_ascii=ensure_ascii, check_circular=check_circular,
                         allow_nan=allow_nan, sort_keys=sort_keys, indent=indent, separators=separators)

    def default(self, o: typing.Any) -> typing.Any:
        if type(o) is not ReactiveConfigNode:
            return super().default(o)

        return o.config


class Serializer(AbstractConfigManager.Serializer):
    def __init__(self, indent=4):
        self.__indent = indent

    @property
    def indent(self):
        return self.__indent

    def serialize(self, config_node: ReactiveConfigNode) -> str:
        return json.dumps(config_node, indent=self.__indent, cls=JSONEncoder)

    def deserialize(self, config_string: str) -> ReactiveConfigNode:
        return json.loads(config_string, cls=JSONDecoder)


class JSONConfigManager(AbstractConfigManager.AbstractConfigManager):
    def __init__(
            self,
            file_path: str,
            binding_mode=AbstractConfigManager.AbstractConfigManager.BindingMode.DOUBLE):
        super().__init__(Serializer(), file_path, binding_mode)
