# -*- coding: utf-8 -*-
import logging
import threading
import typing


class BaseThread(threading.Thread):
    def __init__(self, paused=False):
        super().__init__(name=self.__class__.__name__)
        self.__logger = logging.getLogger(self.name)
        self.__running = True
        self.__paused = paused
        self.__resume_condition = threading.Condition()
        self.__exception: typing.Optional[BaseException] = None

    @property
    def logger(self):
        return self.__logger

    @property
    def running(self):
        return self.__running

    @property
    def paused(self):
        return self.__paused

    @property
    def exception(self) -> typing.Optional[Exception]:
        return self.__exception

    @exception.setter
    def exception(self, value):
        self.__exception = value

    @property
    def resume_condition(self):
        return self.__resume_condition

    def before_looper(self):
        pass

    def after_looper(self):
        pass

    def looper(self):
        while self.__running:
            if self.__paused:
                self.__resume_condition.wait()
            self.loop()

    def loop(self):
        pass

    def on_exception(self, exception):
        pass

    def run(self):
        try:
            self.before_looper()
            self.looper()
            self.after_looper()
        except BaseException as e:
            self.__logger.error("Thread exception occurred")
            self.__exception = e
            self.on_exception(e)
            self.__logger.debug("Stopping thread")
            self.stop()

    def pause(self):
        self.__paused = True

    def resume(self):
        self.__paused = False
        self.__resume_condition.notify_all()

    def stop(self):
        self.__running = False

    def join(self, timeout: float | None = None):
        super().join(timeout)
        if self.__exception is not None:
            raise self.__exception

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.__class__.__name__
