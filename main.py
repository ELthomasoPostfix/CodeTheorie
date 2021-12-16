from src.Enigma.EnigmaDecryption import enigmaDecryption
from src.Playfair.PlayfairDecryption import playfairDecryption
from src.Utils.TextManipulation import toLatin
from src.Vigenere.VigenerePlusDecryption import vigenerePlusDecryption
from src.AFDGVX.testADFGVX import adfgvxDecryption







def vigenerePlus(testText: str = None, ctTextLenLimiter: int = -1):
    vgPlusCipherText = ""
    if testText is None or testText == "":
        file = open("input/Vigenere input.txt")
        vgPlusCipherText = toLatin(file.read())
    else:
        vgPlusCipherText = testText

    vigenerePlusDecryption(vgPlusCipherText, ctTextLenLimiter)


def playfair(testText: str = None):
    playfairCipherText = ""
    if testText is None or testText == "":
        file = open("input/Playfair input.txt")
        playfairCipherText = toLatin(file.read())
    else:
        playfairCipherText = testText

    playfairDecryption(playfairCipherText)


def enigma(testText: str = None):
    enigmaCipherText = ""
    if testText is None or testText == "":
        file = open("input/Enigma input.txt")
        enigmaCipherText = toLatin(file.read())
    else:
        enigmaCipherText = testText

    enigmaDecryption(enigmaCipherText)



def ADFGVX():
    adfgvxDecryption("input/ADFGVX.txt")


if __name__ == '__main__':

    # No arg or None means using file text

    # vigenerePlus(ctTextLenLimiter=300)

    # playfair(None)

    # enigma(None)

    # ADFGVX()

    print("end main")



