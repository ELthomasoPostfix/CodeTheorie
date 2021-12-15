import random
from io import TextIOWrapper
from math import ceil
from typing import List
from src.Utils.LatinNGrams import LatinNGrams


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



def writePairList(pList: List, of, sort=False, reverse=False):

    opened = False
    if isinstance(of, str):
        opened = True
        of = open(of, 'w')

    if not isinstance(of, TextIOWrapper):
        raise ValueError("The of parameter of writePairList accepts a string or a TextIOWrapper type")

    if sort:
        pList.sort(key=lambda p: p[1], reverse=reverse)

    for item in pList:
        of.write(str(item[0]) + " " + str(item[1]) + ("\n" if item != pList[-1] else ""))

    if opened:
        of.close()



def exchange2letters(lst: List[str]):
    i = random.randint(0, 24)
    j = random.randint(0, 24)


    temp = lst[i]
    lst[i] = lst[j]
    lst[j] = temp

    
def swap2rows(lst: List[str]):
        i = random.randint(0, 4) * 5
        j = random.randint(0, 4) * 5

        for k in range(5):
            temp = lst[i + k]
            lst[i + k] = lst[j + k]
            lst[j + k] = temp


def swap2cols(lst: List[str]):
    i = random.randint(0, 4)
    j = random.randint(0, 4)

    for k in range(5):
        k *= 5
        temp = lst[k + i]
        lst[k + i] = lst[k + j]
        lst[k + j] = temp


def copyList(lst: List[str], toCopy: List[str], reverse=False):
    if reverse:
        endIndex = len(lst) - 1
        for i in range(len(lst)):
            lst[i] = toCopy[endIndex - i]
    else:
        for i in range(len(lst)):
            lst[i] = toCopy[i]


def generateMonoFiles(cipherText: str, countFreq: str,
                      storedPath:str, measuredPath: str, combinedPath: str):

    monoCounts = {}
    for c in cipherText:
        monoCounts.setdefault(c, 0)
        monoCounts[c] += 1
    writePairList(list(monoCounts.items()), measuredPath, True, True)

    storedMono = LatinNGrams(iPath=storedPath, statType=countFreq, toLogFreq=False).getFrequenciesList()
    measuredMono = LatinNGrams(iPath=measuredPath, statType=countFreq, toLogFreq=False).getFrequenciesList()


    of = open(combinedPath, 'w')
    of.write("stored mono freq\n")
    writePairList(storedMono, of)
    of.write("\n\n")
    of.write("measured mono freq\n")
    writePairList(measuredMono, of)
    of.close()


def generateBiFiles(cipherText: str, countFreq: str,
                    storedPath: str, measuredPath: str, combinedPath: str):

    biCounts = {}
    for index in range(len(cipherText)-1):
        bigram = cipherText[index] + cipherText[index+1]
        biCounts.setdefault(bigram, 0)
        biCounts[bigram] += 1
    writePairList(list(biCounts.items()), measuredPath, True, True)

    storedMono = LatinNGrams(iPath=storedPath, statType=countFreq, toLogFreq=False).getFrequenciesList()
    measuredMono = LatinNGrams(iPath=measuredPath, statType=countFreq, toLogFreq=False).getFrequenciesList()

    of = open(combinedPath, 'w')
    of.write("stored bi freq\n")
    writePairList(storedMono, of)
    of.write("\n\n")
    of.write("measured bi freq\n")
    writePairList(measuredMono, of)
    of.close()