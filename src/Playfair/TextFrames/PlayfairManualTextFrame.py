import time
from typing import List

from src.Playfair.TextFrames.PlayfairTextFrame import PlayfairTextFrame



class PlayfairManualTextFrame(PlayfairTextFrame):
    def __init__(self, text: str):
        super().__init__(text)
        self.decipheredText = self.text
        self.__decipheredChars = set()

    def decipher(self):
        self.decipheredText = super().decipher()

    def replaceDeciphered(self, old: str, new: str):
        if set(old).issubset(self.__decipheredChars):
            raise ValueError(f"already deciphered playfair text using {old}")

        self.decipheredText = self.decipheredText.replace(old, new)
        self.__decipheredChars.add(old)

    def replaceCiphered(self, old: str, new: str):
        self.decipheredText = self.text.replace(old, new)
        self.__resetDecipheredChars()
        self.__decipheredChars.add(old)

    def findCompletions(self, unfinishedText: List[str]):
        utLen = len(unfinishedText)
        completions = []

        for ngramBase in range(self.__len__() - utLen + 1):
            match = True
            for i, c in enumerate(unfinishedText):
                if c != '' and c != self.decipheredText[ngramBase + i]:
                    match = False
                    break
            if match:
                completions.append(self.decipheredText[ngramBase: ngramBase + utLen])

        return set(completions)

    def findBiMappingsTo(self, bigram: str):
        if len(bigram) != 2:
            raise ValueError("The bigram parameter of findBiMappings() only accepts input of len 2")

        mappings = []
        for index in range(0, self.__len__() - 1, 2):
            to = self.decipheredText[index: index+2]
            if bigram == to:
                mappings.append(''.join(self.text[index:index+2]))

        return mappings

    def getSurroundings(self, text: str, distance: int):
        tLen = len(text)
        res = []        # (baseIndex, leftNeighbours, rightNeighbours)

        for baseIndex in range(self.__len__() - len(text) + 1):
            if self.decipheredText[baseIndex:baseIndex+tLen] == text:
                res.append((baseIndex,
                            self.decipheredText[max(0, baseIndex-distance): baseIndex],
                            self.decipheredText[baseIndex+tLen: baseIndex+tLen+distance]))

        return res

    def count(self, text: str):
        return self.decipheredText.count(text)

    def resetDecipheredText(self):
        self.__resetDecipheredChars()
        self.decipheredText = self.text

    def updateText(self):
        self.text = self.decipheredText

    def getBigramRepresentation(self):
        return ''.join([self.text[i] + self.text[i+1] +
                        (' ' if i != len(self.text) - 2 else '')
                        for i in range(0, len(self.text) - 1, 2)])

    def getDecipheredBigramRepresentation(self):
        return ''.join([self.decipheredText[i] + self.decipheredText[i+1] +
                        (' ' if i != len(self.decipheredText) - 2 else '')
                        for i in range(0, len(self.decipheredText) - 1, 2)])

    def toDecipheredBigramSubstring(self, subString: str, occurrence: int):
        occurrence = max(0, occurrence)
        subLen = len(subString)
        for i in range(len(self.decipheredText) - len(subString) + 1):
            if self.decipheredText[i: i+subLen] == subString:
                if occurrence == 0:
                    i = i if i % 2 == 0 else i - 1
                    subLen = subLen if subLen % 2 == 0 else subLen + 1
                    return ''.join([self.decipheredText[i2] + self.decipheredText[i2 + 1] +
                                    (' ' if i2 != i+subLen - 2 else '')
                                    for i2 in range(i, i+subLen, 2)])
                else:
                    occurrence -= 1

    def __resetDecipheredChars(self):
        self.__decipheredChars = set()



