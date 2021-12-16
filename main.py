import random
from itertools import permutations
from math import factorial

from src.Enigma.Enigma import Enigma, Rotor
from src.Enigma.EnigmaDecryption import enigmaDecryption
from src.Enigma.Mapper import MessageDirection, Mapper
from src.Playfair.Playfair import playfair
from src.Playfair.PlayfairDecryption import playfairDecryption
from src.Utils.Keys.KeyN10 import KeyN10
from src.Utils.Statistics.statistics import ic
from src.Utils.TextManipulation import toLatin, latinAlphabet
from src.Utils.Utils import columnTransposition, \
    invertedColumnTransposition
from src.Vigenere.VigenerePlusDecryption import vigenerePlusDecryption








def realVig(testText: str = None, ctTextLenLimiter: int = -1):
    vgPlusCipherText = ""
    if testText is None or testText == "":
        file = open("input/Vigenere input.txt")
        vgPlusCipherText = toLatin(file.read())
    else:
        vgPlusCipherText = testText

    vigenerePlusDecryption(vgPlusCipherText, ctTextLenLimiter)


def realPlayfair(testText: str = None):
    playfairCipherText = ""
    if testText is None or testText == "":
        file = open("input/Playfair input.txt")
        playfairCipherText = toLatin(file.read())
    else:
        playfairCipherText = testText

    playfairDecryption(playfairCipherText)


def realEnigma(testText: str = None):
    enigmaCipherText = ""
    if testText is None or testText == "":
        file = open("input/Enigma input.txt")
        enigmaCipherText = toLatin(file.read())
    else:
        enigmaCipherText = testText

    enigmaDecryption(enigmaCipherText)



if __name__ == '__main__':

    # no arg or None means using file text
    #realPlayfair(None)

    #realVig(ctTextLenLimiter=300)

    realEnigma(None)



    print("end main")



