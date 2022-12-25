# -*- coding: utf-8 -*-
class EventDispatcher:
    def __init__(self):
        self.event_type_handler_dict = {}

    def register(self, event_type, handler):
        if event_type in self.event_type_handler_dict:
            self.event_type_handler_dict[event_type].append(handler)
        else:
            self.event_type_handler_dict[event_type] = [handler]

    # TODO: unregister function

    def dispatch(self, event):
        if event.type in self.event_type_handler_dict:
            for handler in self.event_type_handler_dict[event.type]:
                handler(event)

    def dispatch_all(self, events):
        for event in events:
            self.dispatch(event)
