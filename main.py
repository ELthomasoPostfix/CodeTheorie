import copy
import time

from src.Vigenere.Vigenere import vigenere, vigenereInverted
from src.Vigenere.VigenerePlus import vigenerePlus

from src.Utils.FullEncryption import vigenerePlusEncryption

from src.Utils.Utils import *



def icNederlands():
    alphabet = [chr(asciiVal) for asciiVal in range(65, 91)]
    texts = ["input/texts/antons tweestrijd.txt", "input/texts/Columbus de ontdekker van Amerika.txt",
             "input/texts/de vlegeljaren van Pietje Bell.txt", "input/texts/aan gene zijde van den evenaar.txt"]

    return ic(texts, alphabet)


def vig():
    plaintext = "BARRYISEENLIJPEKERELMAARHIJISWELKNAPTOCHVINDIKDATHARRYAANGENAMERISOMMEEOMTEGAANANDERZIJDSKANBARRYRAPHOOFDREKENENWATZEKERGRENZELOZETOEPASSINGSWAARDEHEEFTINDEWERELDDERVOLWASSENENWAARACHTIGDEKEUZEISZEERMOEILIJKGEMAAKTDEAAPEETEENRAAPOPEENSCHAAPMAAREENKNAAPJAAGTHEMWEG"
    cipherText = ""
    vkey = "BLIJTEN"
    ctkey = "POMMEDT"

    cipherText = vigenerePlusEncryption(plaintext, vKey=vkey, ctKey=ctkey)

    icVal = kasiski(cipherText, [3], 10)

    print(icVal)


def rec(nums, currStr, counter):
    arrows = ""
    for i in range(len(nums)):
        num = nums[i]
        newStr = currStr + str(num)
        if len(nums) == 1:
            counter += 1
            newStr += f" | {counter}"
        arrows += f"\"{currStr}\" -> \"{newStr}\" [label=\"{i}\", fontcolor=\"blue\"]\n"

        cpy = copy.deepcopy(nums)
        cpy.remove(num)
        result = rec(cpy, newStr, counter)
        arrows += result[0]
        counter = result[1]
    return arrows, counter


def recf(nums, currStr):
    arrows = ""
    for i in range(len(nums)):
        num = nums[i]
        newStr = currStr + str(num)

        cpy = copy.deepcopy(nums)
        cpy.remove(num)
        arrows += recf(cpy, newStr)
    if len(nums) == 0:
        return currStr + ","
    return arrows


def dot():
    res = "digraph {\n\n"
    res += "start\n"

    # node definitions
    nums = [n for n in range(4)]
    for i, num in enumerate(nums):
        res += str(num)
        if i < len(nums) -1:
            res += ","
    res += "\n\n"

    counter = -1
    for i in range(len(nums)):
        num = nums[i]
        res += f"start -> {num} [label=\"{i}\", fontcolor=\"blue\"]\n"

        cpy = copy.deepcopy(nums)
        cpy.remove(num)
        newStr = str(nums[i])
        result = rec(cpy, newStr, counter)
        res += result[0]
        counter = result[1]
    res += "\n"

    res += "}"
    return res


def numKeyTest(fileName):
    res = dot()

    with open(fileName, "w") as f:
        f.write(res)



if __name__ == '__main__':
    #vig()

    #numKeyTest("output/test.dot")

    pass



