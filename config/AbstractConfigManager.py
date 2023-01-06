# -*- coding: utf-8 -*-
import abc
import enum
import logging
import typing

import readerwriterlock.rwlock

from config.ReactiveConfigNode import ReactiveConfigNode, AfterUpdateCallable


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
        self.__logger = logging.getLogger(self.__class__.__name__)
        self.__config: typing.Optional[ReactiveConfigNode] = None
        self.__config_rw_lock = readerwriterlock.rwlock.RWLockWrite()
        self.__serializer = serializer
        self.__file_path = file_path
        self.__binding_mode = binding_mode
        self.sync_from_file()

    @property
    def file_path(self) -> str:
        return self.__file_path

    @property
    def binding_mode(self) -> BindingMode:
        return self.__binding_mode

    @property
    def after_update(self) -> AfterUpdateCallable:
        return self.__config.after_update

    @after_update.setter
    def after_update(self, value: AfterUpdateCallable):
        def executor(_, v: typing.Any):
            if type(v) is ReactiveConfigNode:
                v.after_update = value

        self.__logger.debug(f"Set after-update callback for all config nodes")
        executor("", self.__config)
        self.__config.dfs_traverse(executor)

    def get(self, config_key: str) -> typing.Any:
        self.__logger.debug(f"Get config entry with key {config_key}")
        fields = config_key.split('.')
        namespace = fields[0]
        key = fields[1:]

        with self.__config_rw_lock.gen_rlock():
            item = self.__config
            for k in key:
                item = item[k]
            return item

    def set(self, config_key: str, value: typing.Any):
        self.__logger.debug(f"Set config value {value} with key {config_key}")
        fields = config_key.split('.')
        namespace = fields[0]
        key = fields[1:]

        with self.__config_rw_lock.gen_wlock():
            item = self.__config
            for k in key[:-1]:
                item = item[k]
            item[key[-1]] = value

    def delete(self, config_key: str):
        self.__logger.debug(f"Deleting config entry with config key {config_key}")
        fields = config_key.split('.')
        namespace = fields[0]
        key = fields[1:]

        with self.__config_rw_lock.gen_wlock():
            item = self.__config
            for k in key[:-1]:
                item = item[k]
            del item[key[-1]]

    def sync_from_file(self):
        self.__logger.debug(f"Syncing config dict from file")
        if not self.__binding_mode & AbstractConfigManager.BindingMode.FROM_FILE:
            return

        with open(self.__file_path, "r") as f:
            config = self.__serializer.deserialize(f.read())
            with self.__config_rw_lock.gen_wlock():
                self.__config = config

    def sync_to_file(self):
        self.__logger.debug(f"Syncing config dict to file")
        if not self.__binding_mode & AbstractConfigManager.BindingMode.TO_FILE:
            return

        with open(self.__file_path, "w") as f:
            with self.__config_rw_lock.gen_rlock():
                f.write(self.__serializer.serialize(self.__config))
