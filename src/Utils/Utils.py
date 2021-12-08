import copy
import queue
from math import ceil, floor, factorial, log
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


def ic(textSource, alphabet: [chr]):
    if isinstance(textSource, type([str])):
        return icf(textSource, alphabet)
    elif isinstance(textSource, str):
        return ics(textSource, alphabet)
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
    A class that simulates a key in string form that contains only arithmetic numerals (the range {0, 1, ..., 9}).
    The string may only contain those arithmetic numerals in the range {0, 1, ..., keyLen}.
    The string may not contain any duplicate characters.
    A key is generated from a seed. The seed is a value from {0, 1, ..., keyLen! - 1}, where
    seed 0 corresponds to key '01 ... 89' and seed (keyLen! - 1) corresponds to '98 ... 10'.
    It provides incrementation and decrementation of the key, such that the key after the
    incr (decr) operation is the key generated by seed+1 (seed-1), with seed being the seed that
    generates the key from before incr (decr) was executed.
"""
class KeyN10:
    def __init__(self, keyLen: int, seed: int):
        keyLen = max(0, min(keyLen, 10))        # clamp 0 <= keyLen <= 10
        seed %= factorial(keyLen)
        self.__symbols = [num for num in range(keyLen)]

        self.__key, self.__indices = self.__generateKey(seed, keyLen)

        self.__cache = None
        self.__cacheIsValid = False

    def __index__(self, index):
        if index >= self.__len__():
            return None
        return self.__key[index]

    def __len__(self):
        return len(self.__key)

    """
        Acts as if index :i: of the seed has just been decremented. As the key may not contain any
        duplicate characters and contains only characters in the range {0, 1, ..., keyLen}, all characters
        from and including the specified index :i: cannot bet guaranteed to remain the same. Overflow of
        the incremented index may still alter characters at an index less than :i: through a carry value.
        :param i: The index to increment. Enforces i < len(key) - 1; the seed must be incremented by
                at least one. Indexation treats negative i values as indexing from the end to
                the front instead of front to end.
        Returns overflow boolean.
    """
    def incr(self, index: int = -1):
        self.__cacheIsValid = False

        # backtrack
        index %= self.__len__()
        backtrackList = self.__key[index:]
        prevBranch = self.__indices[index]
        prevMaxBranch = self.__len__() - index - 1

        while index > 0 and prevBranch == prevMaxBranch:
            index -= 1
            backtrackList.append(self.__key[index])

            prevBranch = self.__indices[index]
            prevMaxBranch += 1

        overflow = prevBranch == prevMaxBranch and len(backtrackList) == self.__len__()
        backtrackList.sort()

        branch = prevBranch + 1 if prevBranch < prevMaxBranch else 0
        self.__key[index] = backtrackList.pop(branch)
        self.__indices[index] = branch
        index += 1

        # rework
        for i in range(index, self.__len__()):
            self.__indices[i] = 0
            self.__key[i] = backtrackList.pop(0)


        return overflow

    """
        Acts as if index :i: of the seed has just been incremented. As the key may not contain any
        duplicate characters and contains only characters in the range {0, 1, ..., keyLen}, all characters
        from and including the specified index :i: cannot bet guaranteed to remain the same. Underflow of
        the decremented index may still alter characters at an index less than :i: through value borrowing.
        :param i: The index to decrement. Enforces i < len(key) - 1; the seed must be decremented by
                at least one. Indexation treats negative i values as indexing from the end to
                the front instead of front to end.
        Returns underflow boolean.
    """
    def decr(self, index: int = -1):
        self.__cacheIsValid = False

        # backtrack
        index %= self.__len__()
        backtrackList = self.__key[index:]
        prevBranch = self.__indices[index]
        MIN_BRANCH = 0   # constant

        while index > 0 and prevBranch == MIN_BRANCH:
            index -= 1
            backtrackList.append(self.__key[index])

            prevBranch = self.__indices[index]

        underflow = prevBranch == MIN_BRANCH and len(backtrackList) == self.__len__()
        backtrackList.sort()

        branch = prevBranch - 1 if prevBranch > MIN_BRANCH else len(backtrackList) - 1
        self.__key[index] = backtrackList.pop(branch)
        self.__indices[index] = branch
        index += 1

        # rework
        for i in range(index, self.__len__()):
            back = len(backtrackList) - 1
            self.__indices[i] = back
            self.__key[i] = backtrackList.pop(back)

        return underflow

    """
        Return the key in string form.
    """
    def key(self):
        self.__updateCache()
        return self.__cache

    """
        Return the key in list form.
    """
    def keyList(self):
        return self.__key

    """
        Return seed of the current key.
    """
    def seed(self):
        seed = 0
        nrChoices = self.__len__()

        for index in self.__indices:
            seed += index * factorial(nrChoices - 1)
            nrChoices -= 1

        return seed

    def __updateCache(self):
        if not self.__cacheIsValid:
            temp = [str(elem) for elem in self.__key]
            self.__cache = ''.join(temp)
            self.__cacheIsValid = True

    def __generateKey(self, seed: int, keyLen: int):
        key = []
        indices = []
        symbols = copy.deepcopy(self.__symbols)
        for nrChoices in range(keyLen, 0, -1):
            nrLeaves = factorial(nrChoices - 1)   # nr of leaves of any subtree on level keyLen - nrChoices (root==0)
            factor = seed / nrLeaves
            index = floor(factor)
            seed -= index * nrLeaves              # choosing subtree index (0 -> nrChoices) trims index*nrLeaves leaves

            res = symbols.pop(index)
            key.append(res)

            indices.append(index)

        return key, indices



"""
    A class that simulates a key in string form that contains only lower case
    OR upper case latin letters, never a combination of both.
    A key is generated from a seed. The seed is a value from
    0 to (26^keyLen)-1, where seed 0 corresponds to key 'AA ... AA'
    and seed (26^keyLen)-1 corresponds to 'ZZ ... ZZ'. The least significant
    character is at index 0 of the key.
    It provides incrementation and decrementation of the key. These operations require you to specify
    an index i to increment or decrement, such that the key after the incr(i) (decr(i)) operation is
    the key generated by seed+(26^i) (seed-(26^i)), with seed being the seed that
    generates the key before incr (decr) is executed.
"""
class KeyB26:
    def __init__(self, keyLen: int, seed: int, upper: bool = True):
        keyLen = keyLen if keyLen > 0 else 1

        self.isUpper = upper
        self.__key = self.__generateKey(seed, keyLen)
        self.__key = [c.upper() if upper else c.lower() for c in self.__key]

        self.__cache = ""
        self.__cacheIsValid = False

    def __index__(self, index):
        if index >= self.__len__():
            return ""
        return self.__key[index]

    def __len__(self):
        return len(self.__key)

    """
        Acts as if index i of the seed has just been incremented.
        :param i: The index to increment. The seed will be increased by 26^i. Indexation
                treats negative i values as indexing from the end to the front instead of front to end.
        Returns overflow boolean.
    """
    def incr(self, index: int = 0):
        self.__cacheIsValid = False
        key = self.__key
        index %= len(key)

        # Push carry value up
        while index < len(key) and key[index] == self.max():
            key[index] = sumChars(key[index], self.one())
            index += 1

        # Lend a value (final carry assignment)
        if index < len(key):
            key[index] = sumChars(key[index], self.one())

        return index == len(key)

    """
        Acts as if the seed has just been decremented.
        :param i: The index to decrement. The seed will be lowered by 26^i. Indexation
                treats negative i values as indexing from the end to the front instead of front to end.
        Returns underflow boolean.
    """
    def decr(self, i: int = 0):
        self.__cacheIsValid = False
        underflow: bool = False
        key = self.__key
        i %= len(key)
        index: int = i

        # find index to borrow from
        while index < len(key) and key[index] == self.zero():
            index += 1

        # handle underflow
        if index >= len(key):
            index -= 1
            underflow = True

        # redistribute borrowed value
        while index >= i:
            key[index] = diffChars(key[index], self.one())
            index -= 1

        return underflow

    """
        Return the key in string form.
    """
    def key(self):
        self.__updateCache()
        return self.__cache

    def isalpha(self):
        self.__updateCache()
        return self.__cache.isalpha()

    def iscapital(self):
        return self.isUpper

    """
        Return seed of the current key.
    """
    def seed(self):
        seed: int = 0
        self.__updateCache()
        for i, c in enumerate(self.__cache.upper()):
            seed += (ord(c) % 0x41) * pow(26, i)
        return seed

    def one(self):
        return 'B'

    def max(self):
        return 'Z'

    def zero(self):
        return 'A'

    def __updateCache(self):
        if not self.__cacheIsValid:
            self.__cache = ''.join(self.__key)
            self.__cacheIsValid = True

    def __generateKey(self, seed: int, keyLen: int):
        key = ['A'] * keyLen
        seed %= pow(26, keyLen)
        for index in range(keyLen - 1, -1, -1):
            powVal = pow(26, index)
            charValue = seed // powVal
            seed %= powVal
            if charValue <= 25:
                key[index] = chr(charValue + 0x41)

        return key

