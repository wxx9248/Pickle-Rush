# -*- coding: utf-8 -*-
import abc
import enum

from config.serializer.IConfigSerializer import IConfigSerializer


# TODO: Thread-safe support for concurrent writing to config dict and config file
#   Considering using a RWLock to protect dict and file

# TODO: Reminder: There also may be a performance issue if too many write operations happen at one time.
#   Considering caching those operations with an event queue if needs very frequent write operation.

class AbstractConfig(abc.ABC):
    class BindingMode(enum.IntFlag):
        FROM_FILE = enum.auto()
        TO_FILE = enum.auto()
        DOUBLE = FROM_FILE | TO_FILE

    @abc.abstractmethod
    def __init__(self, serializer: IConfigSerializer, file_path: str, binding_mode: BindingMode):
        """
        Initialize the config instance
        :param serializer: a serializer that supports serialization/deserialization of a dict
        :param file_path: path of the config file that will be bound to
        :param binding_mode: an enum value that specifies how config file and config dict should be synced
        """
        self.__config = None
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

    def sync_from_file(self):
        if not self.__binding_mode & AbstractConfig.BindingMode.FROM_FILE:
            return

        with open(self.__file_path, "r") as f:
            self.__config = self.__serializer.deserialize(f.read())

    def sync_to_file(self):
        if not self.__binding_mode & AbstractConfig.BindingMode.TO_FILE:
            return

        with open(self.__file_path, "w") as f:
            f.write(self.__serializer.serialize(self.__config))

    # Dictionary operations
    def __setitem__(self, key, item):
        self.__config[key] = item
        self.sync_to_file()

    def __getitem__(self, key):
        return self.__config[key]

    def __repr__(self):
        return repr(self.__config)

    def __len__(self):
        return len(self.__config)

    def __delitem__(self, key):
        del self.__config[key]
        self.sync_to_file()

    def __cmp__(self, other):
        return self.__cmp__(other)

    def __contains__(self, item):
        return item in self.__config

    def __iter__(self):
        return iter(self.__config)

    def keys(self):
        return self.__config.keys()

    def values(self):
        return self.__config.values()

    def items(self):
        return self.__config.items()

    def pop(self, *args):
        item = self.__config.pop(*args)
        self.sync_to_file()
        return item
