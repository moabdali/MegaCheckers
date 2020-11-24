import random
import string
from time import sleep
from betweenTurnFunctionsMegaCheckers import *



def playSoundExceptionCatcher(fileName, block = True):
    try:
        playsound(fileName, block)
    except:
        print(".")


        

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
    




def resetBowlMovement(gameBoard):
    for rows in gameBoard:
        for columns in rows:
            if columns[0].occupied:
                columns[1].bowlMotion = False

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

    # set bowling ball to have movement animation (rolls around)
    gameBoard[sLocRow][sLocCol][1].bowlMotion = True
    
    if direction == "Down":
        for eachRow in gameBoard:

            
            
                #if the next spot is legal
                if curRow+1 < rows:

                    
                    # if there are no pieces on the next row
                    if gameBoard[curRow+1][curCol][0].occupied == False:

                        
                        #if the floor exists in the next row
                        if gameBoard[curRow+1][curCol][0].tileType not in (PublicStats.damagedFloor):

                            
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
                                playSoundExceptionCatcher("sounds/grenade.mp3", block = False)

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
                            playSoundExceptionCatcher("sounds/fall.mp3", block = False)
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
                            resetBowlMovement(gameBoard)
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
                            #explode the enemy
                            j[0].tileType = "exploding"
                            displayBoard(window, gameBoard)
                            window.refresh()
                            playSoundExceptionCatcher("sounds/grenade.mp3", block = False)

                            #occupy it with the bowling ball
                            j[0].tileType = "default"
                            j[0].occupied = True
                            j[1] = copy.deepcopy(tempCopy[1])

                            displayBoard(window, gameBoard)
                            resetBowlMovement(gameBoard)
                            window.refresh()
                            curRow +=1
                            return
                        
                #else if out of bounds
                else:
                    

                    sg.popup("You slammed into the outer wall.",keep_on_top = True)
                    resetBowlMovement(gameBoard)
                    return
                    
    if direction == "Up":
        for eachRow in gameBoard:

            
            
                #if the next spot is legal
                if curRow-1 >-1:

                    
                    # if there are no pieces on the next row
                    if gameBoard[curRow-1][curCol][0].occupied == False:

                        
                        #if the floor exists in the next row
                        if gameBoard[curRow-1][curCol][0].tileType not in (PublicStats.damagedFloor):

                            
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
                                playSoundExceptionCatcher("sounds/grenade.mp3", block = False)

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
                            playSoundExceptionCatcher("sounds/fall.mp3", block = False)
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
                            resetBowlMovement(gameBoard)
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
                            
                            j[0].tileType = "exploding"
                            displayBoard(window, gameBoard)
                            window.refresh()
                            playSoundExceptionCatcher("sounds/grenade.mp3", block = False)

                            #occupy it with the bowling ball
                            j[0].tileType = "default"
                            j[0].occupied = True
                            j[1] = copy.deepcopy(tempCopy[1])

                       
                            #sleep(1)
                            displayBoard(window, gameBoard)
                            resetBowlMovement(gameBoard)
                            window.refresh()
                            curRow -=1
                            return
                #else if out of bounds
                else:
                    sg.popup("You slammed into the outer wall.",keep_on_top = True)
                    resetBowlMovement(gameBoard)
                    
                    return

    if direction == "Left":
        while True:
                #if the next spot is legal
                if curCol-1 > -1:

                    
                    # if there are no pieces on the next row
                    if gameBoard[curRow][curCol-1][0].occupied == False:

                        
                        #if the floor exists in the next row
                        if gameBoard[curRow][curCol-1][0].tileType not in (PublicStats.damagedFloor):

                            
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
                                playSoundExceptionCatcher("sounds/grenade.mp3", block = False)

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
                            playSoundExceptionCatcher("sounds/fall.mp3", block = False)
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
                            resetBowlMovement(gameBoard)
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
                            playSoundExceptionCatcher("sounds/grenade.mp3", block = False)

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
                    resetBowlMovement(gameBoard)
                    return
    if direction == "Right":
        while True:
                #if the next spot is legal
                if curCol+1 < columns:

                    
                    # if there are no pieces on the next row
                    if gameBoard[curRow][curCol+1][0].occupied == False:

                        
                        #if the floor exists in the next row
                        if gameBoard[curRow][curCol+1][0].tileType not in (PublicStats.damagedFloor):

                            
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
                                playSoundExceptionCatcher("sounds/grenade.mp3", block = False)

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
                            playSoundExceptionCatcher("sounds/fall.mp3", block = False)
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
                            resetBowlMovement(gameBoard)
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
                            playSoundExceptionCatcher("sounds/grenade.mp3", block = False)

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
                    resetBowlMovement(gameBoard)
                    return



def roundEarthTheoryFunction(gameBoard,startLocation,endLocation,columns,rows):
#trying to go from right side to left side
    #try to go straight right to straight left
    print("Using round earth theory!")
    if startLocation[0] == endLocation[0]:
        if startLocation[1] == columns-1 and endLocation[1] == 0:
            #sg.popup("Your piece rolled around to the other side!",keep_on_top = True)
            return True
    #trying to go down right
    elif startLocation[0] == endLocation[0]-1 and startLocation[1] == columns -1 and endLocation[1] == 0 and "move diagonal" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
        #sg.popup("Your piece rolled around to the other side!",keep_on_top = True)
        return True
    #trying to go up right
    elif startLocation[0] == endLocation[0]+1 and startLocation[1] == columns -1 and endLocation[1] == 0 and "move diagonal" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
        #sg.popup("Your piece rolled around to the other side!",keep_on_top = True)
        return True
    

#trying to go from left to right side
    #try to go straight left to straight right
    if startLocation[0] == endLocation[0]:
        if startLocation[1] == 0 and endLocation[1] == columns -1:
            #sg.popup("Your piece rolled around to the other side!",keep_on_top = True)
            return True
    #trying to go down right
    elif startLocation[0] == endLocation[0]-1 and startLocation[1] == 0  and endLocation[1] == columns -1 and "move diagonal" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
        #sg.popup("Your piece rolled around to the other side!",keep_on_top = True)
        return True
    #trying to go up right
    elif startLocation[0] == endLocation[0]+1 and startLocation[1] == 0 and endLocation[1] == columns -1 and "move diagonal" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
        #sg.popup("Your piece rolled around to the other side!",keep_on_top = True)
        return True

        
#trying to go from up to down
    #try to go straight up to straight down
    if startLocation[1] == endLocation[1]:
        if startLocation[0] == 0 and endLocation[0] == rows -1:
            #sg.popup("Your piece rolled around to the other side!",keep_on_top = True)
            return True
    #trying to go up right
    elif startLocation[0] == 0 and startLocation[1] == (endLocation[1] +1) and endLocation[0] == rows -1 and "move diagonal" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
        #sg.popup("Your piece rolled around to the other side!",keep_on_top = True)
        return True
    #trying to go up right
    elif startLocation[1] == endLocation[1]-1 and startLocation[0] == 0 and endLocation[0] == rows -1 and "move diagonal" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
        #sg.popup("Your piece rolled around to the other side!",keep_on_top = True)
        return True

#trying to go from down to up
    #try to go straight down to straight up
    if startLocation[1] == endLocation[1]:
        if startLocation[0] == rows-1 and endLocation[0] == 0:
            #sg.popup("Your piece rolled around to the other side!",keep_on_top = True)
            return True
    #trying to go up right
    elif endLocation[0] == 0 and endLocation[1] == (startLocation[1] +1) and startLocation[0] == rows -1 and "move diagonal" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
        #sg.popup("Your piece rolled around to the other side!",keep_on_top = True)
        return True
    #trying to go up right
    elif endLocation[1] == startLocation[1]-1 and endLocation[0] == 0 and startLocation[0] == rows -1 and "move diagonal" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
        #sg.popup("Your piece rolled around to the other side!",keep_on_top = True)
        return True
    
#diagonals (only works with diagonal enabled) REVIEW NOTE - this may be redundant...
    if "move diagonal" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
        #upleft
        if startLocation[0] == 0 and startLocation[1] == 0 and endLocation[0] == rows-1 and endLocation[1] == columns-1:
            #sg.popup("Your piece rolled around to the other side!",keep_on_top = True)
            return True
        #upright
        if startLocation[0] == 0 and startLocation[1] == columns-1 and endLocation[0] == rows-1 and endLocation[1] == 0:
            #sg.popup("Your piece rolled around to the other side!",keep_on_top = True)
            return True
        #downleft
        if startLocation[0] == rows-1 and startLocation[1] == 0 and endLocation[0] == 0 and endLocation[1] == columns-1:
            #sg.popup("Your piece rolled around to the other side!",keep_on_top = True)
            return True
        #downright
        if startLocation[0] == rows-1 and startLocation[1] == columns-1 and endLocation[0] == 0 and endLocation[1] == 0:
            #sg.popup("Your piece rolled around to the other side!",keep_on_top = True)
            return True
    else:
        return False    



def jumpoline(window, gameBoard, location, playerTurn):
    validLocations = emptySpots(gameBoard, trueEmpty = True)
    if len(validLocations) == 0:
        sg.popup("Nowhere valid for you to jumpoline to. :(",keep_on_top=True)
        return
    choice = random.choice(validLocations)
    x=choice[0]
    y=choice[1]
    return x,y


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
        window["Surrender"].update(disabled=False)
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
                items = sg.popup_get_text("Cheaters never prosper.  Except when they do.",title = "cheetz",keep_on_top = True,font="Cambria, 20")
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
            #if surrender is clicked
            if "Surrender" in event:
                sleep(2)
                a = sg.popup_yes_no(
                    "You wanna give up?", keep_on_top=True, font = "Cambria 20"
                )
                pm(window, "Giving up?")
                if a == "Yes":
                    sg.popup("Coward.  You've lost.", keep_on_top=True, font = "Cambria 20")
                    #window.close()
                    return "give up"
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
                        frame1Layout+= [[sg.Button(i, size = (30,10),image_size=(300, 100),key = f"{i}",image_filename = f"images/{i}.png",font="Arial 20",button_color=("pink", "grey"))]]
                    elif iIndex in range (8,16):
                        frame2Layout+= [[sg.Button(i, size = (30,10),image_size=(300, 100),key = f"{i}",image_filename = f"images/{i}.png",font="Arial 20",button_color=("pink", "grey"))]]
                    elif iIndex in range (16,24):
                        frame3Layout+= [[sg.Button(i, size = (30,10),image_size=(300, 100),key = f"{i}",image_filename = f"images/{i}.png",font="Arial 20",button_color=("pink", "grey"))]]
                    elif iIndex in range (24,32):
                        frame4Layout+= [[sg.Button(i, size = (30,10),image_size=(300, 100),key = f"{i}",image_filename = f"images/{i}.png",font="Arial 20",button_color=("pink", "grey"))]]
                    elif iIndex in range (32,40):
                        frame5Layout+= [[sg.Button(i, size = (30,10),image_size=(300, 100),key = f"{i}",image_filename = f"images/{i}.png",font="Arial 20",button_color=("pink", "grey"))]]
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
                        frame6Layout+= [[sg.Button(i, size = (30,10),image_size=(300, 100),key = f"{i}",image_filename = f"images/{i}.png",font="Arial 20",button_color=("pink", "grey"))]]
                    elif iIndex in range (48,56):
                        frame7Layout+= [[sg.Button(i, size = (30,10),image_size=(300, 100),key = f"{i}",image_filename = f"images/{i}.png",font="Arial 20",button_color=("pink", "grey"))]]
                    elif iIndex in range (56,64):
                        frame8Layout+= [[sg.Button(i, size = (30,10),image_size=(300, 100),key = f"{i}",image_filename = f"images/{i}.png",font="Arial 20",button_color=("pink", "grey"))]]
                    elif iIndex in range (64,72):
                        frame9Layout+= [[sg.Button(i, size = (30,10),image_size=(300, 100),key = f"{i}",image_filename = f"images/{i}.png",font="Arial 20",button_color=("pink", "grey"))]]
                    elif iIndex in range (72,80):
                        frame10Layout+= [[sg.Button(i, size = (30,10),image_size=(300, 100),key = f"{i}",image_filename = f"images/{i}.png",font="Arial 20",button_color=("pink", "grey"))]]
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
                        frame11Layout += [[sg.Button(i, size = (30,10),image_size=(300, 100),key = f"{i}",image_filename = f"images/{i}.png",font="Arial 20",button_color=("pink", "grey"))]]
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
                    if event[0] in ("Page 1", "keyA", "keyB", "keyC", "keyD", "keyE", "keyF", "keyG", "keyH", "keyI", "keyJ", "keyK", "keyL", "keyM", "keyN", "keyO") :
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
                    if event[0] in ("Page 2", "keyP","keyQ","keyR", "keyS", "keyT", "keyU","keyV"):
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
                            [ sg.Image(filename = f"images/{event[0]}.png")],
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
        window["Surrender"].update(disabled = True)

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
            sg.popup(f"An exception occurred because you hit an unexpected button: {event}.  Don't do that.  Recovering...",keep_on_top = True)
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
            playSoundExceptionCatcher("sounds/select.mp3",block = False)
            window.disable()
            bowlingMenu = sg.Window("Direction",bowlingLayout,keep_on_top=True)
            event = bowlingMenu.read()
            window.enable()
            bowlingMenu.close()

            #if you pick a direction, go to the function
            if event[0] in ("Up", "Down", "Left", "Right"):
                bowlingBallFunction(window,gameBoard,location,event[0])
                resetBowlMovement(gameBoard)
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
                playSoundExceptionCatcher("sounds/select.mp3",block=False)
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
            playSoundExceptionCatcher("sounds/select.mp3",block=False)
            gameBoard[startLocation[0]][startLocation[1]][1].grey = True
            gameBoard[startLocation[0]][startLocation[1]][1].currentTurnPiece = True
            

        #if the second turn didn't happen
        if repeatRestrictor[0] == False:
            #sg.popup(f"DEBUG: Assuming first turn, Event is {event}",keep_on_top = True)
            startLocation = event[0]
            playSoundExceptionCatcher("sounds/select.mp3",block=False)
            startLocationBackup = startLocation

        #if the second turn did happen
        elif repeatRestrictor[0] == True:
            playSoundExceptionCatcher("sounds/select.mp3",block=False)
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
            playSoundExceptionCatcher("sounds/wrong.mp3",block=False) 
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
                playSoundExceptionCatcher("sounds/wrong.mp3",block=False) 
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
                playSoundExceptionCatcher("sounds/select.mp3",block=False)
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
                playSoundExceptionCatcher("sounds/wrong.mp3",block=False) 
                window["information"].update(f"That's not your piece...")
                pm(window, f"That's not your piece...")
                window["information"].update(text_color="red")
                window.refresh()
                sleep(.3)
                continue
            
            # if the piece belongs to you but doesn't have items
            else:
                playSoundExceptionCatcher("sounds/select.mp3",block=False)
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
            playSoundExceptionCatcher("sounds/wrong.mp3",block=False) 
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
                playSoundExceptionCatcher("sounds/wrong.mp3",block=False) 
                sleep(.4)
                continue
            # shouldn't get to here
            else:
                pm(window, "An error occurred in item lookups")

                
        # if there isn't any piece on the square
        if gameBoard[startLocation[0]][startLocation[1]][0].occupied == False:
            if repeatRestrictor[0] == False:
                gameBoard[startLocation[0]][startLocation[1]][1].currentTurnPiece = False
            playSoundExceptionCatcher("sounds/wrong.mp3",block=False) 
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
            playSoundExceptionCatcher("sounds/wrong.mp3",block=False) 
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
                        playSoundExceptionCatcher("sounds/wrong.mp3",block=False) 
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
                    playSoundExceptionCatcher("sounds/wrong.mp3",block=False) 
                    sg.popup("The tile you're trying to get to is too high",keep_on_top = True)
                    pm(window,"The tile you're trying to get to is too high")
                    continue

                
                




                #####
                # if the landing spot is an item Orb:
                if gameBoard[endLocation[0]][endLocation[1]][0].tileType == "itemOrb":

                    playSoundExceptionCatcher("sounds/getItem.mp3",block=False)
                    pickUpItemOrb(gameBoard, startLocation[0], startLocation[1], window = window)
                    pm(window, "Picked up an item")
                    pickedUpItem = True
                 
                    
                # if the landing spot is missing or still damaged
                if gameBoard[endLocation[0]][endLocation[1]][0].tileType in [PublicStats.damagedFloor]:
                    playSoundExceptionCatcher("sounds/wrong.mp3",block=False) 
                    window["information"].update(f"Can't move here!  The floor is missing/damaged.")
                    pm(window, "Can't move here!  The floor is missing/damaged.")
                    sg.popup("Can't move here!  The floor is missing/damaged.", keep_on_top = True)
                    window.refresh()
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
                            playSoundExceptionCatcher("sounds/grenade.mp3", block = False)
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
                            playSoundExceptionCatcher("sounds/grenade.mp3", block = False)
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
##                            playSoundExceptionCatcher("sounds/grenade.mp3", block = False)
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
                            playSoundExceptionCatcher("sounds/grenade.mp3", block = False)
                            sg.popup("Burned to a crisp by the laser", keep_on_top=True)
                            gameBoard[endLocation[0]][endLocation[1]][
                                0
                            ].tileType = "mystery box"
                            break
                        
                        randomEvent = random.choice( ["getItems", "lose items", "die", "lose buffs", "lose debuffs"])
                        if randomEvent == "getItems":
                            #get three items
                            for i in range(1,4):
                                playSoundExceptionCatcher("sounds/getItem.mp3",block=False)
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
                            playSoundExceptionCatcher("sounds/grenade.mp3", block = False)
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
                            playSoundExceptionCatcher("sounds/grenade.mp3", block = False)
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
                            playSoundExceptionCatcher("sounds/grenade.mp3", block = False)
                            sg.popup("Trip mine went off!", keep_on_top=True)
                            gameBoard[endLocation[0]][endLocation[1]][
                                0
                            ].tileType = "default"
                            break
                    if gameBoard[endLocation[0]][endLocation[1]][0].orbEater == True:
                        sg.popup("You monster!  You killed an orb eater!",keep_on_top = True)
                        gameBoard[endLocation[0]][endLocation[1]][0].orbEater = False

                     

                    playSoundExceptionCatcher("sounds/thump.mp3",block=False)    
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
                    playSoundExceptionCatcher("sounds/wrong.mp3",block=False) 
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
                        playSoundExceptionCatcher("sounds/wrong.mp3",block=False) 
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
                            playSoundExceptionCatcher("sounds/vampire.mp3",block=False)
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
                            playSoundExceptionCatcher("sounds/grenade.mp3", block = False)
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
                            playSoundExceptionCatcher("sounds/grenade.mp3", block = False)
                            sg.popup("Trip mine went off!", keep_on_top=True)
                            gameBoard[endLocation[0]][endLocation[1]][
                                0
                            ].tileType = "default"
                            break
                    if "berzerk" in gameBoard[endLocation[0]][endLocation[1]][1].activeBuffs:
                        playSoundExceptionCatcher("sounds/destroy.mp3",block=False)
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
                        playSoundExceptionCatcher("sounds/destroy.mp3",block=False)
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
                playSoundExceptionCatcher("sounds/wrong.mp3",block=False) 
                window["information"].update(f"That's not your piece!")
                pm(window, "That's not your piece!")
                sleep(.3)
                window.refresh
                continue


