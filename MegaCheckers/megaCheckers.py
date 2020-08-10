import PySimpleGUI as sg
import copy
import math
import random
import string
from time import sleep
from PIL import Image
from io import BytesIO
import base64
from playsound import playsound
import sys
import shutil
import os
from useItemsMegaCheckers import *
from betweenTurnFunctionsMegaCheckers import *



def initializeField(columns, rows, window, gameBoard):
    

    for i in range(2):
        for j in range(columns):
            gameBoard[i][j][0] = Tile(occupied=True)
            piece = Piece(playerTurn=2)
            gameBoard[i][j][1] = piece
            gameBoard[i][j][1].location = (i, j)
            gameBoard[i][j][0].tileType = "player1default"
            gameBoard[i][j][1].avatar = "default"
    for i in range(2):
        for j in range(columns):
            gameBoard[rows - i - 1][j][0] = Tile(occupied=True)
            piece = Piece(playerTurn=1)
            gameBoard[rows - i - 1][j][1] = piece
            gameBoard[rows - i - 1][j][1].location = (rows - i - 1, j)
            gameBoard[rows - i - 1][j][0].tileType = "player2default"
            gameBoard[rows - i - 1][j][1].avatar = "default"

 ###### DELETE ME ##########
##    for i in range(2):
##       for j in range(columns):
##           #middle row generator
##           rows = 6
##           gameBoard[rows - i - 1][j][0] = Tile(occupied=True)
##           piece = Piece(playerTurn=2)
##
##

           #give items to main row
##           gameBoard[i][j][1].storedItems.append("dump items")
##           gameBoard[i][j][1].storedItems.append("teach row")
##           gameBoard[i][j][1].storedItems.append("teach radial")
##           gameBoard[i][j][1].storedItems.append("charity")
##           gameBoard[i][j][1].storedItems.append("mystery box")
##           gameBoard[i][j][1].storedItems.append("study row")
##           gameBoard[i][j][1].storedItems.append("jumpoline")
##           gameBoard[i][j][1].storedItems.append("secretAgent")
##           gameBoard[i][j][1].storedItems.append("shuffle item orbs")
##           gameBoard[i][j][1].storedItems.append("laser row")
##           gameBoard[i][j][1].storedItems.append("mutual treason row")
##           gameBoard[i][j][1].storedItems.append("mutual treason radial")
##           gameBoard[i][j][1].storedItems.append("mutual treason column")
##           gameBoard[i][j][1].storedItems.append("shuffle column")
##           gameBoard[i][j][1].storedItems.append("reproduce")
##           gameBoard[i][j][1].storedItems.append("snake tunneling")
##           gameBoard[i][j][1].storedItems.append("haphazard airstrike")
##           gameBoard[i][j][1].storedItems.append("warp")
##           gameBoard[i][j][1].storedItems.append("purity tile")
##           
##           gameBoard[i][j][1].activeBuffs.append("move again")
##           gameBoard[i][j][1].storedItems.append("trip mine column")
##           gameBoard[i][j][1].storedItems.append("shuffle all")
##           gameBoard[9][0][1].storedItems.append("purity tile")
##           gameBoard[i][j][1].storedItems.append("laser row")
##           gameBoard[i][j][1].storedItems.append("shuffle all")
##           gameBoard[i][j][1].storedItems.append("Energy Forcefield")
##           gameBoard[i][j][1].activeBuffs.append("round earth theory")
##           
##
##           #the middle row
##           gameBoard[rows - i - 1][j][1] = piece
##           gameBoard[rows - i - 1][j][1].location = (rows - i - 1, j)
##           gameBoard[rows - i - 1][j][0].tileType = "player2default"
##           gameBoard[rows - i - 1][j][1].avatar = "default"
##           gameBoard[rows - i - 1][j][1].storedItems.append("haphazard airstrike")
##           gameBoard[rows - i - 1][j][1].storedItems.append("haymaker")
##
##
##
##           #give items to middle row
##           gameBoard[rows - i - 1][j][1].storedItems.append("shuffle radial")
##           gameBoard[rows - i - 1][j][1].storedItems.append("worm hole")
##           gameBoard[rows - i - 1][j][1].storedItems.append("orb eater")
##           gameBoard[rows - i - 1][j][1].storedItems.append("shuffle item orbs")
##           gameBoard[rows - i - 1][j][1].storedItems.append("laser row")
##           gameBoard[rows - i - 1][j][1].storedItems.append("warp")
##           gameBoard[rows - i - 1][j][1].storedItems.append("laser column")
##           gameBoard[rows - i - 1][j][1].storedItems.append("place mine")
##           gameBoard[rows - i - 1][j][1].storedItems.append("haymaker")
##           gameBoard[rows - i - 1][j][1].storedItems.append("haphazard airstrike")
##           gameBoard[rows - i - 1][j][1].storedItems.append("laser row")
##           gameBoard[rows - i - 1][j][1].activeBuffs.append("move diagonal")
##           gameBoard[rows - i - 1][j][1].storedItems.append("bowling ball")
           #print(sg.list_of_look_and_feel_values())
           #gameBoard[2][0][0].tileHeight = 2
           #gameBoard[2][1][0].tileHeight = 1
           #gameBoard[2][2][0].tileHeight = -1
           #gameBoard[2][3][0].tileHeight = -2
           
####### END DELETE ME###########


    






# the actual loop that is used to progress turns
def gamePlay(playerTurn, window, gameBoard):

    
    countPieces(gameBoard, window, PublicStats)
    createOrbs(window, gameBoard)
    #displayBoard(window, gameBoard)

    movePiece(playerTurn, window, gameBoard)
    PublicStats.turnCount += 1
    repairFloor(window, gameBoard)




            
    
# generate item orbs
def createOrbs(window, gameBoard):
    dangerTurn = 40
    #dangerTurn = 1
    emptySpots = 0
    if PublicStats.turnCount == dangerTurn:
        sg.popup(
            "Warning: TRAP ORBS disguised as ITEM ORBS may spawn from now on!  They will explode if either player steps on them.",font = "Cambria 30",
            keep_on_top=True, image = "images/trapOrb.png"
        )
    for i in gameBoard:
        for j in i:
            if j[0].tileType == "default" and j[0].occupied != True and j[0].orbEater == False and j[0].wormHole1 == False and j[0].wormHole2 == False:
                emptySpots += 1
    publicStats = PublicStats()
    orbsToPlace = publicStats.getOrbCount()
    if orbsToPlace > emptySpots:
        orbsToPlace = emptySpots
    attempts = 0
    while orbsToPlace > 0:
        attempts+=1
        if attempts == 300:
            #sg.popup("Space is at a premium for orb generation.  Aborting.",keep_on_top=True)
            return
        
        i = random.randint(0, len(gameBoard) - 1)
        j = random.randint(0, len(gameBoard[0]) - 1)
        if gameBoard[i][j][0].tileType == "default" and gameBoard[i][j][0].occupied != True and gameBoard[i][j][0].orbEater == False and gameBoard[i][j][0].wormHole1 == False and gameBoard[i][j][0].wormHole2 == False:
            orbsToPlace -= 1
            if PublicStats.turnCount > dangerTurn:
                chanceCheck = random.randint(0, 10)
                if chanceCheck > 7:
                    gameBoard[i][j][0].tileType = "trap orb 0"
                    continue
            gameBoard[i][j][0].tileType = "itemOrb"

# check to see if a piece should die from a trip mine
def tripMineCheck(window, gameBoard, x, y):
    g = gameBoard[x][y]

    if "trip mine" in g[1].activeDebuffs:

        if "Energy Forcefield" in g[1].activeBuffs:
            g[1].activeBuffs.remove("Energy Forcefield")
            pm(window, "Trip mine went off!")
            playsound("sounds/grenade.mp3", block = False)
            sleep(1)
            pm(window, "...But your forcefield saved you.")
            while "trip mine" in g[1].activeBuffs:
                g[1].activeDebuffs.remove("trip mine")
        else:
            g[0].occupied = False
            g[0].tileType = "exploding"
            displayBoard(window, gameBoard)
            window.refresh()
            playsound("sounds/grenade.mp3", block = False)
            sleep(0.1)
            g[0].tileType = "default"
            window.refresh()
            sg.popup("Trip mine went off!", keep_on_top=True)
            g[1] = 0
            return "death"



def jumpoline(window, gameBoard, location, playerTurn):
    validLocations = emptySpots(gameBoard, trueEmpty = True)
    if len(validLocations) == 0:
        sg.popup("Nowhere valid for you to jumpoline to. :(",keep_on_top=True)
        return
    choice = random.choice(validLocations)
    x=choice[0]
    y=choice[1]
    return x,y






        
def orbEater(gameBoard):
    # all existing mice appended to this list
    listOfMice = []
    # where the mouse may visit next turn
    legalLocations = []
    # for future use; to get feral mouse
    orbsEaten = 0

    #for every tile in the game, see if there is a mouse there, and if so
    #store it into listOfMice
    for iIndex,i in enumerate(gameBoard):
        for jIndex, j in enumerate(i):
            if j[0].orbEater == True:
                listOfMice.append( (iIndex,jIndex) )
    random.shuffle(listOfMice)
    # for each mouse
    for i in listOfMice:
        ateOrb = False
        legalLocations.clear()
        legalLocations = getCross(i,gameBoard) 
        
        random.shuffle(legalLocations)
        #if the mouse started the turn on a tile, let him eat the item orb
        if gameBoard[i[0]][i[1]][0].tileType in ( "itemOrb", "trap Orb 1", "trap Orb 2", "trap Orb 0"):
            #sg.popup("Orbeater was blessed with an orb!")
            gameBoard[i[0]][i[1]][0].tileType = "default"
            #make orbeater fat
            continue
        
        #for each shuffled location that the mouse can move to
        for j in legalLocations:
            #i refers to mice location, j refers to a adjacent location
            #eat an orb
            if gameBoard[j[0]][j[1]][0].tileType in ( "itemOrb", "trap Orb 1", "trap Orb 2", "trap Orb 0"):
                gameBoard[i[0]][i[1]][0].orbEater = False
                gameBoard[j[0]][j[1]][0].tileType = "default"
                gameBoard[j[0]][j[1]][0].orbEater = True
                #change the picture to a fat mouse if he eats an orb; explode the mouse if it's a trap orb.  If he eats too many orbs, maybe make him crazy?
                
                orbsEaten+=1
                ateOrb = True
                #finish working on the current mouse
                break
            
        #if there wasn't a nearby orb, go somewhere else, if possible
##        if ateOrb == False:
##            random.shuffle(legalLocations)
##            for j in legalLocations:
##                if gameBoard[j[0]][j[1]][0].tileType == "default" and gameBoard[j[0]][j[1]][0].occupied == False:
##                    gameBoard[i[0]][i[1]][0].orbEater = False
##                    gameBoard[j[0]][j[1]][0].tileType = "default"
##                    gameBoard[j[0]][j[1]][0].orbEater = True
##                    break
##                else:
##                    continue
        # if didn't eat orb yet, sniff for nearby food
        if ateOrb == False:
            secondaryLocation = []
            sniffedOrb = False
            for location in legalLocations:
                secondaryLocation.clear()
                secondaryLocation = getCross(location, gameBoard)
                random.shuffle(secondaryLocation)
                for secondaryCoordinates in secondaryLocation:
                    #if the random secondary location has food
                    if gameBoard[secondaryCoordinates[0]][secondaryCoordinates[1]][0].tileType in ( "itemOrb", "trap Orb 1", "trap Orb 2", "trap Orb 0") and gameBoard[location[0]][location[1]][0].orbEater!= True and gameBoard[location[0]][location[1]][0].tileType == "default":
                        gameBoard[i[0]][i[1]][0].orbEater = False
                        #gameBoard[location[0]][location[1]][0].tileType = "default"
                        gameBoard[location[0]][location[1]][0].orbEater = True
                        #sg.popup(f"Sniffing food at {secondaryCoordinates[0]},{secondaryCoordinates[1]}", keep_on_top = True)
                        sniffedOrb = True
                        break

                #if the mouse successfully sniffed food, and moved, exit so he doesn't duplicate
                if sniffedOrb == True:
                    break
                    
                    
        if ateOrb == False and sniffedOrb == False:
            legalLocations = getCross(i,gameBoard)
            random.shuffle(legalLocations)
            for locations in legalLocations:
                if gameBoard[locations[0]][locations[1]][0].tileType == "default" and gameBoard[locations[0]][locations[1]][0].occupied == False and gameBoard[locations[0]][locations[1]][0].orbEater!=True:
                    gameBoard[i[0]][i[1]][0].orbEater = False
                    gameBoard[locations[0]][locations[1]][0].tileType = "default"
                    gameBoard[locations[0]][locations[1]][0].orbEater = True
                    
                    break
                

                
    return orbsEaten

def bowlingBallFunction(window,gameBoard,location,direction):
    sLocRow = location[0]
    sLocCol = location[1]
    rows = len(gameBoard)
    columns = len(gameBoard[0])
    curRow = sLocRow
    curCol = sLocCol

    gameBoard[sLocRow][sLocCol][1].activeDebuffs.clear()
    gameBoard[sLocRow][sLocCol][1].activeBuffs.clear()
    gameBoard[sLocRow][sLocCol][1].activeBuffs.append("bowling ball")
    
    if direction == "Down":
        for eachRow in gameBoard:

            
            
                #if the next spot is legal
                if curRow+1 < rows:

                    
                    # if there are no pieces on the next row
                    if gameBoard[curRow+1][curCol][0].occupied == False:

                        
                        #if the floor exists in the next row
                        if gameBoard[curRow+1][curCol][0].tileType not in (
                            "damaged",
                            "destroyed",
                            "damaged1",
                            "damaged2",
                            "damaged3",
                            "damaged4",
                            "damaged5",
                            "damaged6",
                            "damaged7",
                            "damaged8"):

                            
                            #if the floor is a mine on the next row
                            if gameBoard[curRow+1][curCol][0].tileType in ("mine","trap orb 1","trap orb 0","trap orb 2"):
                                #simplify the gameBoard
                                j = gameBoard[curRow][curCol]
                                #copy the existing piece
                                tempCopy = copy.deepcopy(j)
                                

                                #delete the spot where you were
                                j[0].occupied = False
                                j[1] = 0
                                #careful with this setting; may need to convert to the commented line if glitchy
                                #j[0].tileType = tempCopy[0].tileType
                                j[0].tileType = "default"

                                
                                curRow += 1

                                #j is now pointing to the destination
                                j = gameBoard[curRow][curCol]
                                #explode the mine
                                j[0].tileType = "exploding"
                                displayBoard(window, gameBoard)
                                window.refresh()
                                playsound("sounds/grenade.mp3", block = False)

                                #occupy it with the bowling ball
                                j[0].tileType = "default"
                                j[0].occupied = True
                                j[1] = copy.deepcopy(tempCopy[1])

                                
                                #sleep(1)
                                displayBoard(window, gameBoard)
                                window.refresh()


                            #if the next spot is an item orb or empty    
                            elif gameBoard[curRow+1][curCol][0].tileType in ("default","itemOrb",):
                                
                                
                                #simplify the gameBoard
                                j = gameBoard[curRow][curCol]
                                #copy the existing piece
                                tempCopy = copy.deepcopy(j)
                                
                                

                                #delete the spot where you were
                                j[0].occupied = False
                                j[1] = 0
                                #careful with this setting; may need to convert to the commented line if glitchy
                                #j[0].tileType = tempCopy[0].tileType
                                j[0].tileType = "default"

                                
                                curRow += 1

                                #j is now pointing to the destination
                                j = gameBoard[curRow][curCol]

                                #occupy it with the bowling ball
                                j[0].tileType = "default"
                                j[0].occupied = True
                                j[1] = copy.deepcopy(tempCopy[1])
                                
                                #sleep(1)
                                displayBoard(window, gameBoard)
                                window.refresh()
                            else:
                                curRow +=1
                                continue
                                
                        #else if floor doesn't exist
                        else:
                            j = gameBoard[curRow][curCol]
                            j[0].occupied = False
                            j[0].tileType = "default"
                            j[1] = 0
                            playsound("sounds/fall.wav", block = False)
                            sg.popup("Oh no!  Your bowling ball fell into the void!",keep_on_top = True)
                            #curRow +=1
                            return

                            
                    #else if there is a piece in the next spot
                    else:

                        
                        # simplify the gameBoard
                        # j = starting spot
                        j = gameBoard[curRow][curCol]
                        # k = forecasted spot
                        k = gameBoard[curRow+1][curCol]

                        #if they both belong to you
                        if j[1].ownedBy == k[1].ownedBy:
                            j[1].activeDebuffs.append("stunned")
                            k[1].activeDebuffs.append("stunned")
                            displayBoard(window, gameBoard)
                            window.refresh()
                            sleep(1)
                            return

                        #if the piece is your enemy's
                        elif j[1].ownedBy != k[1].ownedBy:
                            
                            
                            #copy the existing piece
                            tempCopy = copy.deepcopy(j)
                            

                            #delete the spot where you were
                            j[0].occupied = False
                            j[1] = 0
                            #careful with this setting; may need to convert to the commented line if glitchy
                            #j[0].tileType = tempCopy[0].tileType
                            j[0].tileType = "default"

                            
                            curRow += 1

                            #j is now pointing to the destination
                            j = gameBoard[curRow][curCol]
                            #explode the mine
                            j[0].tileType = "exploding"
                            displayBoard(window, gameBoard)
                            window.refresh()
                            playsound("sounds/grenade.mp3", block = False)

                            #occupy it with the bowling ball
                            j[0].tileType = "default"
                            j[0].occupied = True
                            j[1] = copy.deepcopy(tempCopy[1])

                            
                            #sleep(1)
                            displayBoard(window, gameBoard)
                            window.refresh()
                            curRow +=1
                            return
                        
                #else if out of bounds
                else:
                    

                    sg.popup("You slammed into the outer wall.",keep_on_top = True)
                    
                    return
                    
    if direction == "Up":
        for eachRow in gameBoard:

            
            
                #if the next spot is legal
                if curRow-1 >-1:

                    
                    # if there are no pieces on the next row
                    if gameBoard[curRow-1][curCol][0].occupied == False:

                        
                        #if the floor exists in the next row
                        if gameBoard[curRow-1][curCol][0].tileType not in (
                            "damaged",
                            "destroyed",
                            "damaged1",
                            "damaged2",
                            "damaged3",
                            "damaged4",
                            "damaged5",
                            "damaged6",
                            "damaged7",
                            "damaged8"):

                            
                            #if the floor is a mine on the next row
                            if gameBoard[curRow-1][curCol][0].tileType in ("mine","trap orb 1", "trap orb 0","trap orb 2"):
                                #simplify the gameBoard
                                j = gameBoard[curRow][curCol]
                                #copy the existing piece
                                tempCopy = copy.deepcopy(j)
                               

                                #delete the spot where you were
                                j[0].occupied = False
                                j[1] = 0
                                #careful with this setting; may need to convert to the commented line if glitchy
                                #j[0].tileType = tempCopy[0].tileType
                                j[0].tileType = "default"

                                
                                curRow -= 1

                                #j is now pointing to the destination
                                j = gameBoard[curRow][curCol]
                                #explode the mine
                                j[0].tileType = "exploding"
                                displayBoard(window, gameBoard)
                                window.refresh()
                                playsound("sounds/grenade.mp3", block = False)

                                #occupy it with the bowling ball
                                j[0].tileType = "default"
                                j[0].occupied = True
                                j[1] = copy.deepcopy(tempCopy[1])

                                
                                #sleep(1)
                                displayBoard(window, gameBoard)
                                window.refresh()


                            #if the next spot is an item orb or empty    
                            elif gameBoard[curRow-1][curCol][0].tileType in ("default","itemOrb"):
                                
                                
                                #simplify the gameBoard
                                j = gameBoard[curRow][curCol]
                                #copy the existing piece
                                tempCopy = copy.deepcopy(j)
                                

                                #delete the spot where you were
                                j[0].occupied = False
                                j[1] = 0
                                #careful with this setting; may need to convert to the commented line if glitchy
                                #j[0].tileType = tempCopy[0].tileType
                                j[0].tileType = "default"

                                
                                curRow -= 1

                                #j is now pointing to the destination
                                j = gameBoard[curRow][curCol]

                                #occupy it with the bowling ball
                                j[0].tileType = "default"
                                j[0].occupied = True
                                j[1] = copy.deepcopy(tempCopy[1])
                                
                                #sleep(1)
                                displayBoard(window, gameBoard)
                                window.refresh()
                            else:
                                curRow -=1
                                continue
                                
                        #else if floor doesn't exist
                        else:
                            j = gameBoard[curRow][curCol]
                            j[0].occupied = False
                            j[0].tileType = "default"
                            j[1] = 0
                            playsound("sounds/fall.wav", block = False)
                            sg.popup("Oh no!  Your bowling ball fell into the void!",keep_on_top = True)
                            #curRow -=1
                            return
                            
                    #else if there is a piece in the next spot
                    else:

                        
                        # simplify the gameBoard
                        # j = starting spot
                        j = gameBoard[curRow][curCol]
                        # k = forecasted spot
                        k = gameBoard[curRow-1][curCol]

                        #if they both belong to you
                        if j[1].ownedBy == k[1].ownedBy:
                            j[1].activeDebuffs.append("stunned")
                            k[1].activeDebuffs.append("stunned")
                            displayBoard(window, gameBoard)
                            window.refresh()
                            sleep(1)
                            return

                        #if the piece is your enemy's
                        elif j[1].ownedBy != k[1].ownedBy:
                            
                            
                            #copy the existing piece
                            tempCopy = copy.deepcopy(j)
                           

                            #delete the spot where you were
                            j[0].occupied = False
                            j[1] = 0
                            #careful with this setting; may need to convert to the commented line if glitchy
                            #j[0].tileType = tempCopy[0].tileType
                            j[0].tileType = "default"

                            
                            curRow -= 1

                            #j is now pointing to the destination
                            j = gameBoard[curRow][curCol]
                            #explode the mine
                            j[0].tileType = "exploding"
                            displayBoard(window, gameBoard)
                            window.refresh()
                            playsound("sounds/grenade.mp3", block = False)

                            #occupy it with the bowling ball
                            j[0].tileType = "default"
                            j[0].occupied = True
                            j[1] = copy.deepcopy(tempCopy[1])

                       
                            #sleep(1)
                            displayBoard(window, gameBoard)
                            window.refresh()
                            curRow -=1
                            return
                #else if out of bounds
                else:
                    sg.popup("You slammed into the outer wall.",keep_on_top = True)
                    
                    return

    if direction == "Left":
        while True:
                #if the next spot is legal
                if curCol-1 > -1:

                    
                    # if there are no pieces on the next row
                    if gameBoard[curRow][curCol-1][0].occupied == False:

                        
                        #if the floor exists in the next row
                        if gameBoard[curRow][curCol-1][0].tileType not in (
                            "damaged",
                            "destroyed",
                            "damaged1",
                            "damaged2",
                            "damaged3",
                            "damaged4",
                            "damaged5",
                            "damaged6",
                            "damaged7",
                            "damaged8"):

                            
                            #if the floor is a mine on the next row
                            if gameBoard[curRow][curCol-1][0].tileType in ("mine","trap orb 1", "trap orb 0","trap orb 2"):
                                #simplify the gameBoard
                                j = gameBoard[curRow][curCol]
                                #copy the existing piece
                                tempCopy = copy.deepcopy(j)
                            

                                #delete the spot where you were
                                j[0].occupied = False
                                j[1] = 0
                                #careful with this setting; may need to convert to the commented line if glitchy
                                #j[0].tileType = tempCopy[0].tileType
                                j[0].tileType = "default"

                                
                                curCol -= 1

                                #j is now pointing to the destination
                                j = gameBoard[curRow][curCol]
                                #explode the mine
                                j[0].tileType = "exploding"
                                displayBoard(window, gameBoard)
                                window.refresh()
                                playsound("sounds/grenade.mp3", block = False)

                                #occupy it with the bowling ball
                                j[0].tileType = "default"
                                j[0].occupied = True
                                j[1] = copy.deepcopy(tempCopy[1])

                           
                                #sleep(1)
                                displayBoard(window, gameBoard)
                                window.refresh()


                            #if the next spot is an item orb or empty    
                            elif gameBoard[curRow][curCol-1][0].tileType in ("default","itemOrb",):
                                
                                
                                #simplify the gameBoard
                                j = gameBoard[curRow][curCol]
                                #copy the existing piece
                                tempCopy = copy.deepcopy(j)
                            
                                #delete the spot where you were
                                j[0].occupied = False
                                j[1] = 0
                                #careful with this setting; may need to convert to the commented line if glitchy
                                #j[0].tileType = tempCopy[0].tileType
                                j[0].tileType = "default"

                                
                                curCol -= 1

                                #j is now pointing to the destination
                                j = gameBoard[curRow][curCol]

                                #occupy it with the bowling ball
                                j[0].tileType = "default"
                                j[0].occupied = True
                                j[1] = copy.deepcopy(tempCopy[1])
                                
                                #sleep(1)
                                displayBoard(window, gameBoard)
                                window.refresh()
                            else:
                                sg.popup("Shouldn't see this",keep_on_top = True)
                                curCol -=1
                                continue
                                
                        #else if floor doesn't exist
                        else:
                            j = gameBoard[curRow][curCol]
                            j[0].occupied = False
                            j[0].tileType = "default"
                            j[1] = 0
                            playsound("sounds/fall.wav", block = False)
                            sg.popup("Oh no!  Your bowling ball fell into the void!",keep_on_top = True)
                            #curCol -=1
                            return
                            
                    #else if there is a piece in the next spot
                    else:

                        
                        # simplify the gameBoard
                        # j = starting spot
                        j = gameBoard[curRow][curCol]
                        # k = forecasted spot
                        k = gameBoard[curRow][curCol-1]

                        #if they both belong to you
                        if j[1].ownedBy == k[1].ownedBy:
                            j[1].activeDebuffs.append("stunned")
                            k[1].activeDebuffs.append("stunned")
                            displayBoard(window, gameBoard)
                            window.refresh()
                            sleep(1)
                            return

                        #if the piece is your enemy's
                        elif j[1].ownedBy != k[1].ownedBy:
                            
                            
                            #copy the existing piece
                            tempCopy = copy.deepcopy(j)
                   

                            #delete the spot where you were
                            j[0].occupied = False
                            j[1] = 0
                            #careful with this setting; may need to convert to the commented line if glitchy
                            #j[0].tileType = tempCopy[0].tileType
                            j[0].tileType = "default"

                            
                            curCol -= 1

                            #j is now pointing to the destination
                            j = gameBoard[curRow][curCol]
                            #explode the mine
                            j[0].tileType = "exploding"
                            displayBoard(window, gameBoard)
                            window.refresh()
                            playsound("sounds/grenade.mp3", block = False)

                            #occupy it with the bowling ball
                            j[0].tileType = "default"
                            j[0].occupied = True
                            j[1] = copy.deepcopy(tempCopy[1])

                       
                            #sleep(1)
                            displayBoard(window, gameBoard)
                            window.refresh()
                            curCol -=1
                            return
                        
                #else if out of bounds
                else:
                    
                    sg.popup("Slammed into wall!",keep_on_top=True)
                    return
    if direction == "Right":
        while True:
                #if the next spot is legal
                if curCol+1 < columns:

                    
                    # if there are no pieces on the next row
                    if gameBoard[curRow][curCol+1][0].occupied == False:

                        
                        #if the floor exists in the next row
                        if gameBoard[curRow][curCol+1][0].tileType not in (
                            "damaged",
                            "destroyed",
                            "damaged1",
                            "damaged2",
                            "damaged3",
                            "damaged4",
                            "damaged5",
                            "damaged6",
                            "damaged7",
                            "damaged8"):

                            
                            #if the floor is a mine on the next row
                            if gameBoard[curRow][curCol+1][0].tileType in ("mine","trap orb 1", "trap orb 0","trap orb 2"):
                                #simplify the gameBoard
                                j = gameBoard[curRow][curCol]
                                #copy the existing piece
                                tempCopy = copy.deepcopy(j)
                                

                                #delete the spot where you were
                                j[0].occupied = False
                                j[1] = 0
                                #careful with this setting; may need to convert to the commented line if glitchy
                                #j[0].tileType = tempCopy[0].tileType
                                j[0].tileType = "default"

                                
                                curCol += 1

                                #j is now pointing to the destination
                                j = gameBoard[curRow][curCol]
                                #explode the mine
                                j[0].tileType = "exploding"
                                displayBoard(window, gameBoard)
                                window.refresh()
                                playsound("sounds/grenade.mp3", block = False)

                                #occupy it with the bowling ball
                                j[0].tileType = "default"
                                j[0].occupied = True
                                j[1] = copy.deepcopy(tempCopy[1])

                              
                                #sleep(1)
                                displayBoard(window, gameBoard)
                                window.refresh()


                            #if the next spot is an item orb or empty    
                            elif gameBoard[curRow][curCol+1][0].tileType in ("default","itemOrb"):
                                
                                
                                #simplify the gameBoard
                                j = gameBoard[curRow][curCol]
                                #copy the existing piece
                                tempCopy = copy.deepcopy(j)
                            

                                #delete the spot where you were
                                j[0].occupied = False
                                j[1] = 0
                                #careful with this setting; may need to convert to the commented line if glitchy
                                #j[0].tileType = tempCopy[0].tileType
                                j[0].tileType = "default"

                                
                                curCol += 1

                                #j is now pointing to the destination
                                j = gameBoard[curRow][curCol]

                                #occupy it with the bowling ball
                                j[0].tileType = "default"
                                j[0].occupied = True
                                j[1] = copy.deepcopy(tempCopy[1])
                               
                                displayBoard(window, gameBoard)
                                window.refresh()
                            else:
                                curCol +=1
                                continue
                                
                        #else if floor doesn't exist
                        else:
                            j = gameBoard[curRow][curCol]
                            j[0].occupied = False
                            j[0].tileType = "default"
                            j[1] = 0
                            playsound("sounds/fall.wav", block = False)
                            sg.popup("Oh no!  Your bowling ball fell into the void!",keep_on_top = True)
                            #curCol +=1
                            return

                            
                    #else if there is a piece in the next spot
                    else:

                        
                        # simplify the gameBoard
                        # j = starting spot
                        j = gameBoard[curRow][curCol]
                        # k = forecasted spot
                        k = gameBoard[curRow][curCol+1]

                        #if they both belong to you
                        if j[1].ownedBy == k[1].ownedBy:
                            j[1].activeDebuffs.append("stunned")
                            k[1].activeDebuffs.append("stunned")
                            displayBoard(window, gameBoard)
                            window.refresh()
                            sleep(1)
                            return

                        #if the piece is your enemy's
                        elif j[1].ownedBy != k[1].ownedBy:
                            
                            
                            #copy the existing piece
                            tempCopy = copy.deepcopy(j)
                          

                            #delete the spot where you were
                            j[0].occupied = False
                            j[1] = 0
                            #careful with this setting; may need to convert to the commented line if glitchy
                            #j[0].tileType = tempCopy[0].tileType
                            j[0].tileType = "default"

                            
                            curCol += 1

                            #j is now pointing to the destination
                            j = gameBoard[curRow][curCol]
                            #explode the mine
                            j[0].tileType = "exploding"
                            displayBoard(window, gameBoard)
                            window.refresh()
                            playsound("sounds/grenade.mp3", block = False)

                            #occupy it with the bowling ball
                            j[0].tileType = "default"
                            j[0].occupied = True
                            j[1] = copy.deepcopy(tempCopy[1])

                          
                            #sleep(1)
                            displayBoard(window, gameBoard)
                            window.refresh()
                            curCol +=1
                            return
                        
                #else if out of bounds
                else:

                    sg.popup("You slammed into the outer wall.",keep_on_top = True)
                    return



    
def secretAgentCheck(window, gameBoard, startLocation, endLocation, playerTurn):
    
    #if there's no secretAgent
    if gameBoard[endLocation[0]][endLocation[1]][0].secretAgent == False:
        return
    
    #if the secretAgent is yours
    if gameBoard[endLocation[0]][endLocation[1]][0].secretAgent == playerTurn:
        #if you are not burdened (debuff that stops you from picking up items) and you're not a bowling ball and your secretAgent has items
        if "burdened" not in gameBoard[endLocation[0]][endLocation[1]][1].activeDebuffs and len(gameBoard[endLocation[0]][endLocation[1]][0].secretAgentList)>0 and "bowling ball" not in gameBoard[endLocation[0]][endLocation[1]][1].activeBuffs:
            #he gives you the items
            count = 0
            for i in gameBoard[endLocation[0]][endLocation[1]][0].secretAgentList:
                gameBoard[endLocation[0]][endLocation[1]][1].storedItems.append(i)
                count+=1
            sg.popup(f"The allied secret agent gave you all the items he's stolen on your behalf. ({count} total)",keep_on_top=True)
            pm(window, f"The allied secret agent gave you all the items he's stolen on your behalf. ({count} total)")
            #and then erases his collection
            gameBoard[endLocation[0]][endLocation[1]][0].secretAgentList.clear()
        #otherwise, if he doesn't have anything, show a little message
        elif len(gameBoard[endLocation[0]][endLocation[1]][0].secretAgentList) == 0:
            sg.popup("This secret agent is on your side, but isn't interested in small talk.  He nods, but otherwise ignores you.  You should visit him after he steals something from your enemy.",keep_on_top=True)        

    #if the secretAgent is your enemy's
    elif gameBoard[endLocation[0]][endLocation[1]][0].secretAgent != playerTurn:
            #if you're there
            if gameBoard[endLocation[0]][endLocation[1]][0].occupied == True:
                if len(gameBoard[endLocation[0]][endLocation[1]][1].storedItems) > 0:
                    #iterate through the player's list
                    for i in gameBoard[endLocation[0]][endLocation[1]][1].storedItems:
                        #add them to the spy's inventory
                        gameBoard[endLocation[0]][endLocation[1]][0].secretAgentList.append(i)
                    #wipe out the victim's items
                    gameBoard[endLocation[0]][endLocation[1]][1].storedItems.clear()
                    sg.popup("The secret agent stole all your held items",keep_on_top=True)
            else:
                sg.popup("The secret agent sees you don't have any items, so he gives you a dirty look, but doesn't do anything else.",keep_on_top=True)
    

def repairFloor(window, gameBoard):
    for i in gameBoard:
        for j in i:
            if j[0].tileType == "destroyed":
                j[0].tileType = "damaged8"
            elif j[0].tileType == "damaged8":
                j[0].tileType = "damaged7"
            elif j[0].tileType == "damaged7":
                j[0].tileType = "damaged6"
            elif j[0].tileType == "damaged6":
                j[0].tileType = "damaged5"
            elif j[0].tileType == "damaged5":
                j[0].tileType = "damaged4"
            elif j[0].tileType == "damaged4":
                j[0].tileType = "damaged3"
            elif j[0].tileType == "damaged3":
                j[0].tileType = "damaged2"
            elif j[0].tileType == "damaged2":
                j[0].tileType = "damaged"
            elif j[0].tileType == "damaged":
                j[0].tileType = "default"

def findCurrentTurnPiece(window, gameBoard, reset = False):
    rowIndex = 0
    columnIndex = 0
    found = False

    #sg.popup(f"{gameBoard[2][9][1].currentTurnPiece}", keep_on_top = True)
    for i in gameBoard:
        columnIndex = 0
        for j in i:
            
            if j[0].occupied == True:
                
                if j[1].currentTurnPiece == True:
                    found = True
                    #sg.popup(f"DEBUG: FOUND AT {rowIndex},{columnIndex}", keep_on_top = True)
                    return (rowIndex,columnIndex)
            columnIndex +=1
            
        rowIndex +=1
    
    if found == False:
        #sg.popup("NOT FOUND.", keep_on_top = True)
        return False


def AIbomb(window,gameBoard):
    explodeChance = random.randint(0,100)
    bombLocations = []
    emptyTiles = []
    for rIndex,rows in enumerate(gameBoard):
        for cIndex,columns in enumerate(rows):
            if columns[0].tileType == "AI bomb":
                bombLocations.append( (rIndex,cIndex) )
                #sg.popup("Debug: found a bomb", keep_on_top = True)
    for location in bombLocations:
        
        adjacentTiles = getCross(location, gameBoard)
        for i in adjacentTiles:
            if gameBoard[i[0]][i[1]][0].occupied == True:
                #sg.popup("Debug: found a rrigger point", keep_on_top = True)
                if explodeChance > 80:
                    explodeMe = getRadial(location, gameBoard)
                    sg.popup("The AI bomb has been set off!", keep_on_top = True)
                    for j in explodeMe:
                        damageCheck(window, gameBoard, j)
##                        g = gameBoard[j[0]][j[1]]
##                        if g[0].occupied == True:
##                            if g[1].forceFieldTurn == PublicStats.turnCount:
##                                continue
##                            elif "Energy Forcefield" in g[1].activeBuffs:
##                                g[1].activeBuffs.remove("Energy Forcefield")
##                                g[1].forceFieldTurn = PublicStats.turnCount
##                                continue
##                        g[0].tileType = "exploding"
##                        displayBoard(window,gameBoard)
##                        window.refresh()
##                        g[0].occupied = False
##                        g[1] = 0
##                        g[0].tileType = "destroyed"
##                        displayBoard(window,gameBoard)
##                        window.refresh()
                    break
            emptyTiles.clear()
            emptyTiles = getCross(location, gameBoard, trueEmpty = True)
            if len(emptyTiles) == 0:
                continue
            goToLocation = random.choice(emptyTiles)
            x1 = location[0]
            y1 = location[1]
            x2 = goToLocation[0]
            y2 = goToLocation[1]
            gameBoard[x1][y1][0].tileType = "default"
            gameBoard[x2][y2][0].tileType = "AI bomb"
            displayBoard(window, gameBoard)
            window.refresh()
            break
            
def roundEarthTheoryFunction(gameBoard,startLocation,endLocation,columns,rows):
#trying to go from right side to left side
    #try to go straight right to straight left

    #sg.popup("Checking round earth theory!", keep_on_top=True)
   
    if startLocation[0] == endLocation[0] and startLocation[1] == columns-1 and endLocation[1] == 0:
            #sg.popup("Your piece is attempting to roll to the other side!1",keep_on_top=True)
            sg.popup("Your piece is attempting to roll to the other side!", keep_on_top=True)
            return True
    #trying to go down right
    elif startLocation[0] == endLocation[0]-1 and startLocation[1] == columns -1 and endLocation[1] == 0 and "move diagonal" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
        #sg.popup("Your piece is attempting to roll to the other side!2",keep_on_top=True)
        sg.popup("Your piece is attempting to roll to the other side!", keep_on_top=True)
        return True
    #trying to go up right
    elif startLocation[0] == endLocation[0]+1 and startLocation[1] == columns -1 and endLocation[1] == 0 and "move diagonal" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
        #sg.popup("Your piece is attempting to roll to the other side!3",keep_on_top=True)
        sg.popup("Your piece is attempting to roll to the other side!", keep_on_top=True)
        return True
    

#trying to go from left to right side
    #try to go straight left to straight right
    if startLocation[0] == endLocation[0] and startLocation[1] == 0 and endLocation[1] == columns -1:
            #sg.popup("Your piece rolled around to the other side4!",keep_on_top=True)
            sg.popup("Your piece is attempting to roll to the other side!", keep_on_top=True)
            return True
    #trying to go down right
    elif startLocation[0] == endLocation[0]-1 and startLocation[1] == 0  and endLocation[1] == columns -1 and "move diagonal" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
        #sg.popup("Your piece is attempting to roll to the other side!5", keep_on_top=True)
        sg.popup("Your piece is attempting to roll to the other side!", keep_on_top=True)
        return True
    #trying to go up right
    elif startLocation[0] == endLocation[0]+1 and startLocation[1] == 0 and endLocation[1] == columns -1 and "move diagonal" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
        #sg.popup("Your piece is attempting to roll to the other side!6", keep_on_top=True)
        sg.popup("Your piece is attempting to roll to the other side!", keep_on_top=True)
        return True

        
#trying to go from up to down
    #try to go straight up to straight down
    if startLocation[1] == endLocation[1] and startLocation[0] == 0 and endLocation[0] == rows -1:
            #sg.popup("Your piece is attempting to roll to the other side!7", keep_on_top=True)
            sg.popup("Your piece is attempting to roll to the other side!", keep_on_top=True)
            return True
    #trying to go up right
    elif startLocation[0] == 0 and startLocation[1] == (endLocation[1] +1) and endLocation[0] == rows -1 and "move diagonal" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
        #sg.popup("Your piece is attempting to roll to the other side!8", keep_on_top=True)
        sg.popup("Your piece is attempting to roll to the other side!", keep_on_top=True)
        return True
    #trying to go up left
    elif startLocation[1] == endLocation[1]-1 and startLocation[0] == 0 and endLocation[0] == rows -1 and "move diagonal" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
        #sg.popup("Your piece is attempting to roll to the other side!9", keep_on_top=True)
        sg.popup("Your piece is attempting to roll to the other side!", keep_on_top=True)
        return True

#in case of error, below is
    #if startLocation[1] == endLocation[1]:
        #if startLocation[0] == rows-1 and endLocation[0] == 0:
#trying to go from down to up
    #try to go straight down to straight up
    if startLocation[1] == endLocation[1] and startLocation[0] == rows-1 and endLocation[0] == 0:
            #sg.popup("Your piece is attempting to roll to the other side!10", keep_on_top=True)
            sg.popup("Your piece is attempting to roll to the other side!", keep_on_top=True)
            return True
    #trying to go down right
    elif startLocation[0] == rows-1 and startLocation[1] == (endLocation[1] +1) and endLocation[0] == 0 and "move diagonal" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
        #sg.popup("Your piece is attempting to roll to the other side!11", keep_on_top=True)
        sg.popup("Your piece is attempting to roll to the other side!", keep_on_top=True)
        return True
    #trying to go down left
    elif startLocation[1] == endLocation[1]-1 and startLocation[0] == 0 and endLocation[0] == rows-1 and "move diagonal" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
        #sg.popup("Your piece is attempting to roll to the other side!12", keep_on_top=True)
        sg.popup("Your piece is attempting to roll to the other side!", keep_on_top=True)
        return True
    

#diagonals (only works with diagonal enabled
    if "move diagonal" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
        #upleft
        if startLocation[0] == 0 and startLocation[1] == 0 and endLocation[0] == rows-1 and endLocation[1] == columns-1:
            #sg.popup("Your piece is attempting to roll to the other side!13", keep_on_top=True)
            sg.popup("Your piece is attempting to roll to the other side!", keep_on_top=True)
            return True
        #upright
        if startLocation[0] == 0 and startLocation[1] == columns-1 and endLocation[0] == rows-1 and endLocation[1] == 0:
            #sg.popup("Your piece is attempting to roll to the other side!14", keep_on_top=True)
            sg.popup("Your piece is attempting to roll to the other side!", keep_on_top=True)
            return True
        #downleft
        if startLocation[0] == rows-1 and startLocation[1] == 0 and endLocation[0] == 0 and endLocation[1] == columns-1:
            #sg.popup("Your piece is attempting to roll to the other side!15", keep_on_top=True)
            sg.popup("Your piece is attempting to roll to the other side!", keep_on_top=True)
            return True
        #downright
        if startLocation[0] == rows-1 and startLocation[1] == columns-1 and endLocation[0] == 0 and endLocation[1] == 0:
            #sg.popup("Your piece is attempting to roll to the other side!16", keep_on_top=True)
            sg.popup("Your piece is attempting to roll to the other side!", keep_on_top=True)
            return True
        else:
            return False
    else:
        #debug
        #sg.popup("Round earth theory failed.", keep_on_top = True)
        return False



        
def movePiece(playerTurn, window, gameBoard):
    
    # a small list that is used to make sure a player that gets a second turn for a piece can only use that specific piece twice
    repeatRestrictor = [False, (-1, -1)]
    pieceTeleported = False
    startLocation = []
    roundEarthTheory = False
    rows = len(gameBoard)
    columns = len(gameBoard[0])
    pm(window, "--------------------------------")
    pm(window, f"Player {playerTurn}'s turn")


    #set all the pieces to have a false current turn; this is a catch all for in case I forgot to reset it elsewhere in the game
    for i in gameBoard:
        for j in i:
            if j[0].occupied == True:
                j[1].currentTurnPiece = False
                
    index = 0
    listOfItemListCoordinates = []
    for j in range(0,15):
            for i in range(0,3):
                window[f"itemList{i}{j}"].update("")
                window[f"itemList{i}{j}"].update(disabled = True)
                listOfItemListCoordinates+= f"itemList{i}{j}"
                index+=1
    #turn the lasers on and kill what needs to be killed
    laserCheck(window, gameBoard)
            

    #########################################################################
    # MAIN TURN LOOP: major chunk of what happens during your turn is below #
    #########################################################################
    
    while True:

        #####################################################################################################
        #                                                                                                   #
        #  This little section populates the button list of items on the right side of the game board       #
        #                                                                                                   #
        #####################################################################################################
        itemsOwned = []
        for iIndex,i in enumerate(gameBoard):
            for jIndex,j in enumerate(i):
                if j[0].occupied == True:
                    if j[1].ownedBy == playerTurn:
                        #if the piece holds an item
                        if len(j[1].storedItems)  > 0:
                            #for each item that the piece holds
                            for heldItem in j[1].storedItems:
                                #if the itemsOwned list is not empty
                                if len(itemsOwned) > 0:
                                    #run through the buttons' list of items
                                    heldItemCheck = False
                                    for itemsOwnedIterator in itemsOwned:
                                        #if the item the piece is holding is already in the list, break while making note that a break happened
                                        if heldItem in itemsOwnedIterator[1]:
                                            heldItemCheck = True
                                            break
                                    #if a break didn't happen, then that means the item doesn't exist in the button list, so go ahead and add it
                                    if heldItemCheck == False:
                                        clump = ( [iIndex, jIndex], heldItem)
                                        itemsOwned.append(clump)
                                #if it is empty, then append (since this is the first item)
                                else:
                                    clump = ( [iIndex, jIndex], heldItem)
                                    itemsOwned.append(clump)
                                
                                    

        index = 0
        for j in range(0,15):
            for i in range(0,3):
                if index==len(itemsOwned):
                    break
                else:
                    window[f"itemList{i}{j}"].update(itemsOwned[index][1])
                    window[f"itemList{i}{j}"].update(disabled = False)
                    index+=1
                
        
        #turn the lasers on and kill what needs to be killed
        laserCheck(window, gameBoard)

        #update the tooltips
        updateToolTips(window, gameBoard,playerTurn)

        #turn off all highlighting on all pieces (safety net in case any errant highlighting remains)
        highlightValidDistance(gameBoard, window, (0,0),turnOff = True)


        #flag for keeping track of pieces that were teleported
        if pieceTeleported == True:
            a = findCurrentTurnPiece(window, gameBoard)
            if a!=False:
                startLocation = (a[0],a[1])
                gameBoard[startLocation[0]][startLocation[1]][1].currentTurnPiece = True
            else:
                sg.popup("An error has occurred with teleportation.  Using last known location.", keep_on_top = True)
                startLocation = repeatRestrictor[1]
                pieceTeleported = False
                continue

        #update the board (for lasers and highlighting and any leftover changes from last turn)
        displayBoard(window, gameBoard)

        
        #Picked up item is used to show a message if a piece is picked up automatically at the end of the turn
        pickedUpItem = False
        usedItem = False


        #enable buttons
        window["exit"].update(disabled=False)
        window["examineItem"].update(disabled=False)
        window["cheetz"].update(disabled=False)
        window["Read Items"].update(disabled=False)
        window.refresh()

        #update whose turn it is
        window["playerTurn"].update(f"{playerTurn}")
        window["information"].update(text_color="white")

        # message for pick your piece to move
        pm(window, f"Pick a piece to move.")



##########################################
#   IF FIRST TURN                        #
##########################################

        
        # check to see if this is your second [or higher] turn (you don't get to choose a new piece).  False means this isn't your second move (so if False, it's your first turn)
        if repeatRestrictor[0] == False:

###########################
#FIRST PIECE PICKED HERE  #
###########################
            
            # This is your initial selection option for choosing a piece or clicking an option
            event = window.read()
            

            #if you wanna cheat
            if "cheetz" in event:
                items = sg.popup_get_text("",keep_on_top = True)
                itemsList = pickUpItemOrb(getItemsList = True)
                if items not in itemsList:
                    sg.popup("BOGUS CHEETZ ATTEMPT.  GET OUTTA HERE.", keep_on_top = True)
                    continue
                for i in gameBoard:
                    for j in i:
                        if j[0].occupied == True:
                            j[1].storedItems.append(items)
                pm(window,"CHEETZed some items.  What a cheetzer.")
                continue


            #if exit is clicked
            if "exit" in event:
                a = sg.popup_yes_no(
                    "Seriously, you want to exit this awesome game?", keep_on_top=True, font = "Cambria 20"
                )
                pm(window, "You're a fool if you're wanting to quit this game.")
                if a == "Yes":
                    sg.popup("Wow, your loss.", keep_on_top=True, font = "Cambria 20")
                    window.close()
                    raise SystemExit
                else:
                    continue

            #if player wants to examine a tile/piece
            if "examineItem" in event:
                highlightValidDistance(gameBoard, window, (0,0),turnOff = True)
                window["examineItem"].update(disabled=True)
                window["information"].update(
                    f"What do you want to examine?", text_color="red"
                )
                disableEverything(window)
                event = window.read()
                disableEverything(window, turnOn = True)
                window["information"].update(text_color="white")
                # if no pieces exist here:
                if gameBoard[event[0][0]][event[0][1]][0].occupied == False:
                    pm(window, gameBoard[event[0][0]][event[0][1]][0].describeSelf())
                # if there is a piece:
                else:
                    gameBoard[event[0][0]][event[0][1]][1].activeBuffs.sort()
                    gameBoard[event[0][0]][event[0][1]][1].activeDebuffs.sort()
                    gameBoard[event[0][0]][event[0][1]][1].storedItems.sort()
                    
                    if playerTurn == gameBoard[event[0][0]][event[0][1]][1].ownedBy:
                        owner = "you"
                    else:
                        owner = "your opponent"
                    buffslist = ""
                    debuffslist = ""
                    for i in gameBoard[event[0][0]][event[0][1]][1].activeBuffs:
                        buffslist += i + "\n"
                    for i in gameBoard[event[0][0]][event[0][1]][1].activeDebuffs:
                        debuffslist += i + "\n"
                    if buffslist == "":
                        buffslist = "NONE"
                    if debuffslist == "":
                        debuffslist = "NONE"
                    sg.popup(f"The piece here belongs to {owner}.\nIt currently holds {len(gameBoard[event[0][0]][event[0][1]][1].storedItems)} inactive items.\nIt has the following buffs:\n{buffslist}\nIt has the current debuffs:\n{debuffslist}\n\n\nThe tile elevation is {gameBoard[event[0][0]][event[0][1]][0].tileHeight}",keep_on_top = True)
                    pm(
                        window,
                        f"The piece here belongs to {owner}.\nIt currently holds {len(gameBoard[event[0][0]][event[0][1]][1].storedItems)} inactive items.\nIt has the following buffs:\n{buffslist}\nIt has the current debuffs:\n{debuffslist}",
                    )
                window["examineItem"].update(disabled=False)
                continue

            lastOpenPage = 1
            endReadItems = False
            if "Read Items" in event:
                itemsList = pickUpItemOrb(getItemsList = True)
                frame1Layout = []
                frame2Layout = []
                frame3Layout = []
                frame4Layout = []
                frame5Layout = []
                frame6Layout = []
                frame7Layout = []
                frame8Layout = []
                frame9Layout = []
                frame10Layout = []
                frame11Layout = []
                frame0Layout = [  [ sg.Button( i, key = f"key{i}", font = "Cambria 30") for i in string.ascii_uppercase] ]
                frame00Layout = [  [ sg.Button( i, key = f"key{i}", font = "Cambria 30") for i in string.ascii_uppercase] ]

                frame000Layout = [  [ sg.Button( i, key = f"key{i}", font = "Cambria 30") for i in string.ascii_uppercase] ]

                
                for iIndex,i in enumerate(itemsList):
                    if iIndex < 8:
                        frame1Layout+= [[sg.Button(i, size = (30,10),image_size=(300, 100),key = f"{i}",image_filename = f"images\\{i}.png",font="Arial 20",button_color=("pink", "grey"))]]
                    elif iIndex in range (8,16):
                        frame2Layout+= [[sg.Button(i, size = (30,10),image_size=(300, 100),key = f"{i}",image_filename = f"images\\{i}.png",font="Arial 20",button_color=("pink", "grey"))]]
                    elif iIndex in range (16,24):
                        frame3Layout+= [[sg.Button(i, size = (30,10),image_size=(300, 100),key = f"{i}",image_filename = f"images\\{i}.png",font="Arial 20",button_color=("pink", "grey"))]]
                    elif iIndex in range (24,32):
                        frame4Layout+= [[sg.Button(i, size = (30,10),image_size=(300, 100),key = f"{i}",image_filename = f"images\\{i}.png",font="Arial 20",button_color=("pink", "grey"))]]
                    elif iIndex in range (32,40):
                        frame5Layout+= [[sg.Button(i, size = (30,10),image_size=(300, 100),key = f"{i}",image_filename = f"images\\{i}.png",font="Arial 20",button_color=("pink", "grey"))]]
                    if iIndex == 40:
                        frame0 = sg.Frame("",frame0Layout)
                        frame00 = sg.Frame("", frame00Layout)
                        frame000 = sg.Frame("", frame000Layout)
                        frame1 = sg.Frame("",frame1Layout)
                        frame2 = sg.Frame("",frame2Layout)
                        frame3 = sg.Frame("",frame3Layout)
                        frame4 = sg.Frame("",frame4Layout)
                        frame5 = sg.Frame("",frame5Layout)
                        layout = [ [frame0],[frame1,frame2,frame3,frame4,frame5] ]


                        #Page 1's layout
                        #layout+= [ [sg.Button("Page 1", font = "Cambria 20",disabled = True),sg.Button("Page 2", font = "Cambria 20"),sg.Button("Page 3", font = "Cambria 20")] ]
                        layout+= [ [sg.Button("Page 1", font = "Cambria 20",disabled = True),sg.Button("Page 2", font = "Cambria 20",disabled = False),sg.Button("Page 3", font = "Cambria 20", disabled = False)] ]


                    if iIndex in range(40,48):
                        frame6Layout+= [[sg.Button(i, size = (30,10),image_size=(300, 100),key = f"{i}",image_filename = f"images\\{i}.png",font="Arial 20",button_color=("pink", "grey"))]]
                    elif iIndex in range (48,56):
                        frame7Layout+= [[sg.Button(i, size = (30,10),image_size=(300, 100),key = f"{i}",image_filename = f"images\\{i}.png",font="Arial 20",button_color=("pink", "grey"))]]
                    elif iIndex in range (56,64):
                        frame8Layout+= [[sg.Button(i, size = (30,10),image_size=(300, 100),key = f"{i}",image_filename = f"images\\{i}.png",font="Arial 20",button_color=("pink", "grey"))]]
                    elif iIndex in range (64,72):
                        frame9Layout+= [[sg.Button(i, size = (30,10),image_size=(300, 100),key = f"{i}",image_filename = f"images\\{i}.png",font="Arial 20",button_color=("pink", "grey"))]]
                    elif iIndex in range (72,80):
                        frame10Layout+= [[sg.Button(i, size = (30,10),image_size=(300, 100),key = f"{i}",image_filename = f"images\\{i}.png",font="Arial 20",button_color=("pink", "grey"))]]
                    if iIndex== 80:
                        frame6 = sg.Frame("",frame6Layout)
                        frame7 = sg.Frame("",frame7Layout)
                        frame8 = sg.Frame("",frame8Layout)
                        frame9 = sg.Frame("",frame9Layout)
                        frame10 = sg.Frame("",frame10Layout)
                        layout2 = [ [frame00],[frame6,frame7,frame8,frame9,frame10] ]
                        #page 2's layout
                        #layout2+= [ [sg.Button("Page 1", font = "Cambria 20"),sg.Button("Page 2", font = "Cambria 20",disabled = True),sg.Button("Page 3", font = "Cambria 20")] ]
                        layout2+= [ [sg.Button("Page 1", font = "Cambria 20", disabled = False),sg.Button("Page 2", font = "Cambria 20",disabled = True),sg.Button("Page 3", font = "Cambria 20",disabled = False)] ]
                    if iIndex in range(80,84):
                        frame11Layout += [[sg.Button(i, size = (30,10),image_size=(300, 100),key = f"{i}",image_filename = f"images\\{i}.png",font="Arial 20",button_color=("pink", "grey"))]]
                    if iIndex == 84:
                        
                        frame11 = sg.Frame("",frame11Layout)
                        #page 3's layout
                        layout3 = [ [frame000],[frame11] ]
                        layout3+= [ [sg.Button("Page 1", font = "Cambria 20",disabled = False),sg.Button("Page 2", font = "Cambria 20",disabled=False),sg.Button("Page 3", font = "Cambria 20", disabled = True)] ]
               
                window.disable()



                #ITEM READ WINDOWS MADE HERE
                readItemWindow3 = sg.Window("Item Guide: ", layout3,keep_on_top = True, size = (1920,1080), element_justification="center")
                readItemWindow2 = sg.Window("Item Guide: ", layout2,keep_on_top = True, size = (1920,1080), element_justification="center")
                
                readItemWindow = sg.Window("Item Guide: ", layout,keep_on_top = True, size = (1920,1080), element_justification="center")


                #This flag below is needed because if you finalize the window early, it causes a flashing to occur on the screen
                #We need to finalize it later in the code, but only once.  So the flag will have to be used to avoid multiple
                #finalizes.
                win2Finalize = False
                win3Finalize = False
                
                while True:
                    #if page 1 is open, read from page 1
                    if lastOpenPage == 1:
                        event = readItemWindow.read()
                    #if page 2 is open, read from page 2
                    elif lastOpenPage == 2:
                        event = readItemWindow2.read()
                    elif lastOpenPage == 3:
                        event = readItemWindow3.read()

                    #if you choose something to open page 1
                    if event[0] in ("Page 1", "keyA", "keyB", "keyC", "keyD", "keyE", "keyF", "keyG", "keyH", "keyI", "keyJ", "keyK", "keyL", "keyM", "keyN", "keyO", "keyP", "keyR") :
                        #reveal page 1
                        readItemWindow.UnHide()
                        #if page 2 was created, hide it
                        if win2Finalize == True:
                            readItemWindow2.Hide()
                        if win3Finalize == True:
                            readItemWindow2.Hide()
                        #set the open page to 1
                        lastOpenPage = 1
                        continue
                    #if you choose something to open page 2
                    if event[0] in ("Page 2", "keyS", "keyT", "keyU","keyV"):
                        if win2Finalize == False:
                            readItemWindow2.finalize()
                            win2Finalize = True
                        readItemWindow2.UnHide()
                        if win3Finalize == True:
                            readItemWindow3.Hide()
                        #show page 2, hide page 1
                        
                        readItemWindow.Hide()
                        #readItemWindow3.Hide()
                        lastOpenPage = 2
                        continue
                    
                    
                     #placeholder comment below for if a page 3 is ever needed
                    if event[0] in ( "keyW", "keyX", "keyY", "keyZ","Page 3"):
                        
                        
                        if win3Finalize == False:
                            readItemWindow3.finalize()
                            win3Finalize = True
                        readItemWindow3.UnHide()
                        if win2Finalize == True:
                            readItemWindow2.Hide()
                        readItemWindow.Hide()
                        lastOpenPage = 3
                        continue

                    #if you hit X, close the readitems
                    if None in event:
                        window.enable()
                        endReadItems = True
                        break
                    #backup in case None wasn't sufficient
                    if event == sg.WIN_CLOSED:
                        window.enable()
                        endReadItems = True
                    window.enable()

                
                    #if event 0 is equal to the name of an item
                    if event[0] in itemsList:
                        #hide the windows to avoid errant clicks    
                        readItemWindow.hide()
                        window.disable()

                        #if window2 was created, close it
                        if win2Finalize == True:
                            readItemWindow2.hide()
                        #if win3Finalize == True:
                        #    readItemWindow3.hide()

                        #layout for the item description; add gifs when possible
                        clickedItemLayout = [
                            [ sg.T(event[0], font = "cambria 30", justification = "center", size = (50,1), text_color = "Red")],
                            [ sg.Image(filename = f"images//{event[0]}.png")],
                            [ sg.T(longExplanation(window,event[0]),font = "cambria 20", justification = "center", size = (50,15))],
                            [ sg.Button("OK", size = (20,10))]
                            ]
                        
                        clickedItemWindow = sg.Window("Item Info", clickedItemLayout, keep_on_top = True, element_justification = "center")

                        #to pause the window without breaking the program
                        event1 = clickedItemWindow.read()

                        #go to the last page you were on
                        if lastOpenPage == 1:
                            readItemWindow.UnHide()
                        if win2Finalize == True:
                            if lastOpenPage == 2:
                                readItemWindow2.UnHide()
                        if win3Finalize == True:
                            if lastOpenPage == 3:
                                readItemWindow3.UnHide()
                        if event1[0] == None or event1[0] == "OK":
                            clickedItemWindow.close()
                        window.enable()
                        continue
                            
                            
                    
                window.enable()
        if endReadItems == True:
            continue


        
        try:
            #if you clicked an item button
            if event[0][0] in listOfItemListCoordinates:
                #grab the name of the item
                itemSelected = window[f"{event[0]}"].GetText()
                #assume the item wasn't found
                foundItems = False
                #check all allied pieces for the existence of an item
                for i in gameBoard:
                    for j in i:
                        if j[0].occupied and j[1].ownedBy == playerTurn and len(j[1].storedItems) > 0:
                            if itemSelected in j[1].storedItems:
                                j[0].highlight = True
                                foundItems = True
                #if the items were found, highlight pieces that have the item                
                if foundItems == True:
                    displayBoard(window, gameBoard)
                    window.refresh()
                    sg.popup("The following highlighted pieces have the item you selected.", keep_on_top = True)
                    #disable the items button because it'll cause errors otherwise
                    for j in range(0,15):
                        for i in range(0,3):
                            window[f"itemList{i}{j}"].update(disabled = True)
                    highlightValidDistance(gameBoard, window, (0,0),turnOff = True)
                    event = window.read()
                    displayBoard(window, gameBoard)
                    window.refresh()
        except:
            sg.popup(f"An error occurred, the input that caused it is: {event}", keep_on_top = True)
            #print( sys.exc_info())
            #print('Error opening %s: %s' % (value.filename, value.strerror))
            pass

        
        #disable the exit and cheetz buttons to avoid issues
        window["exit"].update(disabled=True)
        window["cheetz"].update(disabled=True)
        window["Read Items"].update(disabled=True)

        #disable the item lookup buttons when selecting a piece
        for j in range(0,15):
            for i in range(0,3):
                window[f"itemList{i}{j}"].update(disabled = True)
                    
        
##############################################################
#  Assuming a window tile was clicked for the start location #
##############################################################

        try:
            if event[0][0] >= 0 and event[0][0] < rows and event[0][1] >= 0 and event[0][1] < columns:
                location = ( event[0][0] , event[0][1] )
            else:
                sg.popup("An error occurred during piece selection.  Please try again.",keep_on_top = True)
                continue
        except:
            sg.popup("An exception occurred because you hit an unexpected button.  Don't do that.  Recovering...",keep_on_top = True)
            continue

            
       
        
        #IS THE PIECE A BOWLING BALL?  
        if gameBoard[event[0][0]][event[0][1]][0].occupied == True and "bowling ball" in gameBoard[event[0][0]][event[0][1]][1].activeBuffs:
            #highlightValidDistance(gameBoard, window, startLocation,turnOff = True)
            #if it's your enemy's bowling ball
            if gameBoard[event[0][0]][event[0][1]][1].ownedBy != playerTurn:
                pm(window,"That's not your piece!")
                sleep(.4)
                continue

            #row/column values of the bowling ball
            xloc = event[0][0]
            yloc = event[0][1]
            location = (xloc,yloc)
            #show the direction menu for the bowling ball
            bowlingLayout = [
                [sg.Button("Up",size = (55,4),image_filename = "images/bowlingUp.png",pad = (0,0))],
                [sg.Button("Left", image_filename = "images/bowlingLeft.png",size = (24,4),pad = (0,0)), sg.Button("Right",image_filename = "images/bowlingRight.png", size = (24,4),pad = (0,0))],
                [sg.Button("Down",image_filename = "images/bowlingDown.png", size = (55,4),pad = (0,0))],
                [sg.Button("Cancel", size = (19,1),pad = (0,0))]
                ]
            playsound("sounds/select.wav",block = False)
            window.disable()
            bowlingMenu = sg.Window("Direction",bowlingLayout,keep_on_top=True)
            event = bowlingMenu.read()
            window.enable()
            bowlingMenu.close()

            #if you pick a direction, go to the function
            if event[0] in ("Up", "Down", "Left", "Right"):
                bowlingBallFunction(window,gameBoard,location,event[0])
                #turn ends when bowling ball is moved
                return
            #otherwise catch all for errors - start this part of the turn over
            else:
                continue
            #reenable the exit button
            window["exit"].update(disabled=False)


        ######################################
        #  IF SECOND TURN (OR HIGHER)        #
        ######################################
        
        previousTurnLocation = []
        #force the piece to be last moved piece

        #if we're going again and the location saved as the last known location is occupied, and it's flagged as the piece that just moved:
        if repeatRestrictor[0] == True and gameBoard[repeatRestrictor[1][0]][repeatRestrictor[1][1]][0].occupied == True and gameBoard[repeatRestrictor[1][0]][repeatRestrictor[1][1]][1].currentTurnPiece == True:
            
            #repeat restrictor keeps track of where the player was last and forces the event to equal that location
            #sg.popup(f"DEBUG: 1 Event is {event}",keep_on_top = True)
            #sg.popup(f"DEBUG: 2 Forcing location as {repeatRestrictor[1]}",keep_on_top = True)

            #save the last known location to previousTurnLocation (clear first in case extra data remains)
            previousTurnLocation.clear()
            previousTurnLocation.append(repeatRestrictor[1])
            

            #if an error occurs, try from the beginning
            if event[0] == (-1,- 1):
                sg.popup("An error has occurred while determining last known location of a move again piece.  Please try again.", keep_on_top=True)
                repeatRestrictor = False
                continue
        
        window["examineItem"].update(disabled=True)



#if it's the same piece they moved earlier, make it grey.  If the piece isn't there, find it using the currentTurnPiece function
        if (repeatRestrictor[0] == True) and (startLocation == repeatRestrictor[1])and ( gameBoard[startLocation[0]][startLocation[1]][0].occupied == True and gameBoard[startLocation[0]][startLocation[1]][1].currentTurnPiece == True):
            try:
                playsound("sounds/select.wav",block=False)
                gameBoard[startLocation[0]][startLocation[1]][1].grey = True
                gameBoard[startLocation[0]][startLocation[1]][1].currentTurnPiece = True
            except:
                startLocation = findCurrentTurnPiece(window, gameBoard)
                if startLocation == False:
                    sg.popup("err 1: An item caused an error that made it impossible to determine which piece was using the Move Again.  In order to prevent crashes, your turn will end now.", keep_on_top = True)
                    return

                repeatRestrictor[1] = startLocation
            displayBoard(window, gameBoard)
        elif (repeatRestrictor[0] == True):
            startLocation = findCurrentTurnPiece(window, gameBoard)
            #pieceTeleported = True
            repeatRestrictor[1] = startLocation
            if startLocation == False:
                    sg.popup("err 2: An item caused an error that made it impossible to determine which piece was using the Move Again.  In order to prevent crashes, your turn will end now.", keep_on_top = True)
                    return
            
            repeatRestrictor[1] = startLocation
            displayBoard(window, gameBoard)
            playsound("sounds/select.wav",block=False)
            gameBoard[startLocation[0]][startLocation[1]][1].grey = True
            gameBoard[startLocation[0]][startLocation[1]][1].currentTurnPiece = True
            

        #if the second turn didn't happen
        if repeatRestrictor[0] == False:
            #sg.popup(f"DEBUG: Assuming first turn, Event is {event}",keep_on_top = True)
            startLocation = event[0]
            playsound("sounds/select.wav",block=False)
            startLocationBackup = startLocation

        #if the second turn did happen
        elif repeatRestrictor[0] == True:
            playsound("sounds/select.wav",block=False)
            #sg.popup(f"DEBUG: Assuming repeat turn, repeatRestriction is {repeatRestrictor[1]}",keep_on_top = True)
            startLocation = repeatRestrictor[1]
            startLocationBackup = startLocation

            

        #highlight the area around the piece that is designated as selected CHANGE THIS IF YOU WANT TO ADD AN INFO THINGY
        if gameBoard[startLocation[0]][startLocation[1]][0].occupied == True and gameBoard[startLocation[0]][startLocation[1]][1].currentTurnPiece == True and gameBoard[startLocation[0]][startLocation[1]][1].ownedBy == playerTurn:
        #if gameBoard[startLocation[0]][startLocation[1]][0].occupied == True and gameBoard[startLocation[0]][startLocation[1]][1].currentTurnPiece == True:
            #sg.popup(f"DEBUG:4 highlight after selection  startLocation is {startLocation}",keep_on_top = True)
            
            highlightValidDistance(gameBoard, window, startLocation)


        #if the person is trying to move a piece that isn't the same piece they just moved - either force the piece to be picked, or end your turn
        if (repeatRestrictor[0] == True) and ( (startLocation[0],startLocation[1]) != repeatRestrictor[1]):
            getChoice = sg.popup_yes_no(
                "You can only move the same piece twice.  Move again? Click yes to force that piece to be selected.  Otherwise choose no to end your turn.",
                keep_on_top=True,
            )
            if getChoice == "Yes":
                startLocation = repeatRestrictor[1]
                highlightValidDistance(gameBoard, window, startLocation)
            else:
                return


        
##########################################################
# NO PIECES EXISTS ON THE STARTING TILE THAT WAS CLICKED #                          
##########################################################

        # if there's no piece on that square
##        if gameBoard[event[0][0]][event[0][1]][0].occupied == False:
        if gameBoard[startLocation[0]][startLocation[1]][0].occupied == False:
            window["information"].update(text_color="red")
            window["information"].update(
                f"You can't interact directly with unoccupied spaces."
            )
            playsound("sounds/wrong.wav",block=False) 
            pm(window, f"You can't interact directly with unoccupied spaces.")
            window.refresh()
            sleep(0.25)
            continue
        
###########################################
#  PIECE EXISTS ON STARTING TILE          #
###########################################

        # otherwise, if a tile is picked and a piece exists on it
        #elif gameBoard[event[0][0]][event[0][1]][0].occupied == True:
        elif gameBoard[startLocation[0]][startLocation[1]][0].occupied == False:

            # if that piece is stunned and it's your piece
            if (
                playerTurn == gameBoard[startLocation[0]][startLocation[1]][1].ownedBy
                and "stunned" in gameBoard[startLocation[0]][startLocation[1]][1].activeDebuffs
            ):
                playsound("sounds/wrong.wav",block=False) 
                window["information"].update(
                    f"You cannot use a stunned/sleeping piece."
                )
                pm(window, f"Pick a piece to move.")
                window["information"].update(text_color="red")
                window.refresh()
                continue

            # if the piece belongs to you and it has items (and isn't stunned)
            elif (
                #playerTurn == gameBoard[event[0][0]][event[0][1]][1].ownedBy
                playerTurn == gameBoard[startLocation[0]][startLocation[1]][1].ownedBy
                #and len(gameBoard[event[0][0]][event[0][1]][1].storedItems) > 0
                and len(gameBoard[startLocation[0]][startLocation[1]][1].storedItems)
            ):
                playsound("sounds/select.wav",block=False)
                window["information"].update(
                    f"Selection made. Pick a destination.\nOR CLICK THE PIECE AGAIN TO SEE AVAILABLE ITEMS."
                )
                pm(
                    window,
                    f"Selection made, pick a destination or click the same piece again to access items.",
                )

                ###window["readItems"].update(disabled=True)
            
            # if the piece doesn't belong to you
            #elif playerTurn != gameBoard[event[0][0]][event[0][1]][1].ownedBy:
            elif playerTurn != gameBoard[startLocation[0]][startLocation[1]].ownedBy:
                playsound("sounds/wrong.wav",block=False) 
                window["information"].update(f"That's not your piece...")
                pm(window, f"That's not your piece...")
                window["information"].update(text_color="red")
                window.refresh()
                sleep(.3)
                continue
            
            # if the piece belongs to you but doesn't have items
            else:
                playsound("sounds/select.wav",block=False)
                window["information"].update(f"Selection made, pick a destination.")
                pm(window, f"Selection made, pick a destination.")

        
        # if there is a piece there and it belongs to you, highlight it to show you selected it
        if gameBoard[startLocation[0]][startLocation[1]][1] != 0 and gameBoard[startLocation[0]][startLocation[1]][1].ownedBy == playerTurn:
            gameBoard[startLocation[0]][startLocation[1]][1].grey = True
            gameBoard[startLocation[0]][startLocation[1]][1].currentTurnPiece = True
            highlightValidDistance(gameBoard, window, startLocation)
            
        # update the board (to show highlighting)
        displayBoard(window, gameBoard)
        window.refresh()

        if gameBoard[startLocation[0]][startLocation[1]][1] != 0 and gameBoard[startLocation[0]][startLocation[1]][1].ownedBy != playerTurn:
            playsound("sounds/wrong.wav",block=False) 
            window["information"].update(f"That's not your piece...")
            pm(window, f"That's not your piece...")
            window["information"].update(text_color="red")
            window.refresh()
            sleep(.3)
            continue

#########################################
#  ASK DESTINATION                      #
#########################################
        
        # get the next location
        event = window.read()
        
        
        highlightValidDistance(gameBoard, window, startLocation,turnOff = True)
        displayBoard(window, gameBoard)
        window.refresh
        window["examineItem"].update(disabled=True)
        
########################################
#   DESTINATION OFFICIALLY SAVED HERE  #
########################################

        # this is where we're attempting to move 
        endLocation = event[0]

        
        # trying to use item (if the player clicked a piece and then the item button, or clicked the same icon twice)
        if (
            startLocation == endLocation
            and gameBoard[startLocation[0]][startLocation[1]][0].occupied == True
        ):

            # check to see if it's legal to use item
            if len(
                gameBoard[startLocation[0]][startLocation[1]][1].storedItems
            ) > 0 and (
                gameBoard[startLocation[0]][startLocation[1]][1].ownedBy == playerTurn
            ):
                
                earlyBreak = useItems(gameBoard, startLocation[0], startLocation[1], window)
                if earlyBreak == "earlyBreak":
                    startLocation = startLocationBackup

                if gameBoard[startLocation[0]][startLocation[1]][0].occupied == True:
                    gameBoard[startLocation[0]][startLocation[1]][1].grey = False
                    #sg.popup("DEBUG: setting false due to item", keep_on_top = True)
                    if repeatRestrictor[0] == False:
                        gameBoard[startLocation[0]][startLocation[1]][1].currentTurnPiece = False
                #check to see if any piece counts changed
                countPieces(gameBoard, window,PublicStats)
                displayBoard(window, gameBoard)
                continue
            
            # if the piece isn't yours
            elif gameBoard[startLocation[0]][startLocation[1]][1].ownedBy != playerTurn:
                gameBoard[startLocation[0]][startLocation[1]][1].grey = False
                if repeatRestrictor[0] == False:
                    gameBoard[startLocation[0]][startLocation[1]][1].currentTurnPiece = False
                pm(window, "That's not your piece")
                sleep(.4)
                continue

            # if the piece has no items
            elif len(gameBoard[startLocation[0]][startLocation[1]][1].storedItems) < 1:
                gameBoard[startLocation[0]][startLocation[1]][1].grey = False
                if repeatRestrictor[0] == False:
                    gameBoard[startLocation[0]][startLocation[1]][1].currentTurnPiece = False
                pm(window, "There are no items on this piece.")
                playsound("sounds/wrong.wav",block=False) 
                sleep(.4)
                continue
            # shouldn't get to here
            else:
                pm(window, "An error occurred in item lookups")

                
        # if there isn't any piece on the square
        if gameBoard[startLocation[0]][startLocation[1]][0].occupied == False:
            if repeatRestrictor[0] == False:
                gameBoard[startLocation[0]][startLocation[1]][1].currentTurnPiece = False
            playsound("sounds/wrong.wav",block=False) 
            pm(window, f"Nothing exists on the initial square!")
            window.refresh
            continue

        # if the piece no longer exists on the original point, ungrey it
        if gameBoard[startLocation[0]][startLocation[1]][1] != 0:
            gameBoard[startLocation[0]][startLocation[1]][1].grey = False
            if repeatRestrictor[0] == False:
                gameBoard[startLocation[0]][startLocation[1]][1].currentTurnPiece = False
        displayBoard(window, gameBoard)



        
        #if your start location contains no pieces
        if gameBoard[startLocation[0]][startLocation[1]][0].occupied == False:
            playsound("sounds/wrong.wav",block=False) 
            window["information"].update(f"Nothing here to move!")
            pm(window, "Nothing here to move!")
            window.refresh
            continue
        
        # if the spot you're moving from contains a piece (which it should)
        elif gameBoard[startLocation[0]][startLocation[1]][0].occupied == True:

            # if the piece is yours
            if gameBoard[startLocation[0]][startLocation[1]][1].ownedBy == playerTurn:

#########################################
#   BEGIN MOVE TESTS                    #
#########################################

                #worm hole override

                #test for tripmine trip mine
                wormHole = False
                #if player 1's turn and there's a worm hole there
                if gameBoard[endLocation[0]][endLocation[1]][0].wormHole1 == True and playerTurn == 1:
                    if gameBoard[endLocation[0]][endLocation[1]][0].occupied == False or (gameBoard[endLocation[0]][endLocation[1]][0].occupied and gameBoard[endLocation[0]][endLocation[1]][1].ownedBy != playerTurn):
                        wormHole = True
                    elif gameBoard[endLocation[0]][endLocation[1]][0].occupied == True and "berzerk" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
                        wormHole = True
                if gameBoard[endLocation[0]][endLocation[1]][0].wormHole2 == True and playerTurn == 2:
                    if gameBoard[endLocation[0]][endLocation[1]][0].occupied == False or (gameBoard[endLocation[0]][endLocation[1]][0].occupied and gameBoard[endLocation[0]][endLocation[1]][1].ownedBy != playerTurn):
                        wormHole = True
                    elif gameBoard[endLocation[0]][endLocation[1]][0].occupied == True and "berzerk" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
                        wormHole = True

                # assume the player isn't trying to move diagonally at first
                diagonalCheck = False




                # if you have a round earth theory item equipped (to "pac man" around the edge of the screen to the opposite side)
                if "round earth theory" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
                    roundEarthTheory = roundEarthTheoryFunction(gameBoard,startLocation,endLocation,columns,rows)




                
                    
                # if you're attemmpting to go somewhere that is too far...
                # ...but you have a move diagonal and it turns out you're actually within range:
                if roundEarthTheory == False and wormHole == False:
                    if (
                        getDistance(
                            startLocation[0],
                            startLocation[1],
                            endLocation[0],
                            endLocation[1],
                        )
                        > 1
                    ):
                        if (
                            "move diagonal"
                            in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs
                        ):
                            
                            validRange = getRadial(
                                (startLocation[0], startLocation[1]), gameBoard
                            )
                            # if they're trying to move diagonally
                            if (endLocation[0], endLocation[1]) in validRange:
                                diagonalCheck = True

                    # ....and it's not because you want to move diagonally with a move diagonal
                    if (
                        getDistance(
                            startLocation[0],
                            startLocation[1],
                            endLocation[0],
                            endLocation[1],
                        )
                        > gameBoard[startLocation[0]][startLocation[1]][1].distanceMax
                    ) and diagonalCheck == False:
                        playsound("sounds/wrong.wav",block=False) 
                        window["information"].update(
                            f"That location is too far for you to move to!"
                        )
                        pm(window, f"That location is too far for you to move to!")
                        gameBoard[startLocation[0]][startLocation[1]][1].currentTurnPiece = True
                        window.refresh
                        continue
                
                ##################################################
                # if it's close enough:  (DESTINATION/LEGAL MOVE)#
                ##################################################

                

                #tile height gate (stops you from moving if the elevation is too high)
                if (gameBoard[startLocation[0]][startLocation[1]][0].tileHeight+1 < gameBoard[endLocation[0]][endLocation[1]][0].tileHeight) and ("grappling hook" not in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs) and wormHole == False:
                    playsound("sounds/wrong.wav",block=False) 
                    sg.popup("The tile you're trying to get to is too high",keep_on_top = True)
                    pm(window,"The tile you're trying to get to is too high")
                    continue

                
                




                #####
                # if the landing spot is an item Orb:
                if gameBoard[endLocation[0]][endLocation[1]][0].tileType == "itemOrb":

                    playsound("sounds/getItem.wav",block=False)
                    pickUpItemOrb(gameBoard, startLocation[0], startLocation[1], window = window)
                    pm(window, "Picked up an item")
                    pickedUpItem = True
                 
                    
                # if the landing spot is missing or still damaged
                if gameBoard[endLocation[0]][endLocation[1]][0].tileType in [
                    "damaged",
                    "destroyed",
                    "damaged1",
                    "damaged2",
                    "damaged3",
                    "damaged4",
                    "damaged5",
                    "damaged6",
                    "damaged7",
                    "damaged8"
                ]:
                    playsound("sounds/wrong.wav",block=False) 
                    window["information"].update(f"Can't move here!  The floor is missing/damaged.")
                    pm(window, "Can't move here!  The floor is missing/damaged.")
                    sg.popup("Can't move here!  The floor is missing/damaged.", keep_on_top = True)
                    window.refresh()
                    sleep(.3)
                    continue

                
##########################################################
#  Start location = occupied, destination != occupied    #
##########################################################
                # if the landing spot is not occupied by a piece
                if gameBoard[endLocation[0]][endLocation[1]][0].occupied == False:
                    g = gameBoard[endLocation[0]][endLocation[1]][0]
                    deathCheck(window, gameBoard)

                    #jumpoline check
                    if gameBoard[endLocation[0]][endLocation[1]][0].tileType == "jumpoline":
                        if g.horiLaser == True or g.vertLaser == True or g.crossLaser == True:

                            #forcefield check needs to be added
                            
                            gameBoard[endLocation[0]][endLocation[1]][
                                0
                            ].occupied = False
                            gameBoard[startLocation[0]][startLocation[1]][0].occupied = False
                            gameBoard[startLocation[0]][startLocation[1]][1] = 0
                            gameBoard[endLocation[0]][endLocation[1]][1] = 0
                            gameBoard[endLocation[0]][endLocation[1]][1] = 0
                            gameBoard[endLocation[0]][endLocation[1]][
                                0
                            ].tileType = "exploding"
                            displayBoard(window, gameBoard)
                            window.refresh()
                            playsound("sounds/grenade.mp3", block = False)
                            sg.popup("Burned to a crisp by the laser", keep_on_top=True)
                            gameBoard[endLocation[0]][endLocation[1]][
                                0
                            ].tileType = "jumpoline"
                            break
                        endlocation = []
                        endLocation = jumpoline(window, gameBoard, (endLocation[0],endLocation[1]), playerTurn)
                        sg.popup("Bounced to a new spot!",keep_on_top = True)
                        pm(window,"Bounced to a new spot!")
                        
  
                    # copy the actual piece object over from the old address to the new one (deepcopy needed?)
                    gameBoard[endLocation[0]][endLocation[1]][1] = gameBoard[startLocation[0]][startLocation[1]][1]

                    #might be glitchy
                    gameBoard[endLocation[0]][endLocation[1]][0].occupied = True
                    #might be glitchy
                    
                    # set the original location as being empty; delete the class
                    gameBoard[startLocation[0]][startLocation[1]][0].occupied = False
                    gameBoard[startLocation[0]][startLocation[1]][1] = 0





                    
                    #purity tile check
                    if gameBoard[endLocation[0]][endLocation[1]][0].purityTile == True:
                        debuffsCleaned = ""
                        if gameBoard[endLocation[0]][endLocation[1]][0].occupied == True:
                            if gameBoard[endLocation[0]][endLocation[1]][1].stickyTimeBomb != False:
                                    debuffsCleaned += "Sticky Bomb\n"
                                    gameBoard[endLocation[0]][endLocation[1]][1].stickyTimeBomb = False
                            for debuffs in gameBoard[endLocation[0]][endLocation[1]][1].activeDebuffs:
                                debuffsCleaned += debuffs+"\n"
                        sg.popup(f"All negative effects on this piece have been cleared:\n {debuffsCleaned}",keep_on_top = True)
                        gameBoard[endLocation[0]][endLocation[1]][1].activeDebuffs.clear()


                    #item dump
                    if gameBoard[endLocation[0]][endLocation[1]][0].tileType == "itemDump":
                        if g.horiLaser == True or g.vertLaser == True or g.crossLaser == True:

                            #forcefield check needs to be added
                            
                            gameBoard[endLocation[0]][endLocation[1]][
                                0
                            ].occupied = False
                            gameBoard[startLocation[0]][startLocation[1]][0].occupied = False
                            gameBoard[startLocation[0]][startLocation[1]][1] = 0
                            
                            gameBoard[endLocation[0]][endLocation[1]][1] = 0
                            gameBoard[endLocation[0]][endLocation[1]][
                                0
                            ].tileType = "exploding"
                            displayBoard(window, gameBoard)
                            window.refresh()
                            playsound("sounds/grenade.mp3", block = False)
                            sg.popup("Burned to a crisp by the laser", keep_on_top=True)
                            gameBoard[endLocation[0]][endLocation[1]][
                                0
                            ].tileType = "itemDump"
                            break
                        
                        elif "inhibited" not in gameBoard[endLocation[0]][endLocation[1]][1].activeDebuffs:
                            itemsGained = 0
                            for i in gameBoard[endLocation[0]][endLocation[1]][0].dumpList:
                                gameBoard[endLocation[0]][endLocation[1]][1].storedItems.append(i)
                                itemsGained += 1
                            sg.popup(f"Gained {itemsGained} items from the item dump!",keep_on_top = True)
                            gameBoard[endLocation[0]][endLocation[1]][0].tileType = "default"





                        
##                    if gameBoard[endLocation[0]][endLocation[1]][0].secretAgent != False:
##                        
##                        if g.horiLaser == True or g.vertLaser == True or g.crossLaser == True:
##
##                            #forcefield check needs to be added
##                            
##                            gameBoard[endLocation[0]][endLocation[1]][
##                                0
##                            ].occupied = False
##                            gameBoard[startLocation[0]][startLocation[1]][0].occupied = False
##                            gameBoard[startLocation[0]][startLocation[1]][1] = 0
##                            gameBoard[endLocation[0]][endLocation[1]][1] = 0
##                            gameBoard[endLocation[0]][endLocation[1]][1] = 0
##                            gameBoard[endLocation[0]][endLocation[1]][
##                                0
##                            ].tileType = "exploding"
##                            displayBoard(window, gameBoard)
##                            window.refresh()
##                            playsound("sounds/grenade.mp3", block = False)
##                            sg.popup("Burned to a crisp by the laser", keep_on_top=True)
##                            return
                            
                        
                        

                    #mystery box
                    
                    
                    if gameBoard[endLocation[0]][endLocation[1]][0].tileType == "mystery box":
                        
                        if g.horiLaser == True or g.vertLaser == True or g.crossLaser == True:

                            #forcefield check needs to be added
                            
                            gameBoard[endLocation[0]][endLocation[1]][
                                0
                            ].occupied = False
                            gameBoard[startLocation[0]][startLocation[1]][0].occupied = False
                            gameBoard[startLocation[0]][startLocation[1]][1] = 0
                            
                            gameBoard[endLocation[0]][endLocation[1]][1] = 0
                            gameBoard[endLocation[0]][endLocation[1]][
                                0
                            ].tileType = "exploding"
                            displayBoard(window, gameBoard)
                            window.refresh()
                            playsound("sounds/grenade.mp3", block = False)
                            sg.popup("Burned to a crisp by the laser", keep_on_top=True)
                            gameBoard[endLocation[0]][endLocation[1]][
                                0
                            ].tileType = "mystery box"
                            break
                        
                        randomEvent = random.choice( ["getItems", "lose items", "die", "lose buffs", "lose debuffs"])
                        if randomEvent == "getItems":
                            #get three items
                            for i in range(1,4):
                                playsound("sounds/getItem.wav",block=False)
                                pickUpItemOrb(gameBoard, endLocation[0], endLocation[1], window = window)
                        elif randomEvent == "lose items":
                            gameBoard[endLocation[0]][endLocation[1]][1].storedItems.clear()
                            sg.popup("The mystery box has confiscated all of your held items",keep_on_top = True)
                            pm(window,"The mystery box has confiscated all of your held items")
                        elif randomEvent == "lose debuffs":
                            gameBoard[endLocation[0]][endLocation[1]][1].activeDebuffs.clear()
                            sg.popup("The mystery box has purified you of all negative effects.")
                            pm(window,"The mystery box has purified you of all negative effects.")
                        elif randomEvent == "lose buffs":
                            gameBoard[endLocation[0]][endLocation[1]][1].activeBuffs.clear()
                            sg.popup("The mystery box has stripped you of all your active buffs.  At least it didn't kill ya, I guess?")
                            pm(window,"The mystery box has stripped you of all your active buffs.  At least it didn't kill ya, I guess?")
                        elif randomEvent == "die":
                            gameBoard[endLocation[0]][endLocation[1]][0].occupied = False
                            gameBoard[startLocation[0]][startLocation[1]][0].occupied = False
                            gameBoard[startLocation[0]][startLocation[1]][1] = 0
                            
                            gameBoard[endLocation[0]][endLocation[1]][1] = 0
                            gameBoard[endLocation[0]][endLocation[1]][0].tileType = "exploding"
                            displayBoard(window, gameBoard)
                            window.refresh()
                            playsound("sounds/grenade.mp3", block = False)
                            sg.popup("The mystery box has killed ya!  Get wrecked.", keep_on_top=True)
                            gameBoard[endLocation[0]][endLocation[1]][0].tileType = "mystery box"
                            return
                        
                    if (
                        gameBoard[endLocation[0]][endLocation[1]][1].standingOnSelfOrb
                        == True
                    ):
                        gameBoard[startLocation[0]][startLocation[1]][
                            0
                        ].tileType = f"trap orb {playerTurn}"
                    else:
                        gameBoard[startLocation[0]][startLocation[1]][0].tileType = "default"

                    
                    
                    # set the new location as occupied; set the tile as the type of the tile that moved (needs to be updated in future revisions)
                    gameBoard[endLocation[0]][endLocation[1]][0].occupied = True
                    gameBoard[endLocation[0]][endLocation[1]][1].location = (
                        endLocation[0],
                        endLocation[1],
                    )
                    # check for mine death
                    deathCheck(window, gameBoard)
                    
                    if (
                        gameBoard[endLocation[0]][endLocation[1]][1] != 0
                        and gameBoard[endLocation[0]][endLocation[1]][0].tileType
                        != f"trap orb {playerTurn}"
                    ):
                        gameBoard[endLocation[0]][endLocation[1]][
                            0
                        ].tileType = f"player{playerTurn}default"
                    elif gameBoard[endLocation[0]][endLocation[1]][1] == 0:
                        break

                    if (
                        gameBoard[endLocation[0]][endLocation[1]][0].tileType
                        == f"trap orb {playerTurn}"
                    ):
                        gameBoard[endLocation[0]][endLocation[1]][
                            1
                        ].standingOnSelfOrb = True

                    if (
                        "trip mine"
                        in gameBoard[endLocation[0]][endLocation[1]][1].activeDebuffs
                    ):

                        if (
                            "Energy Forcefield"
                            in gameBoard[endLocation[0]][endLocation[1]][1].activeBuffs
                        ):
                            gameBoard[endLocation[0]][endLocation[1]][
                                1
                            ].activeBuffs.remove("Energy Forcefield")
                            pm(window, "Trip mine went off!")
                            playsound("sounds/grenade.mp3", block = False)
                            sleep(1)
                            pm(window, "...But your forcefield saved you.")
                            while (
                                "trip mine"
                                in gameBoard[endLocation[0]][endLocation[1]][
                                    1
                                ].activeBuffs
                            ):
                                gameBoard[endLocation[0]][endLocation[1]][
                                    1
                                ].activeDebuffs.remove("trip mine")

                        else:
                            gameBoard[endLocation[0]][endLocation[1]][
                                0
                            ].occupied = False
                            gameBoard[endLocation[0]][endLocation[1]][1] = 0
                            gameBoard[endLocation[0]][endLocation[1]][1] = 0
                            gameBoard[endLocation[0]][endLocation[1]][
                                0
                            ].tileType = "exploding"
                            displayBoard(window, gameBoard)
                            window.refresh()
                            playsound("sounds/grenade.mp3", block = False)
                            sg.popup("Trip mine went off!", keep_on_top=True)
                            gameBoard[endLocation[0]][endLocation[1]][
                                0
                            ].tileType = "default"
                            break
                    if gameBoard[endLocation[0]][endLocation[1]][0].orbEater == True:
                        sg.popup("You monster!  You killed an orb eater!",keep_on_top = True)
                        gameBoard[endLocation[0]][endLocation[1]][0].orbEater = False

                     

                    playsound("sounds/thump.mp3",block=False)    
                    pm(window, f"Player {playerTurn} moved successfully.")
                    #gameBoard[endLocation[0]][endLocation[1]][1].currentTurnPiece = False
                    window.refresh

                    # go again if you have moveAgain equipped

##                    if (
##                        gameBoard[endLocation[0]][endLocation[1]][1] != 0
##                        and gameBoard[endLocation[0]][endLocation[1]][1].moveAgain > 0
##                    ):

# debug attempt
                    if (
                        gameBoard[endLocation[0]][endLocation[1]][1] != 0
                        and gameBoard[endLocation[0]][endLocation[1]][1].moveAgain > 0
                        
                    ):
                        window["information"].update(
                            f"This piece gets to move again; {gameBoard[ endLocation[0] ] [ endLocation[1] ][1].moveAgain} remaining!"
                        )
                        displayBoard(window, gameBoard)
                        window.disable()
                        moveAgainCheck = sg.popup_yes_no(
                            "This piece has a Move Again buff, and gets to go again. Would you like to use it again?", keep_on_top=True,font = "Cambria 30",background_color="black", text_color = "green" , line_width = 15
                        )
                        window.enable()
                        if moveAgainCheck == "Yes":
                            gameBoard[endLocation[0]][endLocation[1]][1].moveAgain -= 1
                            repeatRestrictor[0] = True
                            repeatRestrictor[1] = (endLocation[0], endLocation[1])
##                            for i in gameBoard:
##                                for j in i:
##                                    if j[0].occupied == True:
##                                        j[1].currentTurnPiece = False
##                            gameBoard[endLocation[0]][endLocation[1]][1].currentTurnPiece = True
                            gameBoard[endLocation[0]][endLocation[1]][1].currentTurnPiece = True
                            pm(window, "Move again perk activated.")
                            continue
                        else:
                            return

                    else:
                        return 1

                # killing own piece (illegal)
                elif gameBoard[endLocation[0]][endLocation[1]][1].ownedBy == playerTurn and "berzerk" not in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
                    playsound("sounds/wrong.wav",block=False) 
                    pm(window, "You can't jumpkill your own piece.")
                    window.refresh
                    continue

                # kill enemy piece; elif enemy owns the ending location
                elif gameBoard[endLocation[0]][endLocation[1]][1].ownedBy != playerTurn or "berzerk" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
                    # test to see if the piece can be jumped
                    if (
                        "jump proof"
                        in gameBoard[endLocation[0]][endLocation[1]][1].activeBuffs
                    ):
                        playsound("sounds/wrong.wav",block=False) 
                        pm(window, "No!  This opponent is jump proof!")
                        window.refresh()
                        sleep(1)
                        continue

                    #Program dead man's trigger
                    elif ("dead man's trigger" in gameBoard[endLocation[0]][endLocation[1]][1].activeBuffs):
                        sg.popup("The piece had a dead man's trigger.  Your piece died as well.",keep_on_top = True)
                        deadMansTrigger = True

                        #delete the original location
                        gameBoard[startLocation[0]][startLocation[1]][1] = 0
                        gameBoard[startLocation[0]][startLocation[1]][0].occupied = False

                        #delete where the bomb is
                        gameBoard[endLocation[0]][endLocation[1]][1] = 0
                        gameBoard[endLocation[0]][endLocation[1]][0].occupied = False
                        
                        return

                    #if vampiricism, then steal the pieces
                    if "vampiricism" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs and len(gameBoard[endLocation[0]][endLocation[1]][1].activeBuffs)>0:
                        stealPowersCount = 0
                        powersList = ""
                        for buffs in gameBoard[endLocation[0]][endLocation[1]][1].activeBuffs:
                            if buffs not in ("bowling ball"):
                                gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs.append(buffs)
                                powersList += f"{buffs}\n"
                                stealPowersCount +=1
                        if stealPowersCount > 0:
                            playsound("sounds/vampire.mp3",block=False)
                            sg.popup(f"You stole {stealPowersCount} powers from the victim: \n{powersList}", keep_on_top = True)
                            pm(window,f"You stole {stealPowersCount} powers from the victim: \n{powersList}")
                                
                    # set the internal location of the piece to where you want to end up
                    gameBoard[startLocation[0]][startLocation[1]][1].location = (
                        endLocation[0],
                        endLocation[1],
                    )
                    
                    # move the piece object
                    gameBoard[endLocation[0]][endLocation[1]][1] = gameBoard[
                        startLocation[0]
                    ][startLocation[1]][1]
                    # delete the original piece
                    gameBoard[startLocation[0]][startLocation[1]][1] = 0
                    # set the original location as empty
                    gameBoard[startLocation[0]][startLocation[1]][0].occupied = False
                    # set the new location as full
                    gameBoard[endLocation[0]][endLocation[1]][0].occupied = True
                    # if gameBoard[startLocation[0]][startLocation[1]][0].tileType == "itemOrb":
                    if pickedUpItem == True:
                        pm(
                            window,
                            "The piece you just killed was sitting on an item orb.  You picked it up.  Lucky you got to it before he recovered from his stun",
                        )
                        # pickUpItemOrb(gameBoard,x,y)

                    # set the original tile as either a trap orb or default, depending on what was there  (ending spot default)
                    if (
                        gameBoard[endLocation[0]][endLocation[1]][1].standingOnSelfOrb== True):
                        gameBoard[startLocation[0]][startLocation[1]][
                            0
                        ].tileType = f"trap orb {playerTurn}"
                    else:
                        if gameBoard[startLocation[0]][startLocation[1]][0].tileType == "secretAgent":
                            gameBoard[startLocation[0]][startLocation[1]][0].tileType = "secretAgent"
                        else:
                            gameBoard[startLocation[0]][startLocation[1]][0].tileType = "default"
                    if (
                        "trip mine"
                        in gameBoard[endLocation[0]][endLocation[1]][1].activeDebuffs
                    ):
                        if (
                            "Energy Forcefield"
                            in gameBoard[endLocation[0]][endLocation[1]][1].activeBuffs
                        ):
                            gameBoard[endLocation[0]][endLocation[1]][
                                1
                            ].activeBuffs.remove("Energy Forcefield")
                            pm(window, "Trip mine went off!")
                            playsound("sounds/grenade.mp3", block = False)
                            sleep(1)
                            pm(window, "...But your forcefield saved you.")
                            while (
                                "trip mine"
                                in gameBoard[endLocation[0]][endLocation[1]][
                                    1
                                ].activeBuffs
                            ):
                                gameBoard[endLocation[0]][endLocation[1]][
                                    1
                                ].activeDebuffs.remove("trip mine")

                        else:
                            gameBoard[endLocation[0]][endLocation[1]][
                                0
                            ].occupied = False
                            gameBoard[endLocation[0]][endLocation[1]][1] = 0
                            gameBoard[endLocation[0]][endLocation[1]][1] = 0
                            gameBoard[endLocation[0]][endLocation[1]][
                                0
                            ].tileType = "exploding"
                            displayBoard(window, gameBoard)
                            window.refresh()
                            playsound("sounds/grenade.mp3", block = False)
                            sg.popup("Trip mine went off!", keep_on_top=True)
                            gameBoard[endLocation[0]][endLocation[1]][
                                0
                            ].tileType = "default"
                            break
                    if "berzerk" in gameBoard[endLocation[0]][endLocation[1]][1].activeBuffs:
                        playsound("sounds/destroy.wav",block=False)
                        pm(window, f"THE BEZERKER KILLED A PIECE AND ENRAGED!  IT HAS EATEN PART OF THE VICTIM AND IS STORING THE REST FOR LATER!")
                        displayBoard(window, gameBoard)
                        window.refresh()
                        gameBoard[endLocation[0]][endLocation[1]][1].berzerkAttacksLeft -=1
                        gameBoard[endLocation[0]][endLocation[1]][1].berzerkMeatCount +=1
                        sg.popup(f"THE BEZERKER KILLED A PIECE AND ENRAGED!  IT HAS EATEN PART OF THE VICTIM AND IS STORING THE REST FOR LATER!",keep_on_top = True)
                        
                        if gameBoard[endLocation[0]][endLocation[1]][1].berzerkAttacksLeft > 0:
                            sleep(1)
                            window["information"].update(f"THE BEZERKER IS STILL ENRAGED AND HAS {gameBoard[endLocation[0]][endLocation[1]][1].berzerkAttacksLeft} ATTACKS LEFT, AND HAS STORED {gameBoard[endLocation[0]][endLocation[1]][1].berzerkMeatCount} MEATS")
                            sg.popup(f"THE BEZERKER IS STILL ENRAGED AND HAS {gameBoard[endLocation[0]][endLocation[1]][1].berzerkAttacksLeft} ATTACKS LEFT, AND HAS STORED {gameBoard[endLocation[0]][endLocation[1]][1].berzerkMeatCount} MEATS",keep_on_top = True)
                            repeatRestrictor[0] = True
                            repeatRestrictor[1] = (endLocation[0], endLocation[1])
                            gameBoard[endLocation[0]][endLocation[1]][1].currentTurnPiece = True
                            continue
                        else:
                            return
                        #


                    else:
                        playsound("sounds/destroy.wav",block=False)
                        window["information"].update(f"Jumpkilled an enemy piece!")
                        pm(window, "Jumpkilled an enemy piece!")

                    secretAgentCheck(window, gameBoard, startLocation, endLocation, playerTurn)
                    

                    # go again if you have moveAgain equipped (needed to bypass the "end after attacking" process
                    if (
                        gameBoard[endLocation[0]][endLocation[1]][1] != 0
                        and gameBoard[endLocation[0]][endLocation[1]][1].moveAgain > 0
                    ):


                        window["information"].update(
                            f"This piece gets to move again; {gameBoard[ endLocation[0] ] [ endLocation[1] ][1].moveAgain} remaining!"
                        )
                        # sleep(1)
                        moveAgainCheck = sg.popup_yes_no(
                            "Would you like to move this piece again?", keep_on_top=True
                        )

                        if moveAgainCheck == "Yes":

                            gameBoard[endLocation[0]][endLocation[1]][1].moveAgain -= 1
                            repeatRestrictor[0] = True
                            repeatRestrictor[1] = (endLocation[0], endLocation[1])
                            gameBoard[endLocation[0]][endLocation[1]][1].currentTurnPiece = True
                            continue
                        else:
                            return
                    return 2
            
            else:
                playsound("sounds/wrong.wav",block=False) 
                window["information"].update(f"That's not your piece!")
                pm(window, "That's not your piece!")
                sleep(.3)
                window.refresh
                continue



# after your ends, get back your max "move again" turns
def resetMoveAgain(gameBoard):
    moveAgainCount = 0
    for i in gameBoard:
        for j in i:
            moveAgainCount = 0
            if j[0].occupied == True:
                if len(j[1].activeBuffs) > 0:
                    for k in j[1].activeBuffs:
                        if k == "move again":
                            moveAgainCount += 1
            if j[0].occupied == True:
                j[1].moveAgain = moveAgainCount



def spookyHand(window, gameBoard):
    PublicStats.spookyHandTurnCount -= 1
    attempts = 50
    if PublicStats.spookyHandTurnCount == 0:
        while attempts > 0:
            attempts -= 1
            xrand = random.randint(0, len(gameBoard)-1)
            yrand = random.randint(0, len(gameBoard[0])-1)

            #only attack spaces with pieces
            if  gameBoard[xrand][yrand][0].occupied == True:
                nums = [1,2]
                choice = random.choice(nums)
                playsound(f"sounds\spookyHand{choice}.mp3", block = False)
                gameBoard[xrand][yrand][0].tileType = "hand1"
                displayBoard(window, gameBoard)
                sleep(.5)
                window.refresh()
                
                gameBoard[xrand][yrand][0].tileType = "hand2"
                sleep(.5)
                displayBoard(window, gameBoard)
                window.refresh()

                gameBoard[xrand][yrand][0].tileType = "hand3"
                sleep(.5)
                displayBoard(window, gameBoard)
                window.refresh()

                gameBoard[xrand][yrand][1].ownedby=3
                displayBoard(window, gameBoard)
                window.refresh()


                gameBoard[xrand][yrand][0].tileType = "hand2"
                displayBoard(window, gameBoard)
                window.refresh()

                
                gameBoard[xrand][yrand][0].tileType = "hand1"
                displayBoard(window, gameBoard)
                window.refresh()
                gameBoard[xrand][yrand][0].occupied = False
                
                gameBoard[xrand][yrand][0].tileType = "destroyed"
                displayBoard(window, gameBoard)
                window.refresh()

                
                gameBoard[xrand][yrand][1] = 0
                gameBoard[xrand][yrand][0].occupied = False

                sg.popup("The spooky hand claimed a victim; and he will return for more...",keep_on_top = True)

                pm(window, "The spooky hand claimed a victim; and he will return for more...")

                PublicStats.spookyHandTurnCount = random.randint(10,15)

                break

                
def recallFunction(window,gameBoard):
    for iIndex,i in enumerate(gameBoard):
        for jIndex,j in enumerate(i):
            

            #if there's a piece at the spot we're on, see if the piece is supposed to disappear this turn
            if j[0].occupied == True:
                #if the recall turn count equals the current turn count, remove it
                if j[1].recallTurn == PublicStats.turnCount:
                    #sg.popup(f"Recall turn equals a piece match, deleting at {iIndex}{jIndex}")
                    gameBoard[iIndex][jIndex][1] = 0
                    gameBoard[iIndex][jIndex][0].tileType = "default"
                    gameBoard[iIndex][jIndex][0].occupied = False

            #if the recall turn count equals this turn, revert the tile to what it was (including the tile piece)        
            if j[0].recallTurn == PublicStats.turnCount:
                #sg.popup("Recall turn equals a tile")
                
                PublicStats.recallCount -=1
                gameBoard[iIndex][jIndex] = copy.deepcopy(j[0].recallBackup)
                
                displayBoard(window, gameBoard)
                sleep(.5)
                window.refresh()

                ## The following chunks of code are an animation showing the returning piece flashing so that the players know where the piece returned
                backupRecallTileTurn = gameBoard[iIndex][jIndex][0].recallTurn
                gameBoard[iIndex][jIndex][0].occupied = False
                gameBoard[iIndex][jIndex][0].tileType = "default"
                gameBoard[iIndex][jIndex][0].recallTurn = 1
                displayBoard(window, gameBoard)
                sleep(.5)
                window.refresh()

                ## flash the piece
                gameBoard[iIndex][jIndex] = copy.deepcopy(j[0].recallBackup)
                gameBoard[iIndex][jIndex][0].recallTurn = backupRecallTileTurn
                displayBoard(window, gameBoard)
                sleep(.5)
                window.refresh()

                #flash an empty tile with a clock
                backupRecallTileTurn = gameBoard[iIndex][jIndex][0].recallTurn
                gameBoard[iIndex][jIndex][0].occupied = False
                gameBoard[iIndex][jIndex][0].tileType = "default"
                gameBoard[iIndex][jIndex][0].recallTurn = 1
                displayBoard(window, gameBoard)
                sleep(.5)
                window.refresh()

                #show the piece again (and leave it this time)
                gameBoard[iIndex][jIndex] = copy.deepcopy(j[0].recallBackup)
                gameBoard[iIndex][jIndex][0].recallTurn = backupRecallTileTurn
                displayBoard(window, gameBoard)
                sleep(.5)
                window.refresh()
                
                sg.popup("A piece has recalled",keep_on_top = True)


        
            
def stickyTimeBomb(window,gameBoard):
    validLocations = []
    for iIndex,i in enumerate(gameBoard):
        for jIndex,j in enumerate(i):
            if j[0].occupied == True:
                if j[1].stickyTimeBomb != False and "sticky time bomb" in j[1].activeDebuffs:
                    if j[1].stickyTimeBomb == PublicStats.turnCount:
                        location = (iIndex,jIndex)
                        validLocations = getRadial(location, gameBoard)
                        for i in validLocations:
                            gameBoard[i[0]][i[1]][0].occupied = False
                            cleanTile(gameBoard[i[0]][i[1]][0])
                            gameBoard[i[0]][i[1]][1] = 0
                            gameBoard[i[0]][i[1]][0].tileType = "exploding"
                            displayBoard(window, gameBoard)
                            window.refresh()
                            sleep(.1)
                            
                            gameBoard[i[0]][i[1]][0].tileType = "destroyed"
                            displayBoard(window, gameBoard)
                            window.refresh()
                            sleep(.1)
                        sg.popup("The sticky time bomb went off!",keep_on_top=True)
                        #validLocations.clear()
                                
def itemOrbForecast(window):
    #print each member of the orb list (used for balancing)
    for iIndex, i in enumerate(PublicStats.orbCycleList):
        window[f"Orb{iIndex}"].update(i,text_color = "grey30",font = "Cambria 20")
        
    
    index = (PublicStats.turnCount+1)%len(PublicStats.orbCycleList)
    
    if index >= len(PublicStats.orbCycleList):
        index = 0
    window[f"Orb{index}"].update(f"{PublicStats.orbCycleList[index]}",text_color = ("orange"), font = "Cambria 30")

        
def begin(screenSize):

    # variables
    columns = 10
    rows = 10
    gameBoard = []
    
    #safety measure in case the screensize wasn't saved properly
    if screenSize not in ("normal","small"):
        screenSize = PublicStats.screenSize
        if screenSize not in ("normal","small"):
            screenSize = "normal"

    workingDirectoryName = os.getcwd()
    #print(f"{workingDirectoryName}\images\\")
    if screenSize == "normal":
        buttonSize = (75,75)
        if os.path.exists(f"{workingDirectoryName}\images"):
            shutil.rmtree(f"{workingDirectoryName}\images")
            
        shutil.copytree(workingDirectoryName+"\imagesNormal", workingDirectoryName+"\images")
    else:
        buttonSize = (40,40)
        sg.popup("Note that this mode is a backup mode designed for rarer laptops that don't have normal 1900x1080 resolutions. Enough development time does not exist for focused changes to this mode, so things may look weird.  I recommend you get a normal sized monitor in order to enjoy the game properly.",keep_on_top = True)
        if os.path.exists(f"{workingDirectoryName}\images"):
            shutil.rmtree(f"{workingDirectoryName}\images")
        shutil.copytree(workingDirectoryName+"\imagesSmall", workingDirectoryName+"\images")

    PublicPNGList.clear()
    publicPNGloader()
    
    # window 
    frame_main = [
        [
            #individual squares
            sg.Button(
                image_filename="images/default.png",
                #image_size = buttonSize,
                key=(i, j),
                size= buttonSize,
                button_color=("white", "grey"),
                tooltip="square",
                #pad=(2, 2),
                pad = (1,1),
                
            )
            for j in range(columns)
        ]
        for i in range(0, rows)
    ]

    frame_itemInfo = [
        #[sg.Button("Toggle Item Guide (Disabled until a future update)", size = (50,10), disabled = True)]

        [sg.Button("Read Items", size = (50,10))]

    ]

    frame_elevation = [
            [sg.Image(filename = "images\elevation.png", tooltip = "Each shade represents the height of a given tile.  A piece can jump down safely from any height to any tile that is lower than it.\nHowever, it cannot climb a tile that is more than one elevation unit taller.")]

        ]
    frame_turnsPassed = [
        [sg.T(f"{1:3}",font = "Cambria, 30",text_color = "Black",key = 'turnspassed',size = (3,1))]
        ]

    frame_itemOrbForecast =[
        [sg.T(f"123:>3",key = f"Orb{i}",size = (4,1),pad = (0,0),font = "Cambria, 30", )for i in range(0,len(PublicStats.orbCycleList))]
    ]
    
    frame_remaining = [
        [
            sg.T(
                f"Player 1 Controls: xx",
                key="player1piececount",
                font="Cambria 20",
                text_color="blue",
            )
        ],
        [
            sg.T(
                f"Player 2 Controls: xx",
                key="player2piececount",
                font="Cambria 20",
                text_color="red",
            )
        ],
    ]

    #top_right_frame = [[ sg.T("Text", size = (45,22),key = "itemsCollection", font = "Cambria 14")] ]
    top_right_frame = [  [ sg.Button("",key = f"itemList{i}{j}",disabled = True, size = (15,1)) for i in range(0,3)]for j in range(0,15)  ]
    #lookhere
    top_inner_frame = [
        [sg.Image("images/down.png", key="turn", visible=True)],
        [
            sg.T(f"Player:", font="Cambria 30", pad=(4, 4)),
            sg.T(f"", key="playerTurn", font="Cambria 30", pad=(4, 4)),
        ],
        [sg.T(f" " * 50, key="information", size=(25, 3), font="Cambria 30")],

        ]
    
    #item info is in this frame
    frame_layout = [
        [sg.Frame("Main stats", top_inner_frame), sg.Frame("Items Held By Your Pieces", top_right_frame)],
        [sg.Frame("Elevation Info",frame_elevation), sg.Frame("Item Info",frame_itemInfo), sg.Frame("Pieces Remaining", frame_remaining) ],
        [sg.Frame("Current Turn", frame_turnsPassed), sg.Frame("Item Orb Forecast (expected number of orbs that will spawn after your turn ends):",frame_itemOrbForecast, title_color = "Silver",font = "Cambria, 15")],
        [
            sg.Output(
                size=(70, 10),
                background_color="silver",
                font="Cambria 18",
                text_color="black",
            )
        ],
        
    ]

    
        

    layout = [
        [
            sg.T("MegaCheckers", font="Cambria 50"),
            #sg.Button(
            #    "USE ITEMS", key="itemButton", image_filename="images/backpack.png"
            #),
            sg.Button(
                "Look",
                button_color=("Blue", "White"),
                tooltip="Examine",
                font="Cambria 20",
                key="examineItem",
                image_filename="images/examine.png",
            ),
            #sg.Button("Learn about items",key="readItems",size=(40,4)),
            sg.Button("Exit", size=(20,4), key="exit"),
            sg.Button("cheetz")
        ]
    ]
    layout += [
        [
            sg.Frame("Playing Field", frame_main),
            sg.Frame(
                "Information:", frame_layout, font="Calibri 20", title_color="blue"
            ),
        ],
    ]
    #no_titlebar=True,
    window = sg.Window(
        "MegaCheckers",
        layout,
        no_titlebar=True,
        keep_on_top = True,
        disable_close=False,
        finalize = True,
        location=(0, 0),
        
    )
    
    
    #grab_anywhere=True,
    
    window.maximize()
    
    # gameBoard for logic
    gameBoard = []
    line = []
    for i in range(columns):
        line.append([Tile(), 0])
        gameBoard.append(0)

    for j in range(rows):
        gameBoard[j] = copy.deepcopy(line)

    
    initializeField(columns, rows, window, gameBoard)
    
    resetMoveAgain(gameBoard)


    


    
    #Between turns
    playerTurn = 1


        
    

        
        
    while True:

        updateToolTips(window, gameBoard,playerTurn)
        itemOrbForecast(window)
        
        if PublicStats.playerAutoWin != 0:
            if PublicStats.playerAutoWinTurn == PublicStats.turnCount:
                sg.popup(f"Congrats to player {playerAutoWin}.  Your AutoWin item has allowed you to automatically win.  Enjoy your empty, undeserved victory.")
        gamePlay(playerTurn, window, gameBoard)
        x = -1
        y = -1
        # end player one's turn, begin player two's turn, switch players
        if playerTurn == 1:
            
            window["turn"].update(filename="images/up.png")
            window['turnspassed'].update(f"{PublicStats.turnCount:>3}")
            itemOrbForecast(window)
            #check for recalled pieces
            if PublicStats.recallCount > 0:
                recallFunction(window,gameBoard)

            #check for sticky bombs
            stickyTimeBomb(window,gameBoard)
            AIbomb(window,gameBoard)
                
            for i in gameBoard:
                x += 1
                for j in i:
                    y += 1
                    if j[0].occupied == True:
                        if j[1].ownedBy == 1:
                            if "stunned" in j[1].activeDebuffs:
                                j[1].activeDebuffs.remove("stunned")
                                if j[0].tileType == "itemOrb":
                                    sg.popup(
                                        "A stunned piece recovered and picked up the item orb it had landed on",
                                        keep_on_top=True,
                                    )
                                    playsound("sounds/getItem.wav",block=False)
                                    pickUpItemOrb(gameBoard, x, y, window = window)
                y = -1
            playerTurn = 2



            updateToolTips(window, gameBoard,playerTurn)

            #End player 1's turn
            
            if PublicStats.spookyHand == True:
                spookyHand(window,gameBoard)

            orbsEaten = orbEater(gameBoard)    
            resetMoveAgain(gameBoard)
            laserSoundCheck = True
            laserCheck(window, gameBoard, laserSoundCheck = True)
            laserSoundCheck = False
            if orbsEaten > 0:
                pm(window, f"Orbs eaten by the orb eaters: {orbsEaten}")
                fileNum = random.randint(1,4)
                playsound(f"sounds/squeak{fileNum}.mp3", block = False)
            berzerkFunction(window, gameBoard, playerTurn)



            
        # end player two's turn, begin player one's turn
        else:
            window["turn"].update(filename="images/down.png")
            window['turnspassed'].update(f"{PublicStats.turnCount:>3}")
            itemOrbForecast(window)
            
            if PublicStats.playerAutoWin != 0:
                    if PublicStats.playerAutoWinTurn == PublicStats.turnCount:
                        sg.popup(f"Congrats to player {playerAutoWin}.  Your AutoWin item has allowed you to automatically win.  Enjoy your empty, undeserved victory.")
                
            #check for recalled pieces
            if PublicStats.recallCount > 0:
                recallFunction(window,gameBoard)

            #check for sticky time bomb
            stickyTimeBomb(window,gameBoard)
            AIbomb(window,gameBoard)
            
            for i in gameBoard:
                x += 1
                for j in i:
                    y += 1
                    if j[0].occupied == True:
                        if j[1].ownedBy == 2:
                            if "stunned" in j[1].activeDebuffs:
                                j[1].activeDebuffs.remove("stunned")
                                if j[0].tileType == "itemOrb":
                                    sg.popup(
                                        "A stunned piece recovered and picked up the item orb it had landed on",
                                        keep_on_top=True,
                                    )
                                    playsound("sounds/getItem.wav",block=False)
                                    pickUpItemOrb(gameBoard, x, y, window = window)
                y = -1
            playerTurn = 1

            
            
            if PublicStats.spookyHand == True:
                spookyHand(window,gameBoard)
            orbsEaten = orbEater(gameBoard)
            laserSoundCheck = True
            laserCheck(window, gameBoard, laserSoundCheck = True)
            laserSoundCheck = False
            resetMoveAgain(gameBoard)
            if orbsEaten > 0:
                pm(window, f"Orbs eaten by the orb eaters: {orbsEaten}")
                fileNum = random.randint(1,4)
                playsound(f"sounds/squeak{fileNum}.mp3", block = False)
            berzerkFunction(window, gameBoard, playerTurn)


def tutorial():
    frame_1 = [
        [sg.Button("Object of the game", key = "object") ],
        [sg.Button("Selecting a piece/How to move", key = "selection")],
        [sg.Button("Attacking enemies", key = "attacking")],
        [sg.Button("Picking up items", key = "pickUpItem")],
        [sg.Button("Use an item", key = "useItems")],
        [sg.Button("Read about items", key = "readItems")],
        [sg.Button("Exit", key = "Exit")]
    ]

    frame_2 =[
        [ sg.Image("gifs/jumpkill.gif",key="animatedImage", size = (300,300)), sg.Text(size = (100,20), key = "explanationText") ]
    ]
    
    layout = [[sg.T("MegaCheckers", font="Cambria 50", key="title")]]
    layout += [ [sg.Frame("Options", frame_1 )]]
    layout2 = [[sg.Frame("Video", frame_2)]]
    window1 = sg.Window("How to play", layout)
    window2 = sg.Window("Image", layout2)
    window2.finalize()
    
    window2.Hide()
    window1.finalize()
    window1.maximize()
    while True:
        event = window1.read()
        if event[0] in ( (None,None),None, sg.WIN_CLOSED, "Exit"):
            window1.close()
            main()
        if event[0] == "selection":
            window2.maximize()
            window2.UnHide()
            #window1.Hide()
            
            while True:
                event = window2.read(timeout = 50)
                
                if event in ( (None,None),None, sg.WIN_CLOSED):
                    window1.UnHide()
                    
                    break
                window2['animatedImage'].update_animation_no_buffering("gifs/movement.gif", 100)
                window2['explanationText'].update("Selecting a piece: simply click your piece to select it.  Left click where you want it to go.  You can normally move up/down/left/right, as shown by the highlighted paths.  You cannot move your own piece on top of your own piece.",font="Cambria 20")
        #window1['animatedImage'].update_animation_no_buffering("gifs/jumpkill.gif", 50)
        if event[0] == "attacking":
            window2.maximize()
            window2.UnHide()
            #window1.Hide()
            
            while True:
                event = window2.read(timeout = 50)
                
                if event in ( (None,None),None, sg.WIN_CLOSED):
                    window1.UnHide()
                    
                    break
                window2['animatedImage'].update_animation_no_buffering("gifs/jumpkill.gif", 100)
                window2['explanationText'].update("Attacking: simply click your piece and move it onto an enemy to do what we call a 'jump kill'.  You cannot jump kill your own pieces (except for when you use certain items).  Note that pieces that are in attack range turn red when you select a piece.", font = "Cambria 20")
        if event[0] == "pickUpItem":
            window2.maximize()
            window2.UnHide()
            #window1.Hide()
            
            while True:
                event = window2.read(timeout = 50)
                
                if event in ( (None,None),None, sg.WIN_CLOSED):
                    window1.UnHide()
                    
                    break
                window2['animatedImage'].update_animation_no_buffering("gifs/itemPickup.gif", 100)
                window2['explanationText'].update("Picking up items: simply step onto an item orb (the blue orb with the ???) to pick it up.  You will get a random item, whose name will be shown upon pickup.  You may hover over the picture to see what the item does.  Note that your piece grows dark and grows bigger when it's holding an item.", font = "Cambria 20")
##    # variables
##    columns = 10
##    rows = 10
##    gameBoard = []
##
##    frame_1 = [
##        [sg.Button("Object of the game", key="object")],
##        [sg.Button("How to select a piece", key="select")],
##        [sg.Button("How to move", key="move")],
##        [sg.Button("Items", key="items")],
##        #[sg.Button("Getting info on pieces", key="info")],
##        [sg.Button("EXIT", key="EXIT")],
##        
##    ]
##    frame_2 = [
##        [
##            sg.Button(
##                image_filename="images/default.png",
##                key=(i, j),
##                size=(20, 20),
##                tooltip="tooltip",
##                #pad=(10, 10),
##            )
##            for j in range(columns)
##        ]
##        for i in range(0, rows)
##    ]
##    frame_3 = [[sg.T(" " * 100, key="tutorialInfo", font="Cambria 13", size=(50, 10))]]
##    frame_4 = [[sg.T(" " * 100, key="information", font="Cambria 13", size=(88, 20))]]
##
##    layout = [
##        [
##            sg.T("MegaCheckers", font="Cambria 50", key="title"),
##            #sg.Button("use item", image_filename="images/backpack.png", visible=False),
##        ],
##    ]
##    layout += [
##        [
##            sg.Frame("Main screen", frame_1, key="options", visible=True),
##            sg.Frame("Game Play", frame_2, key="gamePlay", visible=True),
##            sg.Frame("Tutorial Info", frame_3)
##            
##        ],
##        [ sg.Frame("Information", frame_4)]
##        
##    ]
##    #layout += [[sg.Frame("Tutorial Info", frame_3), sg.Frame("Information", frame_4)]]
##
##    # gameBoard for logic
##    gameBoard = []
##    line = []
##    for i in range(columns):
##        line.append([Tile(), 0])
##        gameBoard.append(0)
##
##    for j in range(rows):
##        gameBoard[j] = copy.deepcopy(line)
##
##    window = sg.Window("MegaCheckers", layout, location=(0, 0)).finalize()
##    window.maximize()
##
##    initializeField(columns, rows, window, gameBoard)
##
##    window["options"].update(visible=True)
##
##    while True:
##        event = window.read()
##        if event[0] == "EXIT":
##            # QUIT
##            window.close()
##            main()
##            raise SystemExit
##        if event[0] == "object":
##            window["gamePlay"].update(visible=True)
##            myText = """OBJECT: The object of the game is to destroy all of your opponent's pieces or make it impossible for them to take a turn.  Your main method to do this will be by jumping on enemy pieces to kill them (don't worry, the pieces aren't sentient, so no one is getting hurt).  You will also be able to employ items that you find on the field to either protect yourself from your enemies or to blow them up someway or another.  Pick another topic from the menu on the left."""
##            window["tutorialInfo"].update(myText)
##
##        elif event[0] == "select":
##            window["gamePlay"].update(visible=True)
##            while True:
##                myText = """SELECTING A PIECE: to select your piece, simply left click on it.  Try it now!  Left click a blue piece."""
##                window["tutorialInfo"].update(myText)
##                displayBoard(window, gameBoard)
##
##                event = window.read()
##
##                if event[0] in ["object", "select", "move", "items", "info", "cancel"]:
##                    sg.popup("Restarting tutorial", keep_on_top=True)
##                    window.close()
##                    tutorial()
##                if event[0] == "EXIT":
##                    sg.popup("Exiting to main screen.", keep_on_top=True)
##                    window.close()
##                    main()
##
##                x = int(event[0][0])
##                y = int(event[0][1])
##                if (
##                    gameBoard[event[0][0]][event[0][1]][1] != 0
##                    and gameBoard[x][y][1].ownedBy == 1
##                ):
##                    myText = "Great job!  You've selected a piece.  Move onto a different topic."
##                    window["tutorialInfo"].update(myText)
##                    break
##                else:
##                    myText = "Sorry, that's not right.  Left click on a blue piece."
##                    window["tutorialInfo"].update(myText, text_color="red")
##                    window.refresh()
##                    sleep(1)
##                    window["tutorialInfo"].update(myText, text_color="white")
##
##        elif event[0] == "move":
##            window["gamePlay"].update(visible=True)
##            outOfRangeTutorialIncomplete = True
##            while True:
##
##                while True:
##                    notValidSelection = True
##                    myText = """MOVING: normally you can move once per turn, and can only move one piece per turn.  Unless they have specific items, pieces can only move one space forward/back/sideways.  Let's try moving a piece now!  Start by selecting a blue piece on the second row from the top."""
##                    window["tutorialInfo"].update(myText)
##                    displayBoard(window, gameBoard)
##                    while notValidSelection:
##                        event = window.read()
##
##                        if event[0][0] == 1:
##                            validSelection = False
##                            myText = (
##                                "Good work!  Now we can continue on to the next step."
##                            )
##                            rowOrig = event[0][0]
##                            colOrig = event[0][1]
##                            window["tutorialInfo"].update(myText)
##                            window.refresh()
##                            sleep(1.5)
##                            break
##                        else:
##                            myText = "That's not correct.  You'll have to select a blue piece on the second row before we can continue."
##                            window["tutorialInfo"].update(myText, text_color="red")
##                            window.refresh()
##                            sleep(1)
##                            window["tutorialInfo"].update(myText, text_color="white")
##
##                    window["information"].update(
##                        f"Piece selected!  Choose a destination tile within range."
##                    )
##                    window.refresh
##                    if outOfRangeTutorialIncomplete == True:
##                        myText = """Now that we have clicked on one of your pieces, we can move it.  Notice that the information window lets you know that your piece was selected.  It's asking you to choose a location within range.  HOWEVER - try clicking on any empty space EXCEPT the one that's right in front of your selected piece."""
##                    else:
##                        myText = """Now that you know what it looks like when you try to move to an invalid space, let's do a valid space.  Choose the spot right in front of your selected piece."""
##
##                    window["tutorialInfo"].update(myText)
##                    window.refresh()
##                    event = window.read()
##
##                    if (
##                        (event[0][0] < 2)
##                        or (event[0][0]) > (rows - 2)
##                        and outOfRangeTutorialIncomplete == True
##                    ):
##                        myText = """That's not right.  For this tutorial, we need you to click on an empty space.  You clicked on a space that's occupied.  No worries, let's start over."""
##                        window["tutorialInfo"].update(myText, text_color="red")
##                        sleep(2)
##                        window["tutorialInfo"].update(myText, text_color="white")
##                        break
##                    if (
##                        (event[0][0] == rowOrig + 1)
##                        and (event[0][1] == colOrig)
##                        and outOfRangeTutorialIncomplete == True
##                    ):
##                        myText = """You're getting ahead of yourself.  Normally this would be the right move, but trust me...  Just do what the tutorial says and pick any empty spot except for this one."""
##                        window["tutorialInfo"].update(myText, text_color="red")
##                        window["information"].update("")
##                        window.refresh()
##                        sleep(4)
##                        window["tutorialInfo"].update(myText, text_color="white")
##                        continue
##                    if (
##                        outOfRangeTutorialIncomplete == False
##                        and event[0][0] == rowOrig + 1
##                        and event[0][1] == colOrig
##                    ):
##                        myText = "Good job!  You've successfully moved a piece!  If you move onto a enemy in this way, you kill it!  Click on the items tutorial next!"
##
##                        window["tutorialInfo"].update(myText, text_color="white")
##                        playerBackup = gameBoard[rowOrig][colOrig][1]
##                        gameBoard[rowOrig][colOrig][1] = 0
##                        gameBoard[event[0][0]][event[0][1]][1] = playerBackup
##
##                        gameBoard[rowOrig][colOrig][0].occupied = False
##                        gameBoard[rowOrig][colOrig][0].tileType = "default"
##                        gameBoard[rowOrig + 1][colOrig][0].occupied = True
##                        displayBoard(window, gameBoard)
##                        window.refresh()
##                        window.read()
##                        window.close()
##                        tutorial()
##                    else:
##                        if outOfRangeTutorialIncomplete == True:
##                            window["information"].update(
##                                f"That location is too far for you to move to!"
##                            )
##                            myText = (
##                                "Good work!  Notice the error message in the information box.  During normal gameplay, you can keep an eye out on it to see what you can do.  Alright, now that you know what happens if you try to move out of range, let's try doing an actual move.  Choose a blue piece and then move it one square forward."
##                                ""
##                            )
##                            window["tutorialInfo"].update(myText, text_color="white")
##                            window.refresh()
##                            sleep(4)
##                            window["information"].update("")
##                            outOfRangeTutorialIncomplete = False
##                            window.refresh
##                            sleep(2)
##                            break
##                        else:
##                            myText = """That's not a valid choice.  Let's try again."""
##                            window["tutorialInfo"].update(myText, text_color="white")
##                            window.refresh()
##                            sleep(1)
##
##        elif event[0] == "items":
##            myText = "This part of the tutorial assumes you've mastered selecting your pieces and moving around.  If you're still not familiar with that, please practice that some more before doing this next part.  Please grab the power tile in the middle: do this by selecting your blue tile that's next to it."
##            window["gamePlay"].update(visible=True)
##            window["tutorialInfo"].update(myText)
##            gameBoard[2][4][0].tileType = "itemOrb"
##            displayBoard(window, gameBoard)
##
##            # click the thingy
##            while True:
##                event = window.read()
##                if event[0] != (1, 4):
##                    myText = "You have to select the piece that's right next to the item orb tile"
##                    window["tutorialInfo"].update(myText)
##                    window.refresh()
##                    continue
##                else:
##
##                    while True:
##                        myText = "Now that you've selected your piece, we need to click on the item orb to have your piece grab it."
##                        window["tutorialInfo"].update(myText)
##                        event = window.read()
##                        if event[0] != (2, 4):
##                            myText = "That's not right.  You have to move your piece onto the item orb to grab it.  Let's try again."
##                            window["tutorialInfo"].update(myText)
##                            window.refresh()
##                            sleep(1)
##                            continue
##                        else:
##                            myText = "Cool, your piece now holds a powerup!  Notice how it looks different compared to the others.  Let's try it out!  Normally you have to take turns, but we'll just cheat - I've disabled red from having any turns."
##                            window["tutorialInfo"].update(myText)
##                            rowOrig = 1
##                            colOrig = 4
##                            playerBackup = gameBoard[rowOrig][colOrig][1]
##                            gameBoard[rowOrig][colOrig][1] = 0
##                            gameBoard[event[0][0]][event[0][1]][1] = playerBackup
##                            gameBoard[rowOrig][colOrig][0].occupied = False
##                            gameBoard[rowOrig][colOrig][0].tileType = "default"
##                            gameBoard[rowOrig + 1][colOrig][0].occupied = True
##                            gameBoard[rowOrig + 1][colOrig][1].storedItems.append(
##                                "Energy Forcefield"
##                            )
##                            gameBoard[rowOrig + 1][colOrig][1].determineAvatar()
##
##                            displayBoard(window, gameBoard)
##                            window.refresh()
##
##                            sleep(1)
##                            while True:
##                                myText = "Alright, click on the powered up piece"
##
##                                event = window.read()
##                                window["tutorialInfo"].update(myText)
##                                if event[0] != (2, 4):
##                                    sg.popup(
##                                        "Click on the piece that you just moved",
##                                        keep_on_top=True,
##                                    )
##                                    continue
##                                else:
##                                    #window["use item"].update(visible=True)
##                                    myText = "Click on the same piece twice to see the item menu."
##
##                                    event = window.read()
##                                    window["tutorialInfo"].update(myText)
##
##                                    if event[0] == (2, 4):
##                                        myText = "Click on the same piece again to see the item menu."
##                                        explodeLayout = [
##                                            [
##                                                sg.Button(
##                                                    "Cheater's Instawin Item of Instant Winning"
##                                                )
##                                            ]
##                                        ]
##                                        x = sg.Window("Items", explodeLayout)
##
##                                        event = x.read()
##                                        window["tutorialInfo"].update(myText)
##
##                                        if (
##                                            event[0]
##                                            == "Cheater's Instawin Item of Instant Winning"
##                                        ):
##                                            x.close()
##                                            myText = "Congrats, you cheater.  This weapon (which only exists in this tutorial mode) will instantly destroy any enemy pieces on the field.  You now know pretty much everything you need to know to win.  Go out there and start playing with a friend."
##
##                                            window["tutorialInfo"].update(myText)
##                                            window.refresh()
##                                            sleep(1)
##
##                                            for i in range(2):
##                                                for j in range(columns):
##                                                    window[rows - i - 1, j].update(
##                                                        image_filename="images/exploding.png"
##                                                    )
##                                            window.refresh()
##                                            sleep(1)
##
##                                            for i in range(2):
##                                                for j in range(columns):
##                                                    window[rows - i - 1, j].update(
##                                                        image_filename="images/destroyed.png"
##                                                    )
##                                            window.refresh()
##                                            sleep(1)
##
##                                            for i in range(2):
##                                                for j in range(columns):
##                                                    window[rows - i - 1, j].update(
##                                                        image_filename="images/exploding.png"
##                                                    )
##                                            window.refresh()
##                                            sleep(1)
##
##                                            for i in range(2):
##                                                for j in range(columns):
##                                                    window[rows - i - 1, j].update(
##                                                        image_filename="images/default.png"
##                                                    )
##                                            window.refresh()
##                                            sleep(5)
##                                        sg.popup(
##                                            "Restarting the tutorial", keep_on_top=True
##                                        )
##                                        window.close()
##                                        tutorial()
##
##                                    else:
##                                        sg.popup("Nope, try again", keep_on_top=True)
##                                        continue
##
##        else:
##            myText = "Invalid choice.  There are no tutorials in progress. Try clicking something on the menu on the left."
##            window["tutorialInfo"].update(myText)

def popupItemExplanation():
    itemsList = pickUpItemOrb(getItemsList = True)
        
    text = "THIS IS A TEMPORARY SOLUTION TO SHOWING ALL THE ITEMS.  IT'LL BE REPLACED BY SOMETHING PRETTIER... EVENTUALLY.\n\n\n"
    for i in itemsList:
        explanation = itemExplanation(i)
        text+= f"{i}: {explanation}"
        text+="\n\n\n"
    sg.PopupScrolled(text)
    

def main():
    workingDirectoryName = os.getcwd()
    if os.path.exists(f"{workingDirectoryName}\images"):
        shutil.rmtree(f"{workingDirectoryName}\images")
    shutil.copytree(workingDirectoryName+"\imagesNormal", workingDirectoryName+"\images")

    publicPNGloader()
    introLayout = [[sg.Text("Mega\nCheckers", font="Cambria 100", justification = "center")]]
    frame_1 = [
        [sg.Button("Begin game (normal size)", button_color = ("black","green"),key="beginNormal", size = (20,5))],
        [sg.Button("Begin game (small size)", button_color = ("black","green"),key="beginSmall", size = (20,5))],
        [sg.Button("How to play", key="tutorial", size = (20,2))],
        #[sg.Button("Read about items", size = (20,2))]
    ]
    frame_2 = [
        #name of item
        [sg.T(f"",key="itemName",text_color = "blue",font = "Cambria, 40",size = (20,1))],
        #address of item picture
        [sg.Image("",size=(400,400),key="itemPic"),],
        [sg.T(f"(No description)",key = "itemDescription",size = (100,7),font = "Cambria 20")]
        ]
    introLayout += [[sg.Frame("Choose an option", frame_1, key="options"),sg.Frame("Items Spotlight:",frame_2,key="itemBlurb", element_justification = "center")]]
    introWindow = sg.Window("MegaCheckers", introLayout, element_justification = "center").finalize()
    #introWindow.disappear()
    introWindow.Maximize()
    while True:
        
            itemName = pickUpItemOrb(introOnly = True)
            
            introWindow["itemPic"].update(filename = f"images/{itemName}.png")
            
            introWindow["itemName"].update(itemName)
            
            description = itemExplanation(itemName)
            
            introWindow["itemDescription"].update(description)
            #introWindow.reappear()
            
            
            break
        
            sg.popup("Error in introwindow")
            continue
    event = introWindow.read()
    if event[0] == "tutorial":
        introWindow.close()
        tutorial()
    if event[0] == "beginNormal":
        PublicStats.screenSize = "normal"
        introWindow.close()
        begin("normal")
    if event[0] == "beginSmall":
        PublicStats.screenSize = "small"
        introWindow.close()
        begin("small")
    if event[0] in (None, sg.WIN_CLOSED):
        quit()






main()
