"""
This file implements the vigenere encryption technique.
"""


from src.Utils.Utils import sumChars, diffChars


def vigenereAlg(text: str, key: str, function):
    res: str = ""
    keyLen: int = len(key)
    key = key.upper()

    for i, c in enumerate(text):
        res += function(c, key[i % keyLen])

    return res


def vigenere(plainText: str, key: str) -> str:
    return vigenereAlg(plainText, key, sumChars)


def invertedVigenere(cipherText: str, key: str) -> str:
    return vigenereAlg(cipherText, key, diffChars)

