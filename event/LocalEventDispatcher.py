# -*- coding: utf-8 -*-
import pygame

from event.EventDispatcher import EventDispatcher
from event.EventHandler import EventHandler
from event.LocalEventReceiver import LocalEventReceiver
from util.util import catch_exception_and_print


class LocalEventDispatcher(EventDispatcher):
    def __init__(self, global_event_dispatcher: EventDispatcher, event_receiver: LocalEventReceiver):
        super().__init__()
        self.__global_event_dispatcher = global_event_dispatcher
        self.__event_receiver = event_receiver

    def register(self, event_type: int, namespace: str, handler: EventHandler):
        super().register(event_type, namespace, handler)
        proxy_handler = EventHandler(handler.identifier, lambda e: self.__event_receiver.receive(e))
        self.__global_event_dispatcher.register(event_type, namespace, proxy_handler)

    def unregister(self, event_type: int, namespace: str, handler: EventHandler):
        super().unregister(event_type, namespace, handler)
        # We actually only need the identifier to unregister
        proxy_handler = EventHandler(handler.identifier, lambda _: None)
        self.__global_event_dispatcher.unregister(event_type, namespace, proxy_handler)

    def dispatch(self, event: pygame.event.Event):
        if event.type not in self.event_handler_dict:
            return

        [catch_exception_and_print(lambda: handler.handle(event))
         for handlers in self.event_handler_dict[event.type].values()
         for handler in handlers]
