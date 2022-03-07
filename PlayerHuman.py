from PlayerInterface import PlayerInterface

class PlayerHuman(PlayerInterface):
    def makeMove(self, playGrid):
        columnNumber = input("Bitte Spaltennummer (0-" + str(playGrid.numColumns-1) + ") für den Zug angeben: ")
        rowNumber = input("Bitte Zeilennummer (0-" + str(playGrid.numRows-1) + ") für den Zug angeben: ")
        return int(rowNumber), int(columnNumber)
