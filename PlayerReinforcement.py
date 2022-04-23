from PlayGrid import PlayGrid
from PlayerInterface import PlayerInterface
import copy
import pickle
from os.path import exists
import random
class PlayerReenforcement(PlayerInterface):
    winValue = 1.0
    loseValue = -1.0
    drawValue = 0.0
    unknownValue = 0.0
    states = None
    lastState = None
    stateFileName = 'states'
    explorationProbability = 0.3
    stepSizeParameter = 0.15
    training = True

    def __init__(self):
        if exists(self.stateFileName):
            with open(self.stateFileName, 'rb') as config_dictionary_file:
                self.states = pickle.load(config_dictionary_file)

    def saveStates(self):
        with open(self.stateFileName, 'wb') as config_dictionary_file:
            pickle.dump(self.states, config_dictionary_file)


    def makeMove(self, playGrid):
        if self.states is None:
            #Wurde keine Datei geladen, somit wird die Struktur aufgrund des aktuellen PlayGrids angelegt
            self.createStates(playGrid)

        if self.lastState is None:
            #Aktuellen Zustand in States finden
            self.lastState = [item for item in self.states if item[0] == playGrid][0]
        #else:
            #self.updateScore(playGrid)
            #Last State aktualisieren, da ja der Gegner den letzten Zug gemacht hat
            #self.lastState = [item for item in self.lastState[2] if item[0] == playGrid][0]

        if self.training and random.random() <= self.explorationProbability:
            #Explore
            nextMove = self.determinExplorationMove()
        else:
            #Greedy
            nextMove = self.determinGreedyMove()

        #self.updateScoreAndLastMove(nextMove[0])
        #self.lastState = nextMove
        return self.getIndexOfDifference(playGrid, nextMove[0])

    def updateScoreAndLastMove(self, playGrid):
        playGridState = [item for item in self.lastState[2] if item[0] == playGrid][0]
        playGridStateValue = playGridState[1]
        currentStateValue = self.lastState[1]
        newStateValue = currentStateValue + self.stepSizeParameter * (playGridStateValue - currentStateValue)
        print("Value von ", currentStateValue, " auf ", newStateValue, " gesetzt.")
        self.lastState[1] = newStateValue
        self.lastState = playGridState


    def getIndexOfDifference(self, gridBeforeMove, gridAfterMove):
        for x in range(gridBeforeMove.numRows):
            for y in range(gridBeforeMove.numColumns):
                if gridBeforeMove.grid[x][y] != gridAfterMove.grid[x][y]:
                    return x, y

    def determinGreedyMove(self):
        maxValueOfFollowStates = max(self.lastState[2], key=lambda item: item[1])[1]
        #Alle Folgezustände die den größten Value haben
        possibleFollowStates = [item for item in self.lastState[2] if item[1] == maxValueOfFollowStates]
        followState = random.choice(possibleFollowStates)
        return followState

    def determinExplorationMove(self):
        #Alle Folgezustände die den größten Value haben
        possibleFollowStates = self.lastState[2]
        followState = random.choice(possibleFollowStates)
        return followState

    def createStates(self, playGrid):
        self.states = []
        emptyGrid = PlayGrid(numColumns=playGrid.numColumns, numRows=playGrid.numRows)

        subStates = self.createSubStates(emptyGrid, playGrid)
        #SubStates (ein Feld ist schon befüllt)
        self.states.extend(subStates)
        #Leeres Feld mit Value und Substates
        self.states.append([emptyGrid, self.unknownValue, subStates])

    def createSubStates(self, currentGrid, playGrid):
        newSubStates = []
        subStatePlayerSymbol = currentGrid.getNextPlayer()
        for x in range(playGrid.numRows):
            for y in range(playGrid.numColumns):
                if currentGrid.grid[x][y] == None:
                    newSubGrid = copy.deepcopy(currentGrid)
                    newSubGrid.grid[x][y] = subStatePlayerSymbol
                    subSubStates = None

                    #Gibt es auf den Substate einen Gewinner und wenn ja, wer ist es?
                    isFinished, winner = newSubGrid.isGameFinished()
                    if isFinished == False:
                        initialValue = self.unknownValue
                        #Spiel ist nich zuende, subsubstates erstellen
                        subSubStates = self.createSubStates(newSubGrid, playGrid)
                    elif winner == None:
                        initialValue = self.drawValue
                    elif winner == playGrid.getNextPlayer():
                        #Der aktuelle Spieler (Instanz dieser Klasse) ist der Gewinner
                        initialValue = self.winValue
                    else:
                        #Der anderen Spieler hat gewonnen
                        initialValue = self.loseValue

                    newSubStates.append([newSubGrid, initialValue, subSubStates])
        return newSubStates



