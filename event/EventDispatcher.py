# -*- coding: utf-8 -*-
import typing

import pygame.event
from readerwriterlock.rwlock import RWLockWrite

from event.EventHandler import EventHandler
from util.util import catch_exception_and_print

EventHandlerDictType: typing.TypeAlias = typing.Dict[int, typing.Dict[str, typing.Set[EventHandler]]]


class EventDispatcher:
    def __init__(self):
        self.__event_handler_dict: EventHandlerDictType = {}
        self.__rwlock = RWLockWrite()

    @property
    def event_handler_dict(self) -> EventHandlerDictType:
        return self.__event_handler_dict

    def register(self, event_type: int, namespace: str, handler: EventHandler):
        with self.__rwlock.gen_wlock():
            if event_type not in self.__event_handler_dict:
                self.__event_handler_dict[event_type] = {}

            if namespace not in self.__event_handler_dict[event_type]:
                self.__event_handler_dict[event_type][namespace] = set()

            self.__event_handler_dict[event_type][namespace].add(handler)

    def unregister(self, event_type: int, namespace: str, handler: EventHandler):
        with self.__rwlock.gen_wlock():
            self.__event_handler_dict[event_type][namespace].remove(handler)

    def dispatch(self, event: pygame.event.Event):
        with self.__rwlock.gen_rlock():
            if event.type not in self.__event_handler_dict:
                return

            [catch_exception_and_print(lambda: handler.handle(event))
             for handlers in self.__event_handler_dict[event.type].values()
             for handler in handlers]

    def dispatch_all(self, events: typing.List[pygame.event.Event]):
        for event in events:
            self.dispatch(event)
