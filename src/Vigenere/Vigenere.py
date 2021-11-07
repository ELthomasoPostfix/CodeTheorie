"""
This file implements the vigenere and column transposition encryption techniques.
"""


def vigenere(msg: str, key: str) -> str:
    transformedMsg: str = ""



    return transformedMsg


def columnTransposition(msg: str, key: str) -> str:
    transposed = ""

    msg = msg.lower()
    key = key.lower()
    s = sorted(key)
    m: dict = {c: v for c, v in enumerate(s)}
    columns = [(-1, -1)] * len(key)   # (sorted key index, unsorted key index)

    for pair in m.items():
        for index in range(len(key)):
            if key[index] == pair[1] and columns[index][0] == -1:
                columns[index] = (pair[0], index)
                break

    # sort the columns based on assigned numerical value (sort a-z)
    columns = sorted(columns, key=lambda pair: pair[0])

    for col in columns:
        msgInd = col[1]
        while msgInd < len(msg):
            transposed += msg[msgInd]
            msgInd += len(key)

    return transposed
