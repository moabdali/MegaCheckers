import PySimpleGUI as sg
import copy

class Player:
    def __init__(self,playerName=None,columns = None,rows = None,window = None,gameBoard = None):
        if playerName == 1:
            playerPiece = []
            for j in range(2):
                for i in range(columns):
                    playerPiece.append(Piece(row = j, column = i, playerTurn = playerName))
                    gameBoard[j][i]=(playerPiece[i])
        elif playerName == 2:
            playerPiece = []
            for j in range(2):
                for i in range(columns):
                    playerPiece.append(Piece(row = rows-j, column = i, playerTurn = playerName))
                    gameBoard[rows-1-j][i]=(playerPiece[i])

                
class Piece:
    def __init__(self,row = None,column = None,playerTurn = None):
        #where the piece is currently residing
        location = (row,column)
        #what bonuses the player has
        activeBuffs = ()
        #what maluses the player has
        activeDebuffs = ()
        #what the player is holding (need a max; 5?)
        storedItems = ()
        #what it looks like
        avatar = f".//player{playerTurn}default.png"

def initializeField(player1,player2,columns,rows,window):
    
    for j in range(2):
        for i in range(columns): 
            window[j,i].update(image_filename="player1default.png")
    for j in range(2):
        for i in range(columns):
            window[rows-j-1,i].update(image_filename="player2default.png")
def main():

    #variables 
    columns = 10
    rows = 10
    gameBoard = []
    
    #window
    layout = [
        [sg.T("MegaCheckers")]
        ]
    layout += [
            [sg.Button(image_filename = ".\\blank.png",key=(i,j),size = (20,20), pad = (10,10))for j in range (columns)]for i in range(0,rows)
            ]
    
    window = sg.Window("MegaCheckers",layout).finalize()


    #gameBoard for logic
    gameBoard = []
    line = []
    for i in range(columns):
        line.append(0)
        gameBoard.append(0)
    
    
    for j in range(rows):
        gameBoard[j] = copy.deepcopy(line)

    
    
    player1 = Player(playerName = 1,columns = columns, window = window,gameBoard = gameBoard)
    print("Player 1 created")
    player2 = Player(playerName = 2, columns = columns, rows = rows, window = window,gameBoard = gameBoard)
    print("Player 2 created")

    initializeField(player1,player2,columns,rows,window)
    

    while True:
        print(gameBoard)
        window.read()

main()
