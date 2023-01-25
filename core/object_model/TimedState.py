class TimedState:
    def __init__(self, frame_limit: int):
        self.__frame_counter = 0
        self.__frame_limit = frame_limit
        self.activate = False
        self.pause = True

    def update(self):
        if self.pause:
            return

        if not self.activate:
            self.state_end_event()
            self.reset()
        else:
            self.__frame_counter += 1
            if self.__frame_counter >= self.__frame_limit:
                self.activate = False

    def state_end_event(self):
        pass

    def start(self):
        self.pause = False
        self.activate = True

    def reset(self):
        self.__frame_counter = 0
        self.activate = False
        self.pause = True
