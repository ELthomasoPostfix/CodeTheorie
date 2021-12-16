import readMorse


def test():
    input = "../../input/ADFGVX.txt"

    output = readMorse.read_morse(input)
    print(output)


if __name__ == '__main__':
    test()
