import heapq
import typing
from typing import Any


class PriorityQueue:
    def __init__(self):
        self.__elements = []
        self.__counter = 0

    def empty(self) -> bool:
        return len(self.__elements) == 0

    def push(self, item: typing.Any, priority: int):
        heapq.heappush(self.__elements, (priority, self.__counter, item))
        self.__counter += 1

    def pop_element(self):
        return heapq.heappop(self.__elements)[2]

    def pop(self) -> tuple[int, Any]:
        (priority, _, element) = heapq.heappop(self.__elements)
        return priority, element
