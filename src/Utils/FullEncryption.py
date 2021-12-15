"""
This file implements encryption methods. The implemented methods are as follows:
    1) vigenerePlusEncryption
    Vigenere followed by single columnar transposition, requiring two distinct keywords .
    It is assumed that the plaintext consists of only characters in the latin alphabet.
    No punctuation is allowed is allowed nor checked for. All characters should be capital
    letters.
"""
from src.Playfair.Playfair import playfair
from src.Vigenere.Vigenere import vigenere
from src.Utils.Utils import columnTransposition




def vigenerePlusEncryption(plaintext: str, vKey: str, ctKey: str) -> str:
    vKey = vKey.upper()
    ctKey = ctKey.upper()
    
    if vKey == ctKey:
        raise RuntimeError(f"identical keywords for VigenerePlus encryption: {vKey} and {ctKey}")
    
    return columnTransposition(vigenere(plaintext, vKey), ctKey)


def playfairEncryption(plaintext: str, keyWord: str) -> str:
    return playfair(plaintext, keyWord)


