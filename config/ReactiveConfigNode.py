from __future__ import annotations

import typing


class ReactiveConfigNode:
    def __init__(
            self, config: ReactiveConfigNode | dict = None,
            after_update: AfterUpdateCallable = None,
            after_delete: AfterDeleteCallable = None):

        self.__config = config
        if config is None:
            self.__config = {}

        self.__after_update = after_update
        self.__after_delete = after_delete

    @property
    def after_update(self):
        return self.__after_update

    @after_update.setter
    def after_update(self, value: AfterUpdateCallable):
        self.__after_update = value

    @property
    def after_delete(self):
        return self.__after_delete

    @after_delete.setter
    def after_delete(self, value: AfterDeleteCallable):
        self.__after_delete = value

    # Dictionary operations
    def __setitem__(self, key: str, item: any):
        self.__config[key] = item
        if self.__after_update is not None:
            self.__after_update(self, key, item)

    def __getitem__(self, key: str):
        item = self.__config[key]
        return item

    def __repr__(self):
        return repr(self.__config)

    def __str__(self):
        return str(self.__config)

    def __len__(self):
        return len(self.__config)

    def __delitem__(self, key: str):
        del self.__config[key]
        if self.__after_delete is not None:
            self.__after_delete(self, key)

    def __cmp__(self, other: ReactiveConfigNode):
        return self.__cmp__(other)

    def __contains__(self, item: any):
        return item in self.__config

    def __iter__(self):
        return iter(self.__config)

    def keys(self):
        return self.__config.keys()

    def values(self):
        return self.__config.values()

    def items(self):
        return self.__config.items()

    def dfs_traverse(self, callback: TraverseCallbackType):
        for key, value in self.__config.items():
            callback(key, value)

            if type(value) is not ReactiveConfigNode:
                continue

            value.dfs_traverse(callback)


AfterUpdateCallable: typing.TypeAlias = typing.Callable[[ReactiveConfigNode, str, any], None]
AfterDeleteCallable: typing.TypeAlias = typing.Callable[[ReactiveConfigNode, str], None]
TraverseCallbackType: typing.TypeAlias = typing.Callable[[str, any], None]
