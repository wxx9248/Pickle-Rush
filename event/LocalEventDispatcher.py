# -*- coding: utf-8 -*-
import queue
import typing

import pygame

from event.EventDispatcher import EventDispatcher
from event.EventHandler import EventHandler
from util.util import catch_exception_and_print

EventHandlerDictType: typing.TypeAlias = typing.Dict[int, typing.Dict[str, typing.Set[EventHandler]]]


class LocalEventDispatcher:
    def __init__(self, identifier: str, global_event_dispatcher: EventDispatcher):
        self.__identifier = identifier
        self.__event_handler_dict: EventHandlerDictType = {}
        self.__registered_event_handler_count: typing.Dict[int, int] = {}
        self.__global_event_dispatcher = global_event_dispatcher
        self.__event_queue: queue.Queue[pygame.event.Event] = queue.Queue()

    @property
    def identifier(self):
        return self.__identifier

    def receive(self, event: pygame.event.Event):
        self.__event_queue.put(event)

    def register(self, event_type: int, namespace: str, handler: EventHandler):
        # Register to local store
        if event_type not in self.__event_handler_dict:
            self.__event_handler_dict[event_type] = {}
        if namespace not in self.__event_handler_dict[event_type]:
            self.__event_handler_dict[event_type][namespace] = set()
        self.__event_handler_dict[event_type][namespace].add(handler)

        # Update counter
        if event_type not in self.__registered_event_handler_count:
            self.__registered_event_handler_count[event_type] = 0
        self.__registered_event_handler_count[event_type] += 1

        # Register to global event dispatcher if not yet
        if self.__registered_event_handler_count[event_type] > 0:
            proxy_handler = EventHandler("proxy", lambda e: self.receive(e))
            self.__global_event_dispatcher.register(event_type, self.__identifier, proxy_handler)

    def unregister(self, event_type: int, namespace: str, handler: EventHandler):
        # Unregister from local store
        self.__event_handler_dict[event_type][namespace].remove(handler)

        # Update counter
        self.__registered_event_handler_count[event_type] -= 1

        # Unregister to global event dispatcher if no local event handler is registered
        if self.__registered_event_handler_count[event_type] == 0:
            # We actually only need the identifier to unregister, so lambda can be a dummy
            proxy_handler = EventHandler("proxy", lambda _: None)
            self.__global_event_dispatcher.unregister(event_type, self.__identifier, proxy_handler)

    def dispatch(self):
        while not self.__event_queue.empty():
            event = self.__event_queue.get()

            if event.type not in self.__event_handler_dict:
                continue

            [catch_exception_and_print(lambda: handler.handle(event))
             for handlers in self.__event_handler_dict[event.type].values()
             for handler in handlers]
