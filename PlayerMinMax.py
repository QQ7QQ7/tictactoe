import copy
from itertools import chain

from PlayerInterface import PlayerInterface

class PlayerMinMax(PlayerInterface):
    def makeMove(self, playGrid):
        koordinatenXY, score = self.max(playGrid)
        return koordinatenXY[0], koordinatenXY[1]

    def max(self, playGrid):
        currentPlayer = self.currentPlayer(playGrid)
        emtpyCellCooridnatesXY = playGrid.getEmptyCells()
        possibleMoveScores = {}
        for xy in emtpyCellCooridnatesXY:
            gridCopy = copy.deepcopy(playGrid)
            gridCopy.updateScore(currentPlayer, xy[0], xy[1])
            isFinished, winner = gridCopy.isGameFinished()

            if isFinished == False:
                #Spiel geht noch weiter
                koordinaten, score = self.min(gridCopy)
            elif winner == None:
                #Kein Gewinner
                score = 0
            elif winner == currentPlayer:
                #Spieler hat gewonnen
                score = 1
            else:
                #Anderer Spieler hat gewonnen
                score = -1

            possibleMoveScores[xy] = score

        #Key zum höchsten Score ermitteln
        maxKey = max(possibleMoveScores, key=possibleMoveScores.get)
        return maxKey, possibleMoveScores[maxKey]

    def min(self, playGrid):
        currentPlayer = self.currentPlayer(playGrid)
        emtpyCellCooridnatesXY = playGrid.getEmptyCells()
        possibleMoveScores = {}
        for xy in emtpyCellCooridnatesXY:
            gridCopy = copy.deepcopy(playGrid)
            gridCopy.updateScore(currentPlayer, xy[0], xy[1])
            isFinished, winner = gridCopy.isGameFinished()

            if isFinished == False:
                #Spiel geht noch weiter
                koordinaten, score = self.max(gridCopy)
            elif winner == None:
                #Kein Gewinner
                score = 0
            elif winner == currentPlayer:
                #Spieler hat gewonnen
                score = -1
            else:
                #Anderer Spieler hat gewonnen
                score = 1

            possibleMoveScores[xy] = score

        # Key zum höchsten Score ermitteln
        minKey = min(possibleMoveScores, key=possibleMoveScores.get)
        return minKey, possibleMoveScores[minKey]

    def currentPlayer(self, playGrid):
        symbolsOnGridCount = {}
        for playerSymbol in playGrid.playerSymbols:
            symbolsOnGridCount[playerSymbol] = [item for sublist in playGrid.grid for item in sublist].count(playerSymbol)

        if len(set(symbolsOnGridCount.values())) == 1:
            #Gleich viele Symbole
            return playGrid.playerSymbols[0]
        else:
            #Mitten in der Runde, deshalb unterschiedlich viele Symbole je nach Spieler
            return min(symbolsOnGridCount, key=symbolsOnGridCount.get)
