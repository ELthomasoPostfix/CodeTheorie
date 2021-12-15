from itertools import permutations

from src.Playfair.Substitution import Substitution
from src.Utils.TextFrame import TextFrame
from src.Utils.Utils import latinAlphabet


class PlayfairTextFrame(TextFrame):
    def __init__(self, text: str):
        super().__init__(text)

        la = latinAlphabet(True)
        la.remove(Substitution.REPLACEABLE)
        la = ''.join(la)

        self.__mapping = {}


    def defineMapping(self, key: str, value: str, force=False):
        revKey = key[::-1]
        prevKeyValue = self.__mapping.get(key)
        prevRevKeyValue = self.__mapping.get(revKey)

        if not ((prevKeyValue is None and prevRevKeyValue is None) or
                (prevKeyValue[::-1] == prevRevKeyValue)):
            raise ValueError(f"PlayfairTextFrame mapping error. key-value mapping of bigrams must result\
            in a mapping of the reverse bigrams, but instead we found: '{key}: {prevKeyValue}' and '{revKey}: {prevRevKeyValue}'")


        if force or (not force and (prevKeyValue is None and prevRevKeyValue is None)):
            self.__mapping[key] = value
            self.__mapping[revKey] = value[::-1]

        return prevKeyValue, prevRevKeyValue

    def decipher(self):
        plaintext = ""
        for index in range(0, len(self.text) - 1, 2):
            digram = self.text[index:index+2]
            digramValue = self.__mapping.get(digram)
            if digramValue is not None:
                plaintext += digramValue
            else:
                plaintext += digram
        return plaintext

    def getMappingRepresentation(self):
        repr = ""
        for mapping in self.__mapping.items():
            repr += f"{mapping[0]} --> {mapping[1]}\n"
        return repr