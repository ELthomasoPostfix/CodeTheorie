"""
This file decrypts a message encrypted using first the vigenere technique and then
a single column transposition.

ct = kolom transpositie
v = vigenere
m = message
(  ct(v(m))  )⁻¹  =  (ct ° v)⁻¹(m) = (v⁻¹ ° ct⁻¹)(m) = v⁻¹(ct⁻¹(m))

"""
from itertools import permutations

from src.Utils.Keys.KeyN10 import KeyN10
from src.Utils.TextManipulation import latinAlphabet
from src.Utils.Utils import *
from src.Utils.Statistics.statistics import *
from src.Vigenere.TextFrames.VigenerePlusTextFrame import VigenerePlusTextFrame
from src.Vigenere.TextFrames.VigenerePlusTextFrame2 import VigenerePlusTextFrame2


def statComp(cipherText: str):
    resTxt = ""

    resTxt += "kasiski :\n"
    res = kasiski(cipherText, [3, 4], 10)
    for key in res.keys():
        subRes: dict = res[key]
        resTxt += f"\t{key} :\n"
        resTxt += "\t"*2 + str(sorted(subRes.items())) + "\n"

        for k in range(2, 11):
            multiples = []
            resTxt += "\t"*3
            for multiple in range(k, 100, k):
                if multiple in subRes.keys():
                    multiples.append((multiple, subRes[multiple]))
            tot = 0
            for m in multiples:
                tot += m[1]
            resTxt += (f"({tot} / {len(multiples)} = {tot / len(multiples)}) "if len(multiples) > 0 else "(0)") + "\n" + "\t"*4 + str(multiples) + "\n"

    resTxt += "\n"
    resTxt += "autocorrelation :\n"
    res= autocorrelation(cipherText, 100)
    resTxt += "\t\t" + str(res) + "\n"
    for k in range(2, 11):
        multiples = []
        resTxt += "\t" * 3
        for multiple in range(k, 100, k):
            if multiple in res.keys():
                multiples.append((multiple, res[multiple]))
        tot = 0
        for m in multiples:
            tot += m[1]
        resTxt += (f"({tot} / {len(multiples)} = {tot / len(multiples)}) " if len(multiples) > 0 else "(0)") + "\n" + "\t"*4 + str(multiples) + "\n"

    f = open("output/statistics.txt", 'w')
    f.write(resTxt)


def avgICs(cipherText: str):

    """
    step 1 : decode vig+ct into vig
    step 2 : load vig into frame
        The getAvgColumnIC() function will measure the avg ic of all columns. Thus, the order in which the
        ct technique scrambled the columns does not affect the avg ic of all columns (significantly?),
        as their individual ic remains the same? Just calculating the avg column ic per vigenere keyLen will result
        in likely key lengths, regardless of which seed was selected for a given ct key, as long as the ct key length
        is good.
    """

    # TODO important
    """
        open vigKeyLens.txt and spam run. ctKeyLen 5 and 10 come up often as highest avgs and also have
        the highest average values overall ==> ctKey of length 5???
    """


    output = ""     # TODO  output

    maxColAvg = 0
    mcaCTKeyLen = -1
    mcaPeriod = -1
    maxMulAvg = 0
    mmaCTKeyLen = -1
    mmaMul = -1

    for ctkeyLen in range(1, 9):
        ctkey = KeyN10(ctkeyLen, 0)
        overflow = False

        while not overflow:
            # output += f"ctkey :\tlen = {ctkeyLen} | key = '{ctkey.key()}' | seed = {ctkey.seed()}\n\n"    # TODO
            vgTextFrame = VigenerePlusTextFrame(invertedColumnTransposition(cipherText, ctkey.keyList()), rowWidth=ctkeyLen)

            # avg ic
            averages = []
            for vkeyLen in range(1, 11):
                vgTextFrame.reassignColumns(vkeyLen)
                avgIC = vgTextFrame.getAvgColumnIC()
                averages.append(avgIC)

            # multiples
            multiples = {}
            for keyLen in range(2, 11):
                sumAvgs = 0
                ctr = 0
                for key in range(keyLen - 1, 10, keyLen):
                    sumAvgs += averages[key]
                    ctr += 1
                multiples[keyLen] = sumAvgs / ctr

            # TODO  output
            # output += "period\t\t\tavg col ic\n"
            # for i, avg in enumerate(averages):
            #     output += str(i+1) + "\t"*2 + str(avg) + "\t\n"
            # output += "\n"
            #
            # output += "multiple\t\tavg ic\n"
            # for key in sorted(multiples.keys()):
            #     output += str(key) + "\t" * 2 + str(multiples[key]) + "\n"
            # output += "\n\n-------------------------------------------\n\n"

            for i, avg in enumerate(averages):
                if avg > maxColAvg:
                    maxColAvg = avg
                    mcaCTKeyLen = ctkeyLen
                    mcaPeriod = i + 1
            for mul, avg in multiples.items():
                if avg > maxMulAvg:
                    maxMulAvg = avg
                    mmaCTKeyLen = ctkeyLen
                    mmaMul = mul

            overflow = ctkey.incr()


    output = f"maxColAvg: period   = {mcaPeriod} | avg = {maxColAvg} | ctKeyLen = {mcaCTKeyLen}\n" +\
             f"maxMulAvg: multiple = {mmaMul} | avg = {maxMulAvg} | ctKeyLen = {mmaCTKeyLen}\n" +\
             "\n===========================================\n\n" +\
             output

    f = open("output/vigKeyLens.txt", 'w')
    f.write(output)



def getBestKey(cipherText: str, ctKey: KeyN10, vgKeyLen: int,
               starterWidth: int, starterPerms, trigrams: LatinNGrams,
               quadgrams: LatinNGrams, topKeyCap: int, textLenLimit: int = -1):

    # Limit the vigenere text to decipher. We may not limit the ciphertext before
    # the columnar transposition is inverted, as this would result in an incorrectly
    # deciphered columnar transposition.
    textLenLimit = len(cipherText) if textLenLimit < 1 else textLenLimit

    ctTF = VigenerePlusTextFrame2(
        invertedColumnTransposition(cipherText, ctKey.keyList())[:textLenLimit],
        vgKeyLen)

    currentBestKeys: List[tuple] = []

    t = time.time()

    for key in starterPerms:
        key = ''.join(key)
        ctTF.decipher(key)
        score = ctTF.score(starterWidth, trigrams)  # get ngram score for starterWidth decoded columns
        currentBestKeys.append((score, key))

    currentBestKeys.sort(reverse=True)
    currentBestKeys = currentBestKeys[:topKeyCap]

    print("part1 ", time.time() - t)

    newBestKeys: List[tuple] = []
    for remainingKeyChar in range(0, vgKeyLen - starterWidth):  # remaining key indexes
        for keyIndex in range(topKeyCap):
            for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':  # loop over alphabet
                key = currentBestKeys[keyIndex][1] + char  # increment key
                # TODO  deciphering with the letter A does nothing.
                #   By not lengthening the key with A's, we don't have to
                #   decipher all of the vigenere cipher. The VigenerePlusTextFrame2
                #   will only decipher columns 0 -> len(key)-1 and leave the columns
                #   len(key) -> vgKeyLen untouched.
                #   ==> less processing, as this does not impact the result
                # fullkey = key + 'A' * (vgKeyLen - len(key))     # fill out with A's
                # ctTF.decipherText(fullkey) # TODO makes use of filled out key, so also tests A-filled-deciphered columns

                ctTF.decipher(key)
                score = ctTF.score(len(key), quadgrams)
                newBestKeys.append((score, key))

        newBestKeys.sort(reverse=True)
        currentBestKeys = newBestKeys[:topKeyCap]  # keys to extend in next iteration
        newBestKeys = []

    # select best key
    bestkey = currentBestKeys[0][1]  # get best scoring key
    ctTF.decipher(bestkey)
    bestscore = ctTF.score(len(bestkey), quadgrams)  # plaintext quadgram score of best key
    for i in range(topKeyCap):
        key = currentBestKeys[i][1]
        ctTF.decipher(key)
        score = ctTF.score(len(key), quadgrams)
        if score > bestscore:
            bestkey = currentBestKeys[i][1]
            bestscore = score

    return bestscore, bestkey, ctKey.seed()


def writeResults(results, postfixCounter: int):
    results.sort(key=lambda k: k[0], reverse=True)
    fileName = f"2vigenerePlus_{postfixCounter}.txt"
    f = open(f"output/large2/{fileName}", 'w')
    for r in results:
        f.write(str(r) + "\n")
    f.close()
    print("past")


def vigenerePlusDecryption(cipherText: str, ctTextLimit: int = -1):


    """
    key = KeyN10(5, 0)                                                              # keyLen irrelevant for CT
    intermediate = invertedColumnTransposition(cipherText, key.keyList())
    print(ic(intermediate, latinAlphabet(True)))

    ==> 0.04266682146692596
    ==> (ic * 26) == 1.109337358140075
    ==> english ??
    """


    """
    statComp(cipherText)

    autocorrelation spikes at keyLen 7 (190 matches) and kasiski contains many multiples of 7 as divisors.
    Kasiski spikes at keyLen 2, with may multiples of 2 still having decent divisor counts.
    ==> keyLen == 7 or keyLen in [2, 4, 8] ??? 
    """

    avgICs(cipherText)


    """
    for keyLen in [7, 2, 4, 6, 8]:
        seed = random.randint(0, factorial(keyLen) - 1)
        key = KeyN10(keyLen, seed)
        vigText = VigenerePlusCiphertext(cipherText, rowWidth=keyLen)
        vigText = invertedColumnTransposition(cipherText, key.keyList())
    """

    ctTextLimit = len(cipherText) if ctTextLimit < 1 else ctTextLimit

    ctKeyLen = 8        # TODO  IS THIS REALLY THE CASE ????
    ctKey = KeyN10(ctKeyLen, 0) # TODO  set to 0 ????????????????????
    ctSeed = ctKey.seed()

    vgKeyLen = 7

    unfinishedCTIndex = -1
    unfinishedVGIndex = 0

    ctresults = []        # (vg, ctSeed, vgSeed)
    ctresults2 = []        # (vg, ctSeed, vgSeed)

    batchSize = 20
    batchCount = 0  # TODO  set to 0 ?????????????????
    sizeCounter = 0

    ctOverflow = False
    vgOverflow = False

    countFrequency = "CF"
    percentageFrequency = "PF"

    NGRAMPATH = "input/ngram data"
    PCPATH = "practicalcryptography.com"
    STPATH = "sttmedia.com"

    # TODO  'ß' is transformed to 'ss', how is 'ß' represented in the ciphers??? 'B' ??

    germanTrigrams = f"{NGRAMPATH}/{PCPATH}/german_trigrams.txt"
    germanQuadgrams = f"{NGRAMPATH}/{PCPATH}/german_quadgrams.txt"

    trigramsE: LatinNGrams = LatinNGrams(iPath=germanTrigrams, statType=countFrequency)
    quadgramsE: LatinNGrams = LatinNGrams(iPath=germanQuadgrams, statType=countFrequency)


    starterWidth = 3
    starterPerms = list(permutations(''.join(latinAlphabet(True)), starterWidth))
    topKeyCap = 800     # TODO  set to 800+ ????????????


    dirChosen = False
    keyDirLeft = False

    maxVeerSteps = 20
    veerCounter = 0

    progress = 0    # TODO set to some val
    maxProgress = factorial(8)
    stepSize = 100

    badStreak = 0
    maxBadStreak = 10

    prevRes = (-10000000, '', 0)


    ctKey = KeyN10(ctKeyLen, progress)

    ctr = 0

    # TODO werk met recursion depth ???
    #   ==> Divide range into 4 and select center seed
    #   ==> Divide subranges into 4 and select center seeds
    #   somehow select based on score

    # TODO  try counting the trigram counts for all column transpositions ?
    #   Then try matching trigrams to actual words
    #   e.g.    THE == 20 8  5
    #           VJG == 22 10 7
    #       a shift of 2 chars

    # TODO   when done, make a chart that maps ctSeed to score
    while progress < (maxProgress - maxVeerSteps):

        if dirChosen is False:
            prevRes = (-10000000, '', 0)
            ctKey = KeyN10(ctKeyLen, progress)
            ctSeed = ctKey.seed()

            middleVal = getBestKey(cipherText, ctKey, vgKeyLen, starterWidth,
                                   starterPerms, trigramsE, quadgramsE, topKeyCap,
                                   ctTextLimit)
            ctresults2.append(middleVal)
            sizeCounter += 1

            leftKey = KeyN10(ctKeyLen, ctSeed-1)
            leftVal = getBestKey(cipherText, leftKey, vgKeyLen, starterWidth,
                                 starterPerms, trigramsE, quadgramsE, topKeyCap,
                                 ctTextLimit)
            ctresults2.append(leftVal)

            ctKey.incr()
            rightKey = ctKey
            rightVal = getBestKey(cipherText, rightKey, vgKeyLen, starterWidth,
                                  starterPerms, trigramsE, quadgramsE, topKeyCap,
                                  ctTextLimit)
            ctresults2.append(rightVal)

            if middleVal > leftVal and middleVal > rightVal:
                progress += int(stepSize / 2)
                continue

            if leftVal > rightVal:
                keyDirLeft = True
                ctKey = leftKey
                leftKey.decr()
                prevRes = leftVal

            else:
                keyDirLeft = False
                rightKey.incr()
                prevRes = rightVal

            sizeCounter += 1
            veerCounter += 1
            dirChosen = True
            continue

        if veerCounter >= (maxVeerSteps + 5 * (badStreak < maxBadStreak)) or\
                badStreak >= maxBadStreak:
            progress += stepSize
            ctKey = KeyN10(ctKeyLen, progress)
            veerCounter = 0
            badStreak = 0
            dirChosen = False
            continue

        # TODO \/ \/ \/ attempt 2: ngrams
        #   !! IMPORTANT !!
        #   Adapted the code from break_vigenere.py from
        #       practicalcryptography.com
        #   to fit this project
        # The text is now only vigenere encrypted. It is divided into its vgKeyLen vigenere columns.

        t = time.time()

        res = getBestKey(cipherText, ctKey, vgKeyLen, starterWidth,
                         starterPerms, trigramsE, quadgramsE, topKeyCap,
                         ctTextLimit)
        ctresults2.append(res)

        badStreak += prevRes > res
        print("eyo 1 ", prevRes)
        prevRes = res
        print("eyo 2 ", prevRes)


        veerCounter += 1

        diff = time.time() - t
        print("total ", diff, f"  {diff/60} mins")


        if keyDirLeft is True:
            ctKey.decr()
        else:
            ctKey.incr()

        sizeCounter += 1

        # Write current progress, but keep progress it in memory
        if sizeCounter < 0 or sizeCounter >= batchSize:
            sizeCounter = 0
            print(len(ctresults))
            writeResults(ctresults2, batchCount)
            batchCount += 1



        ctr += 1
        print(ctr)
        print(ctKey.seed())
        print(veerCounter)


        # TODO \/ \/ \/ duurt te lang; te veel vig keys om af te gaan

        # # The text is now only vigenere encrypted. It is divided into its vgKeyLen vigenere columns.
        # ctTF = VigenerePlusTextFrame(invertedColumnTransposition(cipherText, ctKey.keyList()), vgKeyLen)
        #
        #
        #
        # t = time.time()
        # keys = [(0, KeyB26(vgKeyLen, 0))]
        # # Per column, find good key chars
        # for col in range(vgKeyLen):
        #     newKeys = []
        #     # Per partially found key, choose 5 best extended keys
        #     for kic, key in keys:
        #         results = []
        #
        #         # Setup unchanging vigenere columns
        #         for i in range(col):
        #             ctTF.vigColumn(i, key[i])
        #
        #         sub = key.key()[max(0, col - 2):col]
        #
        #         # Cycle vigenere column
        #         # Note that any key[i] = 'A', for i > col
        #         for i in range(26):
        #
        #             if sub.count(key[col]) == 2 or key.key().count(key[col]) > 3:
        #                 key.incr(col)
        #                 continue
        #             ctTF.vigColumn(col, key[col])
        #             icV = ctTF.getColumnsIC(col)
        #
        #             results.append((icV, key.seed()))
        #             key.incr(col)
        #
        #         results.sort(reverse=True)
        #         newKeys.extend([res for res in results[:8]])
        #
        #     # Limit partial keys to the best ones (key ic clamp, then key count clamp)
        #     #newKeys = [newKey for newKey in newKeys if newKey[0] >= min(0.01 * col, 0.06)]
        #     newKeys.sort(reverse=True)
        #     keys = [(res[0], KeyB26(vgKeyLen, res[1])) for res in newKeys[:250]]
        # diff = time.time() - t
        # print(diff, f"   {diff / 60} mins")
        # print("|keys| ", len(keys))
        # print("|ctres| ", len(ctresults))
        #
        # if len(keys) > 0:
        #     ctresults.extend([(key[0], key[1], ctSeed) for key in keys])
        #     sizeCounter += 1
        #
        # if len(keys) < 100:
        #     ctOverflow = ctKey.incr() or ctKey.incr()
        #
        # if sizeCounter == batchSize:
        #     sizeCounter = 0
        #     print(len(ctresults))
        #     ctresults.sort(key=lambda k: k[0], reverse=True)
        #     f = open(f"output/large/4vigenerePlus_{batchCount}.txt", 'w')
        #     for r in ctresults:
        #         f.write(str(r) + "\n")
        #     print("past")
        #     f.close()
        #     batchCount += 1
        #     ctresults = []

    print("store remaining")

    sizeCounter = 0
    print(len(ctresults))
    writeResults(ctresults2, batchCount)
    batchCount += 1

    print("end vigenere")



    """
    If keyLens found, then
    
    for ctkey of len ctKeyLen:
        tf = VGPlusTF(invCT(ciphertext), vgKeyLen)             # tf.__columns are vigenere columns, where a single column was affected by a ceasar transposition
        for vgkey of len vgKeyLen:
            for column in range(vgKey)
            tf.reassignColumn()
            
    """


