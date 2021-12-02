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


# Define the largest divisor to consider using the maxKeyLen parameter. The divisors of the distances between
# xgrams could be multiples of the key length. If the max key length is known, then we can limit the
# number of divisors to check. The divisors up to the max key length suffice for determining likely key length, although
# multiples of some possible length do add credibility to that length as the actual key length.
# TODO is maxKeyLen a good idea???? ==> Just choose one high enough then,
#
# Increasing minOccurrences will speed up the calculation, but lower the precision of the result. It
# demands that some xgram must occur at least the specified amount of times for its divisors to be
# considered. Higher xgram counts occur less frequently, hence the speedup, but this lowers the
# amount of divisors we consider.
def kasiski(cipherText: str, widths: [int], maxKeyLen: int, minOccurrences: int = 2):

    minOccurrences = minOccurrences if minOccurrences > 2 else 2
    occurrences = {}

    for width in widths:
        widthOccurrences = {}

        # find trigrams and their locations
        for ind in range(len(cipherText) - width + 1):
            subStr = cipherText[ind:ind+width]
            widthOccurrences.setdefault(subStr, []).append(ind)

        # Trim to minOccurrences+ occurrences
        # Transform locations to distances
        # Trim off xgram strings
        widthOccurrences = [
            [locs[ind + 1] - locs[ind] for ind in range(len(locs) - 1)]
            for subStr, locs in widthOccurrences.items() if len(locs) >= minOccurrences
        ]

        # calc divisors
        divisors = {}
        for distances in widthOccurrences:
            for distance in distances:
                divisors[1] = divisors.setdefault(1, 0) + 1     # TODO just ignore 1, as |key| == 1 is caesar shift??
                for divisor in range(2, maxKeyLen + 1):
                    if divisor > distance >> 1:       # divisor > floor(distance/2)
                        break
                    if distance % divisor == 0:
                        divisors[divisor] = divisors.setdefault(divisor, 0) + 1
                divisors[distance] = divisors.setdefault(distance, 0) + 1


        occurrences[width] = divisors


    return occurrences


def ic(i, alphabet: [chr]):
    if isinstance(i, type([str])):
        return icf(i, alphabet)
    elif isinstance(i, str):
        return ics(i, alphabet)
    else:
        return 0.0


def icf(filenames: [str], alphabet: [chr]) -> float:
    charCounts = {char.upper(): 0 for char in alphabet}

    for filename in filenames:
        with open(filename, 'r') as file:

            if len(charCounts) == 0:
                return 0.0

            # calc character counts
            lineMax: int = 100
            line: str = file.readline(lineMax)
            while line != "":
                line = ''.join(c for c in unicodedata.normalize('NFD', line) if c.isalpha() and unicodedata.category(c) != 'Mn')
                for c in line:
                    charCounts[c.upper()] += 1
                line = file.readline(lineMax)

    # calc ic value
    icVal = 0.0
    total = 0.0
    for count in charCounts.values():
        icVal += count * (count - 1.0)
        total += count


    return icVal / (total * (total - 1))


def ics(text: str, alphabet: [chr]) -> float:
    charCounts = {char.upper(): 0 for char in alphabet}

    if len(charCounts) == 0:
        return 0.0

    text = ''.join(c for c in unicodedata.normalize('NFD', text)
                   if c.isalpha() and unicodedata.category(c) != 'Mn')
    text = text.upper()

    # calc character counts
    for c in text:
        charCounts[c] += 1

    # calc ic value
    icVal = 0.0
    total = 0.0
    for count in charCounts.values():
        icVal += count * (count - 1.0)
        total += count


    return icVal / (total * (total - 1))


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


"""
    A class that simulates a key in string form that contains only lower case
    OR upper case latin letters, not a combination of both.
    A key is generated from a seed. The seed is a value from
    0 to (26^keyLen)-1, where seed 0 corresponds to key 'AA ... AA'
    and seed (26^keyLen)-1 corresponds to 'ZZ ... ZZ'. The least significant
    character is at index 0 of the key.
    It provides incrementation and decrementation of the key.
"""
class KeyB26:
    def __init__(self, keyLen: int, seed: int, upper: bool = True):
        self.isUpper = upper
        self.key = self.generateKey(seed, keyLen)
        self.key = self.key.upper() if upper else self.key.lower()

    def __index__(self, index):
        if index >= self.__len__():
            return ""
        return self.key[index]

    def __len__(self):
        return len(self.key)

    """
        Acts as if the seed has just been incremented.
        Returns overflow boolean.
    """
    def incr(self):
        key = list(self.key)
        index: int = 0

        # find index to lend to and redistribute lent value
        while index < len(key) and key[index] == self.max():
            key[index] = sumChars(key[index], self.one())
            index += 1

        # lend value
        if index < len(self.key):
            key[index] = sumChars(key[index], self.one())

        self.key = ''.join(key)
        return index == len(self.key)

    """
        Acts as if the seed has just been decremented.
        Returns underflow boolean.
    """
    def decr(self):
        underflow: bool = False
        key = list(self.key)
        index: int = 0

        # find index to borrow from
        while index < len(key) and key[index] == self.zero():
            index += 1

        # handle underflow
        if index >= len(self.key):
            index -= 1
            underflow = True

        # redistribute borrowed value
        while index >= 0:
            key[index] = diffChars(key[index], self.one())
            index -= 1

        self.key = ''.join(key)
        return underflow

    def isalpha(self):
        return self.key.isalpha()

    def isCapital(self):
        return self.isUpper

    def generateKey(self, seed: int, keyLen: int):
        key = [''] * keyLen
        for index in range(keyLen - 1, -1, -1):
            charValue = seed // pow(26, index)
            if charValue > 25:
                continue
            key[index] = chr(charValue + 0x41)
            seed -= charValue * pow(26, index)

        return ''.join(key)

    def seed(self):
        seed: int = 0
        for i, c in enumerate(self.key):
            seed += (ord(c) % 0x41) * pow(26, i)
        return seed

    def one(self):
        return 'B'

    def max(self):
        return 'Z'

    def zero(self):
        return 'A'


