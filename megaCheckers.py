import PySimpleGUI as sg
import copy
import math
import random
from time import sleep
from PIL import Image


def initializeField(columns,rows,window,gameBoard):
    for i in range(2):
        for j in range(columns): 
            #window[i,j].update(image_filename="player1default.png")
            gameBoard[i][j][0]=Tile(occupied=True)
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
            gameBoard[rows-i-1][j][1]=piece
            gameBoard[rows-i-1][j][1].location = (rows-i-1,j)
            gameBoard[rows-i-1][j][0].tileType = "player2default"
            gameBoard[rows-i-1][j][1].avatar = "default"
    ###### DELETE ME ##########
    for i in range(2):
        for j in range(columns):
            rows = 6
            #window[rows-i-1,j].update(image_filename="player2default.png")
            gameBoard[rows-i-1][j][0]=Tile(occupied=True)
            piece = Piece(playerTurn = 2)
            gameBoard[rows-i-1][j][1]=piece
            gameBoard[rows-i-1][j][1].location = (rows-i-1,j)
            gameBoard[rows-i-1][j][0].tileType = "player2default"
            gameBoard[rows-i-1][j][1].avatar = "default"
            gameBoard[rows-i-1][j][1].storedItems.append("move again")
            gameBoard[rows-i-1][j][1].activeBuffs.append("move again")
            gameBoard[rows-i-1][j][1].activeBuffs.append("move again")
            gameBoard[rows-i-1][j][1].activeBuffs.append("move again")
            gameBoard[i][j][1].storedItems.append("move again")
            gameBoard[i][j][1].activeDebuffs.append("trip mine")
            gameBoard[i][j][1].storedItems.append("place mine")
            gameBoard[i][j][1].storedItems.append("trip mine radial")
            gameBoard[i][j][1].activeBuffs.append("move diagonal")
            gameBoard[i][j][1].activeBuffs.append("move again")
            gameBoard[i][j][1].activeBuffs.append("move again")
            gameBoard[i][j][1].activeBuffs.append("move again")
            gameBoard[i][j][1].storedItems.append("abolish foe powers radial")
            gameBoard[i][j][1].storedItems.append("purify radial")
            
    ####### END DELETE ME###########

            
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
        self.grey = False
        self.moveAgain = 0
        self.standingOnSelfOrb = False
    def determineAvatar(self):
        pass
    
class Tile:
    def __init__(self, occupied = False):
        self.tileHeight = 0
        self.tileType = "default"
        self.occupied = occupied
    def describeSelf(self):
        
        if self.tileType == "default":
            sg.popup(f"This is a regular tile with an elevation of {self.tileHeight}",keep_on_top=True)
            print(f"This is a regular tile with an elevation of {self.tileHeight}")
            return
        elif self.tileType == "itemOrb":
            sg.popup(f"This is an item orb tile with an elevation of {self.tileHeight}",keep_on_top=True)
            print(f"This is an item orb tile with an elevation of {self.tileHeight}")
            return
        elif self.tileType == "destroyed":
            sg.popup(f"This tile has been destroyed!  But don't worry, it'll come back in 5 turns.",keep_on_top=True)
            print(f"This tile has been destroyed!  But don't worry, it'll come back in 5 turns.")
            return
        elif self.tileType == "damaged4":
            sg.popup(f"This tile is being repaired.  It'll be ready for business in 4 turns.",keep_on_top=True)
            print(f"This tile is being repaired.  It'll be ready for business in 4 turns.")
            return
        elif self.tileType == "damaged3":
            sg.popup(f"This tile is being repaired.  It'll be up and at 'em in 3 turns.",keep_on_top=True)
            print(f"This tile is being repaired.  It'll be up and at 'em in 3 turns.")
            return
        elif self.tileType == "damaged2":
            sg.popup(f"This tile is being repaired.  It'll be repaired in 2 turns.",keep_on_top=True)
            print(f"This tile is being repaired.  It'll be repaired in 2 turns.")
            return
        elif self.tileType == "damaged":
            sg.popup(f"This tile is almost ready!  It'll be ready on the next turn!",keep_on_top=True)
            print(f"This tile is almost ready!  It'll be ready on the next turn!")
            return
        elif self.tileType == "Mine":
            sg.popup(f"There's an obvious booby trap on this tile.  Don't move here without protection! It has an elevation of {self.tileHeight}",keep_on_top=True)
            print(f"There's an obvious booby trap on this tile.  Don't move here without protection! It has an elevation of {self.tileHeight}")
            return
        elif self.tileType in ["trap orb 0", "trap orb 1", "trap orb 2"]:
            sg.popup(f"This is an item orb tile with an elevation of {self.tileHeight}",keep_on_top=True)
            print(f"This is an item orb tile with an elevation of {self.tileHeight}")
            return

def getColumn(location, gameBoard, grow = False,emptyOnly = False):
    validLocations = []
    if grow == False:
        for i in range(len( gameBoard ) ):
            validLocations.append( i,location[1])
        
    return validLocations

def filterEmpty(gameBoard,filterList):
    cleanedList = []
    for i in filterList:
        x = i[0]
        y = i[1]
        if gameBoard[x][y][0].tileType == "default":
            cleanedList.append( (x,y) )
    return cleanedList
            
    
def getRow(location, gameBoard):
    validLocations = []
    if grow == False:
        for i in range(len( gameBoard[0] ) ):
            validLocations.append( location[0],i)
    return validLocations

def getRadial(location, gameBoard, grow = False):
    validLocations = []
    rows = len(gameBoard)
    columns = len(gameBoard[0])
    
    if grow == False:
        #check if you can go one row up
        if location[0]-1 != -1:
            #check if you can also go left after going up (only false if you're in the top left corner)
            if location[1]-1 != -1:
                validLocations.append( (location[0]-1,location[1]-1) )
            #one row up (guaranteed already)
            validLocations.append( (location[0]-1,location[1]+0) )
            #check if you can also go right after going up (only false if you're in the top right corner)
            if location[1]+1 != columns:
                validLocations.append( (location[0]-1,location[1]+1) )
        #check if you can go left
        if location[1]-1 != -1:
            validLocations.append( (location[0],location[1]-1) )
        #you are guaranteed to append yourself
        validLocations.append( (location[0],location[1]) )
        #check if you can go right
        if location[1]+1 != columns:
            validLocations.append( (location[0],location[1]+1) )
        #check if you can go down
        if location[0]+1 != rows:
            #check bottom left
            if location[1]-1 != -1:
                validLocations.append( (location[0]+1,location[1]-1) )
            #bottom guaranteed
            validLocations.append( (location[0]+1,location[1]) )
            #check bottom right
            if location[1]+1 != columns:
                validLocations.append( (location[0]+1,location[1]+1) )
    return validLocations

def getCross(location, gameBoard, grow = False, includeSelf = False):
    validLocations = []
    rows = len(gameBoard)
    columns = len(gameBoard[0])
    #check if you can go up one
    if location[0]-1 != -1:
        #one row up (guaranteed already)
        validLocations.append( (location[0]-1,location[1]+0) )
    #check if you can go left
    if location[1]-1 != -1:
        validLocations.append( (location[0],location[1]-1) )
    if includeSelf == True:
        validLocations.append( (location[0],location[1]) )
    #check if you can go right
    if location[1]+1 != columns:
        validLocations.append( (location[0],location[1]+1) )
    #check if you can go down
    if location[0]+1 != rows:
        #bottom guaranteed
        validLocations.append( (location[0]+1,location[1]) )
    return validLocations
       



def countPieces(gameBoard,window):
    player1count = 0
    player2count = 0
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

def getDistance(a,b,c,d):
    verticalDistance = abs(c-a)
    horizontalDistance = abs(d-b)
    distance = verticalDistance + horizontalDistance
    return distance

def createOrbs(window,gameBoard):
    dangerTurn = 15
    emptySpots = 0
    if PublicStats.turnCount == dangerTurn:
        sg.popup("Warning: mines disguised as item orbs may spawn from now on!  They will explode if either player steps on them.", keep_on_top = True)
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
        if gameBoard[i][j][0].tileType == "default":
            orbsToPlace -= 1
            if PublicStats.turnCount > dangerTurn:
                chanceCheck = random.randint(0,10)
                if chanceCheck > 7:
                     gameBoard[i][j][0].tileType = "trap orb 0"
                     continue    
            gameBoard[i][j][0].tileType = "itemOrb"
    
def deathCheck(window, gameBoard):
    for i in gameBoard:
        for j in i:
            #if a regular mine or laser was stepped on
            if j[0].occupied == True and j[0].tileType in ["mine","laser"]:
                if "forceField" in j[1].activeBuffs:
                    j[1].activeBuffs.remove("forecefield")
                    sg.popup("You were protected from certain death by your forcefield",keep_on_top=True)
                    j[0].tileType = "default"
                else:
                    j[0].tileType = "exploding"
                    j[1] = 0
                    j[0].occupied = False
                    displayBoard(window, gameBoard)
                    window.refresh()
                    sleep(1)
                    j[0].tileType = "default"
                    displayBoard(window, gameBoard)
                    window.refresh()
                    sg.popup("A piece died!",keep_on_top=True)
                    
            #if a trap belonging to your enemy was set
            elif j[0].occupied == True and ( (j[0].tileType == "trap orb 1" and j[1].ownedBy != 1) or (j[0].tileType == "trap orb 2" and j[1].ownedBy != 2)  ):
                if "forceField" in j[1].activeBuffs:
                    j[1].activeBuffs.remove("forecefield")
                    sg.popup("You were protected from certain death by your forcefield",keep_on_top=True)
                    j[0].tileType = "default"
                else:
                    j[0].tileType = "exploding"
                    j[1] = 0
                    j[0].occupied = False
                    displayBoard(window, gameBoard)
                    window.refresh()
                    sleep(1)
                    j[0].tileType = "default"
                    displayBoard(window, gameBoard)
                    window.refresh()
                    sg.popup("A piece died!",keep_on_top=True)
                    
            #if a neutral trap was stepped on
            elif j[0].occupied == True and ( (j[0].tileType == "trap orb 0") ):
                if "forceField" in j[1].activeBuffs:
                    j[1].activeBuffs.remove("forecefield")
                    sg.popup("You were protected from certain death by your forcefield",keep_on_top=True)
                    j[0].tileType = "default"
                else:
                    j[0].tileType = "exploding"
                    j[1] = 0
                    j[0].occupied = False
                    displayBoard(window, gameBoard)
                    window.refresh()
                    sleep(1)
                    j[0].tileType = "default"
                    displayBoard(window, gameBoard)
                    window.refresh()
                    sg.popup("A piece died!",keep_on_top=True)
                
            #do something for holes
                    
        
def displayBoard(window,gameBoard):
    
    for i in range(len(gameBoard)):
        for j in range(len(gameBoard[0])):
            #unoccupied spaces
            if gameBoard[i][j][0].tileType == "exploding":
                window[i,j].update(image_filename="exploding.png")
                continue
                
            elif gameBoard[i][j][0].tileType == "damaged4":
                window[i,j].update(image_filename="damaged4.png")
                continue
                
            elif gameBoard[i][j][0].tileType == "damaged3":
                window[i,j].update(image_filename="damaged3.png")
                continue

            elif gameBoard[i][j][0].tileType == "damaged2":
                window[i,j].update(image_filename="damaged2.png")
                continue

            elif gameBoard[i][j][0].tileType == "damaged":
                window[i,j].update(image_filename="damaged.png")
                continue
    

            elif gameBoard[i][j][0].tileType == "snake":
                window[i,j].update(image_filename="snake.png")
                continue
            

            elif gameBoard[i][j][0].tileType == "abolished":
                window[i,j].update(image_filename="abolished.png")
                continue
            
            if gameBoard[i][j][0].occupied == False:
               
                
                if gameBoard[i][j][0].tileType == "default":
                    window[i,j].update(image_filename="blank.png")
                    continue
                elif gameBoard[i][j][0].tileType == "itemOrb":
                    window[i,j].update(image_filename="itemOrb.gif")
                    continue
                elif gameBoard[i][j][0].tileType == "destroyed":
                    window[i,j].update(image_filename="destroyed.png")
                    continue
                elif gameBoard[i][j][0].tileType == "mine":
                    window[i,j].update(image_filename="mine.png")
                    continue
                elif gameBoard[i][j][0].tileType in ["trap orb 0","trap orb 1", "trap orb 2"]:
                    window[i,j].update(image_filename="trapOrb.gif")
                    continue
                else:
                    sg.popup(f"A tile error has occurred, with type {gameBoard[i][j][0].tileType}",keep_on_top=True)
                    window[i,j].update(image_filename="glitch.png")
                    continue
            else:
                if gameBoard[i][j][0].occupied:
                    g = gameBoard[i][j][1]

                    #set the center color
                    if g.ownedBy == 1:
                        avatar = Image.open("p1.png").convert("RGBA")
                    elif g.ownedBy == 2:
                        avatar = Image.open("p2.png").convert("RGBA")

                    #set the meat of the piece
                    if len(g.storedItems) > 0:
                        item = Image.open("items.png").convert("RGBA")
                        avatar.paste(item, (0,0), item)
                    else:
                        donut = Image.open("donut.png").convert("RGBA")
                        avatar.paste(donut, (0,0), donut)

                    #set a forcefield if it exists
                    if "Energy Forcefield" in g.activeBuffs:
                        forcefield = Image.open("forcefield.png").convert("RGBA")
                        avatar.paste(forcefield, (0,0), forcefield)

                    #if the piece is stunned
                    if "stunned" in g.activeDebuffs:
                        stunned = Image.open("stunned.png").convert("RGBA")
                        avatar.paste(stunned, (0,0), stunned)

                    if "trip mine" in g.activeDebuffs:
                        tripmine = Image.open("tripmine.png").convert("RGBA")
                        avatar.paste(tripmine, (0,0), tripmine)

                    if "purified2" in g.activeBuffs:
                        purified2 = Image.open("purified2.png").convert("RGBA")
                        avatar.paste(purified2, (0,0), purified2)
                    elif "purified1" in g.activeBuffs:
                        purified1 = Image.open("purified1.png").convert("RGBA")
                        avatar.paste(purified1, (0,0), purified1)
                    elif "purified0" in g.activeBuffs:
                        purified0 = Image.open("purified0.png").convert("RGBA")
                        avatar.paste(purified0, (0,0), purified0)
                    
                    
                        
                    #if move diagonal exists:
                    if "move diagonal" in g.activeBuffs:
                        diagonal = Image.open("diagonal.png").convert("RGBA")
                        avatar.paste(diagonal,(0,0),diagonal)

                    #see which type of shoe icon needs to be applied
                    if g.moveAgain == 1:
                        step1 = Image.open("moveAgain1.png").convert("RGBA")
                        avatar.paste(step1, (0,0), step1)
                    elif g.moveAgain == 2:
                        step2 = Image.open("moveAgain2.png").convert("RGBA")
                        avatar.paste(step2, (0,0), step2)
                    elif g.moveAgain == 3:
                        step3 = Image.open("moveAgain3.png").convert("RGBA")
                        avatar.paste(step3, (0,0), step3)
                    elif g.moveAgain > 3:
                        stepMax = Image.open("moveAgainMax.png").convert("RGBA")
                        avatar.paste(stepMax, (0,0), stepMax)


                    if "abolished" in g.activeDebuffs:
                        abolished = Image.open("abolished.png").convert("RGBA")
                        avatar.paste(abolished, (0,0), abolished)
                        
                    #if it's supposed to be highlighted... then highlight it
                    if g.grey == True:
                        grey = Image.open("highlight.png").convert("RGBA")
                        avatar = Image.blend(grey,avatar,.50)

                #for making sure the game doesn't crash due to slow harddrives
                try:
                    avatar.save("avatar.png","png")
                except:
                    window["information"].update("Wait for load...")
                    print("Loading pieces...")
                    sleep(.05)
                    avatar.save("avatar.png","png")
            window[i,j].update(image_filename="avatar.png")
                    
                  
def pickUpItemOrb(gameBoard,x,y):
    #items = ["suicideBomb Row","Energy Forcefield","suicideBomb Column","Haphazard Airstrike","suicideBomb Radial","jumpProof","smartBombs"]
    #items = ["trap orb","place mine","move again","suicideBomb Row","Energy Forcefield","suicideBomb Column","Haphazard Airstrike","suicideBomb Radial","jumpProof","smartBombs", "move diagonal", "trip mine radial", "purify radial", "napalm radial", "abolish foe powers radial", "haymaker"]
    items = ["trap orb"]
    randItem = random.choice(items)
    gameBoard[x][y][1].storedItems.append(randItem)
    playerOwned = gameBoard[x][y][1].ownedBy
    gameBoard[x][y][1].avatar = f"player{playerOwned}stored"
    

def useItems(gameBoard,x,y,window):
    layout = []
    for i in gameBoard[x][y][1].storedItems:
        layout+= [ [sg.Button(i)] ]
    layout+= [ [sg.Button("CANCEL")] ]
    itemsMenu = sg.Window("Items Menu", layout,disable_close=True, keep_on_top = True )
    playerTurn = gameBoard[x][y][1].ownedBy
    rows = len(gameBoard)
    columns = len(gameBoard[0])
    location = (x,y)
    while True:
            event = itemsMenu.read()
            i = event[0]

            if i == None:
                break
            
            #suicidebomb row
            if str.find(i,"suicideBomb Row")>=0:
                gameBoard[x][y][1].storedItems.remove("suicideBomb Row")
                #for each item inside the specific gameBoard row
                for j in gameBoard[x]:
                    if isinstance(j[1],Piece):
                        if "Energy Forcefield" in j[1].activeBuffs:
                            
                            j[1].activeBuffs.remove("Energy Forcefield")
                            
                        else:   
                            #set the tile to be empty
                            j[0].occupied = False
                            j[1] = 0
                            j[0].tileType = "default"

            #trip mine radial
            elif str.find(i,"trip mine radial")>=0:
                gameBoard[x][y][1].storedItems.remove("trip mine radial")
                validTargets = getRadial( (x,y), gameBoard)

                for i in validTargets:
                    g = gameBoard[i[0]][i[1]]

                    if g[0].occupied == True:

                        if g[1].ownedBy != playerTurn:
                            g[1].activeDebuffs.append("trip mine")
                            window["information"].update("Trip mine has been placed")
                            print("The mine has been placed")
                            window.refresh()
                            sleep(.5)
                            #add code for graphics
                            
                            
                            
            #suicidebomb column
            elif str.find(i,"suicideBomb Column")>=0:
                gameBoard[x][y][1].storedItems.remove("suicideBomb Column")
                #for each item inside the specific gameBoard row
                for j in gameBoard:
                    if isinstance(j[y][1],Piece):
                        if "Energy Forcefield" in j[y][1].activeBuffs:
                            
                            j[y][1].activeBuffs.remove("Energy Forcefield")
                            
                        else:   
                            #set the tile to be empty
                            j[y][0].occupied = False
                            j[y][1] = 0
                            j[y][0].tileType = "default"
                            
            #suicidebomb radial
            elif str.find(i,"suicideBomb Radial") >=0:
                gameBoard[x][y][1].storedItems.remove("suicideBomb Radial")
                validTargets = getRadial((x,y),gameBoard)
                
                
                for i in validTargets:
                    x = i[0]
                    y = i[1]
                    
                    if isinstance(gameBoard[x][y][1],Piece):
                        if "Energy Forcefield" in gameBoard[x][y][1].activeBuffs:
                            
                            gameBoard[x][y][1].activeBuffs.remove("Energy Forcefield")
                            
                        else:   
                            #set the tile to be empty
                            gameBoard[x][y][0].occupied = False
                            gameBoard[x][y][1] = 0
                            gameBoard[x][y][0].tileType = "default"

            #napalm row
            elif str.find(i,"napalm row")>=0:
                gameBoard[x][y][1].storedItems.remove("napalm row")
                #for each column inside the row
                for j in gameBoard[x]:
                    if isinstance(j[1],Piece):
                        
                        #if there is a piece
                        if j[0].occupied == True:
                            
                            #if it's the enemy's piece
                            if j[1].ownedBy != playerTurn:
                                #test for forcefield
                                if "Energy Forcefield" in j[1].activeBuffs:
                                    backupTile = j=[0].tileType
                                    j[0].tileType = "exploding"
                                    displayBoard(window,gameBoard)
                                    window.refresh()
                                    sleep(1)
                                    j[0].tileType = backupTile
                                    j[1].activeBuffs.remove("Energy Forcefield")
                                    continue
                                #if no forcefield, kill
                                else:
                                    
                                    j[0].occupied = False
                                    j[1] = 0
                                    j[0].tileType = "exploding"
                                    displayBoard(window,gameBoard)
                                    window.refresh()
                                    sleep(1)
                                    j[0].tileType = "destroyed"
                                    continue
                        #if there isn't a piece    
                        else:   
                            formerTileType = j[0].tileType
                            j[0].tileType = "exploding"
                            displayBoard(window,gameBoard)
                            window.refresh()
                            sleep(1)
                        
                            j[0].tileType = formerTileType
                            displayBoard(window,gameBoard)
                            window.refresh()
                            sleep(1)                                     
                            
            #napalm column
            elif str.find(i,"napalm column")>=0:
                gameBoard[x][y][1].storedItems.remove("napalm column")
                #for each item inside the specific gameBoard row
                for j in gameBoard:
                    if isinstance(j[y][1],Piece):
                        
                        #if there is a piece
                        if j[y][0].occupied == True:
                            
                            #if it's the enemy's piece
                            if j[y][1].ownedBy != playerTurn:
                                #test for forcefield
                                if "Energy Forcefield" in j[y][1].activeBuffs:
                                    backupTile = gameBoard[j][y][0].tileType
                                    j[y][0].tileType = "exploding"
                                    displayBoard(window,gameBoard)
                                    window.refresh()
                                    sleep(1)
                                    j[y][0].tileType = backupTile
                                    j[y][1].activeBuffs.remove("Energy Forcefield")
                                    continue
                                #if no forcefield, kill
                                else:
                                    j[y][0].occupied = False
                                    j[y][1] = 0
                                    j[y][0].tileType = "exploding"
                                    displayBoard(window,gameBoard)
                                    window.refresh()
                                    sleep(1)
                                    j[y][0].tileType = "destroyed"
                                    continue
                        #if there isn't a piece    
                        else:   
                            formerTileType = gameBoard[x][y][0].tileType
                            gameBoard[x][y][0].tileType = "exploding"
                            displayBoard(window,gameBoard)
                            window.refresh()
                            sleep(1)
                        
                            gameBoard[x][y][0].tileType = formerTileType
                            displayBoard(window,gameBoard)
                            window.refresh()
                            sleep(1)


            #napalm Radial
            elif str.find(i,"napalm radial")>=0:
                gameBoard[x][y][1].storedItems.remove("napalm radial")
                validSpots = getRadial((x,y), gameBoard)
                for i in validSpots:
                    
                    g = gameBoard[i[0]][i[1]]

                    #if there's a piece
                    if g[0].occupied == True:

                        if g[1].ownedBy != playerTurn:
                            #test for forcefield
                            if "Energy Forcefield" in g[1].activeBuffs:
                                backupTile = g[0].tileType
                                g[0].tileType = "exploding"
                                displayBoard(window,gameBoard)
                                window.refresh()
                                sleep(1)
                                g[0].tileType = backupTile
                                g[1].activeBuffs.remove("Energy Forcefield")
                                continue
                            #if no forcefield, kill
                            else:
                                g[0].occupied = False
                                g[1] = 0
                                g[0].tileType = "exploding"
                                displayBoard(window,gameBoard)
                                window.refresh()
                                sleep(1)
                                g[0].tileType = "destroyed"
                                continue
                    #if there isn't a piece    
                        else:   
                            formerTileType = g[0].tileType
                            g[0].tileType = "exploding"
                            displayBoard(window,gameBoard)
                            window.refresh()
                            sleep(1)
                        
                            g[0].tileType = formerTileType
                            displayBoard(window,gameBoard)
                            window.refresh()
                            sleep(1)
                    
           #purify radial
            elif str.find(i,"purify radial")>=0:
                gameBoard[x][y][1].storedItems.remove("purify radial")
                validSpots = getRadial((x,y), gameBoard)
                cleanCheck = False
                itemsMenu.close()
                for i in validSpots:
                    
                    g = gameBoard[i[0]][i[1]]

                    #if there's a piece
                    if g[0].occupied == True:

                        if g[1].ownedBy == playerTurn:
                            
                            if len(g[1].activeDebuffs) > 0:
                                print("Purifying...")
                                window["information"].update("Purifying...")
                                for i in g[1].activeDebuffs:
                                    cleanCheck = True
                                    previousTile = g[0].tileType
                                    g[1].activeBuffs.append("purified0")
                                    displayBoard(window,gameBoard)
                                    window.refresh()
                                    #sleep(.01)
                                    g[1].activeBuffs.append("purified1")
                                    displayBoard(window,gameBoard)
                                    window.refresh()
                                    #sleep(.01)
                                    g[1].activeBuffs.append("purified2")
                                    displayBoard(window,gameBoard)
                                    window.refresh()
                                    #sleep(.01)
                                    g[1].activeBuffs.remove("purified0")
                                    g[1].activeBuffs.remove("purified1")
                                    g[1].activeBuffs.remove("purified2")
                                    listOfDebuffs = ""
                                    for j in g[1].activeDebuffs:
                                       listOfDebuffs+=j+"\n"
                                    window["information"].update(f"Removed  {listOfDebuffs}")
                                    print(f"Removed  {listOfDebuffs}")
                                    for j in g[1].activeDebuffs:
                                       g[1].activeDebuffs.remove(j)
                                    window["information"].update(text_color = "blue")
                                    window.refresh()
                                    #sleep(.5)
                                    window["information"].update(text_color = "white")
                                    g[0].tileType = previousTile
                                    displayBoard(window,gameBoard)
                                    window.refresh()
                                    #sleep(.5)
                            
                if cleanCheck == False:
                    window["information"].update(f"No corrupted allies were in range. Nothing happened. Well, that was a pointless waste.")
                    window["information"].update(text_color = "red")
                    window.refresh()
                    sleep(1)
                    window["information"].update(text_color = "white")
                                   
                                    
            #move diagonal
            elif str.find(i,"move diagonal")>=0:
                gameBoard[x][y][1].storedItems.remove("move diagonal")
                gameBoard[x][y][1].activeBuffs.append("move diagonal")
                

            #place mine
            elif str.find(i,"place mine")>=0:
                itemsMenu.close()
                validLocations = getRadial(location,gameBoard)
                validLocations = filterEmpty(gameBoard,validLocations)
                
                
                window["information"].update("Where would you like to place the mine?")
                print("Where would you like to place the mine?")
                event = window.read()
                if (event[0][0],event[0][1]) in validLocations:
                    
                    print(f"mine placed at {event[0][0],event[0][1]}")
                    window["information"].update(f"mine placed at {event[0][0],event[0][1]}")
                    gameBoard[ event[0][0]][event[0][1]][0].tileType = "mine"
                    gameBoard[x][y][1].storedItems.remove("place mine")
                    displayBoard(window, gameBoard)
                    window.refresh()
                    continue
                else:
                    
                    window["information"].update("Can't place mine there.  Only in an empty space in range.")
                    print("Can't place mine there.  Only in an ampty space in range.")
                    continue

            #trap orb
            elif str.find(i,"trap orb")>=0:
                itemsMenu.close()
                validLocations = getRadial(location,gameBoard)
                validLocations = filterEmpty(gameBoard,validLocations)
                
                
                window["information"].update("Where would you like to place the trap?")
                print("Where would you like to place the trap?")
                event = window.read()
                if (event[0][0],event[0][1]) in validLocations:
                    
                    print("Done.")
                    window["information"].update("Done.")
                    gameBoard[ event[0][0]][event[0][1]][0].tileType = f"trap orb {playerTurn}"
                    gameBoard[x][y][1].storedItems.remove("trap orb")
                    displayBoard(window, gameBoard)
                    window.refresh()
                    continue
                else:
                    
                    window["information"].update("Can't place that there.  Only in an empty space in range.")
                    print("Can't place that there.  Only in an ampty space in range.")
                    continue
                    
     
            #abolish foe powers radial
            elif str.find(i,"abolish foe powers radial")>=0:
                gameBoard[x][y][1].storedItems.remove("abolish foe powers radial")
                validSpots = getRadial((x,y), gameBoard)
                abolishCheck = False
                itemsMenu.close()
                for i in validSpots:
                    
                    g = gameBoard[i[0]][i[1]]

                    #if there's a piece
                    if g[0].occupied == True:

                        if g[1].ownedBy != playerTurn:
                            if len(g[1].activeBuffs) > 0:
                                print("abolishing")
                                window["information"].update("abolishing")
                                #print(g[1].activeBuffs)
                                for i in g[1].activeBuffs:
                                    abolishCheck = True
                                    previousTile = g[0].tileType
                                    g[1].activeDebuffs.append("abolished")
                                    displayBoard(window,gameBoard)
                                    window.refresh()
                                    g[1].activeDebuffs.remove("abolished")
                                    #sleep(.5)
                                    listOfBuffs = ""
                                    for j in g[1].activeBuffs:
                                       listOfBuffs+=j+"\n"
                                    window["information"].update(f"Removed  {listOfBuffs}")
                                    print(f"Removed  {listOfBuffs}")
                                    for j in g[1].activeBuffs:
                                       g[1].activeBuffs.remove(j)
                                    window["information"].update(text_color = "blue")
                                    window.refresh()
                                    #sleep(.5)
                                    window["information"].update(text_color = "white")
                                    g[0].tileType = previousTile
                                    displayBoard(window,gameBoard)
                                    window.refresh()
                                    #sleep(.5)
                            
                if abolishCheck == False:
                    window["information"].update(f"No powered enemies were in range. Nothing happened. Well, that was a pointless waste.")
                    print(f"No powered enemies were in range. Nothing happened. Well, that was a pointless waste.")
                    window["information"].update(text_color = "red")
                    window.refresh()
                    sleep(1)
                    window["information"].update(text_color = "white")

                            
            #energy forcefield
            elif str.find(i,"Energy Forcefield")>=0:
                gameBoard[x][y][1].storedItems.remove("Energy Forcefield")
                gameBoard[x][y][1].activeBuffs.append("Energy Forcefield")
                displayBoard(window, gameBoard)


            #move again
            elif str.find(i,"move again")>=0:
                gameBoard[x][y][1].storedItems.remove("move again")
                gameBoard[x][y][1].activeBuffs.append("move again")
                gameBoard[x][y][1].moveAgain +=1
                #sg.popup(f"Activated move again.  Bonus moves per turn: {gameBoard[x][y][1].moveAgain}")
                print(f"Activated move again.  Bonus moves per turn: {gameBoard[x][y][1].moveAgain}")
                displayBoard(window, gameBoard)

                
            #haymaker
            elif str.find(i,"haymaker")>=0:
                
                validTargets = getCross( (x,y), gameBoard)
                window["information"].update("Pick a target that is within range")
                print("Pick a target that is within range.")
                event = window.read()
                #print(validTargets)
                #print(event[0])
                #if the target is within range
                if event[0] in validTargets:
                    #print("It is in the events")

                    
                    

                    #s1 is the victim's row, compare to x
                    s1 = event[0][0]

                    #s2 is the victim's column, compare to y
                    s2 = event[0][1]
                    if gameBoard[s1][s2][0].occupied == False:
                        window["information"].update("There's no one to punch at that location!")
                        print("There's no one to punch at that location!")
                        itemsMenu.close()
                        return
                    
                    gameBoard[x][y][1].storedItems.remove("haymaker")
                    direction = 0
                    #print(x)
                    #print(y)
                    #print(s1)
                    #print(s2)
                    #if they are in the same row:
                    if x == s1:
                        #if x is to the left of the target
                        if y < s2:
                            direction = "push right"
                        #if it's to the right:
                        else:
                            direction = "push left"
                    #if they're in the same column
                    elif y == s2:
                        #if the target is below:
                        if x < s1:
                            #print("pushing down")
                            direction = "push down"
                        #if the target is above
                        else:
                            direction = "push up"

                    else:
                        sg.popup("ERROR IN HAYMAKER DIRECTION CALCULATION",keep_on_top=True)

                        
                    
                    if direction == "push down":
                        #print("enter pushing down")
                        #######TRIPMINE FORCEFIELD CHECK NEEDED#####

                        #copy the original piece
                        tempCopyVictim = copy.deepcopy(gameBoard[s1][s2][1])
                        tempCopyTileType = "default"
                        while True:
                        #check for lower wall
                            
                            if s1 == rows-1:
                                gameBoard[s1][s2][1].activeDebuffs.append("stunned")
                                #######TRIPMINE FORCEFIELD CHECK NEEDED#####
                                break
                            
                            #if the next block is empty
                            elif gameBoard[s1+1][s2][0].occupied == False:
                                #print("next block below is empty")
                                #do laser or land mine check here

                                #end laser or land mine check here


                                #if the next location is a hole
                                if gameBoard[s1+1][s2][0].tileType in ["destroyed","damaged4","damaged3","damaged2","damaged"]:
                                    #kill the piece
                                    gameBoard[s1][s2][1] = 0
                                    gameBoard[s1][s2][0].occupied = False
                                    window["information"].update("Brutal!  You just pushed that piece into the void.")
                                    print("Brutal!  You just pushed that piece into the void.")
                                    break

                                #if the next location is safe
                                else:
                                    
                                    
                                    
                                    gameBoard[s1][s2][0].occupied = False
                                    gameBoard[s1+1][s2][0].occupied = True
                                    gameBoard[s1][s2][0].tileType = tempCopyTileType
                                    gameBoard[s1][s2][1] = 0
                                    gameBoard[s1+1][s2][1] = copy.deepcopy(tempCopyVictim)
                                    gameBoard[s1+1][s2][1].occupied = True
                                    s1 = s1+1
                                    displayBoard(window, gameBoard)
                                    window.refresh()
                                    #sleep(.75)
                                    tempCopyTileType = gameBoard[s1+1][s2][0].tileType 
                               
                                    

                            elif gameBoard[s1+1][s2][0].occupied == True:
                                
                                gameBoard[s1][s2][1].activeDebuffs.append("stunned")
                                gameBoard[s1+1][s2][1].activeDebuffs.append("stunned")
                                window["information"].update("Both of the collided pieces are stunned.")
                                print("Both of the collided pieces are stunned.")
                                break
                                
                                
                    elif direction == "push up":
                        #######TRIPMINE FORCEFIELD CHECK NEEDED#####

                        #copy the original piece
                        tempCopyVictim = copy.deepcopy(gameBoard[s1][s2][1])
                        tempCopyTileType = "default"
                        while True:
                        #check for upper wall
                            
                            if s1 == 0:
                                gameBoard[s1][s2][1].activeDebuffs.append("stunned")
                                #######TRIPMINE FORCEFIELD CHECK NEEDED#####
                                break
                            
                            #if the next block is empty
                            elif gameBoard[s1-1][s2][0].occupied == False:
                                
                                #do laser or land mine check here

                                #end laser or land mine check here


                                #if the next location is a hole
                                if gameBoard[s1-1][s2][0].tileType in ["destroyed","damaged4","damaged3","damaged2","damaged"]:
                                    #kill the piece
                                    gameBoard[s1][s2][1] = 0
                                    gameBoard[s1][s2][0].occupied = False
                                    window["information"].update("Brutal!  You just pushed that piece into the void.")
                                    print("Brutal!  You just pushed that piece into the void.")
                                    break

                                #if the next location is safe
                                else:
                                    
                                    
                                    
                                    gameBoard[s1][s2][0].occupied = False
                                    gameBoard[s1-1][s2][0].occupied = True
                                    gameBoard[s1][s2][0].tileType = tempCopyTileType
                                    gameBoard[s1][s2][1] = 0
                                    gameBoard[s1-1][s2][1] = copy.deepcopy(tempCopyVictim)
                                    gameBoard[s1-1][s2][1].occupied = True
                                    s1 = s1-1
                                    displayBoard(window, gameBoard)
                                    window.refresh()
                                    #sleep(.75)
                                    tempCopyTileType = gameBoard[s1-1][s2][0].tileType 
                               
                                    

                            elif gameBoard[s1-1][s2][0].occupied == True:
                                
                                gameBoard[s1][s2][1].activeDebuffs.append("stunned")
                                gameBoard[s1-1][s2][1].activeDebuffs.append("stunned")
                                window["information"].update("Both of the collided pieces are stunned.")
                                print("Both of the collided pieces are stunned.")
                                break
                                                            
                    elif direction == "push right":
                        
                        #######TRIPMINE FORCEFIELD CHECK NEEDED#####

                        #copy the original piece
                        tempCopyVictim = copy.deepcopy(gameBoard[s1][s2][1])
                        tempCopyTileType = "default"
                        while True:
                        #check for right wall
                            
                            if s2 == columns-1:
                                gameBoard[s1][s2][1].activeDebuffs.append("stunned")
                                #######TRIPMINE FORCEFIELD CHECK NEEDED#####
                                break
                            
                            #if the next block is empty
                            elif gameBoard[s1][s2+1][0].occupied == False:
                                
                                #do laser or land mine check here

                                #end laser or land mine check here


                                #if the next location is a hole
                                if gameBoard[s1][s2+1][0].tileType in ["destroyed","damaged4","damaged3","damaged2","damaged"]:
                                    #kill the piece
                                    gameBoard[s1][s2][1] = 0
                                    gameBoard[s1][s2][0].occupied = False
                                    window["information"].update("Brutal!  You just pushed that piece into the void.")
                                    print("Brutal!  You just pushed that piece into the void.")
                                    break

                                #if the next location is safe
                                else:
                                    
                                    
                                    
                                    gameBoard[s1][s2][0].occupied = False
                                    gameBoard[s1][s2+1][0].occupied = True
                                    gameBoard[s1][s2][0].tileType = tempCopyTileType
                                    gameBoard[s1][s2][1] = 0
                                    gameBoard[s1][s2+1][1] = copy.deepcopy(tempCopyVictim)
                                    gameBoard[s1][s2+1][1].occupied = True
                                    s2 = s2+1
                                    displayBoard(window, gameBoard)
                                    window.refresh()
                                    #sleep(.75)
                                    tempCopyTileType = gameBoard[s1][s2+1][0].tileType 
                               
                                    

                            elif gameBoard[s1][s2+1][0].occupied == True:
                                
                                gameBoard[s1][s2][1].activeDebuffs.append("stunned")
                                gameBoard[s1][s2+1][1].activeDebuffs.append("stunned")
                                window["information"].update("Both of the collided pieces are stunned.")
                                print("Both of the collided pieces are stunned.")
                                break

                            
                    elif direction == "push left":
                        
                        #######TRIPMINE FORCEFIELD CHECK NEEDED#####

                        #copy the original piece
                        tempCopyVictim = copy.deepcopy(gameBoard[s1][s2][1])
                        tempCopyTileType = "default"
                        while True:
                        #check for left
                            
                            if s2 == 0:
                                gameBoard[s1][s2][1].activeDebuffs.append("stunned")
                                #######TRIPMINE FORCEFIELD CHECK NEEDED#####
                                break
                            
                            #if the next block is empty
                            elif gameBoard[s1][s2-1][0].occupied == False:
                                
                                #do laser or land mine check here

                                #end laser or land mine check here


                                #if the next location is a hole
                                if gameBoard[s1][s2-1][0].tileType in ["destroyed","damaged4","damaged3","damaged2","damaged"]:
                                    #kill the piece
                                    gameBoard[s1][s2][1] = 0
                                    gameBoard[s1][s2][0].occupied = False
                                    window["information"].update("Brutal!  You just pushed that piece into the void.")
                                    print("Brutal!  You just pushed that piece into the void.")
                                    break

                                #if the next location is safe
                                else:
                                    
                                    
                                    
                                    gameBoard[s1][s2][0].occupied = False
                                    gameBoard[s1][s2-1][0].occupied = True
                                    gameBoard[s1][s2][0].tileType = tempCopyTileType
                                    gameBoard[s1][s2][1] = 0
                                    gameBoard[s1][s2-1][1] = copy.deepcopy(tempCopyVictim)
                                    gameBoard[s1][s2-1][1].occupied = True
                                    s2 = s2-1
                                    displayBoard(window, gameBoard)
                                    window.refresh()
                                    #sleep(.75)
                                    tempCopyTileType = gameBoard[s1][s2-1][0].tileType 
                               
                                    

                            elif gameBoard[s1][s2-1][0].occupied == True:
                                
                                gameBoard[s1][s2][1].activeDebuffs.append("stunned")
                                gameBoard[s1][s2-1][1].activeDebuffs.append("stunned")
                                window["information"].update("Both of the collided pieces are stunned.")
                                print("Both of the collided pieces are stunned.")
                                break 
                
            #jump proof
            elif str.find(i,"jumpProof")>=0:
                gameBoard[x][y][1].storedItems.remove("jumpProof")
                gameBoard[x][y][1].activeBuffs.append("jumpProof")
                displayBoard(window, gameBoard)
                window["information"].update("Congrats; both of your collided pieces are stunned.")
                
                
            #wololo
            elif str.find(i,"Wololo (convert to your side)") >=0:
                    itemsMenu.close()
                    
                    window["information"].update("Choose an enemy to recruit")
                    print("Choose an enemy to recruit")
                    
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
                        print("Wololo only works on enemies.")
                        sleep(1)
                    displayBoard(window, gameBoard)
                    window.refresh()
                    
            #haphazard airstrike
            elif str.find(i,"Haphazard Airstrike") >=0:
                
                gameBoard[x][y][1].storedItems.remove("Haphazard Airstrike")
                i = 5
                itemsMenu.close()
                while (i > 0):
                    i-=1
                    
                    x = random.randint(0,len(gameBoard)-1)
                    y = random.randint(0,len(gameBoard[0])-1)
                    
                    #if someone is on the spot
                    if gameBoard[x][y][0].occupied == True:
                        #if someone has a forcefield there, don't kill them
                        if "Energy Forcefield" in gameBoard[x][y][1].activeBuffs:
                            
                           
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
                            continue
                            
                    else:
                        
                        
                        gameBoard[x][y][0].occupied = False
                        gameBoard[x][y][1] = 0
                        gameBoard[x][y][0].tileType = "exploding"
                        displayBoard(window,gameBoard)
                        window.refresh()
                        sleep(1)
                        gameBoard[x][y][0].tileType = "destroyed"

            #smartBombs
            elif str.find(i,"smartBombs") >=0:
                attempts = 0
                gameBoard[x][y][1].storedItems.remove("smartBombs")
                i = 3
                itemsMenu.close()
                while (i > 0):
                    i-=1
                    #a check to make sure the plane doesn't get stuck in a pseudo infinite loop in case of special scenarios where pretty much the entire field is full of allied squares
                    attempts += 1
                    if attempts > 100:
                        sg.popup("The plane had trouble finding targets, so it flew away early.",keep_on_top=True)
                        print("The plane had trouble finding targets, so it flew away early.")
                        if itemsMenu:    
                            itemsMenu.close()
                        break

                    
                    
                    #generate a random target location on the field
                    x = random.randint(0,len(gameBoard)-1)
                    y = random.randint(0,len(gameBoard[0])-1)
                    
                    #if someone is on the spot
                    if gameBoard[x][y][0].occupied == True:

                        #if the piece belongs to you, don't attack
                        if gameBoard[x][y][1].ownedBy == playerTurn:
                            #continue the loop by incrementing the conditional
                            i+=1
                            continue
                        #if someone has a forcefield there, don't kill them
                        if "Energy Forcefield" in gameBoard[x][y][1].activeBuffs:
                            backupTile = gameBoard[x][y][0].tileType
                            gameBoard[x][y][0].tileType = "exploding"
                            displayBoard(window,gameBoard)
                            window.refresh()
                            sleep(1)
                            gameBoard[x][y][0].tileType = backupTile
                            gameBoard[x][y][1].activeBuffs.remove("Energy Forcefield")
                            continue
                        #if the enemy is targeted and doesn't have a force field, kill them and the block
                        else:
                            gameBoard[x][y][0].occupied = False
                            gameBoard[x][y][1] = 0
                            gameBoard[x][y][0].tileType = "exploding"
                            displayBoard(window,gameBoard)
                            window.refresh()
                            sleep(1)
                            gameBoard[x][y][0].tileType = "destroyed"
                            continue
                    
                        
                        
                        
                    #attack an unoccupied area        
                    else:
                        #smart bombs have a 20% chance of not hitting empty spaces.  If the 80% check succeeds, try a new spot.
                        redo = random.randint(0,10)
                        if redo < 8:
                            i+=1
                            continue
                        #destroy the piece and the floor
                        gameBoard[x][y][0].occupied = False
                        gameBoard[x][y][1] = 0
                        gameBoard[x][y][0].tileType = "exploding"
                        displayBoard(window,gameBoard)
                        window.refresh()
                        sleep(1)
                        gameBoard[x][y][0].tileType = "destroyed"
                        
            #snake tunneling
            elif str.find(i,"Snake Tunneling") >=0:
                gameBoard[x][y][1].storedItems.remove("Snake Tunneling")

                i = 5
                lastSpace = (x,y)
                while i > 0:
                    i-=1
                    
                    validPoints = getCross( (lastSpace[0],lastSpace[1]), gameBoard)
                    attackSquare = random.choice(validPoints)
                    s1 = attackSquare[0]
                    s2 = attackSquare[1]
                    if attackSquare == lastSpace:
                        i+=1
                        continue
                    lastSpace = attackSquare
                    pieceVictim = gameBoard[s1][s2][1]
                    #tileVictim = gameBoard[s1][s2][0].tileType
                    tileVictim = copy.deepcopy(gameBoard[s1][s2][0])
                    #tileVictim = gameBoard[s1][s2][0]

                    gameBoard[s1][s2][0].tileType = "snake"
                    displayBoard(window,gameBoard)
                    window.refresh()
                    sleep(1)

                    if gameBoard[s1][s2][0].occupied == True:
                        if gameBoard[s1][s2][1].ownedBy != playerTurn:
                            gameBoard[s1][s2][0].occupied = False
                            gameBoard[s1][s2][1] = 0
                            gameBoard[s1][s2][0].tileType = "exploding"
                            displayBoard(window,gameBoard)
                            window.refresh()
                            sleep(1)
                            gameBoard[s1][s2][0].tileType = "default"
                            displayBoard(window,gameBoard)
                            window.refresh()
                            sleep(1)
                            
                            gameBoard[s1][s2][0].tileHeight = 3
                        else:
                            gameBoard[s1][s2][0] = copy.deepcopy(tileVictim)
                            gameBoard[s1][s2][0].tileHeight = 3
                    else:
                        gameBoard[s1][s2][0] = copy.deepcopy(tileVictim)
                        gameBoard[s1][s2][0].tileHeight = 3
                    
                    
                    
                    
                    displayBoard(window,gameBoard)
                    window.refresh()
                    sleep(1)



            #after using the menu, close it
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
    #a small list that is used to make sure a player that gets a second turn for a piece can only use that specific piece twice
    repeatRestrictor = [False, (-1,-1)]
    while True:

        displayBoard(window, gameBoard)
        pickedUpItem = False
        window["exit"].update(disabled = False)
        usedItem = False
        window["itemButton"].update(disabled = True)
        window["examineItem"].update(disabled = False)
        window.refresh()
        
        window['playerTurn'].update(f"{playerTurn}")
        window['information'].update(text_color = "white")

        #pick your piece to move
        window['information'].update(f"Pick a piece to move.")
        print(f"Pick a piece to move.")

        #check to see if this is your second (or higher) turn (you don't get to choose a new piece)
        if repeatRestrictor[0] == False:
            event = window.read()
            window["exit"].update(disabled = False)
        elif repeatRestrictor[0] == True:
            event = []
            event.append(repeatRestrictor[1])
            if event[0] == (-1.-1):
                sg.popup("An error has occurred in repeat restrictor's (-1,-1)",keep_on_top=True)
                repeatRestrictor = False
                return
        if "exit" in event:
            a = sg.popup_yes_no("Seriously, you want to exit this awesome game?",keep_on_top=True)
            print("You're a fool if you're wanting to quit this game.")
            if a == "Yes":
                sg.popup("Wow, your loss.",keep_on_top=True)
                window.close()
                raise SystemExit
            else:
                continue
        window["exit"].update(disabled = True)


        if "examineItem" in event:
            window["examineItem"].update(disabled = True)
            window['information'].update(f"What do you want to examine?",text_color = "red")
            event = window.read()
            window['information'].update(text_color = "white")     
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
                window["information"](f"The piece here belongs to {owner}.\nIt currently holds {len(gameBoard[event[0][0]][event[0][1]][1].storedItems)} inactive items.\nIt has the following buffs:\n{buffslist}\nIt has the current debuffs:\n{debuffslist}")
                print(f"The piece here belongs to {owner}.\nIt currently holds {len(gameBoard[event[0][0]][event[0][1]][1].storedItems)} inactive items.\nIt has the following buffs:\n{buffslist}\nIt has the current debuffs:\n{debuffslist}")
            window["examineItem"].update(disabled = False)
            continue


        window["itemButton"].update(disabled = False)
        window["examineItem"].update(disabled = True)
                
        
        startLocation = event[0]
        #print(f"{startLocation} and {repeatRestrictor[1]}")
        if (repeatRestrictor[0] == True) and (startLocation != repeatRestrictor[1]):
            getChoice = sg.popup_yes_no("You can only move the same piece twice.  Click yes to force that piece to be selected.  Otherwise choose no to end your turn.",keep_on_top=True)
            if getChoice == "Yes":
                startLocation = repeatRestrictor[1]
            else:
                return
        if (repeatRestrictor[0] == True) and (startLocation == repeatRestrictor[1]):
            gameBoard[startLocation[0]][startLocation[1]][1].grey = True
            displayBoard(window, gameBoard)
            
        
        #if a square is picked and a piece exists on it
        if gameBoard[event[0][0]][event[0][1]][0].occupied == True:

            #if that piece is stunned
            if playerTurn == gameBoard[event[0][0]][event[0][1]][1].ownedBy and "stunned" in gameBoard[event[0][0]][event[0][1]][1].activeDebuffs:
                window['information'].update(f"You cannot use a stunned/sleeping piece.")
                print(f"Pick a piece to move.")
                window['information'].update(text_color = "red")
                window.refresh()
                continue
            
            #if the piece belongs to you and it has items (and isn't stunned)
            elif playerTurn == gameBoard[event[0][0]][event[0][1]][1].ownedBy and len(gameBoard[event[0][0]][event[0][1]][1].storedItems) > 0:
                window['information'].update(f"Selection made, pick a destination or click the same piece again to access items.")
                print(f"Selection made, pick a destination or click the same piece again to access items.")
            #if the piece doesn't belong to you
            elif playerTurn != gameBoard[event[0][0]][event[0][1]][1].ownedBy:
                window['information'].update(f"That's not your piece...")
                print(f"That's not your piece...")
                window['information'].update(text_color = "red")
                window.refresh()
                continue
            #if the piece belongs to you but doesn't have items
            else:
                window['information'].update(f"Selection made, pick a destination.")
                print(f"Selection made, pick a destination.")
                
        #if there's no piece on that square
        else:
            window['information'].update(text_color = "red")
            window['information'].update(f"You can't interact directly with unoccupied spaces.")
            print(f"You can't interact directly with unoccupied spaces.")
            window.refresh()
            
            sleep(.25)
            continue
        
        #if there is a piece there and it belongs to you, highlight it to show you selected it
        if gameBoard[startLocation[0]][startLocation[1]][1] != 0:
            gameBoard[startLocation[0]][startLocation[1]][1].grey = True
        

        #update the board (to show highlighting)
        displayBoard(window,gameBoard)


        #get the next location
        event = window.read()

        
        window["examineItem"].update(disabled = True)

        #this is where we're attempting to move
        endLocation = event[0]

        

        
        #trying to use item
        if ("itemButton" in event and gameBoard[ startLocation[0] ] [ startLocation[1] ] [0].occupied == True) or (startLocation == endLocation and gameBoard[ startLocation[0] ] [ startLocation[1] ] [0].occupied == True):
            
            #check to see if it's legal to use item
            if len(gameBoard[ startLocation[0] ] [ startLocation[1] ] [1].storedItems) > 0 and (gameBoard[ startLocation[0] ] [ startLocation[1] ] [1].ownedBy == playerTurn):
                
                useItems(gameBoard,startLocation[0],startLocation[1],window)
                
                
                if gameBoard[startLocation[0]][startLocation[1]][0].occupied == True:
                    gameBoard[startLocation[0]][startLocation[1]][1].grey = False
                countPieces(gameBoard,window)
                displayBoard(window,gameBoard)
                continue
            #if the piece isn't yours
            elif gameBoard[ startLocation[0] ] [ startLocation[1] ] [1].ownedBy != playerTurn:
                gameBoard[ startLocation[0] ] [ startLocation[1] ] [1].grey = False
                window["information"].update("That's not your piece.")
                print("That's not your piece")
                continue
            
            #if the piece has no items
            elif len(gameBoard[ startLocation[0] ] [ startLocation[1] ] [1].storedItems )< 1:
                gameBoard[ startLocation[0] ] [ startLocation[1] ] [1].grey = False
                window["information"].update("No items on this piece.")
                print("There are no items on this piece.")
                continue
            #shouldn't get to here
            else:
                print("An error occurred in item lookups")
                window["information"].update("An error occurred in item lookups")
        

        #if there isn't any piece on the square
        if (gameBoard[ startLocation[0] ] [ startLocation[1] ] [0].occupied == False ):
            window['information'].update(f"Nothing exists on the initial square!")
            print(f"Nothing exists on the initial square!")
            window.refresh
            continue

        #if the piece no longer exists on the original point, ungrey it
        if gameBoard[startLocation[0]][startLocation[1]][1] != 0:
            gameBoard[startLocation[0]][startLocation[1]][1].grey = False
        displayBoard(window,gameBoard)    
            
        
        #if the spot you're moving from contains a piece (which it should)
        if( gameBoard[ startLocation[0] ] [ startLocation[1] ] [0] .occupied):
            #if the piece is yours
            if (gameBoard[ startLocation[0] ] [ startLocation[1] ][1].ownedBy == playerTurn):
                
                #assume the player isn't trying to move diagonally at first
                diagonalCheck = False
                #if it's too far...
                #...but you have a move diagonal and it turns out you're actually within range:
                if getDistance(startLocation[0],startLocation[1],endLocation[0],endLocation[1]) > 1:
                    if "move diagonal" in gameBoard[ startLocation[0] ] [ startLocation[1] ] [1].activeBuffs:
                        validRange = getRadial( (startLocation[0],startLocation[1]),gameBoard)
                        #if they're trying to move diagonally
                        if (endLocation[0],endLocation[1]) in validRange:
                            diagonalCheck = True
                            
                
                #....and it's not because you want to move diagonally with a move diagonal
                if (getDistance(startLocation[0],startLocation[1],endLocation[0],endLocation[1]) >  gameBoard[ startLocation[0] ] [ startLocation[1] ][1].distanceMax) and diagonalCheck == False:
                    window['information'].update(f"That location is too far for you to move to!")
                    print(f"That location is too far for you to move to!")
                    window.refresh
                    
                    continue

                #
                #if it's close enough:
                #

                #if the landing spot is an item Orb:
                if gameBoard[ endLocation[0] ] [ endLocation[1] ][0].tileType == "itemOrb":
                    
                    pickUpItemOrb(gameBoard,startLocation[0],startLocation[1])
                    pickedUpItem = True
                    

                if gameBoard[ endLocation[0] ] [ endLocation[1] ][0].tileType in ["destroyed","damaged4","damaged3","damaged2","damaged"]:
                    window['information'].update(f"Can't move here!")
                    print("Can't move here!")
                    continue
                #if the landing spot is not occupied by a piece
                if gameBoard[ endLocation[0] ] [ endLocation[1] ][0].occupied == False:
                   

                    #copy the actual piece object over from the old address to the new one (deepcopy needed?)
                    gameBoard[endLocation[0]][endLocation[1]][1] = gameBoard[startLocation[0]][startLocation[1]][1]
                    
                    #set the original location as being empty; delete the class; set a default tile
                    gameBoard[ startLocation[0] ] [ startLocation[1] ][0].occupied = False
                    gameBoard[ startLocation[0] ] [ startLocation[1] ][1] = 0
                    
                    if gameBoard[endLocation[0]][endLocation[1]][1].standingOnSelfOrb == True:
                        gameBoard[startLocation[0]][startLocation[1]][0].tileType = f"trap orb {playerTurn}"
                    else:
                        gameBoard[startLocation[0]][startLocation[1]][0].tileType = "default"

                    #set the new location as occupied; set the tile as the type of the tile that moved (needs to be updated in future revisions)
                    gameBoard[ endLocation[0] ] [ endLocation[1] ][0].occupied = True
                    gameBoard[ endLocation[0] ] [ endLocation[1] ][1].location = (endLocation[0],endLocation[1])
                    #check for mine death
                    deathCheck(window, gameBoard)
                    
                    if gameBoard[ endLocation[0]][endLocation[1]][1] != 0 and gameBoard[ endLocation[0]][endLocation[1]][0].tileType != f"trap orb {playerTurn}":
                        gameBoard[ endLocation[0]][endLocation[1]][0].tileType = f"player{playerTurn}default"
                    elif gameBoard[ endLocation[0]][endLocation[1]][1] == 0:
                        break



                    
                    if gameBoard[ endLocation[0] ] [ endLocation[1] ][0].tileType == f"trap orb {playerTurn}":
                        gameBoard[ endLocation[0] ] [ endLocation[1] ][1].standingOnSelfOrb = True
                    
                    if "trip mine" in gameBoard[ endLocation[0] ] [ endLocation[1] ][1].activeDebuffs:
                        
                        
                        if "Energy Forcefield" in gameBoard[ endLocation[0] ] [ endLocation[1] ][1].activeBuffs:
                            gameBoard[ endLocation[0] ] [ endLocation[1] ][1].activeBuffs.remove("Energy Forcefield")
                            window["information"].update("Trip mine went off!")
                            print("Trip mine went off!")
                            sleep(1)
                            window["information"].update("But your forcefield saved you.")
                            print("...But your forcefield saved you.")
                            while ("trip mine" in gameBoard[ endLocation[0] ] [ endLocation[1] ][1].activeBuffs):
                                gameBoard[ endLocation[0] ] [ endLocation[1] ][1].activeDebuffs.remove("trip mine")

                        else:
                            gameBoard[ endLocation[0] ] [ endLocation[1] ][0].occupied = False
                            gameBoard[ endLocation[0] ] [ endLocation[1] ][1] = 0
                            
                            
                            gameBoard[ endLocation[0] ] [ endLocation[1] ][1] = 0
                            gameBoard[ endLocation[0] ] [ endLocation[1] ][0].tileType = "exploding"
                            displayBoard(window,gameBoard)
                            window.refresh()
                            sg.popup("Trip mine went off!",keep_on_top=True)
                            gameBoard[ endLocation[0] ] [ endLocation[1] ][0].tileType = "default"
                            break


                    
                    window['information'].update(f"Moved successfully!")
                    print("Moved successfully")
                    window.refresh


                    #go again if you have moveAgain equipped

                 
                    
                    if gameBoard[ endLocation[0] ] [ endLocation[1] ][1]!=0 and gameBoard[ endLocation[0] ] [ endLocation[1] ][1].moveAgain >0:
                        
                        window['information'].update(f"This piece gets to move again; {gameBoard[ endLocation[0] ] [ endLocation[1] ][1].moveAgain} remaining!")
                        displayBoard(window, gameBoard)
                        moveAgainCheck = sg.popup_yes_no("Would you like to move it again?",keep_on_top=True)
                        if moveAgainCheck == "Yes":
                            gameBoard[ endLocation[0] ] [ endLocation[1] ][1].moveAgain -=1
                            repeatRestrictor[0] = True
                            repeatRestrictor[1] = ( (endLocation[0],endLocation[1]) )
                            continue
                        else:
                            return
                        
                    else:
                        return 1

                
                #killing own piece (illegal)
                elif gameBoard[ endLocation[0] ] [ endLocation[1] ][1].ownedBy == playerTurn:
                    window['information'].update(f"You can't jumpkill your own piece.")
                    print("You can't jumpkill your own piece.")
                    window.refresh
                    continue

                
                    
                #kill enemy piece; elif enemy owns the ending location
                elif gameBoard[ endLocation[0] ] [ endLocation[1] ][1].ownedBy != playerTurn:
                    #test to see if the piece can be jumped
                    if "jumpProof" in gameBoard[ endLocation[0] ] [ endLocation[1] ][1].activeBuffs:
                        window['information'].update(f"No! This opponent is jump proof!")
                        print("No!  This opponent is jump proof!")
                        window.refresh()
                        sleep(1)
                        continue
                        
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

                    #if gameBoard[startLocation[0]][startLocation[1]][0].tileType == "itemOrb":
                    if pickedUpItem == True:
                        window['information'].update("The piece you just killed was sitting on an item orb.  You picked it up.  Lucky you got to it before he recovered from his stun")
                        print("The piece you just killed was sitting on an item orb.  You picked it up.  Lucky you got to it before he recovered from his stun")
                        #pickUpItemOrb(gameBoard,x,y)
                        
                    #set the original tile as either a trap orb or default, depending on what was there
                    if gameBoard[endLocation[0]][endLocation[1]][1].standingOnSelfOrb == True:
                        gameBoard[startLocation[0]][startLocation[1]][0].tileType = f"trap orb {playerTurn}"
                    else:
                        gameBoard[startLocation[0]][startLocation[1]][0].tileType = "default"
                        
                    if "Energy Forcefield" in gameBoard[ endLocation[0] ] [ endLocation[1] ][1].activeBuffs:
                            gameBoard[ endLocation[0] ] [ endLocation[1] ][1].activeBuffs.remove("Energy Forcefield")
                            window["information"].update("Trip mine went off!")
                            print("Trip mine went off!")
                            sleep(1)
                            window["information"].update("But your forcefield saved you.")
                            print("...But your forcefield saved you.")
                            while ("trip mine" in gameBoard[ endLocation[0] ] [ endLocation[1] ][1].activeBuffs):
                                gameBoard[ endLocation[0] ] [ endLocation[1] ][1].activeDebuffs.remove("trip mine")

                    else:
                            gameBoard[ endLocation[0] ] [ endLocation[1] ][0].occupied = False
                            gameBoard[ endLocation[0] ] [ endLocation[1] ][1] = 0
                            
                            
                            gameBoard[ endLocation[0] ] [ endLocation[1] ][1] = 0
                            gameBoard[ endLocation[0] ] [ endLocation[1] ][0].tileType = "exploding"
                            displayBoard(window,gameBoard)
                            window.refresh()
                            sg.popup("Trip mine went off!",keep_on_top=True)
                            gameBoard[ endLocation[0] ] [ endLocation[1] ][0].tileType = "default"
                            break
                    
                    
                    window['information'].update(f"Jumpkilled an enemy piece!")
                    print("Jumpkilled an enemy piece!")



                    #go again if you have moveAgain equipped
                    if gameBoard[ endLocation[0] ] [ endLocation[1] ][1]!=0 and gameBoard[ endLocation[0] ] [ endLocation[1] ][1].moveAgain >0:


                        #sg.popup(f"Jump killer repeater {gameBoard[ endLocation[0] ] [ endLocation[1] ][1].moveAgain}",keep_on_top=True)
                        
                        window['information'].update(f"This piece gets to move again; {gameBoard[ endLocation[0] ] [ endLocation[1] ][1].moveAgain} remaining!")
                        #sleep(1)
                        moveAgainCheck = sg.popup_yes_no("Would you like to move it again?",keep_on_top=True)
                        
                        if moveAgainCheck == "Yes":
                            
                            gameBoard[ endLocation[0] ] [ endLocation[1] ][1].moveAgain -=1
                            repeatRestrictor[0] = True
                            repeatRestrictor[1] = ( (endLocation[0],endLocation[1]))
                            continue
                        else:
                            return
                    return 2
                    


            else:
                window['information'].update(f"That's not your piece!")
                print("That's not your piece!")
                window.refresh
                continue
                
        else:
            window['information'].update(f"Nothing here to move!")
            print("Nothing here to move!")
            window.refresh
            continue
        
def resetMoveAgain(gameBoard):
    moveAgainCount = 0
    for i in gameBoard:
        for j in i:
            moveAgainCount = 0
            if j[0].occupied == True:
                if len(j[1].activeBuffs)>0:
                    for k in j[1].activeBuffs:
                        if k == "move again":
                            moveAgainCount +=1
            if j[0].occupied == True:
                j[1].moveAgain = moveAgainCount
                
                    
    
def begin():
    
    #variables 
    columns = 10
    rows = 10
    gameBoard = []
    
    
    #window
    frame_main = [  
                    [sg.Button(image_filename = ".\\blank.png",key=(i,j),size = (75,75), button_color = ("white","grey"), tooltip = "square", pad = (2,2))for j in range (columns)]for i in range(0,rows)
    ]

    frame_remaining = [ [sg.T(f"Player 1 Controls: xx", key = 'player1piececount',font = "Cambria 20", text_color="blue")],
        [sg.T(f"Player 2 Controls: xx",key = 'player2piececount',font = "Cambria 20",text_color="red")],]
    
    
    
    
    frame_layout = [
        [sg.Image("up.png", key = "turn",visible = True)],
        [sg.T(f"Player:",font = "Cambria 30",pad = (4,4)), sg.T(f"",key='playerTurn',font = "Cambria 30",pad = (4,4))],
        [sg.T(f" "*50,key = 'information',size = (37,3),font="Cambria 30")],
        [sg.Frame("Pieces Remaining",frame_remaining)],
        [sg.Output(size=(70,10),background_color = "silver", font = "Cambria 18", text_color = "black")]
        ]
   
    layout = [
        [sg.T("MegaCheckers",font="Cambria 50"),sg.Button("USE ITEMS",key="itemButton",image_filename = "backpack.png"),sg.Button("Look",button_color=("Blue","White"),tooltip = "Examine",font = "Cambria 20", key="examineItem",image_filename="examine.png"),sg.Button("Exit",key="exit")]
        ]
    layout += [
                         
                            [sg.Frame("Playing Field", frame_main),sg.Frame('Information:', frame_layout,font='Calibri 20', title_color='blue')],
                        
            ]
        

    window = sg.Window("MegaCheckers",layout,no_titlebar = True,disable_close = True, grab_anywhere = True, location = (0,0)).finalize()

    #window.maximize()
    
    
    
    #gameBoard for logic
    gameBoard = []
    line = []
    for i in range(columns):
        line.append([Tile(),0])
        gameBoard.append(0)
    
    
    for j in range(rows):
        gameBoard[j] = copy.deepcopy(line)
    

    initializeField(columns,rows,window,gameBoard)
    resetMoveAgain(gameBoard)
    
    
    playerTurn = 1
    while True:
    
        
        gamePlay(playerTurn, window, gameBoard)
        x = -1
        y = -1
        #end player one's turn, begin player two's turn
        if playerTurn == 1:
            window["turn"].update(filename = "down.png")
            for i in gameBoard:
                x+=1
                for j in i:
                    y+=1
                    if j[0].occupied == True:
                        if j[1].ownedBy == 1:
                            if "stunned" in j[1].activeDebuffs:
                                j[1].activeDebuffs.remove("stunned")
                                if j[0].tileType == "itemOrb":
                                    sg.popup("A stunned piece recovered and picked up the item orb it had landed on",keep_on_top=True)
                                    pickUpItemOrb(gameBoard,x,y)
                y=-1
            playerTurn = 2
            resetMoveAgain(gameBoard)
            
        #end player two's turn, begin player one's turn
        else:
            window["turn"].update(filename = "up.png")
            for i in gameBoard:
                x+=1
                for j in i:
                    y+=1
                    if j[0].occupied == True:
                        if j[1].ownedBy == 2:
                            if "stunned" in j[1].activeDebuffs:
                                j[1].activeDebuffs.remove("stunned")
                                if j[0].tileType == "itemOrb":
                                    sg.popup("A stunned piece recovered and picked up the item orb it had landed on",keep_on_top=True)
                                    pickUpItemOrb(gameBoard,x,y)
                y=-1
            playerTurn = 1
            resetMoveAgain(gameBoard)


def tutorial():


    #variables 
    columns = 10
    rows = 10
    gameBoard = []
    
    frame_1 = [
        
            [sg.Button("Object of the game",key="object")],
            [sg.Button("How to select a piece",key="select")],
            [sg.Button("How to move",key="move")],
            [sg.Button("Items",key="items")],
            [sg.Button("Getting info on pieces",key="info")],
            [sg.Button("EXIT",key = "EXIT")]

        ]
    frame_2 = [
        [sg.Button(image_filename = ".\\blank.png",key=(i,j),size = (20,20), tooltip = "tooltip", pad = (10,10))for j in range (columns)]for i in range(0,rows)
        ]
    frame_3 = [

        [sg.T(" "*100, key = "tutorialInfo", font = "Cambria 20",size= (50,5))]

        ]
    frame_4 = [

        [sg.T(" "* 100,key = "information", font = "Cambria 20",size = (88,20) ) ]

        ]
    
    layout = [
                [sg.T("MegaCheckers", font = "Cambria 50",key = "title"), sg.Button("use item",image_filename = "./backpack.png",visible = False)],
                
                
        ]
    layout+= [
        
        [sg.Frame("Main screen",frame_1,key= "options",visible = True), sg.Frame("Game Play", frame_2, key = "gamePlay",visible=True)]
         ]
    layout += [
        [sg.Frame( "Tutorial Info",frame_3), sg.Frame("Information", frame_4)]
        ]




    #gameBoard for logic
    gameBoard = []
    line = []
    for i in range(columns):
        line.append([Tile(),0])
        gameBoard.append(0)
    
    
    for j in range(rows):
        gameBoard[j] = copy.deepcopy(line)


    

    window = sg.Window("MegaCheckers",layout,location = (0,0)).finalize()

    initializeField(columns,rows,window,gameBoard)
            
    
    window["options"].update(visible = True)

    while True:
        event = window.read()
        if event[0] == "EXIT":
            #QUIT
            window.close()
            raise SystemExit
        if event[0] == "object":
            window["gamePlay"].update(visible = True)
            myText = """OBJECT: The object of the game is to destroy all of your opponent's pieces or make it impossible for them to take a turn.  Your main method to do this will be by jumping on enemy pieces to kill them (don't worry, the pieces aren't sentient, so no one is getting hurt).  You will also be able to employ items that you find on the field to either protect yourself from your enemies or to blow them up someway or another."""
            window["tutorialInfo"].update(myText)

            
        elif event[0] == "select":
            window["gamePlay"].update(visible = True)
            while True:
                myText = """SELECTING A PIECE: to select your piece, simply left click on it.  Try it now!  Left click a blue piece."""
                window["tutorialInfo"].update(myText)
                displayBoard(window,gameBoard)
                

                
                event = window.read()

                if event[0] in ["object","select","move","items","info","cancel"]:
                    sg.popup("Restarting tutorial",keep_on_top=True)
                    window.close()
                    tutorial()
                if event[0] == "EXIT":
                    sg.popup("Exiting to main screen.",keep_on_top=True)
                    window.close()
                    main()

                
                x = int(event[0][0])
                y = int(event[0][1])
                if gameBoard[event[0][0]][event[0][1]][1]!=0 and gameBoard[x][y][1].ownedBy == 1:
                    myText = "Great job!  You've selected a piece.  Move onto a different topic."
                    window["tutorialInfo"].update(myText)
                    break
                else:
                    myText = "Sorry, that's not right.  Left click on a blue piece."
                    window["tutorialInfo"].update(myText,text_color="red")
                    window.refresh()
                    sleep(1)
                    window["tutorialInfo"].update(myText,text_color="white")
                    
                    
        elif event[0] == "move":
                window["gamePlay"].update(visible = True)
                outOfRangeTutorialIncomplete = True
                while True:
                    
                    while True:
                        notValidSelection = True
                        myText = """MOVING: normally you can move once per turn, and can only move one piece per turn.  Unless they have specific items, pieces can only move one space forward/back/sideways.  Let's try moving a piece now!  Start by selecting a blue piece on the second row from the top."""
                        window["tutorialInfo"].update(myText)
                        displayBoard(window,gameBoard)
                        while notValidSelection:
                            event = window.read()
                            
                            if event[0][0] == 1:
                                validSelection = False
                                myText = "Good work!  Now we can continue on to the next step."
                                rowOrig = event[0][0]
                                colOrig = event[0][1]
                                window["tutorialInfo"].update(myText)
                                window.refresh()
                                sleep(1.5)
                                break
                            else:
                                myText = "That's not correct.  You'll have to select a blue piece on the second row before we can continue."
                                window["tutorialInfo"].update(myText,text_color="red")
                                window.refresh()
                                sleep(1)
                                window["tutorialInfo"].update(myText,text_color="white")
                                
                        
                        window['information'].update(f"Piece selected!  Choose a destination tile within range.")
                        window.refresh
                        if outOfRangeTutorialIncomplete == True:
                            myText = """Now that we have clicked on one of your pieces, we can move it.  Notice that the information window lets you know that your piece was selected.  It's asking you to choose a location within range.  HOWEVER - try clicking on any empty space EXCEPT the one that's right in front of your selected piece."""
                        else:
                            myText = """Now that you know what it looks like when you try to move to an invalid space, let's do a valid space.  Choose the spot right in front of your selected piece."""
                            
                        window["tutorialInfo"].update(myText)
                        window.refresh()
                        event = window.read()
                        
                        if (event[0][0] < 2) or (event[0][0]) > (rows-2) and outOfRangeTutorialIncomplete == True:
                            myText = """That's not right.  For this tutorial, we need you to click on an empty space.  You clicked on a space that's occupied.  No worries, let's start over."""
                            window["tutorialInfo"].update(myText,text_color = "red")
                            sleep(2)
                            window["tutorialInfo"].update(myText,text_color = "white")
                            break
                        if (event[0][0] == rowOrig+1) and (event[0][1] == colOrig) and outOfRangeTutorialIncomplete == True :
                            myText = """You're getting ahead of yourself.  Normally this would be the right move, but trust me...  Just do what the tutorial says and pick any empty spot except for this one."""
                            window["tutorialInfo"].update(myText,text_color = "red")
                            window["information"].update("")
                            window.refresh()
                            sleep(4)
                            window["tutorialInfo"].update(myText,text_color = "white")
                            continue
                        if outOfRangeTutorialIncomplete == False and event[0][0] == rowOrig+1 and event[0][1] == colOrig:
                            myText = "Good job!  You've successfully moved a piece!  If you move onto a enemy in this way, you kill it!  Click on the items tutorial next!"
                            
                           
                            window["tutorialInfo"].update(myText,text_color = "white")
                            playerBackup = gameBoard[rowOrig][colOrig][1]
                            gameBoard[rowOrig][colOrig][1] = 0
                            gameBoard[event[0][0]][event[0][1]][1] = playerBackup


                            

                            
                            gameBoard[rowOrig][colOrig][0].occupied = False
                            gameBoard[rowOrig][colOrig][0].tileType = "default"
                            gameBoard[rowOrig+1][colOrig][0].occupied = True
                            displayBoard(window,gameBoard)
                            window.refresh()
                            window.read()
                            window.close()
                            tutorial()
                        else:
                            if outOfRangeTutorialIncomplete == True:
                                window['information'].update(f"That location is too far for you to move to!")
                                myText = "Good work!  Notice the error message in the information box.  During normal gameplay, you can keep an eye out on it to see what you can do.  Alright, now that you know what happens if you try to move out of range, let's try doing an actual move.  Choose a blue piece and then move it one square forward."""
                                window["tutorialInfo"].update(myText,text_color = "white")
                                window.refresh()
                                sleep(4)
                                window["information"].update("")
                                outOfRangeTutorialIncomplete = False
                                window.refresh
                                sleep(2)
                                break
                            else:
                                myText = """That's not a valid choice.  Let's try again."""
                                window["tutorialInfo"].update(myText,text_color = "white")
                                window.refresh()
                                sleep(1)
                            
                                
        elif event[0] == "items":
            myText = "This part of the tutorial assumes you've mastered selecting your pieces and moving around.  If you're still not familiar with that, please practice that some more before doing this next part.  Please grab the power tile in the middle: do this by selecting your blue tile that's next to it."
            window["gamePlay"].update(visible = True)
            window["tutorialInfo"].update(myText)
            gameBoard[2][4][0].tileType = "itemOrb"
            displayBoard(window,gameBoard)

            #click the thingy
            while True:
                event = window.read()
                if event[0] != (1,4):
                    myText = "You have to select the piece that's right next to the item orb tile"
                    window["tutorialInfo"].update(myText)
                    window.refresh()
                    continue
                else:
                    
                    while True:
                        myText = "Now that you've selected your piece, we need to click on the item orb to have your piece grab it."
                        window["tutorialInfo"].update(myText)
                        event = window.read()
                        if event[0] != (2,4):
                            myText = "That's not right.  You have to move your piece onto the item orb to grab it.  Let's try again."
                            window["tutorialInfo"].update(myText)
                            window.refresh()
                            sleep(1)
                            continue
                        else:
                            myText = "Cool, your piece now holds a powerup!  Notice how it looks different compared to the others.  Let's try it out!  Normally you have to take turns, but we'll just cheat - I've disabled red from having any turns."
                            window["tutorialInfo"].update(myText)
                            rowOrig = 1
                            colOrig = 4
                            playerBackup = gameBoard[rowOrig][colOrig][1]
                            gameBoard[rowOrig][colOrig][1] = 0
                            gameBoard[event[0][0]][event[0][1]][1] = playerBackup
                            gameBoard[rowOrig][colOrig][0].occupied = False
                            gameBoard[rowOrig][colOrig][0].tileType = "default"
                            gameBoard[rowOrig+1][colOrig][0].occupied = True
                            gameBoard[rowOrig+1][colOrig][1].storedItems.append("Energy Forcefield")
                            gameBoard[rowOrig+1][colOrig][1].determineAvatar()
                            
                            displayBoard(window,gameBoard)
                            window.refresh()
                            
                            sleep(1)
                            while True:
                                myText = "Alright, click on the powered up piece"
                                
                                event = window.read()
                                window["tutorialInfo"].update(myText)
                                if event[0] != (2,4):
                                    sg.popup("Click on the piece that you just moved",keep_on_top=True)
                                    continue
                                else:
                                    window["use item"].update(visible = True)
                                    myText = "There are two ways to use an item.  You can either click on the selected piece again, or you can click on the Use Item icon near the top.  Do either one."
                                
                                    event = window.read()
                                    window["tutorialInfo"].update(myText)

                                    if event[0]  == "use item" or event[0] == (2,4):
                                        myText = "There are two ways to use an item.  You can either click on the selected piece again, or you can click on the Use Item icon near the top.  Do either one."
                                        explodeLayout = [ [sg.Button("Cheater's Instawin Item of Instant Winning")] ]
                                        x = sg.Window("Items",explodeLayout)
                                        
                                        event = x.read()
                                        window["tutorialInfo"].update(myText)

                                        if event[0] == "Cheater's Instawin Item of Instant Winning":
                                            x.close()
                                            myText = "Congrats, you cheater.  This weapon (which only exists in this tutorial mode) will instantly destroy any enemy pieces on the field.  You now know pretty much everything you need to know to win.  Go out there and start playing with a friend."
                                            
                                            
                                            window["tutorialInfo"].update(myText)
                                            window.refresh()
                                            sleep(1)
                                            
                                            for i in range(2):
                                                for j in range(columns):
                                                    window[rows-i-1,j].update(image_filename="exploding.png")
                                            window.refresh()
                                            sleep(1)
                                            
                                            for i in range(2):
                                                for j in range(columns):
                                                    window[rows-i-1,j].update(image_filename="destroyed.png")
                                            window.refresh()
                                            sleep(1)

                                            
                                            for i in range(2):
                                                for j in range(columns):
                                                    window[rows-i-1,j].update(image_filename="exploding.png")
                                            window.refresh()
                                            sleep(1)
                                            
                                            for i in range(2):
                                                for j in range(columns):
                                                    window[rows-i-1,j].update(image_filename="blank.png")
                                            window.refresh()
                                            sleep(5)
                                        sg.popup("Restarting the tutorial",keep_on_top=True)
                                        tutorial()

                                    else:
                                        sg.popup("Nope, try again",keep_on_top=True)
                                        continue
                                
                       
        else:
            myText = "Invalid choice.  Try clicking something on the menu."
            window["tutorialInfo"].update(myText)
            
 
def main():
    introLayout = [[sg.Text("MegaCheckers",font = "Cambria 100")]]
    frame_1 = [
        [sg.Button("Begin game",key="begin")],
        [sg.Button("How to play",key="tutorial")]
        ]
    introLayout+= [[sg.Frame("Choose an option",frame_1,key="options")]]
    introWindow = sg.Window("MegaCheckers",introLayout)
    event = introWindow.read()
    if event[0] == "tutorial":
        introWindow.close()
        tutorial()
    if event[0] == "begin":
        introWindow.close()
        begin()



#delete me after debug
begin()
 #delete me


 
main()
