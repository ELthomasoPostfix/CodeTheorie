from src.Utils.Statistics.statistics import ic
from src.Utils.Utils import toLatin


def icDutch():
    alphabet = [chr(asciiVal) for asciiVal in range(65, 91)]
    texts = ["input/texts/antons tweestrijd.txt", "input/texts/Columbus de ontdekker van Amerika.txt",
             "input/texts/de vlegeljaren van Pietje Bell.txt", "input/texts/aan gene zijde van den evenaar.txt"]

    return ic(texts, alphabet)


def trigramFreqDutch(sorted:bool = True):

    texts = ["input/texts/antons tweestrijd.txt", "input/texts/Columbus de ontdekker van Amerika.txt",
             "input/texts/de vlegeljaren van Pietje Bell.txt", "input/texts/aan gene zijde van den evenaar.txt"]

    threeGrams = {}
    store = ""
    ngramSize = 3
    for fileName in texts:
        f = open(fileName, 'r')
        txt = ""
        ctr3 = 100
        while len(txt) < ngramSize and ctr3 > 0:
            txt += toLatin(f.read(1)).upper()
            ctr3 -= 1

        while len(txt) >= ngramSize:
            threeGrams[txt] = threeGrams.setdefault(txt, 0) + 1
            txt = txt[1:]

            ctr2 = 10
            while store == "" and ctr2 > 0:
                store = toLatin(f.read(10)).upper()
                ctr2 -= 1
            if store == "":
                continue

            txt += store[0]
            store = store[1:]
        f.close()


    totalFreq = 0.0
    totalCount = sum(threeGrams.values())

    if sorted:
        threeGrams = list(threeGrams.items())
        threeGrams.sort(key=lambda p: p[1], reverse=True)
        fo = open("input/ngram data/sttmedia.com/dutch_trigrams_self_calculated.txt", 'w')
        for data in threeGrams:
            freq = data[1] / totalCount
            totalFreq += freq
            fo.write(data[0] + " " + str(freq) + "\n")
        fo.close()
    else:
        fo = open("input/ngram data/sttmedia.com/dutch_trigrams_self_calculated.txt", 'w')
        for key in threeGrams.keys():
            freq = threeGrams[key] / totalCount
            totalFreq += freq
            fo.write(key + " " + str(freq) + "\n")
        fo.close()

