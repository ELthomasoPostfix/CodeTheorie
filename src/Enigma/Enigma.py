from typing import List
from src.Enigma.Mapper import Mapper, MessageDirection
from src.Utils.Keys.KeyB26 import KeyB26, toSeed
from src.Utils.TextManipulation import latinAlphabet
from src.Utils.Utils import sumChars, diffChars


class Rotor:
    def __init__(self, startState: str, mapping: str):
        la = latinAlphabet(True)
        if len(mapping) != 26 or set(la) != set(mapping):
            raise ValueError("Rotor must have a mapping from and to the latin alphabet")

        if len(startState) != 1:
            raise ValueError("Rotor start state must be of length 1")

        self.startState = startState
        self.state = None
        self.resetState()
        self.__mapping: Mapper = Mapper(la, mapping)

    def map(self, direction: int, value: str):
        return diffChars(self.__mapping.get(direction, sumChars(value, self.state.key())), self.state.key())

    def incr(self) -> bool:
        return self.state.incr()

    def resetState(self):
        self.state = KeyB26(1, ord(self.startState.upper()) % 0x41)



class Enigma:
    def __init__(self, plugMapping, rotorMappings: List, reflectorMapping):

        """
        Models an enigma machine.
        :param plugMapping: The ordered iterable that the values 'ABC...XYZ'
            are mapped to. It pertains to the plug board of the enigma machine.
            We assume
                A -> plugMap[0]
                B -> plugMap[1]
                ...
                Z -> plugMap[25]
        :param rotorMappings: A list of pairs of a character and an ordered iterable to which the values
            'ABC...XYZ' are mapped to. The character is the start state of the given rotor. The rotors
             are specified fast/middle/slow in order. We assume
                A -> rotMap[0][0]
                B -> rotMap[0][1]
                ...
                Z -> rotMap[0][25]
                A -> rotMap[1][0]
                ...
                Z -> rotMap[2][25]
        :param reflectorMapping: The ordered iterable that the values 'ABC...XYZ'
            are mapped to. It pertains to the reflector of te enigma machine. We assume
                A -> reflMap[0]
                B -> reflMap[1]
                ...
                Z -> reflMap[25]
        """
        la = latinAlphabet(True)

        for mapping in rotorMappings:
            if mapping[0] not in la:
                raise ValueError("Incorrect rotor start state for Enigma construction")

        # fast to slow rotor ordering
        self.rotors: List[Rotor] = [Rotor(rm[0], rm[1]) for rm in rotorMappings]
        self.reflector: Mapper = Mapper(la, reflectorMapping)
        self.keyBoard: List[str] = la
        self.plugBoard: Mapper = Mapper(la, plugMapping)

    def convert(self, text: str, rotorsMove: bool = True):

        res: str = ""
        char: str = self.plug(text[0])

        for i in range(0, len(text)):

            for rot in self.rotors:
                char = rot.map(MessageDirection.TO, char)

            # reflector
            char = self.reflector.get(MessageDirection.TO, char)

            # BACK
            for rot in reversed(self.rotors):
                char = rot.map(MessageDirection.BACK, char)

            # alter rotors
            if rotorsMove:
                self.cycle()

            res += char
            char = text[min(i+1, len(text)-1)]

        # plugboard back
        return self.plug(res)


    def cycle(self):
        for rot in self.rotors:
            if not rot.incr():
                return False        # no overflow, following rotors unchanged
        return True     # last rotor overflowed


    def setRotorsState(self, newState: str):
        """
        Set the state of the rotors to the new value. The new state is interpreted
        as fast/middle/slow.
        :param newState: New enigma rotor state.
        """
        for i in range(3):
            self.rotors[i].state = newState[i]

    def incrementRotorsState(self, amount: int):
        newState = KeyB26(3, toSeed(self.rotorsState()) + amount).key()
        for i in range(3):
            self.rotors[i].state = KeyB26(1, toSeed(newState[i]))


    def rotorsState(self) -> str:
        """
        Get the state of the rotors. Ordered fast/middle/slow
        :return: String  representation of rotor states.
        """
        return ''.join([r.state.key() for r in self.rotors])

    def rotorsStartState(self) -> str:
        """
        Get the start state of the rotors. Ordered fast/middle/slow
        :return: String  representation of rotor states.
        """
        return ''.join([r.startState for r in self.rotors])

    def resetRotors(self):
        for rotor in self.rotors:
            rotor.resetState()

    def swapOutRotors(self, rotorMappings: List):
        for i in range(3):
            self.rotors = [Rotor(rm[0], rm[1]) for rm in rotorMappings]

    def plug(self, char: str):
        # state to state + 1
        return char

