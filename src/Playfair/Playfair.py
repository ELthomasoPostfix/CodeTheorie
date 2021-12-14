from collections import OrderedDict
from src.Utils.Utils import latinAlphabet, toLatin


def playfair(plaintext: str, key: str):
    replaceable: str = 'J'.upper()
    substitute: str = 'I'.upper()
    filler: str = 'X'.upper()

    la = latinAlphabet(True)
    la.remove(replaceable)

    plaintext = toLatin(plaintext).upper().replace(replaceable, substitute)

    key = toLatin(key).upper().replace(replaceable, substitute)
    keyWord = ''.join(OrderedDict.fromkeys(key)) +\
          ''.join(sorted(list(set(la) - set(key))))

    digramText = ""
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
            digramText += c1 + filler
            c1, c2 = c2, ''
            i += 1
        else:
            digramText += c1 + c2
            c1, c2 = '', ''
            i += 2

    if i == len(plaintext) - 1:
        digramText += plaintext[-1] + filler

    # keyChar : (x, y)
    positions = { c: (i % 5, i // 5 if i else 0) for i, c in enumerate(keyWord) }
    rowSubstIndex = lambda loc: ((loc[0]+1) % 5) + loc[1]*5
    colSubstIndex = lambda loc: loc[0] + ((loc[1]+1) % 5)*5
    corSubstIndex = lambda locself, locother: locother[0] + locself[1]*5

    cipherText = ""
    for i in range(0, len(digramText) - 1, 2):
        loc1 = positions[digramText[i]]
        loc2 = positions[digramText[i+1]]

        # same row
        if loc1[0] == loc2[0]:
            cipherText += keyWord[rowSubstIndex(loc1)]
            cipherText += keyWord[rowSubstIndex(loc2)]
        # same col
        elif loc1[1] == loc2[1]:
            cipherText += keyWord[colSubstIndex(loc1)]
            cipherText += keyWord[colSubstIndex(loc2)]
        else:
            cipherText += keyWord[corSubstIndex(loc1, loc2)]
            cipherText += keyWord[corSubstIndex(loc2, loc1)]

    return cipherText

