from enum import Enum


class MessageDirection(Enum):
    TO: int = 0
    BACK: int = 1


class Mapper:
    def __init__(self, fromValues, toValues):
        self.__rightToLeft = {fromValues[i]: toValues[i] for i in range(len(fromValues))}
        self.__leftToRight = {i[1]: i[0] for i in self.__rightToLeft.items()}

    def get(self, direction: int, value: str):
        if direction == MessageDirection.TO:
            return self.__rightToLeft.get(value)
        if direction == MessageDirection.BACK:
            return self.__leftToRight.get(value)
        return None


