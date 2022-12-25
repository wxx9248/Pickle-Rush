# -*- coding: utf-8 -*-
import typing

import pygame.event

HandlerCallable: typing.TypeAlias = typing.Callable[[pygame.event.Event], None]


class EventDispatcher:
    def __init__(self):
        self.event_type_handler_dict = {}

    def register(self, event_type: pygame.event.Event.type, handler: HandlerCallable):
        if event_type in self.event_type_handler_dict:
            self.event_type_handler_dict[event_type].append(handler)
        else:
            self.event_type_handler_dict[event_type] = [handler]

    # TODO: unregister function

    def dispatch(self, event: pygame.event.Event):
        if event.type in self.event_type_handler_dict:
            for handler in self.event_type_handler_dict[event.type]:
                handler(event)

    def dispatch_all(self, events: typing.List[pygame.event.Event]):
        for event in events:
            self.dispatch(event)
