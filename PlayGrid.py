from itertools import chain


class PlayGrid:
    def __init__(self, numColumns, numRows):
        self.numColumns = numColumns
        self.numRows = numRows
        self.grid = [[None for x in range(self.numColumns)] for y in range(self.numRows)]
        self.playerSymbols = ["X", "O"]
        self.winningLength = 3

    def prettyPrint(self):
        # Kopfzeile
        headerString = "  "
        for columnNumber in range(self.numColumns):
            headerString += str(columnNumber) + "\t  "
        print(headerString)

        # Spielfläche
        for x in range(self.numRows):
            # Zeileninhalt
            rowAsString = str(x)
            for y in range(self.numColumns):
                cellContent = self.grid[x][y]
                if cellContent is None:
                    rowAsString += "\t"
                else:
                    rowAsString += " " + cellContent + " "

                if y < self.numColumns - 1:
                    rowAsString += '|'
            print(rowAsString)

            # Trennstrich
            # seperatorLine = " "
            # for columnNumber in range(self.numColumns):
            #    seperatorLine += "=="
            # print(seperatorLine)

    def getEmptyCells(self):
        emptyCells = []
        for y in range(self.numRows):
            for x in range(self.numColumns):
                if self.grid[x][y] is None:
                    emptyCells.append((x,y))
        return emptyCells

    def updateScore(self, playerSymbol, x, y):
        self.grid[x][y] = playerSymbol

    def isGameFinished(self):
        for row in range(self.numRows):
            tmp_symbol = None
            win_counter = 1
            for column in range(self.numColumns):
                if self.grid[row][column] is not None and tmp_symbol == self.grid[row][column]:
                    win_counter += 1
                    if win_counter == self.winningLength:
                        return True, tmp_symbol
                else:
                    win_counter = 1
                    tmp_symbol = self.grid[row][column]

        # vertical
        for column in range(self.numColumns):
            tmp_symbol = None
            win_counter = 1
            for row in range(self.numRows):
                if self.grid[row][column] is not None and tmp_symbol == self.grid[row][column]:
                    win_counter += 1
                    if win_counter == self.winningLength:
                        return True, tmp_symbol
                else:
                    win_counter = 1
                    tmp_symbol = self.grid[row][column]

        # diagonal links oben nach rechts unten
        for index in range(self.numColumns):
            tmp_symbol = self.grid[index][0]
            win_counter = 1
            for move in range(1, self.numColumns - index):
                if self.grid[index + move][move] is not None and tmp_symbol == self.grid[index + move][move]:
                    win_counter += 1
                    if win_counter == self.winningLength:
                        return True, tmp_symbol
                else:
                    win_counter = 1
                    tmp_symbol = self.grid[index + move][move]

        for index in range(1, self.numRows):
            tmp_symbol = self.grid[0][index]
            win_counter = 1
            for move in range(1, self.numRows - index):
                if self.grid[move][index + move] is not None and tmp_symbol == self.grid[move][index + move]:
                    win_counter += 1
                    if win_counter == self.winningLength:
                        return True, tmp_symbol
                else:
                    win_counter = 1
                    tmp_symbol = self.grid[move][index + move]

        # diagonal links unten nach rechts oben
        for index in range(self.numColumns - 1, 0, -1):
            tmp_symbol = self.grid[index][0]
            win_counter = 1
            for move in range(1, index + 1):
                if self.grid[index - move][move] is not None and tmp_symbol == self.grid[index - move][move]:
                    win_counter += 1
                    if win_counter == self.winningLength:
                        return True, tmp_symbol
                else:
                    win_counter = 1
                    tmp_symbol = self.grid[index - move][move]

        for index in range(self.numRows - 1, 1, -1):
            tmp_symbol = self.grid[0][index]
            win_counter = 1
            for move in range(1, index + 1):
                if self.grid[index - move][move] is not None and tmp_symbol == self.grid[move][index - move]:
                    win_counter += 1
                    if win_counter == self.winningLength:
                        return True, tmp_symbol
                else:
                    win_counter = 1
                    tmp_symbol = self.grid[move][index - move]

        if None in chain(*self.grid):
            #Kein Gewinner, aber es gibt noch freie Felder
            return False, None
        else:
            #Kein Gewinner, aber das Spielfeld ist komplett gefüllt
            return True, None

    def getNextPlayer(self):
        symbolsOnGridCount = {}
        for playerSymbol in self.playerSymbols:
            symbolsOnGridCount[playerSymbol] = [item for sublist in self.grid for item in sublist].count(playerSymbol)

        if len(set(symbolsOnGridCount.values())) == 1:
            # Gleich viele Symbole
            return self.playerSymbols[0]
        else:
            # Mitten in der Runde, deshalb unterschiedlich viele Symbole je nach Spieler
            return min(symbolsOnGridCount, key=symbolsOnGridCount.get)
