
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
import collections
import time
import unicodedata
from src.Utils.Utils import toLatin


def kasiski(cipherText: str, widths: [int], maxKeyLen: int, minOccurrences: int = 2, includeOne: bool = False):

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
                if includeOne:
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
                line = toLatin(line)
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
    for char, count in collections.Counter(text).items():
        charCounts[char] = count


    # calc ic value
    icVal = 0.0
    total = 0.0
    for count in charCounts.values():
        icVal += count * (count - 1.0)
        total += count


    return icVal / (total * (total - 1))


def autocorrelation(text: str, maxShift: int):
    shiftMatches = {}

    for shift in range(1, maxShift+1):
        matches = 0
        shiftedIndex = 0
        for originalIndex in range(shift, len(text)):
            matches += text[originalIndex] == text[shiftedIndex]
            shiftedIndex += 1

        shiftMatches[shift] = matches

    return shiftMatches

