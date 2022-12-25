# -*- coding: utf-8 -*-
import abc
import enum
import typing

from config.ReactiveConfigNode import ReactiveConfigNode


class Serializer(abc.ABC):
    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def serialize(self, config_node: ReactiveConfigNode) -> str:
        pass

    @abc.abstractmethod
    def deserialize(self, config_string: str) -> ReactiveConfigNode:
        pass

    @abc.abstractmethod
    def object_hook(self, config_node: ReactiveConfigNode | dict) -> ReactiveConfigNode:
        pass


class AbstractConfigManager(abc.ABC):
    class BindingMode(enum.IntFlag):
        FROM_FILE = enum.auto()
        TO_FILE = enum.auto()
        DOUBLE = FROM_FILE | TO_FILE

    @abc.abstractmethod
    def __init__(self, serializer: Serializer, file_path: str, binding_mode: BindingMode):
        """
        Initialize the config instance
        :param serializer: a serializer that supports serialization/deserialization of a dict
        :param file_path: path of the config file that will be bound to
        :param binding_mode: an enum value that specifies how config file and config dict should be synced
        """
        self.__config: typing.Optional[ReactiveConfigNode] = None
        self.__serializer = serializer
        self.__file_path = file_path
        self.__binding_mode = binding_mode
        self.sync_from_file()

    @property
    def file_path(self):
        return self.__file_path

    @property
    def binding_mode(self):
        return self.__binding_mode

    @property
    def config(self):
        return self.__config

    @property
    def after_update(self):
        return self.__config.after_update

    @after_update.setter
    def after_update(self, value):
        def setter(_, v: any):
            if type(v) is ReactiveConfigNode:
                v.after_update = value

        setter("", self.__config)
        self.__config.dfs_traverse(setter)

    @property
    def after_delete(self):
        return self.__config.after_delete

    @after_delete.setter
    def after_delete(self, value):
        def setter(_, v: any):
            if type(v) is ReactiveConfigNode:
                v.after_delete = value

        setter("", self.__config)
        self.__config.dfs_traverse(setter)

    def sync_from_file(self):
        if not self.__binding_mode & AbstractConfigManager.BindingMode.FROM_FILE:
            return

        with open(self.__file_path, "r") as f:
            self.__config = self.__serializer.deserialize(f.read())

    def sync_to_file(self):
        if not self.__binding_mode & AbstractConfigManager.BindingMode.TO_FILE:
            return

        with open(self.__file_path, "w") as f:
            f.write(self.__serializer.serialize(self.__config))
