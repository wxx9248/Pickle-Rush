# -*- coding: utf-8 -*-
import threading


class BaseThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__()

    def __repr__(self):
        return f"{self.__class__.name}()"

    def __str__(self):
        return self.__class__.name
