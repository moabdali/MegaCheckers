import PySimpleGUI as sg
import copy
import math
import random
from time import sleep



class PublicStats:
    
    turnCount = 1
    cycle = 0
    orbCycleList = [5,10,0,0,3,1,0,2,1]
    def getOrbCount(self):
        
        cycle = PublicStats.turnCount%9
        return PublicStats.orbCycleList[cycle]
                
class Piece:
    def __init__(self,row = None,column = None,playerTurn = None):
        #where the piece is currently residing
        self.location = (row,column)
        #what bonuses the player has
        self.activeBuffs = []
        #what maluses the player has
        self.activeDebuffs = []
        #what the player is holding (need a max; 5?)
        self.storedItems = []
        #what it looks like
        self. avatar = f".//player{playerTurn}default.png"
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
            gameBoard[i][j][0].tileType = "player1default"
            gameBoard[i][j][1].avatar = "default"
            
            
    for i in range(2):
        for j in range(columns):
            #window[rows-i-1,j].update(image_filename="player2default.png")
            gameBoard[rows-i-1][j][0]=Tile(occupied=True)
            piece = Piece(playerTurn = 2)
            #print("Created a piece for player 2")
            gameBoard[rows-i-1][j][1]=piece
            gameBoard[rows-i-1][j][1].location = (rows-i-1,j)
            gameBoard[rows-i-1][j][0].tileType = "player2default"
            gameBoard[rows-i-1][j][1].avatar = "default"
    



def countPieces(gameBoard,window):
    player1count = 0
    player2count = 0
    #print(gameBoard)
    for i in gameBoard:
        for j in i:
            
            if j[1] != 0:
                
                if j[1].ownedBy == 1:
                    print(f"{player1count}: Player one piece at {j[1].location}")
                    player1count+=1
                elif j[1].ownedBy == 2:
                    player2count+=1
                    print(f"{player2count}: Player two piece at {j[1].location}")
    
    window['player1piececount'].update(f"Player 1 controls: {player1count}")
    window['player2piececount'].update(f"Player 2 controls: {player2count}")
    window.refresh()

def gamePlay(playerTurn, window, gameBoard):
    
        countPieces(gameBoard,window)
        createOrbs(window,gameBoard)
        displayBoard(window,gameBoard)
        movePiece(playerTurn, window,gameBoard)
        PublicStats.turnCount += 1
        
        print(f"Turn count is {PublicStats.turnCount}")
        


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
    publicStats = PublicStats()
    orbsToPlace = publicStats.getOrbCount()

    if orbsToPlace > emptySpots:
        orbsToPlace = emptySpots

    while orbsToPlace > 0:
        i = random.randint(0,len(gameBoard)-1)
        j = random.randint(0,len(gameBoard[0])-1)
        print(i,j)
        if gameBoard[i][j] == 0:
            print("Dire error")
        if gameBoard[i][j][0].tileType == "default":
            orbsToPlace -= 1
            print("Placing item orb")
            gameBoard[i][j][0].tileType = "itemOrb"
    
    #sg.popup(f"There are {emptySpots} emptySpots")

        
def displayBoard(window,gameBoard):
    
    for i in range(len(gameBoard)):

        for j in range(len(gameBoard[0])):
            
            if gameBoard[i][j][0].occupied == False:
                
                if gameBoard[i][j][0].tileType == "default":
                    window[i,j].update(image_filename="blank.png")
                elif gameBoard[i][j][0].tileType == "itemOrb":
                    window[i,j].update(image_filename="itemOrb.png")
            else:
               
                if gameBoard[i][j][0].occupied:
                    
                    if gameBoard[i][j][1].ownedBy == 1:
                        if gameBoard[i][j][1].avatar=="default":
                            window[i,j].update(image_filename="player1default.png")
                        elif gameBoard[i][j][1].avatar=="player1stored":
                            window[i,j].update(image_filename="player1stored.png")
                    else:
                        if gameBoard[i][j][1].avatar=="default":
                            window[i,j].update(image_filename="player2default.png")
                        elif gameBoard[i][j][1].avatar=="player2stored":
                            window[i,j].update(image_filename="player2stored.png")
                if gameBoard[i][j][0].occupied == False:
                    print("Not occupied")

                    
def pickUpItemOrb(gameBoard,x,y):
    items = ["Suicide Row"]
    randItem = random.choice(items)
    gameBoard[x][y][1].storedItems.append(randItem)
    playerOwned = gameBoard[x][y][1].ownedBy
    gameBoard[x][y][1].avatar = f"player{playerOwned}stored"
    print(f"Piece has {len(gameBoard[x][y][1].storedItems)}")




def useItems(gameBoard,x,y,window):
    layout = []
    for i in gameBoard[x][y][1].storedItems:
        layout+= [ [sg.Button(i)] ]
    layout+= [ [sg.Button("CANCEL")] ]
    itemsMenu = sg.Window("Items Menu", layout,disable_close=True )

    while True:
        event = itemsMenu.read()

        #if you use Suicide Row
        print (event)
        for i in event:
            
            if str.find(i,"Suicide")>=0:
                print("SUICIDING")
                #for each item inside the specific gameBoard row
                for j in gameBoard[x]:
                    if isinstance(j[1],Piece):
                        if "Shield" in j[1].activeBuffs:
                            print("Shield!")
                            j[1].activeBuffs.remove("Shield")
                            #### Make a function for this
                            j[1].avatar = "default"
                        else:   
                            #set the tile to be empty
                            j[0].occupied = False
                            j[1] = 0
                            j[0].tileType = "default"
            else:
                print("SUICIDE NOT FOUND")
            
            itemsMenu.close()
            return
        if event[0] == "CANCEL":
            itemsMenu.close()
            return
    
        




def movePiece(playerTurn, window, gameBoard):
    while True:
        usedItem = False
        #sg.popup_timed(f" It's player {playerTurn}'s turn.",font = "Cambria, 20",auto_close_duration=1)
        window["itemButton"].update(disabled = True)
        window.refresh()
        sleep(1.25)
        window['playerTurn'].update(f"{playerTurn}")
        window['information'].update(f"Pick a piece to move.")
        event = window.read()
        window["itemButton"].update(disabled = False)
        
                
        
        startLocation = event[0]
        window['information'].update(f"Selection made, pick destination.")
        event = window.read()

        print(event)
        
        if "itemButton" in event and gameBoard[ startLocation[0] ] [ startLocation[1] ] [0].occupied == True:
            print("Pressed item button")
            
            if len(gameBoard[ startLocation[0] ] [ startLocation[1] ] [1].storedItems) > 0 and gameBoard[ startLocation[0] ] [ startLocation[1] ] [1].ownedBy == playerTurn:
                print("VALID")
                useItems(gameBoard,startLocation[0],startLocation[1],window)
                countPieces(gameBoard,window)
                displayBoard(window,gameBoard)
                continue
            elif len(gameBoard[ startLocation[0] ] [ startLocation[1] ] [1].storedItems )< 1:
                print("No items")
                sg.popup("No items")
                continue
            elif gameBoard[ startLocation[0] ] [ startLocation[1] ] [1].ownedBy != playerTurn:
                print("Not yours")
                sg.popup("Not yours")
                continue
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


                #if it's too far
                if getDistance(startLocation[0],startLocation[1],endLocation[0],endLocation[1]) >  gameBoard[ startLocation[0] ] [ startLocation[1] ][1].distanceMax:
                    window['information'].update(f"That location is too far for you to move to!")
                    window.refresh
                    #print( f" {getDistance(startLocation[0],startLocation[1],endLocation[0],endLocation[1])} attempted, {gameBoard[ startLocation[0] ] [ startLocation[1] ].distanceMax} allowed")
                    continue

                #
                #if it's close enough:
                #

                #if the landing spot is an item Orb:
                if gameBoard[ endLocation[0] ] [ endLocation[1] ][0].tileType == "itemOrb":
                    print("ITEM ORB STEPPED ON")
                    pickUpItemOrb(gameBoard,startLocation[0],startLocation[1])
                    
                #if the landing spot is empty
                if gameBoard[ endLocation[0] ] [ endLocation[1] ][0].occupied == False:
                    #print( f" {getDistance(startLocation[0],startLocation[1],endLocation[0],endLocation[1])} attempted, {gameBoard[ startLocation[0] ] [ startLocation[1] ][1].distanceMax} allowed")

                    #copy the actual object over from the old address to the new one
                    gameBoard[endLocation[0]][endLocation[1]][1] = gameBoard[startLocation[0]][startLocation[1]][1]
                    
                    #set the original location as being empty; delete the class; set a default tile
                    gameBoard[ startLocation[0] ] [ startLocation[1] ][0].occupied = False
                    gameBoard[ startLocation[0] ] [ startLocation[1] ][1] = 0
                    gameBoard[startLocation[0]][startLocation[1]][0].tileType = "default"

                    #set the new location as occupied; set the tile as the type of the tile that moved (needs to be updated in future revisions)
                    gameBoard[ endLocation[0] ] [ endLocation[1] ][0].occupied = True
                    gameBoard[ endLocation[0] ] [ endLocation[1] ][1].location = (endLocation[0],endLocation[1])
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
        [sg.T("MegaCheckers",font="Cambria 50"),sg.Button("USE ITEMS",key="itemButton",image_filename = "backpack.png")]
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
