

"""
    TODO  If the key A is pressed, then lamp A is cut off from the circuit and
     will never light up. This means that if you find an A at position i of the
     cipher text, then the plaintext will never contain an a at that location.
"""
import copy
from itertools import permutations
from math import factorial

from src.Enigma.Enigma import Enigma
from src.Enigma.PotentialGraph import PotentialGraph
from src.Utils.Keys.KeyB26 import KeyB26
from src.Utils.Keys.KeyN10 import KeyN10
from src.Utils.TextManipulation import latinAlphabet
from src.Utils.Utils import sumChars


def enigmaDecryption(ciphertext: str):
    rotorMappings = [
        ['A', "AJDKSIRUXBLHWTMCQGZNPYFVOE"],
        ['A', "EKMFLGDQVZNTOWYHXUSPAIBRCJ"],
        ['A', "BDFHJLCPRTXVZNYEIWGAKMUSQO"],
        ['A', "THEQUICKBROWNFXJMPSVLAZYDG"],
        ['A', "XANTIPESOKRWUDVBCFGHJLMQYZ"]
    ]

    selectedRotorsIndexes = [0, 1, 2]
    selectedRotors = [rotorMappings[i] for i in selectedRotorsIndexes]

    reflectorMapping = "YRUHQSLDPXNGOKMIEBFZCWVJAT"
    crib = "DEOPGAVEVOORENIGMA"
    cribGraph = {(ciphertext[i], crib[i]): i+1 for i in range(len(crib))}

    la = latinAlphabet(True)
    variableGraph: PotentialGraph = PotentialGraph()

    # Set up row connections
    # Cycling the potential graph will cycle all row connections (cycle k)
    for vertexPair in cribGraph.keys():
        cribIndex = cribGraph[vertexPair]
        rotorMapping = copy.deepcopy(selectedRotors)

        # update start position of rotors to reflect the eps_k+i rotor
        # state that this row connection encodes/requires
        # TODO  don't add i to EVERY rotor start state, add it to the overall start state AAA
        rotor = KeyB26(3, cribIndex)
        for i in range(3):
            rotorMapping[i][0] = sumChars(rotorMapping[i][0], la[cribIndex])

        # cipherRow, cribRow, eps_k+i
        variableGraph.addRowConnection(vertexPair[0], vertexPair[1], Enigma(la, rotorMapping, reflectorMapping))



    # TODO   guess k
    #   ==> If we suspect that some sigma(L1) = L2, then charge node at row L1 and col L2
    #   ==> This will lead to the symmetric nodes of (col, row)
    #   ==> Choose some vertex in the crib graph that is part of a lot of connected
    #       components/edges
    #   ==> choose connected graph vertex (T, G), because crib graph vertices T and G are the most
    #       well connected vertices in the crib graph
    #   ==> OR (E, G) OR (O, G)   --> others as well??


    # setup for while loop
    v = ("T", "G")
    rotorKey = KeyN10(5, 0)
    overflow = False

    # Try all rotor combinations
    while not overflow:
        rotorCombination = rotorKey.keyList()[:3]
        selectedRotors = [rotorMappings[i] for i in copy.deepcopy(rotorCombination)]

        # tune row connectors
        variableGraph.swapOutRotors(selectedRotors)

        for k in range(0, pow(26, 3)):

            if variableGraph.isGoodGraph(True, False):
                print(f"k : {k},  rotorComb = {rotorCombination}")

            # clean up
            variableGraph.resetCharge()
            variableGraph.cycle()

        overflow = rotorKey.incr() or rotorKey.incr()



    # pg.chargeNode("B", "C")
    # print(pg.toChargeString())
    # pg.resetCharge()
    # print(pg.toChargeString())

    pass


