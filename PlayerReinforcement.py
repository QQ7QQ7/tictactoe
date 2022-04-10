from PlayGrid import PlayGrid
from PlayerInterface import PlayerInterface
import copy
import pickle
from os.path import exists
from random import random
class PlayerReenforcement(PlayerInterface):
    winValue = 1
    loseValue = -1
    drawValue = 0
    unknownValue = 0
    states = None
    currentState = None
    stateFileName = 'states'
    explorationProbability = 0.2

    def makeMove(self, playGrid):
        if self.states is None:
            if exists(self.stateFileName):
                # Step 2
                with open(self.stateFileName, 'rb') as config_dictionary_file:
                    # Step 3
                    self.states = pickle.load(config_dictionary_file)
                    self.states[2][0].prettyPrint()
            else:
                self.createStates(playGrid)
                # Step 2
                with open(self.stateFileName, 'wb') as config_dictionary_file:
                    # Step 3
                    pickle.dump(self.states, config_dictionary_file)
            #Aktuellen Zustand in States finden
            self.currentState = [item for item in self.states if item[0] == playGrid][0]

        #TODO UPDATE SCORE

        if random() <= self.explorationProbability:
            #Explore
            self.currentState = self.determineExplorationMove()
        else:
            #Greedy
            self.currentState = self.determinGreedyMove()

        return self.getIndexOfDifference(playGrid, self.currentState)

    def getIndexOfDifference(self, gridBeforeMove, gridAfterMove):
        for x in range(gridBeforeMove.numRows):
            for y in range(gridBeforeMove.numColumns):
                if gridBeforeMove.grid[x][y] != gridAfterMove.grid[x][y]:
                    return x, y

    def determinGreedyMove(self):
        #Alle Folgezustände die den größten Value haben
        possibleFollowStates = max(self.currentState[2], key=lambda item: item[1])
        followState = random.choice(possibleFollowStates)
        return followState

    def determinExplorationMove(self):
        #Alle Folgezustände die den größten Value haben
        possibleFollowStates = self.currentState[2]
        followState = random.choice(possibleFollowStates)
        return followState

    def createStates(self, playGrid):
        self.states = []
        emptyGrid = PlayGrid(numColumns=playGrid.numColumns, numRows=playGrid.numRows)

        subStates = self.createSubStates(emptyGrid, playGrid)
        #SubStates (ein Feld ist schon befüllt)
        self.states.extend(subStates)
        #Leeres Feld mit Value und Substates
        self.states.append((emptyGrid, self.unknownValue, subStates))

    def createSubStates(self, currentGrid, playGrid):
        newSubStates = []
        playerSymbol = currentGrid.getNextPlayer()
        for x in range(playGrid.numRows):
            for y in range(playGrid.numColumns):
                if currentGrid.grid[x][y] == None:
                    newSubGrid = copy.deepcopy(currentGrid)
                    newSubGrid.grid[x][y] = playerSymbol
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

                    newSubStates.append((newSubGrid, initialValue, subSubStates))
        return newSubStates



