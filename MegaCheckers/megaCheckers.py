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
from movePieceMegaCheckers import*


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

# the actual loop that is used to progress turns
def gamePlay(playerTurn, window, gameBoard):

    
    countPieces(gameBoard, window, PublicStats)
    createOrbs(window, gameBoard)
    movePiece(playerTurn, window, gameBoard)
    PublicStats.turnCount += 1
    repairFloor(window, gameBoard)

            
    
# generate item orbs
def createOrbs(window, gameBoard):
    #dangerturn = the turn when item orbs might spawn as trap orbs instead
    DANGERTURN = 40
    emptySpots = 0
    if PublicStats.turnCount == DANGERTURN:
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
            return
        
        i = random.randint(0, len(gameBoard) - 1)
        j = random.randint(0, len(gameBoard[0]) - 1)
        if gameBoard[i][j][0].tileType == "default" and gameBoard[i][j][0].occupied != True and gameBoard[i][j][0].orbEater == False and gameBoard[i][j][0].wormHole1 == False and gameBoard[i][j][0].wormHole2 == False:
            orbsToPlace -= 1
            if PublicStats.turnCount > DANGERTURN:
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
