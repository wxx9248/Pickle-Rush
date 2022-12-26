# -*- coding: utf-8 -*-
from core.BaseThread import BaseThread
from event.EventDispatcher import EventDispatcher


class GameThread(BaseThread):
    def __init__(self, event_dispatcher: EventDispatcher):
        super().__init__(event_dispatcher)

    def run(self):
        pass
