

"""
    TODO  If the key A is pressed, then lamp A is cut off from the circuit and
     will never light up. This means that if you find an A at position i of the
     cipher text, then the plaintext will never contain an a at that location.
"""
import time

from src.Enigma.Enigma import Enigma
from src.Enigma.PotentialGraph import PotentialGraph
from src.Utils.Keys.KeyN10 import KeyN10
from src.Utils.TextManipulation import latinAlphabet


def enigmaDecryption(ciphertext: str):
    # !! IMPORTANT !! Assuming that all start states are A is ok, because we will cycle using the turing
    #   bomb to find k. The text representation/enigma state that k represents is the start state of
    #   the enigma machine for the given message
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
    cribGraph = {(ciphertext[i], crib[i]): i+1 for i in range(len(crib))}       # TODO  don't assume crib is at the very start?

    la = latinAlphabet(True)
    variableGraph: PotentialGraph = PotentialGraph()

    # Set up row connections
    # Cycling the potential graph will cycle all row connections (cycle k)
    for vertexPair in cribGraph.keys():
        cribIndex = cribGraph[vertexPair]

        # Update start position of rotors to reflect the eps_k+i enigma
        # state that this row connection encodes/requires
        # !! IMPORTANT !!  don't add i to EVERY rotor start state, add it to the overall start state, e.g. 'AAA' + i.
        #       Then adjust the connector enigma state to the new state.
        connector = Enigma(la, selectedRotors, reflectorMapping)
        connector.incrementRotorsState(cribIndex)

        # cipherRow, cribRow, eps_k+i       (here 'AAA' + i == 1 + i)
        variableGraph.addRowConnection(vertexPair[0], vertexPair[1], connector)



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

    t = time.time()
    of = open("output/Enigma/enigma.txt", 'w')

    batchCtr = 0
    maxBatch = 20

    # Try all rotor combinations (find 1/3 enigma settings: the rotor combination)
    while not overflow:
        # Choose rotor combination
        rotorCombination = rotorKey.keyList()[:3]
        selectedRotors = [rotorMappings[i] for i in rotorCombination]

        # Tune row connectors
        variableGraph.swapOutRotors(selectedRotors)

        # Loop over all possible rotor states
        # (find 2/3 enigma settings: the rotors state)
        for k in range(0, pow(26, 3)):

            # Charge the variable graph
            variableGraph.chargeNode(v[0], v[1])

            #print(variableGraph.toChargeString())

            if variableGraph.isPermutationMatrix(True):      # (find 3/3 enigma settings: the plug combination)
                of.write(f"{k} {rotorCombination}\n")
                #print(f"k (enigma start state/KeyB26 seed) : {k},\n  rotorComb = {rotorCombination}")

            # clean up
            variableGraph.resetCharge()
            variableGraph.cycle()

        overflow = rotorKey.incr() or rotorKey.incr()

    of.close()
    print(time.time() - t)

    # pg.chargeNode("B", "C")
    # print(pg.toChargeString())
    # pg.resetCharge()
    # print(pg.toChargeString())

    pass


