import copy
import time

from unidecode import unidecode

from src.Playfair.Playfair import playfair
from src.Utils import Frequencies
from src.Utils.Keys.KeyN10 import KeyN10
from src.Utils.LatinNGrams import LatinNGrams
from src.Utils.Statistics.statistics import *
from src.Vigenere.Vigenere import vigenere, invertedVigenere
from src.Vigenere.VigenerePlus import vigenerePlus

from src.Utils.FullEncryption import vigenerePlusEncryption
from src.Utils.Utils import invertedColumnTransposition, latinAlphabet, diffChars, isChrLatin, columnTransposition
from src.Utils.Keys.KeyB26 import KeyB26, toSeed
from src.Vigenere.VigenerePlus import VigenerePlusTextFrame



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





if __name__ == '__main__':
    pass



