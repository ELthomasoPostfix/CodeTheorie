from collections import Callable

from src.Utils.Utils import *
from src.Utils.Statistics.statistics import *
from src.Utils.TextFrame import TextFrame




class VigenerePlusTextFrame(TextFrame):
    def __init__(self, text: str, rowWidth: int):
        super().__init__(text)

        self.__rowWidth = rowWidth
        self.__columns = []
        self.__columnChars = []
        self.reassignColumns(self.__rowWidth)

        self.__alphabet = latinAlphabet(True)

    def reassignColumns(self, rowWidth: int):
        self.__rowWidth = max(0, min(rowWidth, self.__len__()))  # clamp
        self.__columns = []
        self.__columnChars = [''] * rowWidth
        for baseIndex in range(self.__rowWidth):
            column = ""
            index = baseIndex
            while index < self.__len__():
                column += self.text[index]
                index += self.__rowWidth
            self.__columns.append(column)


    def transformColumn(self, index: int, transformer: Callable):
        """
        Alter a column using a transformer.
        :param index:       The column to transform permanently.
        :param transformer: The transformation function applied to each character of the initial column.
        """
        index %= len(self.__columns)
        self.__columns[index] = self.__transform(self.__columns[index], transformer)
        self.__columnChars[index] = ''





    def vigColumn(self, index: int, char: str):
        index %= self.__rowWidth
        res = ""

        if self.__columnChars[index] == char:
            return

        self.__columnChars[index] = char
        for i in range(index, len(self.text), self.__rowWidth):
            res += diffChars(self.text[i], char)
        self.__columns[index] = res

    def getColumnsIC(self, maxIndex: int = -1):
        maxIndex %= len(self.__columns)
        return ic(''.join([self.__columns[i] for i in range(maxIndex + 1)]), self.__alphabet)





    def getColumns(self):
        return self.__columns

    def getIC(self, transformer: Callable = None):
        return ic(''.join(
            self.__transform(self.text, transformer) if transformer is not None else self.text),
            self.__alphabet)

    def getColumnIC(self, column: int, transformer: Callable = None):
        return ic(self.getColumn(column, transformer), self.__alphabet)

    def getAvgColumnIC(self):
        icVal = 0
        for col in range(self.__rowWidth):
            icVal += self.getColumnIC(col)

        return icVal / self.__rowWidth

    def getColumn(self, column: int, transformer: Callable = None):
        column = max(0, min(column, self.__rowWidth - 1))

        if transformer is not None:
            return self.__transform(self.__columns[column], transformer)

        return self.__columns[column]

    def __transform(self, text, transformer: Callable):
        if transformer is None:
            raise ValueError("Transformer for vigenerePlus frame is None")

        if isinstance(text, str):
            text = list(text)

        if not isinstance(text, type([str])):
            raise TypeError("Incorrect type for vigenerePlus frame transformation")

        for i in range(len(text)):
            text[i] = transformer(text[i])
        return ''.join(text)
