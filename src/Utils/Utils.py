import copy
import queue
from math import ceil, floor, factorial, log
import unicodedata

from unidecode import unidecode



def keyCharOrdering(key: str) -> [int]:

    if not key.isalpha():
        raise ValueError(f"non-alpha key cannot be converted to unordered numeric form: {key}")

    key = key.upper()
    s = sorted(key)
    m: dict = {c: v for c, v in enumerate(s)}
    ordering = [-1] * len(key)   # (sorted key index, unsorted key index)

    for keyInd, keyChr in m.items():
        for index, order in enumerate(ordering):
            if key[index] == keyChr and order == -1:
                ordering[index] = keyInd
                break

    return ordering


def columnTransposition(msg: str, key: str) -> str:
    transposed = ""

    columns = [(orderedInd, unorderedInd) for unorderedInd, orderedInd in enumerate(keyCharOrdering(key))]

    # sort the columns based on assigned numerical value (sort a-z)
    columns = sorted(columns, key=lambda pair: pair[0])

    for col in columns:
        msgInd = col[1]
        while msgInd < len(msg):
            transposed += msg[msgInd]
            msgInd += len(key)

    return transposed


def invertedColumnTransposition(cipherText: str, key) -> str:
    columns = key

    if isinstance(columns, str):
        columns = keyCharOrdering(key)
    if not isinstance(columns, type([int])):
        raise TypeError("Incorrect columns type for invertedColumnTransposition()")

    invColTrans: str = ""

    rowCount = ceil(float(len(cipherText)) / len(columns))
    fillCol = len(cipherText) % len(columns)        # index in columns of first unfilled col


    shortColumns = columns[fillCol:] if fillCol > 0 else []     # unfilled column (last row)
    leftShiftAmounts = {c: sum(sc < c for sc in shortColumns) for ind, c in enumerate(columns)}

    for row in range(rowCount):
        for ind, col in enumerate(columns):
            msgInd = row + col*rowCount - leftShiftAmounts[col]
            if fillCol and ind >= fillCol and row == rowCount-1:
                continue
            invColTrans += cipherText[msgInd]

    return invColTrans


def isChrLatin(c: str):
    return c.isalpha() and unicodedata.category(c) != 'Mn'


def toLatin(text: str):
    return ''.join(unidecode(c) for c in unicodedata.normalize('NFKD', text) if isChrLatin(c))


def latinAlphabet(uppercase: bool = False):
    a: int = 0x61 - 0x20 * uppercase
    return [chr(asciiVal) for asciiVal in range(a, a + 26)]


"""
    Each character in the latin alphabet is assigned a value of O-25.
    To sum two characters, do 
        ( val(a) + val(b) ) % 26
    where the value wraps around as to stay in the 0-25 range.
    Keeps case of a.
"""
def sumChars(a: chr, b: chr):
    lower = ord(a) >= 0x61
    a = a.upper()
    b = b.upper()
    c = chr(((ord(a) + ord(b)) % 26) + 0x41)
    return c.lower() if lower else c.upper()


"""
    Each character in the latin alphabet is assigned a value of O-25.
    To subtract two characters, do 
        ( val(a) - val(b) ) % 26
    where the value wraps around as to stay in the 0-25 range.
    Keeps case of a.
"""
def diffChars(a: chr, b: chr):
    lower = ord(a) >= 0x61
    a = a.upper()
    b = b.upper()
    c = chr(((ord(a) - ord(b)) % 26) + 0x41)
    return c.lower() if lower else c.upper()



