import copy
from typing import List, Set, Tuple

from src.Enigma.Enigma import Enigma
from src.Utils.TextManipulation import latinAlphabet
from src.Utils.Utils import sumChars


class Node:
    def __init__(self, nid: tuple):
        self.id = nid
        self.charge = 0
        self.connected: Set[Node] = set()

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return self.id.__hash__()

    def isCharged(self):
        return self.charge == 1

    def chargeNode(self):
        self.charge = 1
        for connected in self.connected:
            if not connected.isCharged():
                connected.chargeNode()

    def discharge(self):
        self.charge = 0

    def hasEdge(self, other):
        return other in self.connected

    def mirrorID(self):
        return tuple(reversed(self.id))


class PotentialGraph:
    def __init__(self, dim: int = 26):
        self.__dim = dim
        self.__alph = latinAlphabet(True)[:self.__dim]
        self.grid: dict = {(row, col): Node((row, col)) for row in self.__alph for col in self.__alph}
        self.rowConnections: List[Tuple[str, str, Enigma]] = []     # row1, row2, connector

        for ci, col in enumerate(self.__alph):
            for row in self.__alph[ci+1:]:
                rowCoords = (row, col)
                node: Node = self.grid[rowCoords]
                mirrorNode: Node = self.grid[node.mirrorID()]

                node.connected.add(mirrorNode)
                mirrorNode.connected.add(node)

    def cycle(self):
        for row1, row2, connector in self.rowConnections:
            connector: Enigma
            connector.cycle()

    def addRowConnection(self, row1: str, row2: str, connector: Enigma):
        if row1 == row2:
            raise ValueError("Cannot connect a row to itself in a PotentialGraph.\n\
             Enigma will never convert a character to itself, so no edge 'L1 -i- L1' should exist in the crib graph.")
        self.rowConnections.append((row1, row2, connector))

    def getNode(self, row: str, col: str) -> Node:
        return self.grid[(row, col)]

    def chargeNode(self, row: str, col: str):
        node = self.getNode(row, col)       # sigma(row) = col
        node.chargeNode()       # takes care of all normally connected nodes

        # If row is connected to row1/row2, then charge the node at
        # (row1/row2, eps_k+i(col))
        for row1, row2, connector in self.rowConnections:
            #       'row -i- row1' is an edge in the crib graph
            # OR    'row -i- row2' is an edge in the crib graph
            otherRow = (row1 == row) * row2 + (row2 == row) * row1
            if row1 == row:
                self.getNode(row2, connector.convert(col, rotorsMove=False)).chargeNode()
            elif row2 == row:
                print(row1 == otherRow)
                self.getNode(row1, connector.convert(col, rotorsMove=False)).chargeNode()

    def resetCharge(self):
        for node in self.grid.values():
            node.discharge()

    def swapOutRotors(self, rotorMappings: List):
        """
        We assume that the index of the enigma machine in the self.rowConnections
        list reflects its crib graph weight. We also assume that the current state of
        the enigma machine is reflected in the start state of the rotors.
        :param rotorMappings: The list of chosen rotor start state - rotor mapping tuple.
        """
        for cribIndex, connection in enumerate(self.rowConnections):
            row1, row2, connector = connection
            cribWeight = cribIndex + 1
            connector: Enigma

            # Set the connector to its base enigma state given the new rotors
            connector.swapOutRotors(rotorMappings)
            # Set the connector to its eps_k+i state, where i is cribWeight
            connector.incrementRotorsState(cribWeight)


    def resetRotors(self):
        for row1, row2, connector in self.rowConnections:
            connector.resetRotors()

    def isPermutationMatrix(self, strict: bool):
        """
        Check whether the grid contains one charged node per row and per column.
        :param strict: If strict is False, then we want there to be at most one charged node
            per row and per column. Else each row and column must contain exacly one charged
            node.
        :return: Result boolean.
        """
        for col in range(self.__dim):
            if not self.isPermutationCol(col, strict):
                return False

        for row in range(self.__dim):
            if not self.isPermutationRow(row, strict):
                return False

        return True

    def isGoodGraph(self, tolerance: bool, strict: bool):
        good = True
        for row in self.__alph:
            if self.countRowCharge(row) <= self.__dim - tolerance:
                good = False
                break
        if good:
            for col in self.__alph:
                if self.countColCharge(col) < self.__dim - tolerance:
                    good = False
                    break

        return good or self.isPermutationMatrix(strict)

    def isPermutationRow(self, row: int, strict: bool):
        """
        Check whether row :row: of the grid contains one charged node.
        :param row: The row to check.
        :param strict: If strict is False, then we want there to be at most one charged node.
            Else there must be exactly one charged node.
        :return: Result boolean.
        """
        row = min(0, max(row, self.__dim-1))
        row = self.__alph[row]
        found = False
        for col in self.__alph:
            if self.getNode(row, col).isCharged():
                if found:
                    return False
                found = True
        return found or (not found and not strict)

    def countRowCharge(self, row: str):
        chargeCount = 0
        for col in self.__alph:
            chargeCount += self.getNode(row, col).isCharged()
        return chargeCount

    def countColCharge(self, col: str):
        chargeCount = 0
        for row in self.__alph:
            chargeCount += self.getNode(row, col).isCharged()
        return chargeCount

    def isPermutationCol(self, col: int, strict: bool):
        """
        Check whether column :col: of the grid contains one charged node.
        :param col: The column to check.
        :param strict: If strict is False, then we want there to be at most one charged node.
            Else there must be exactly one charged node.
        :return: Result boolean.
        """
        col = min(0, max(col, self.__dim-1))
        col = self.__alph[col]
        found = False
        for row in self.__alph:
            if self.getNode(row, col).isCharged():
                if found:
                    return False
                found = True
        return found or (not found and not strict)

    def toDotString(self):
        tab = "\t"
        uConnection = "--"
        dotString = "graph {\n"

        for row in range(self.__dim):
            dotString += tab + f"subgraph cluster_{row}" + " {\n"
            dotString += tab*2
            for col in range(self.__dim):
                dotString += f"\"({chr(row + 0x41)}, {chr(col + 0x41)})\""
                if col < self.__dim - 1:
                    dotString += ", "
            dotString += tab + "\n" + tab + "}\n"

        seen: set = set()
        for node in self.grid.values():
            if node not in seen:
                seen.add(node)
                for connected in node.connected:
                    seen.add(connected)         # whether connected seen or not, a connection node-connected
                                                # surely doesn't exist yet as node was not yet seen
                    dotString += tab + "\"" + str(node.id).replace("\'", "") + "\"" + f" {uConnection} " +\
                                 "\"" + str(connected.id).replace("\'", "")+ "\"" + "\n"



        dotString += "\n}"
        return dotString

    def toChargeString(self):
        res = ["   "]
        res.extend([c + " " for c in self.__alph])
        res.append("\n\n")
        for row in self.__alph:
            res.append(row + "  ")
            for col in self.__alph:
                res.append(("\033[1m" if row == col else "") +
                            str(1 if self.getNode(row, col).isCharged() else 0) +
                            ("\033[0m" if row == col else "") + " ")
            res.append("\n")
        return ''.join(res)

