# -*- coding: utf-8 -*-
import typing

import pygame.event
from readerwriterlock.rwlock import RWLockWrite

from event.EventHandler import EventHandler


class EventDispatcher:
    def __init__(self):
        self.__event_handler_dict: typing.Dict[int, typing.Dict[str, typing.Set[EventHandler]]] = {}
        self.__rwlock = RWLockWrite()

    def register(self, event_type: int, namespace: str, handler: EventHandler):
        with self.__rwlock.gen_wlock():
            if event_type not in self.__event_handler_dict:
                self.__event_handler_dict[event_type] = {}

            if namespace not in self.__event_handler_dict[event_type]:
                self.__event_handler_dict[event_type][namespace] = set()

            self.__event_handler_dict[event_type][namespace].add(handler)

    def unregister(self, namespace: str, event_type: int, handler: EventHandler):
        with self.__rwlock.gen_wlock():
            self.__event_handler_dict[event_type][namespace].remove(handler)

    def dispatch(self, event: pygame.event.Event):
        with self.__rwlock.gen_rlock():
            if event.type not in self.__event_handler_dict:
                return

            [handler.handle(event)
             for handlers in self.__event_handler_dict[event.type].values()
             for handler in handlers]

    def dispatch_all(self, events: typing.List[pygame.event.Event]):
        for event in events:
            self.dispatch(event)
