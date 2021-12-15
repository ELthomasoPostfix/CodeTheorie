from enum import Enum


class MessageDirection(Enum):
    IN: int = 0
    OUT: int = 1


class Mapper:
    def __init__(self):
        self.__in = {}
        self.__out = {}

    def get(self, direction: int, s: str):
        if direction == MessageDirection.IN:
            return self.__in[s]
        if direction == MessageDirection.OUT:
            return self.__out[s]
        return None


