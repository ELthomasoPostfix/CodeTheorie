from math import ceil, floor
import unicodedata

def keyCharOrdering(key: str) -> [int]:

    if not key.isalpha():
        raise RuntimeError(f"non-alpha key cannot be converted to unordered numeric form: {key}")

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
        raise RuntimeError("Incorrect columns type for invertedColumnTransposition()")

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


def kasiski(cipherText: str, widths: [int]):

    occurrences = {}

    for width in widths:
        for ind, c in cipherText:
            pass


def ic(filenames: [str], alphabet: [chr]) -> float:
    charCounts = {char.upper(): 0 for char in alphabet}

    for filename in filenames:
        with open(filename, 'r') as file:

            if len(charCounts) == 0:
                return 0.0

            # calc character counts
            lineMax: int = 100
            line: str = file.readline(lineMax)
            while line != "":
                line = ''.join(c for c in unicodedata.normalize('NFD', line) if unicodedata.category(c) != 'Mn')
                for c in line:
                    if c.isalpha():
                        charCounts[c.upper()] += 1
                line = file.readline(lineMax)

    # calc ic value
    icVal = 0.0
    total = 0.0
    for count in charCounts.values():
        icVal += count * (count - 1.0)
        total += count


    return icVal / (total * (total - 1))

