from src.Utils.Keys.KeyN10 import KeyN10
from src.Utils.Utils import columnTransposition, invertedColumnTransposition
from src.Utils.Statistics.statistics import ic
from src.AFDGVX.readMorse import read_morse

def thomasADFGVX ():
    file = "../../input/ADFGVX.txt"
    text = read_morse(file)

    output = ""  # TODO  output

    maxIC = -1
    maxCTKeyLen = -1
    maxSeed = 0


    combs = []
    for s1 in 'ADFGVX':
        for s2 in 'ADFGVX':
            combs.append(s1+s2)

    # TODO : add list of lists, the outer list contains lists for every length we discuss
    # TODO : every inner list contains the key and its frequencies, we go check if one corresponds to a language later

    for ctkeyLen in range(1, 9):
        print(ctkeyLen)
        ctkey = KeyN10(ctkeyLen, 0)
        overflow = False

        while not overflow:
            output += f"ctkey :\tlen = {ctkeyLen} | key = '{ctkey.key()}' | seed = {ctkey.seed()}\n\n"    # TODO
            ADFGVXtext = (invertedColumnTransposition(text, ctkey.keyList()))

            icVal = ic(ADFGVXtext, combs, True)
            output += f"ic value = {icVal}\n"

            bigramFreqs = {b: 0 for b in combs}
            for i in range(0, len(ADFGVXtext) - 1, 2):
                bigram = ADFGVXtext[i] + ADFGVXtext[i+1]
                bigramFreqs[bigram] += 1

            output += f"total bigram count = {sum(bigramFreqs.values())}\n\n"

            bigramFreqs = sorted(list(bigramFreqs.items()), key=lambda p: p[1], reverse=True)
            output += "bigram\t\tfrequency\n"
            for p in bigramFreqs:
                output += p[0] + "\t"*3 + str(p[1] / len(ADFGVXtext) / 2.0) + "\n"
            output += "\n\n-------------------------------------------\n\n"

            if icVal > maxIC:
                maxIC = icVal
                maxCTKeyLen = ctkeyLen
                maxSeed = ctkey.seed()

            overflow = ctkey.incr()

    outputHeader = f"maxIC = {maxIC} | ctKeyLen = {maxCTKeyLen} | maxSeed = {maxSeed}\n" + \
                       "\n===========================================\n\n"

    of = open("../../output/ADFGVX_CT_stats.txt", 'w')
    of.write(outputHeader)
    of.write(output)
    of.close()


def adfgvx ():
    file = "../../input/ADFGVX.txt"
    text = read_morse(file)

    combs = []
    for s1 in 'ADFGVX':
        for s2 in 'ADFGVX':
            combs.append(s1 + s2)

    # TODO : add list of lists, the outer list contains lists for every length we discuss
    # TODO : every inner list contains the key and its frequencies, we go check if one corresponds to a language later
    # For every key length
    for ctKeyLen in range(1, 11):            # we check every key of length 1 to 10


        # setup for while loop
        ctKey = KeyN10(ctKeyLen, 0)
        overflow = False



        # loop over all possible ct keys of length ctKeyLen
        while not overflow:
            ADFGVXtext = invertedColumnTransposition(text, ctKey.keyList())

            # body

            overflow = ctKey.incr()         # last key tested?

