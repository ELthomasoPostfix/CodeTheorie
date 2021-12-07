import copy
import time

from src.Vigenere.Vigenere import vigenere, vigenereInverted
from src.Vigenere.VigenerePlus import vigenerePlus

from src.Utils.FullEncryption import vigenerePlusEncryption

from src.Utils.Utils import *






if __name__ == '__main__':

    key = KeyB26(7, 0 + 25*26 + 25*26*26 + 2*26*26*26)
    print(key.key())
    print(key.seed())
    print()

    key.incr(1)
    print(key.key())
    print(key.seed())
    print()

    key.decr(4)
    print(key.key())
    print(key.seed())
    print()

    key.incr(4)
    print(key.key())
    print(key.seed())
    print()
