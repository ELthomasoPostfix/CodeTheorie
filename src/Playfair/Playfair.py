from collections import OrderedDict
from typing import List

from src.Playfair.Substitution import Substitution
from src.Utils.Utils import latinAlphabet, toLatin


def playfair(plaintext: str, keyWord: str):
    replaceable: str = Substitution.REPLACEABLE.upper()
    substitute: str = Substitution.SUBSTITUTE.upper()
    filler: str = Substitution.FILLER.upper()

    la = latinAlphabet(True)
    la.remove(replaceable)

    plaintext = toLatin(plaintext).upper().replace(replaceable, substitute)

    keyWord = toLatin(keyWord).upper().replace(replaceable, substitute)
    key = ''.join(OrderedDict.fromkeys(keyWord)) +\
              ''.join(sorted(list(set(la) - set(keyWord))))

    ciphertext = ""
    c1: str = ''
    c2: str = ''
    i: int = 0
    while i < len(plaintext) - 1:

        # assign digram
        if c1 == '':
            c1 = plaintext[i]
            c2 = plaintext[i+1]
        # prev iteration used filler
        else:
            c2 = plaintext[i+1]

        # filler necessary
        if c1 == c2:
            ciphertext += c1 + filler
            c1, c2 = c2, ''
            i += 1
        else:
            ciphertext += c1 + c2
            c1, c2 = '', ''
            i += 2

    if i == len(plaintext) - 1:
        ciphertext += plaintext[-1] + filler

    # keyChar : (x, y)
    positions = { c: (i % 5, i // 5) for i, c in enumerate(key) }
    rowSubstIndex = lambda loc: ((loc[0]+1) % 5) + loc[1]*5
    colSubstIndex = lambda loc: loc[0] + ((loc[1]+1) % 5)*5
    corSubstIndex = lambda locself, locother: locother[0] + locself[1]*5

    cipherText = ""
    for i in range(0, len(ciphertext) - 1, 2):
        loc1 = positions[ciphertext[i]]
        loc2 = positions[ciphertext[i+1]]

        # same col (x)  --> go down
        if loc1[0] == loc2[0]:
            cipherText += key[colSubstIndex(loc1)]
            cipherText += key[colSubstIndex(loc2)]
        # same row (y)  --> go right
        elif loc1[1] == loc2[1]:
            cipherText += key[rowSubstIndex(loc1)]
            cipherText += key[rowSubstIndex(loc2)]
        # rectangle     --> same row corner
        else:
            cipherText += key[corSubstIndex(loc1, loc2)]
            cipherText += key[corSubstIndex(loc2, loc1)]

    return cipherText, key



def invertedPlayfair(ciphertext: str, keyWord):

    """
    Deciphers playfair encoded ciphertext using a keyword.
    :param ciphertext: To decode text. Must be of even length
    :param keyWord: To use keyword. Must be of length 25. May contain any combination of unique characters.
    Must be of type str or List[str].
    :return: The decoded text in string form.
    """

    # keyChar : (x, y)      with x in {0, 1, 2, 3, 4} and y in {0, 5, 10, 15, 20}
    positions = { c: (i % 5, (i // 5)*5) for i, c in enumerate(keyWord) }

    plaintext = [''] * len(ciphertext)
    for i in range(0, len(ciphertext) - 1, 2):
        loc1 = positions[ciphertext[i]]
        loc2 = positions[ciphertext[i+1]]

        # same col (x)  --> go up
        if loc1[0] == loc2[0]:
            plaintext[i]   = keyWord[loc1[0] + ((loc1[1]-5) % 25)]
            plaintext[i+1] = keyWord[loc2[0] + ((loc2[1]-5) % 25)]
        # same row (y)  --> go left
        elif loc1[1] == loc2[1]:
            plaintext[i]   = keyWord[((loc1[0]-1) % 5) + loc1[1]]
            plaintext[i+1] = keyWord[((loc2[0]-1) % 5) + loc2[1]]
        # rectangle     --> same row corner
        else:
            plaintext[i]   = keyWord[loc2[0] + loc1[1]]
            plaintext[i+1] = keyWord[loc1[0] + loc2[1]]

    return ''.join(plaintext)



