# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from PlayGrid import PlayGrid
from PlayerHuman import PlayerHuman
from PlayerMinMax import PlayerMinMax
from PlayerReinforcement import PlayerReenforcement


def init():
    numColumns = 3
    numRows = numColumns
    playGrid: PlayGrid = PlayGrid(numColumns=numColumns, numRows=numRows)

    return playGrid

#TODO's: Loop zum Trainieren einbauen,
# Step-Size Parameter korrekt setzen und verändern,
# Trainierte States in Datei schreiben
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    playGrid = init()
    player1 = PlayerReenforcement()
    player2 = PlayerMinMax()
    endGame = False
    playGrid.prettyPrint()

    while not endGame:
        print("Spieler 'X' ist dran")
        x, y = player1.makeMove(playGrid)
        playGrid.updateScore('X', x, y)
        playGrid.prettyPrint()
        print()
        endGame, winner = playGrid.isGameFinished()
        if endGame:
            break

        print("Spieler 'O' ist dran")
        x, y = player2.makeMove(playGrid)
        playGrid.updateScore('O', x, y)
        playGrid.prettyPrint()
        print()
        endGame, winner = playGrid.isGameFinished()

    if winner is None:
        print("Das Spiel ist unentschieden!")
    else:
        print("Der Gewinner ist ", winner + "!")
