from PlayerInterface import PlayerInterface

class PlayerHuman(PlayerInterface):
    def makeMove(self, playGrid):
        columnNumber = input("Bitte Spaltennummer (1-" + str(playGrid.numColumns) + ") für den Zug angeben: ")
        rowNumber = input("Bitte Zeilennummer (1-" + str(playGrid.numRows) + ") für den Zug angeben: ")
        return int(rowNumber) - 1, int(columnNumber) - 1
