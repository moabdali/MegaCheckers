import PySimpleGUI as sg
import copy
import math
from time import sleep

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
        self.distanceMax = 1
    


def initializeField(player1,player2,columns,rows,window):
    
    for j in range(2):
        for i in range(columns): 
            window[j,i].update(image_filename="player1default.png")
    for j in range(2):
        for i in range(columns):
            window[rows-j-1,i].update(image_filename="player2default.png")



def countPieces(gameBoard,window):
    player1count = 0
    player2count = 0
    print(gameBoard)
    for i in gameBoard:
        for j in i:
            if j != 0:
                if j.ownedBy == 1:
                    player1count+=1
                elif j.ownedBy == 2:
                    player2count+=1
    print(f"playercount1 is {player1count} playercount2 is {player2count}")
    window['player1piececount'].update(f"Player 1 controls: {player1count}")
    window['player2piececount'].update(f"Player 2 controls: {player2count}")
    window.refresh()

def gamePlay(playerTurn, window, gameBoard):
        countPieces(gameBoard,window)
        movePiece(playerTurn, window,gameBoard)
        displayBoard(window,gameBoard)


def getDistance(a,b,c,d):
    verticalDistance = abs(c-a)
    horizontalDistance = abs(d-b)
    distance = verticalDistance + horizontalDistance
    return distance


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
        #sg.popup_timed(f" It's player {playerTurn}'s turn.",font = "Cambria, 20",auto_close_duration=1)
        window.refresh()
        sleep(1.25)
        window['playerTurn'].update(f"{playerTurn}")
        window['information'].update(f"Pick a piece to move.")
        event = window.read()
        
        startLocation = event[0]
        window['information'].update(f"Selection made, pick destination.")
        event = window.read()
        endLocation = event[0]


        try:
            ( gameBoard[ startLocation[0] ] [ startLocation[1] ].ownedBy )
            
            
        except:
            window['information'].update(f"Nothing exists on the initial square!")
            window.refresh
            #sg.popup(f"Piece doesn't exist,  {gameBoard[ startLocation[0] ] [ startLocation[1] ]}", )
            continue

        
        #if the spot you're moving from contains a piece
        if( gameBoard[ startLocation[0] ] [ startLocation[1] ] ) != 0:
            #if the piece is yours
            if (gameBoard[ startLocation[0] ] [ startLocation[1] ].ownedBy == playerTurn):



                if getDistance(startLocation[0],startLocation[1],endLocation[0],endLocation[1]) >  gameBoard[ startLocation[0] ] [ startLocation[1] ].distanceMax:
                    window['information'].update(f"That location is too far for you to move to!")
                    window.refresh
                    print( f" {getDistance(startLocation[0],startLocation[1],endLocation[0],endLocation[1])} attempted, {gameBoard[ startLocation[0] ] [ startLocation[1] ].distanceMax} allowed")
                    continue


                
                #if the landing spot is empty
                if gameBoard[ endLocation[0] ] [ endLocation[1] ] == 0:
                    print( f" {getDistance(startLocation[0],startLocation[1],endLocation[0],endLocation[1])} attempted, {gameBoard[ startLocation[0] ] [ startLocation[1] ].distanceMax} allowed")
                    gameBoard[ startLocation[0] ] [ startLocation[1] ].location = (endLocation[0],endLocation[1])
                    gameBoard[ endLocation[0] ] [ endLocation[1] ] = gameBoard[ startLocation[0] ] [ startLocation[1] ]
                    gameBoard[ startLocation[0] ] [ startLocation[1] ] = 0
                    window['information'].update(f"Moved successfully!")
                    window.refresh
                    print("Moved!")
                    return 1


                #killing own piece (illegal)
                elif gameBoard[ endLocation[0] ] [ endLocation[1] ].ownedBy == playerTurn:
                    window['information'].update(f"You can't jumpkill your own piece.")
                    window.refresh
                    continue

                #kill enemy piece
                elif gameBoard[ endLocation[0] ] [ endLocation[1] ].ownedBy != playerTurn:
                    gameBoard[ startLocation[0] ] [ startLocation[1] ].location = (endLocation[0],endLocation[1])
                    gameBoard[ endLocation[0] ] [ endLocation[1] ] = gameBoard[ startLocation[0] ] [ startLocation[1] ]
                    gameBoard[ startLocation[0] ] [ startLocation[1] ] = 0
                    window['information'].update(f"Jumpkilled an enemy piece!")
                    sleep(1)
                    return 2
                    


            else:
                window['information'].update(f"That's not your piece!")
                window.refresh
                continue
                
        else:
            window['information'].update(f"Nothing here to move!")
            window.refresh
            continue
            
        
    
def main():

    #variables 
    columns = 10
    rows = 10
    gameBoard = []
    
    #window

    frame_layout = [
        [sg.T(f"Player:",font = "Cambria 30",pad = (4,4)), sg.T(f"",key='playerTurn',font = "Cambria 30",pad = (4,4))],
        [sg.T(f" "*100,key = 'information',size = (40,2),font="Cambria 30")]
        ]
    frame_layout2 = [
        [sg.T(f"Player 1 Controls: xx", key = 'player1piececount',font = "Cambria 20", text_color="blue"),sg.T(f"Player 2 Controls: xx",key = 'player2piececount',font = "Cambria 20",text_color="red")],
        
        ]
    layout = [
        [sg.T("MegaCheckers")]
        ]
    layout += [
            [sg.Button(image_filename = ".\\blank.png",key=(i,j),size = (20,20), pad = (10,10))for j in range (columns)]for i in range(0,rows)
            ]
    layout += [
        [sg.Frame('Information:', frame_layout,font='Calibri 20', title_color='blue')],
        [sg.Frame('Remaining pieces:', frame_layout2,font='Calibri 20', title_color='blue')]
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
