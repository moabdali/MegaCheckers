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
        self.location = (row,column)
        #what bonuses the player has
        self.activeBuffs = ()
        #what maluses the player has
        self.activeDebuffs = ()
        #what the player is holding (need a max; 5?)
        self.storedItems = ()
        #what it looks like
        self. avatar = f".//player{playerTurn}default.png"
        self.ownedBy = playerTurn


def initializeField(player1,player2,columns,rows,window):
    
    for j in range(2):
        for i in range(columns): 
            window[j,i].update(image_filename="player1default.png")
    for j in range(2):
        for i in range(columns):
            window[rows-j-1,i].update(image_filename="player2default.png")


def gamePlay(playerTurn, window, gameBoard):


    

        movePiece(playerTurn, window,gameBoard)
        displayBoard(window,gameBoard)





def displayBoard(window,gameBoard):
    
    for i in range(len(gameBoard)):

        for j in range(len(gameBoard[0])):

            if gameBoard[i][j] == 0:
                window[i,j].update(image_filename="blank.png")
            else:
                if gameBoard[i][j].ownedBy == 1:
                    window[i,j].update(image_filename="player1default.png")
                else:
                    window[i,j].update(image_filename="player2default.png")
                       




def movePiece(playerTurn, window, gameBoard):
    while True:
        sg.popup(f" It's ({playerTurn}'s) turn.")
        event = window.read()
        startLocation = event[0]
        event = window.read()
        endLocation = event[0]


        try:
            ( gameBoard[ startLocation[0] ] [ startLocation[1] ].ownedBy )
            
            
        except:
            sg.popup(f"Piece doesn't exist,  {gameBoard[ startLocation[0] ] [ startLocation[1] ]}", )

        
        #if the spot you're moving from contains a piece
        if( gameBoard[ startLocation[0] ] [ startLocation[1] ] ) != 0:
            #if the piece is yours
            if (gameBoard[ startLocation[0] ] [ startLocation[1] ].ownedBy == playerTurn):
                #if the landing spot is empty
                if gameBoard[ endLocation[0] ] [ endLocation[1] ] == 0:
                    gameBoard[ startLocation[0] ] [ startLocation[1] ].location = (endLocation[0],endLocation[1])
                    gameBoard[ endLocation[0] ] [ endLocation[1] ] = gameBoard[ startLocation[0] ] [ startLocation[1] ]
                    gameBoard[ startLocation[0] ] [ startLocation[1] ] = 0
                    print("Moved!")
                    return 1


                #killing own piece (illegal)
                elif gameBoard[ endLocation[0] ] [ endLocation[1] ].ownedBy == playerTurn:
                    sg.popup("Can't kill own piece")
                    continue

                #kill enemy piece
                elif gameBoard[ endLocation[0] ] [ endLocation[1] ].ownedBy != playerTurn:
                    gameBoard[ startLocation[0] ] [ startLocation[1] ].location = (endLocation[0],endLocation[1])
                    gameBoard[ endLocation[0] ] [ endLocation[1] ] = gameBoard[ startLocation[0] ] [ startLocation[1] ]
                    gameBoard[ startLocation[0] ] [ startLocation[1] ] = 0
                    print("KILL")
                    return 2
                    


            else:
                sg.popup("Not your piece.")
                continue
                
        else:
            sg.popup("Nothing here to move")
            continue
            
        
    
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
    player2 = Player(playerName = 2, columns = columns, rows = rows, window = window,gameBoard = gameBoard)

    initializeField(player1,player2,columns,rows,window)
    
    playerTurn = 1
    while True:
        print(gameBoard)
    
        
        gamePlay(playerTurn, window, gameBoard)
        if playerTurn == 1:
            playerTurn = 2
        else:
            playerTurn = 1
        

main()
