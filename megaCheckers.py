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
        #self. avatar = f".//player{playerTurn}default.png"
        self. avatar = "default"
        self.ownedBy = playerTurn
        self.distanceMax = 1

    def determineAvatar(self):

        #if you have a shield
        if "Energy Forcefield" in self.activeBuffs:
            #and holding an item
            if len(self.storedItems)>0:
                #shield + item
                self.avatar = "shIt"
            else:
                #just shield
                self.avatar = "sh"
        #if you don't have a shield
        else:
            # if you have items
            if len(self.storedItems )>0:
                #items only
                self.avatar = f"player{self.ownedBy}stored"
            else:
                #nothing at all
                self. avatar = "default"

    
    
class Tile:
    def __init__(self, occupied = False):
        self.tileHeight = 0
        self.tileType = "default"
        self.occupied = occupied
    def describeSelf(self):
        
        if self.tileType == "default":
            sg.popup(f"This is a regular tile with an elevation of {self.tileHeight}")
            return
        elif self.tileType == "itemOrb":
            sg.popup(f"This is an item orb tile with an elevation of {self.tileHeight}")
            return
        elif self.tileType == "destroyed":
            sg.popup(f"This tile has been destroyed!  But don't worry, it'll come back in 5 turns.")
            return
        elif self.tileType == "damaged4":
            sg.popup(f"This tile is being repaired.  It'll be ready for business in 4 turns.")
            return
        elif self.tileType == "damaged3":
            sg.popup(f"This tile is being repaired.  It'll be up and at 'em in 3 turns.")
            return
        elif self.tileType == "damaged2":
            sg.popup(f"This tile is being repaired.  It'll be repaired in 2 turns.")
            return
        elif self.tileType == "damaged":
            sg.popup(f"This tile is almost ready!  It'll be ready on the next turn!")
            return
        elif self.tileType == "boobyTrap":
            sg.popup(f"There's an obvious booby trap on this tile.  Don't move here without protection! It has an elevation of {self.tileHeight}")
            return

        
        
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
                    
                    player1count+=1
                elif j[1].ownedBy == 2:
                    player2count+=1
                    
    
    window['player1piececount'].update(f"Player 1 controls: {player1count}\n")
    window['player2piececount'].update(f"Player 2 controls: {player2count}\n")
    window.refresh()

def gamePlay(playerTurn, window, gameBoard):
    
        countPieces(gameBoard,window)
        createOrbs(window,gameBoard)
        displayBoard(window,gameBoard)
        movePiece(playerTurn, window,gameBoard)
        PublicStats.turnCount += 1
        repairFloor(window,gameBoard)
        
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
            #print("Placing item orb")
            gameBoard[i][j][0].tileType = "itemOrb"
    
    #sg.popup(f"There are {emptySpots} emptySpots")

        
def displayBoard(window,gameBoard):
    
    for i in range(len(gameBoard)):

        for j in range(len(gameBoard[0])):

            if gameBoard[i][j][0].tileType == "exploding":
                window[i,j].update(image_filename="exploding.png")
                
            if gameBoard[i][j][0].tileType == "damaged4":
                window[i,j].update(image_filename="damaged4.png")
                
            if gameBoard[i][j][0].tileType == "damaged3":
                window[i,j].update(image_filename="damaged3.png")

            if gameBoard[i][j][0].tileType == "damaged2":
                window[i,j].update(image_filename="damaged2.png")

            if gameBoard[i][j][0].tileType == "damaged":
                window[i,j].update(image_filename="damaged.png")
    
            
            if gameBoard[i][j][0].occupied == False:
                
                if gameBoard[i][j][0].tileType == "default":
                    window[i,j].update(image_filename="blank.png")
                    
                elif gameBoard[i][j][0].tileType == "itemOrb":
                    window[i,j].update(image_filename="itemOrb.png")

                elif gameBoard[i][j][0].tileType == "destroyed":
                    window[i,j].update(image_filename="destroyed.png")
            else:
                if gameBoard[i][j][0].occupied:
                    gameBoard[i][j][1].determineAvatar()
                    
                    if gameBoard[i][j][1].avatar=="default":
                        
                        window[i,j].update(image_filename=f"player{gameBoard[i][j][1].ownedBy}default.png")
                    elif gameBoard[i][j][1].avatar==f"player{gameBoard[i][j][1].ownedBy}stored":
                        window[i,j].update(image_filename=f"player{gameBoard[i][j][1].ownedBy}stored.png")
    
                    elif gameBoard[i][j][1].avatar==f"shIt":
                        window[i,j].update(image_filename=f"p{gameBoard[i][j][1].ownedBy}shIt.png")
                    elif gameBoard[i][j][1].avatar==f"sh":
                        window[i,j].update(image_filename=f"p{gameBoard[i][j][1].ownedBy}sh.png")
                    
                

                    
def pickUpItemOrb(gameBoard,x,y):
    #items = ["suicideBomb Row","Energy Forcefield","suicideBomb Column","Haphazard Airstrike"]
    items = ["Wololo (convert to your side)"]


    
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
        
            #if you use suicideBomb Row
            print (event[0])
            i = event[0]

            if i == None:
                break
            print(i)
            #suicidebomb row
            if str.find(i,"suicideBomb Row")>=0:
                gameBoard[x][y][1].storedItems.remove("suicideBomb Row")
                #for each item inside the specific gameBoard row
                for j in gameBoard[x]:
                    if isinstance(j[1],Piece):
                        if "Energy Forcefield" in j[1].activeBuffs:
                            print("Energy Forcefield!")
                            j[1].activeBuffs.remove("Energy Forcefield")
                            
                        else:   
                            #set the tile to be empty
                            j[0].occupied = False
                            j[1] = 0
                            j[0].tileType = "default"

            #energy forcefield
            elif str.find(i,"Energy Forcefield")>=0:
                gameBoard[x][y][1].storedItems.remove("Energy Forcefield")
                gameBoard[x][y][1].activeBuffs.append("Energy Forcefield")
                displayBoard(window, gameBoard)
                

            #suicidebomb column
            elif str.find(i,"suicideBomb Column")>=0:
                gameBoard[x][y][1].storedItems.remove("suicideBomb Column")
                #for each item inside the specific gameBoard row
                for j in gameBoard:
                    if isinstance(j[y][1],Piece):
                        if "Energy Forcefield" in j[y][1].activeBuffs:
                            print("Energy Forcefield!")
                            j[y][1].activeBuffs.remove("Energy Forcefield")
                            
                        else:   
                            #set the tile to be empty
                            j[y][0].occupied = False
                            j[y][1] = 0
                            j[y][0].tileType = "default"

                            
            elif str.find(i,"Wololo (convert to your side)") >=0:
                    itemsMenu.close()
                    
                    window["information"].update("Choose an enemy to recruit")
                    
                    event = window.read()
                    player = gameBoard[x][y][1].ownedBy
                    if player == 1:
                        enemy = 2
                    elif player == 2:
                        enemy = 1
                    if gameBoard[event[0][0]][event[0][1]][1] == 0:
                        window["information"].update("Choose an enemy, not a vacant tile...")
                        sleep(1)
                        continue
                    elif gameBoard[event[0][0]][event[0][1]][1].ownedBy == enemy:
                        gameBoard[event[0][0]][event[0][1]][1].ownedBy = player
                        gameBoard[x][y][1].storedItems.remove("Wololo (convert to your side)")
                    else:
                        window["information"].update("Wololo only works on enemies.")
                        sleep(1)
                    displayBoard(window, gameBoard)
                    window.refresh()
                    

            elif str.find(i,"Haphazard Airstrike") >=0:
                
                gameBoard[x][y][1].storedItems.remove("Haphazard Airstrike")
                i = 5
                itemsMenu.close()
                while (i > 0):
                    i-=1
                    
                    x = random.randint(0,len(gameBoard)-1)
                    y = random.randint(0,len(gameBoard[0])-1)
                    print(x,y)
                    #if someone is on the spot
                    if gameBoard[x][y][0].occupied == True:
                        #if someone has a forcefield there, don't kill them
                        if "Energy Forcefield" in gameBoard[x][y][1].activeBuffs:
                            print("Energy Forcefield!")
                           
                            backupTile = gameBoard[x][y][0].tileType
                            gameBoard[x][y][0].tileType = "exploding"
                            displayBoard(window,gameBoard)
                            window.refresh()
                            sleep(1)
                            gameBoard[x][y][0].tileType = backupTile
                            gameBoard[x][y][1].activeBuffs.remove("Energy Forcefield")
                            continue
                        else:
                            gameBoard[x][y][0].occupied = False
                            gameBoard[x][y][1] = 0
                            gameBoard[x][y][0].tileType = "exploding"
                            displayBoard(window,gameBoard)
                            window.refresh()
                            sleep(1)
                            gameBoard[x][y][0].tileType = "destroyed"
                            
                    else:
                        
                        
                        gameBoard[x][y][0].occupied = False
                        gameBoard[x][y][1] = 0
                        gameBoard[x][y][0].tileType = "exploding"
                        displayBoard(window,gameBoard)
                        window.refresh()
                        sleep(1)
                        gameBoard[x][y][0].tileType = "destroyed"
                    
                if itemsMenu:    
                    itemsMenu.close()
                return
            if event[0] == "CANCEL":
                itemsMenu.close()
                return
        
def repairFloor (window, gameBoard):
    for i in gameBoard:
        for j in i:
            if j[0].tileType == "destroyed":
                j[0].tileType = "damaged4"
            elif j[0].tileType == "damaged4":
                j[0].tileType = "damaged3"
            elif j[0].tileType == "damaged3":
                j[0].tileType = "damaged2"
            elif j[0].tileType == "damaged2":
                j[0].tileType = "damaged"
            elif j[0].tileType == "damaged":
                j[0].tileType = "default"
    
        




def movePiece(playerTurn, window, gameBoard):
    while True:
        usedItem = False
        #sg.popup_timed(f" It's player {playerTurn}'s turn.",font = "Cambria, 20",auto_close_duration=1)
        window["itemButton"].update(disabled = True)
        window["examineItem"].update(disabled = False)
        window.refresh()
        sleep(1.25)
        window['playerTurn'].update(f"{playerTurn}")
        window['information'].update(f"Pick a piece to move.")
        event = window.read()



        if "examineItem" in event:
            window["examineItem"].update(disabled = True)
            window['information'].update(f"What do you want to examine?",text_color = "red")
            event = window.read()

            
            #if no pieces exist here:
            if gameBoard[event[0][0]][event[0][1]][0].occupied == False:
                gameBoard[event[0][0]][event[0][1]][0].describeSelf()

            #if there is a piece:
            else:
                if playerTurn == gameBoard[event[0][0]][event[0][1]][1].ownedBy:
                    owner = "you"
                else:
                    owner = "your opponent"
                buffslist =""
                debuffslist = ""
                for i in gameBoard[event[0][0]][event[0][1]][1].activeBuffs:
                    buffslist += i + "\n"
                for i in gameBoard[event[0][0]][event[0][1]][1].activeDebuffs:
                    debuffslist += i + "\n"
                if buffslist == "":
                    buffslist = "NONE"
                if debuffslist == "":
                    debuffslist = "NONE"
                sg.popup(f"The piece here belongs to {owner}.\nIt currently holds {len(gameBoard[event[0][0]][event[0][1]][1].storedItems)} inactive items.\nIt has the following buffs:\n{buffslist}\nIt has the current debuffs:\n{debuffslist}")
            window["examineItem"].update(disabled = False)
            continue


            
        window["itemButton"].update(disabled = False)
        window["examineItem"].update(disabled = True)
                
        
        startLocation = event[0]
        window['information'].update(f"Selection made, pick destination.")
        event = window.read()
        window["examineItem"].update(disabled = True)
        endLocation = event[0]
        print(event)

        
        
        if ("itemButton" in event and gameBoard[ startLocation[0] ] [ startLocation[1] ] [0].occupied == True) or (startLocation == endLocation and gameBoard[ startLocation[0] ] [ startLocation[1] ] [0].occupied == True):
            
            
            if len(gameBoard[ startLocation[0] ] [ startLocation[1] ] [1].storedItems) > 0 and (gameBoard[ startLocation[0] ] [ startLocation[1] ] [1].ownedBy == playerTurn):
                
                useItems(gameBoard,startLocation[0],startLocation[1],window)
                countPieces(gameBoard,window)
                displayBoard(window,gameBoard)
                continue
            elif len(gameBoard[ startLocation[0] ] [ startLocation[1] ] [1].storedItems )< 1:
                
                sg.popup("No items here")
                continue
            elif gameBoard[ startLocation[0] ] [ startLocation[1] ] [1].ownedBy != playerTurn:
                
                sg.popup("That's not yours to use.")
                continue
            else:
                sg.popup("Look for this line!!!")
        

        
        if (gameBoard[ startLocation[0] ] [ startLocation[1] ] [0].occupied == False ):
            window['information'].update(f"Nothing exists on the initial square!")
            window.refresh
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



                if gameBoard[ endLocation[0] ] [ endLocation[1] ][0].tileType in ["destroyed","damaged4","damaged3","damaged2","damaged"]:
                    window['information'].update(f"Can't move here!")
                    continue
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
    frame_main = [
                    [sg.Button(image_filename = ".\\blank.png",key=(i,j),size = (20,20), tooltip = "tooltip", pad = (10,10))for j in range (columns)]for i in range(0,rows)
    ]
    
    

    
    frame_layout = [
        [sg.T(f"Player:",font = "Cambria 30",pad = (4,4)), sg.T(f"",key='playerTurn',font = "Cambria 30",pad = (4,4))],
        [sg.T(f" "*100,key = 'information',size = (37,2),font="Cambria 30")]
        ]
    frame_layout2 = [

        [sg.T(f"Player 1 Controls: xx", key = 'player1piececount',font = "Cambria 20", text_color="blue")],
        [sg.T(f"Player 2 Controls: xx",key = 'player2piececount',font = "Cambria 20",text_color="red")]
        
        ]
    layout = [
        [sg.T("MegaCheckers",font="Cambria 50"),sg.Button("USE ITEMS",key="itemButton",image_filename = "backpack.png"),sg.Button("Look",button_color=("Blue","White"),tooltip = "Examine",font = "Cambria 20", key="examineItem",image_filename="examine.png")]
        ]
    layout += [
                        [sg.Frame("Playing Field", frame_main),
                        sg.Frame('Remaining pieces:', frame_layout2,font='Calibri 20', title_color='blue')]]
        
            
    layout += [
        [sg.Frame('Information:', frame_layout,font='Calibri 20', title_color='blue')],
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


    initializeField(columns,rows,window,gameBoard)
    
    
    playerTurn = 1
    while True:
    
        
        gamePlay(playerTurn, window, gameBoard)
        if playerTurn == 1:
            playerTurn = 2
        else:
            playerTurn = 1
        

main()
