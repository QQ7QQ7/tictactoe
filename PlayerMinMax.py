import copy
from itertools import chain

from PlayerInterface import PlayerInterface

class PlayerMinMax(PlayerInterface):
    def makeMove(self, playGrid):
        #TODO
        koordinaten = self.max(playGrid)

        return koordinaten

    def max(self, playGrid):
        currentPlayer = self.currentPlayer(playGrid)
        emtpyCellCooridnatesXY = playGrid.getEmptyCells()
        moveScore = {}
        for xy in emtpyCellCooridnatesXY:
            gridCopy = copy.deepcopy(playGrid)
            gridCopy.updateScore(currentPlayer, xy[0], xy[1])
            isFinished, winner = gridCopy.isGameFinished()

            if isFinished == False:
                score = min(gridCopy)
            elif winner == None:
                score = 0
            elif winner == currentPlayer:
                score = 1
            else:
                score -1

            moveScore[xy] = score
            #TODO
            return maxVonMoveSocre #Key als auch Value

    def min(self, playGrid):
        currentPlayer = self.currentPlayer(playGrid)
        emtpyCellCooridnatesXY = playGrid.getEmptyCells()
        for xy in emtpyCellCooridnatesXY:
            gridCopy = copy.deepcopy(playGrid)
            gridCopy.updateScore(currentPlayer, xy[0], xy[1])
            max(gridCopy)
            #TODO

    def currentPlayer(self, playGrid):
        symbolsOnGridCount = {}
        for playerSymbol in playGrid.playerSymbols:
            symbolsOnGridCount[playerSymbol] = [item for sublist in playGrid.grid for item in sublist].count(playerSymbol)

        if len(set(symbolsOnGridCount.values())) == 1:
            #Gleich viele Symbole
            return list(playGrid.playerSymbols.values())[0]
        else:
            #Mitten in der Runde, deshalb unterschiedlich viele Symbole je nach Spieler
            return min(symbolsOnGridCount, key=symbolsOnGridCount.get)
