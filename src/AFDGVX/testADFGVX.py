import ADFGVX


def adfgvxDecryption(input):
    output = ADFGVX.adfgvx(input)
    ADFGVX.writeOptionsToFile(output)



if __name__ == '__main__':
    adfgvxDecryption()
