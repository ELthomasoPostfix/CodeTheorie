import math
import random
import sys
import time
from typing import List

from src.Playfair.Playfair import invertedPlayfair
from src.Playfair.Substitution import Substitution
from src.Playfair.TextFrames.PlayfairManualTextFrame import PlayfairManualTextFrame
from src.Utils.LatinNGrams import LatinNGrams
from src.Utils.Utils import writePairList, latinAlphabet, swap2rows, copyList, swap2cols, exchange2letters


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
                    storedPath:str, measuredPath: str, combinedPath: str):

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


def generateFiles(cipherText: str):
    countFreq = "CF"
    percentFreq = "PF"

    storedMonoPath = "input/ngram data/practicalcryptography.com/english_monograms.txt"
    measuredMonoPath: str = "output/Playfair/playfairmonogramCounts.txt"
    combinedMonoPath = "output/Playfair/cmonogramCounts.txt"
    generateMonoFiles(cipherText, countFreq, storedMonoPath, measuredMonoPath, combinedMonoPath)

    storedBiPath = "input/ngram data/practicalcryptography.com/english_bigrams.txt"
    measuredBiPath: str = "output/Playfair/playfairbigramCounts.txt"
    combinedBiPath = "output/Playfair/cbigramCounts.txt"
    generateBiFiles(cipherText, countFreq, storedBiPath, measuredBiPath, combinedBiPath)



def decipherTest1(cipherText: str):
    pTF = PlayfairManualTextFrame(cipherText)

    # Load digram statistics
    englishBigrams = LatinNGrams("input/ngram data/practicalcryptography.com/english_bigrams.txt",
                                 "CF", toLogFreq=False)
    enBigrams = sorted(englishBigrams.getFrequenciesList(), key=lambda p: p[1], reverse=True)
    playfairBigrams = LatinNGrams("output/Playfair/playfairbigramCounts.txt", "CF", toLogFreq=False)
    pfBigrams = sorted(playfairBigrams.getFrequenciesList(), key=lambda p: p[1], reverse=True)

    # try most probable mapping pairs
    for i in range(50):
        enBigram = enBigrams[i][0]
        if enBigram[0] != enBigram[1]:
            pTF.defineMapping(pfBigrams[i][0], enBigrams[i][0])


    pTF.decipher()

    print(pTF.text)
    print(pTF.getBigramRepresentation())

    print(pTF.getDecipheredBigramRepresentation())
    print(pTF.toDecipheredBigramSubstring("FINA", 0))
    print(pTF.decipheredText)

    surroundings = pTF.getSurroundings('THE', 10)

    for s in surroundings:
        print(s)

    print()
    #print(pTF.getMappingRepresentation())




def modifyKey(newKey: List[str], oldKey: List[str]):
    i = random.randint(0, 49)

    if i == 0:
        copyList(newKey, oldKey)
        swap2rows(newKey)
    elif i == 1:
        copyList(newKey, oldKey)
        swap2cols(newKey)
    elif i == 2:
        copyList(newKey, oldKey, reverse=True)
    # swap rows up-down
    elif i == 3:
        for k in range(5):
            k *= 5
            for j in range(5):
                newKey[k + j] = oldKey[20 - k + j]      # read   newKey[5*k + j] = oldKey[(4 - k)*5 + j]
    # swap cols left-right
    elif i == 4:
        for k in range(5):
            for j in range(5):
                newKey[j * 5 + k] = oldKey[(4 - j) * 5 + k]
    else:
        copyList(newKey, oldKey)
        exchange2letters(newKey)



def playfairCrack(ciphertext: str, bestKey: List[str], qgrams: LatinNGrams, tgrams: LatinNGrams, bgrams: LatinNGrams,
                  TEMP_START: float, TEMP_STEP: float, COUNT: int):

    deciphered: str
    testKey = [""] * 25
    maxKey = [""] * 25

    prob: float
    dF: float
    maxScore: float
    score: float
    bestScore: float

    copyList(maxKey, bestKey)
    deciphered = invertedPlayfair(ciphertext, maxKey)
    maxScore = qgrams.score(deciphered)
    maxScore += tgrams.score(deciphered)
    maxScore += bgrams.score(deciphered)
    bestScore = maxScore        # current optimum score

    temperature: float = TEMP_START
    while temperature >= 0:
        t = time.time()        # TODO del
        for currCount in range(COUNT):
            modifyKey(testKey, maxKey)      # choose child key

            deciphered = invertedPlayfair(ciphertext, testKey)
            score = qgrams.score(deciphered)
            score += tgrams.score(deciphered)
            score += bgrams.score(deciphered)

            dF = score - maxScore

            # child > parent
            if dF >= 0:
                maxScore = score
                copyList(maxKey, testKey)   # child ==> parent
            # not yet greedy algorithm
            elif temperature > 0:
                prob = pow(math.e, dF / temperature)
                # chance to select worse child as parent
                if prob > (random.randint(0, sys.maxsize) / sys.maxsize):
                    maxScore = score
                    copyList(maxKey, testKey)
            # store best score so far
            if maxScore > bestScore:
                bestScore = maxScore
                copyList(bestKey, maxKey)

        temperature -= TEMP_STEP
        if temperature < TEMP_START/2:
            print("temp at ", temperature)
        diff = time.time() - t              # TODO del
        print(diff, f"   {diff/60} mins")   # TODO del
    return bestScore




def playfairDecryption(cipherText: str):
    cipherText = cipherText.upper()[:100]#1500]      # TODO 1500 / 4252 ???

    TEMP_START: int = 20 #20
    TEMP_STEP: float = .2       # TODO .5  ==> relatively quickly restricts to high values
    ITERATIONS: int = 1000 #5000     # TODO high for textLen of 1500?

    score: float
    key: List[str] = latinAlphabet(True)
    key.remove(Substitution.REPLACEABLE)
    maxScore: float = -sys.float_info.max
    bestKey: List[str] = [""] * 25
    bestText: str

    batchCtr: int = 2

    ofPath = "output/Playfair/large"

    qgramPath = "input/ngram data/practicalcryptography.com/english_quadgrams.txt"
    qgrams: LatinNGrams = LatinNGrams(qgramPath, "CF")
    tgramPath = "input/ngram data/practicalcryptography.com/english_trigrams.txt"
    tgrams: LatinNGrams = LatinNGrams(tgramPath, "CF")
    bgramPath = "input/ngram data/practicalcryptography.com/english_bigrams.txt"
    bgrams: LatinNGrams = LatinNGrams(bgramPath, "CF")



    print(f"Starting up playfair decryption with the following parameters:\n\
            \tstart temp : {TEMP_START}\n\
            \ttemp step  : {TEMP_STEP}\n\
            \titerations : {ITERATIONS}")


    iteration: int = 0
    while True:
        print(f"start iteration {iteration}")
        score = playfairCrack(cipherText, key, qgrams, tgrams, bgrams,
                              TEMP_START, TEMP_STEP, ITERATIONS)
        print(score, maxScore)
        if score > maxScore:
            maxScore = score
            copyList(bestKey, key)
            bestText = invertedPlayfair(cipherText, key)
            print(f"Best score so far : {score}        (iteration {iteration})")
            print(f"Best key so far   : {''.join(key)}")

            # write to file
            of = open(f"{ofPath}/playfair_3_{batchCtr}.txt", 'w')
            of.write(str(score) + "\n")
            of.write(''.join(bestKey) + "\n")
            of.write(bestText)
            of.close()

            # incr filename postfix
            batchCtr += 1

        else:
            print("No better score during iteration", iteration)

        iteration += 1





# TODO  delete ???
def rubbish(cipherText: str):
    #decipherTest1(cipherText)
    #return



    # TODO   step 1: analysis
    #generateFiles(cipherText)


    # replace two most frequent measured by
    # two most frequent stored
    pTF = PlayfairManualTextFrame(cipherText)
    pTF.replaceDeciphered('P', 'E')
    pTF.replaceDeciphered('A', 'T')

    # TODO   In the original ciphertext any trigram 'THE' would actually
    #   be the trigram 'A.P'
    missingChar = 'H'
    completions = pTF.findCompletions(['T', '', 'E'])

    # update base text for use in loop
    pTF.updateText()

    # Find the char which when replaced by 'H' results
    # in the highest 'THE' count in the current text
    counts = []
    for comp in completions:
        pTF.replaceCiphered(comp[1], missingChar)
        counts.append((pTF.count('THE'), comp[1]))

    # reset to preloop state
    pTF.decipheredText = pTF.text
    pTF.text = cipherText
    progress = pTF.decipheredText




    # Apply replacement of found char by 'H'.
    # This results in a text with many 'THE' trigrams
    bestCount = max(counts)
    pTF.replaceDeciphered(bestCount[1], missingChar)

    biMappingsTH = pTF.findBiMappingsTo('TH')
    biMappingsHE = pTF.findBiMappingsTo('HE')

    sTH = set(biMappingsTH)
    sHE = set(biMappingsHE)

    print(biMappingsTH)
    print({f: biMappingsTH.count(f) for f in sTH})
    print("-> TH")
    print(biMappingsHE)
    print({f: biMappingsHE.count(f) for f in sHE})
    print("-> HE")


    # print(bestCount, f"{bestCount[1]} -> {missingChar}")
    # print(pTF.decipheredText)
    # print(pTF.getDecipheredBigramRepresentation())
    # surroundings = pTF.getSurroundings('THE', 10)
    # for c in surroundings:
    #     print(c)













