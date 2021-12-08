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





if __name__ == '__main__':
    pass



