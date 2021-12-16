
def read_morse (inputfile):
    text = open(inputfile, "r")
    file = open("morseDecoded.txt", "w")
    fileOutput = ""

    # split the text from the file into the morse letters
    splitted = text.read().split("/")

    output = list()

    for item in splitted:
        if item == '.-':    # if it is an 'a'
            output.append("A")
            fileOutput += "A"
        elif item == '-..':              # if it is a 'd'
            output.append("D")
            fileOutput += "D"
        elif item == '..-.':              # if it is a 'f'
            output.append("F")
            fileOutput += "F"
        elif item == '--.':              # if it is a 'g'
            output.append("G")
            fileOutput += "G"
        elif item == '...-':              # if it is a 'v'
            output.append("V")
            fileOutput += "V"
        elif item == '-..-':              # if it is a 'x'
            output.append("X")
            fileOutput += "X"

    file.write(fileOutput)
    file.close()
    return output
