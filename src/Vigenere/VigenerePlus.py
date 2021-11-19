"""
This file decrypts a message encrypted using first the vigenere technique and then
a single column transposition.

ct = kolom transpositie
v = vigenere
m = message
(  ct(v(m))  )⁻¹  =  (ct ° v)⁻¹(m) = (v⁻¹ ° ct⁻¹)(m) = v⁻¹(ct⁻¹(m))

"""

from src.Vigenere.Vigenere import vigenere



from itertools import *
from src.Utils.Utils import invertedColumnTransposition


def vigenerePlus(cipherText: str):

    for keyLen in range(1, 11):
        key = len(list(permutations(range(keyLen))))
        print(key)
        invCTCipherText: str = invertedColumnTransposition(cipherText, key)



