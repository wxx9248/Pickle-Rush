# -*- coding: utf-8 -*-


class FrameRateStabilizer:
    def __init__(self, target_fps: int = 60, sample_size: int = 30):
        self.__target_fps = target_fps
        self.__sample_size = sample_size

        self.get_tick = self.get_tick()

        self.__average = self.__target_fps

    def get_tick(self):
        while True:
            fps = yield self.calculate_tick(self.__average)
            self.__average += (fps - self.__target_fps) / self.__sample_size

    def calculate_tick(self, average: float):
        return 2 * self.__target_fps - average
