from src.Utils.TextManipulation import latinAlphabet
from src.Utils.Utils import *
from src.Utils.TextFrame import TextFrame




class VigenerePlusTextFrame2(TextFrame):
    def __init__(self, text: str, keyLen: int):
        super().__init__(text)

        self.__decipheredText = list(self.text)
        self.__decipheredChars = [''] * keyLen

        self.__keyLen = keyLen
        self.__alphabet = latinAlphabet(True)

    def getDecipheredText(self):
        return ''.join(self.__decipheredText)

    def score(self, substrWidth: int, ngrams: LatinNGrams):
        substrWidth = max(0, min(substrWidth, self.__keyLen))
        score = 0
        for i in range(0, len(self.__decipheredText), self.__keyLen):
            score += ngrams.score(''.join(self.__decipheredText[i:i + substrWidth]))
        return score

    def resetDecipheredText(self):
        self.__decipheredChars = [''] * self.__keyLen
        self.__decipheredText = list(self.text)

    def decipher(self, key: str):
        for keyIndex in range(min(len(key), self.__keyLen)):
            self.decipherColumn(keyIndex, key[keyIndex])

    def decipherColumn(self, keyIndex: int, keyChar: str):
        keyIndex %= self.__keyLen

        # The stored deciphered column has already been translated from
        # the original text using the specified character
        if self.__decipheredChars[keyIndex] == keyChar:
            return

        # Decipher the specified column
        for index in range(keyIndex, self.__len__(), self.__keyLen):
            self.__decipheredText[index] = diffChars(self.text[index], keyChar)
        self.__decipheredChars[keyIndex] = keyChar

