# -*- coding: utf-8 -*-
import abc


class IConfigSerializer(abc.ABC):
    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def serialize(self, config_dict: dict) -> str:
        pass

    @abc.abstractmethod
    def deserialize(self, config_string: str) -> dict:
        pass
