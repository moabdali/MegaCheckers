import PySimpleGUI as sg
import copy
import math
import random
from time import sleep

##class Player:
##    def __init__(self,playerName=None,columns = None,rows = None,window = None,gameBoard = None):
##        if playerName == 1:
##            playerPiece = []
##            for i in range(2):
##                for j in range(columns):
##                    playerPiece.append(Piece(row = i, column = j, playerTurn = playerName))
##                    gameBoard[i][j][1]=(playerPiece[j])
##        elif playerName == 2:
##            playerPiece = []
##            for i in range(2):
##                for j in range(columns):
##                    playerPiece.append(Piece(row = rows-i, column = j, playerTurn = playerName))
##                    gameBoard[rows-1-i][j][1]=(playerPiece[j])


class publicStats:
    def __init__(self):
        turnCount = 1
                
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
        #self. avatar = f".//player{playerTurn}default.png"
        self.ownedBy = playerTurn
        self.distanceMax = 1
    
class Tile:
    def __init__(self, occupied = False):
        self.tileHeight = 0
        self.tileType = "default"
        self.occupied = occupied

        
        
def initializeField(columns,rows,window,gameBoard):
    
    for i in range(2):
        for j in range(columns): 
            #window[i,j].update(image_filename="player1default.png")
            gameBoard[i][j][0]=Tile(occupied=True)
            #print("Created a piece for player 1")
            piece = Piece(playerTurn = 1)
            gameBoard[i][j][1]=piece
            gameBoard[i][j][1].location = (i,j)
            gameBoard[i][j][1].tileType = "player1default"
            
    for i in range(2):
        for j in range(columns):
            #window[rows-i-1,j].update(image_filename="player2default.png")
            gameBoard[rows-i-1][j][0]=Tile(occupied=True)
            piece = Piece(playerTurn = 2)
            #print("Created a piece for player 2")
            gameBoard[rows-i-1][j][1]=piece
            gameBoard[rows-i-1][j][1].location = (i,j)
            gameBoard[i][j][1].tileType = "player2default"
    



def countPieces(gameBoard,window):
    player1count = 0
    player2count = 0
    #print(gameBoard)
    for i in gameBoard:
        for j in i:
            #print(f"J[1] is {j[1]}")
            if j[1] != 0:
                #print(f"J[1] is {j[1]}")
                if j[1].ownedBy == 1:
                    player1count+=1
                elif j[1].ownedBy == 2:
                    player2count+=1
    #print(f"playercount1 is {player1count} playercount2 is {player2count}")
    window['player1piececount'].update(f"Player 1 controls: {player1count}")
    window['player2piececount'].update(f"Player 2 controls: {player2count}")
    window.refresh()

def gamePlay(playerTurn, window, gameBoard):
    
        countPieces(gameBoard,window)
        createOrbs(window,gameBoard)
        displayBoard(window,gameBoard)
        movePiece(playerTurn, window,gameBoard)
        


def getDistance(a,b,c,d):
    verticalDistance = abs(c-a)
    horizontalDistance = abs(d-b)
    distance = verticalDistance + horizontalDistance
    return distance

def createOrbs(window,gameBoard):
    emptySpots = 0
    for i in gameBoard:
        for j in i:
                if j[0].tileType == "default":
                    emptySpots+=1
    #sg.popup(f"There are {emptySpots} emptySpots")

        
def displayBoard(window,gameBoard):
    
    for i in range(len(gameBoard)):

        for j in range(len(gameBoard[0])):
            #print(gameBoard[i][j])
            if gameBoard[i][j][0].occupied == False:
                #print("empty")
                if gameBoard[i][j][0].tileType == "default":
                    window[i,j].update(image_filename="blank.png")    
            else:
                if gameBoard[i][j][0].occupied:
                    if gameBoard[i][j][1].ownedBy == 1:
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


        if (gameBoard[ startLocation[0] ] [ startLocation[1] ] [0].occupied == False ):
            window['information'].update(f"Nothing exists on the initial square!")
            window.refresh
            #sg.popup(f"Piece doesn't exist,  {gameBoard[ startLocation[0] ] [ startLocation[1] ]}", )
            continue

            
            
            
        
        #if the spot you're moving from contains a piece
        if( gameBoard[ startLocation[0] ] [ startLocation[1] ] [0] .occupied):
            #if the piece is yours
            if (gameBoard[ startLocation[0] ] [ startLocation[1] ][1].ownedBy == playerTurn):



                if getDistance(startLocation[0],startLocation[1],endLocation[0],endLocation[1]) >  gameBoard[ startLocation[0] ] [ startLocation[1] ][1].distanceMax:
                    window['information'].update(f"That location is too far for you to move to!")
                    window.refresh
                    #print( f" {getDistance(startLocation[0],startLocation[1],endLocation[0],endLocation[1])} attempted, {gameBoard[ startLocation[0] ] [ startLocation[1] ].distanceMax} allowed")
                    continue


                
                #if the landing spot is empty
                if gameBoard[ endLocation[0] ] [ endLocation[1] ][0].occupied == False:
                    #print( f" {getDistance(startLocation[0],startLocation[1],endLocation[0],endLocation[1])} attempted, {gameBoard[ startLocation[0] ] [ startLocation[1] ][1].distanceMax} allowed")
                    
                    #change the internal address location of the piece to where the piece moved to
                    #gameBoard[startLocation[0]] [startLocation[1]][1].location = (endLocation[0],endLocation[1])

                    #copy the actual object over from the old address to the new one
                    gameBoard[endLocation[0]][endLocation[1]][1] = gameBoard[startLocation[0]][startLocation[1]][1]
                    
                    #set the original location as being empty; delete the class; set a default tile
                    gameBoard[ startLocation[0] ] [ startLocation[1] ][0].occupied = False
                    gameBoard[ startLocation[0] ] [ startLocation[1] ][1] = 0
                    gameBoard[startLocation[0]][startLocation[1]][0].tileType = "default"

                    #set the new location as occupied; set the tile as the type of the tile that moved (needs to be updated in future revisions)
                    gameBoard[ endLocation[0] ] [ endLocation[1] ][0].occupied = True
                    #print(f"does it exist here? {gameBoard[ endLocation[0] ] [ endLocation[1] ][0].occupied}")
                    gameBoard[ endLocation[0]][endLocation[1]][0].tileType = f"player{playerTurn}default"
                    
                    window['information'].update(f"Moved successfully!")
                    window.refresh
                    print("Moved!")
                    return 1


                #killing own piece (illegal)
                elif gameBoard[ endLocation[0] ] [ endLocation[1] ][1].ownedBy == playerTurn:
                    window['information'].update(f"You can't jumpkill your own piece.")
                    window.refresh
                    continue

                #kill enemy piece; elif enemy owns the ending location
                elif gameBoard[ endLocation[0] ] [ endLocation[1] ][1].ownedBy != playerTurn:
                    #set the internal location of the piece to where you want to end up
                    gameBoard[ startLocation[0] ] [ startLocation[1] ][1].location = (endLocation[0],endLocation[1])
                    #move the piece object
                    gameBoard[ endLocation[0] ] [ endLocation[1] ][1] = gameBoard[ startLocation[0] ] [ startLocation[1]][1]
                    #delete the original piece
                    gameBoard[ startLocation[0] ] [ startLocation[1]][1]=0
                    #set the original location as empty
                    gameBoard[ startLocation[0] ] [ startLocation[1] ] [0].occupied = False

                    #set the new location as full
                    gameBoard[ endLocation[0] ] [ endLocation[1] ] [0].occupied = True
                    #set the original tile as default look
                    gameBoard[startLocation[0]][startLocation[1]][0].tileType = "default"
                    
                    
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
        line.append([Tile(),0])
        gameBoard.append(0)
    
    
    for j in range(rows):
        gameBoard[j] = copy.deepcopy(line)

    
    
    #player1 = Player(playerName = 1,columns = columns, window = window,gameBoard = gameBoard)
    #player2 = Player(playerName = 2, columns = columns, rows = rows, window = window,gameBoard = gameBoard)

    initializeField(columns,rows,window,gameBoard)
    
    
    playerTurn = 1
    while True:
    
        
        gamePlay(playerTurn, window, gameBoard)
        if playerTurn == 1:
            playerTurn = 2
        else:
            playerTurn = 1
        

main()
