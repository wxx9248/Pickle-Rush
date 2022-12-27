# -*- coding: utf-8 -*-
import queue

import pygame.event


class LocalEventReceiver:
    def __init__(self, event_queue: queue.Queue):
        self.__event_queue = event_queue

    def receive(self, event: pygame.event.Event):
        self.__event_queue.put(event)
