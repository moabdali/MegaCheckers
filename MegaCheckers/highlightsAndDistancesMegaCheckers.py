# imported by displayBoardMegaCheckers -> useItemsMegaCheckers -> megaCheckers
from publicObjectsMegaCheckers import *

# see if any pieces are sitting on death spots
def deathCheck(window, gameBoard, move=False):
    for i in gameBoard:
        for j in i:
            # if a regular mine or laser was stepped on
            if (j[0].occupied == True) and (j[0].tileType == "mine" or (j[0].vertLaser == True or j[0].horiLaser == True or j[0].crossLaser == True) ):
                death = forcefieldCheck(window, gameBoard, endLocation = j ,danger ="both")
                #if you didn't die, then start looking in a different direction
                if death == False:
                    break
                #sg.popup(f"FFT: {j[1].forceFieldTurn}", keep_on_top = True)
                if j[1].forceFieldTurn == PublicStats.turnCount:
                    j[0].tileType = "default"
                    #sg.popup("Forcefield saved you",keep_on_top=True)
                else:
                    owner = j[1].ownedBy
                    j[0].tileType = "exploding"
                    j[1] = 0
                    j[0].occupied = False
                    displayBoard(window, gameBoard)
                    
                    window.refresh()
                    playsound("sounds/grenade.mp3", block = False)
                    j[0].tileType = "default"
                    displayBoard(window, gameBoard)
                    window.refresh()
                    #sg.popup("A piece died!", keep_on_top=True)
                    sg.popup(f"A piece owned by player {owner} died to a hazard!", keep_on_top=True)
                    return "death"

            # if a trap belonging to your enemy was set
            elif j[0].occupied == True and (
                (j[0].tileType == "trap orb 1" and j[1].ownedBy != 1)
                or (j[0].tileType == "trap orb 2" and j[1].ownedBy != 2)
            ):
                death = forcefieldCheck(window, gameBoard, endLocation = j ,danger ="both")
                #if you didn't die, then start looking in a different direction
                if death == False:
                    break
                #sg.popup(f"FFT: {j[1].forceFieldTurn}", keep_on_top = True)
                if j[1].forceFieldTurn == PublicStats.turnCount:
                    j[0].tileType = "default"
                else:
                    j[0].tileType = "exploding"
                    j[1] = 0
                    j[0].occupied = False
                    displayBoard(window, gameBoard)
                    window.refresh()
                    playsound("sounds/grenade.mp3", block = False)
                    sleep(1)
                    j[0].tileType = "default"
                    displayBoard(window, gameBoard)
                    window.refresh()
                    
                    sg.popup("A piece died to a player-set trap orb!", keep_on_top=True)
                    return "death"

            # if a neutral trap was stepped on
            elif j[0].occupied == True and ((j[0].tileType == "trap orb 0")):
                death = forcefieldCheck(window, gameBoard, endLocation = j ,danger ="both")
                #if you didn't die, then start looking in a different direction
                if death == False:
                    break
                #sg.popup(f"FFT: {j[1].forceFieldTurn}", keep_on_top = True)
                if j[1].forceFieldTurn == PublicStats.turnCount:
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
                    playsound("sounds/grenade.mp3", block = False)
                    sg.popup("A piece died to a neutral trap orb!", keep_on_top=True)
                    return "death"
            # do something for holes
            elif j[0].occupied == True and  j[0].tileType in(
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
                        ):
                    tileBackup = j[0].tileType
                    j[0].occupied = False
                    displayBoard(window, gameBoard)
                    window.refresh()
                    sleep(1)
                    j[0].tileType = tileBackup
                    displayBoard(window, gameBoard)
                    window.refresh()
                    playsound("sounds/fall.wav", block = False)
                    sg.popup("A piece fell to its demise in the void!", keep_on_top=True)
                    return "death"


def getColumn(location, gameBoard, grow=False):
    validLocations = []
    if grow == False:
        for i in range(len(gameBoard)):
            validLocations.append( (i, location[1]) )
    return validLocations

def highlightValidDistance(gameBoard, window, startLocation, actionType = "walk", reachType = "cross", turnOff = False):
    x = startLocation[0]
    y = startLocation[1]
    g = gameBoard
    columns = len(gameBoard)
    rows = len(gameBoard)

    if g[x][y][0].occupied == True:
        playerTurn = g[x][y][1].ownedBy
    else:
        if PublicStats.turnCount % 2 == 0:
            playerTurn = 2
        else:
            playerTurn = 1

    if playerTurn == 1:
        enemyTurn = 2
    else:
        enemyTurn = 1
    location = (x,y)
    if turnOff == True:
        for i in gameBoard:
            for j in i:
                if j[0].highlight == True or j[0].highlightRed or j[0].highlightGreen or j[0].highlightBrown:
                    j[0].highlight = False
                    j[0].highlightRed = False
                    j[0].highlightGreen = False
                    j[0].highlightBrown = False
        return
    validLocations = []
    
    if actionType == "walk":
        for iIndex,i in enumerate(g):
            for jIndex,j in enumerate(i):
                #if there's a worm hole and it's your turn
                
                if j[0].wormHole1 == True and playerTurn == 1:
                    
                    #if the location of the warp is empty
                    if j[0].occupied == False:
                        
                        #highlight it
                        j[0].highlight = True
                    #if you're there, don't allow movement there, unless berzerk
                    elif j[1].ownedBy == playerTurn and "berzerk" not in g[x][y][1].activeBuffs:
                        continue
                    else:
                        j[0].highlightRed = True
               
                if j[0].wormHole2 == True and playerTurn==2:
                    #if it's empty
                    
                    if j[0].occupied == False:
                        #highlight it
                        
                        j[0].highlight = True
                    #if you're there, don't allow movement there, unless berzerk
                    elif j[1].ownedBy == playerTurn and "berzerk" not in g[x][y][1].activeBuffs:
                        continue
                    else:
                        j[0].highlightRed = True
                        
        if "move diagonal" in g[x][y][1].activeBuffs: #and "round earth theory" not in g[x][y][1].activeBuffs
            validLocations = getRadial(location, gameBoard)
            for i in validLocations:
                xi = i[0]
                yi = i[1]
                
                #if the floor isn't gone
                if g[xi][yi][0].tileType not in [
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
                    if g[xi][yi][0].tileHeight-1 > g[x][y][0].tileHeight:
                        if "grappling hook" not in g[x][y][1].activeBuffs:
                            continue
                        
                        
                    #if nothing's there
                    if g[xi][yi][0].occupied == False:
                        g[xi][yi][0].highlight = True
                    #if someone is there
                    elif g[xi][yi][0].occupied == True:
                        if g[xi][yi][1].ownedBy != g[x][y][1].ownedBy:
                            g[xi][yi][0].highlightRed = True
                        if g[xi][yi][1].ownedBy == g[xi][yi][1].ownedBy:
                            if "berzerk" in g[x][y][1].activeBuffs:
                                g[xi][yi][0].highlightRed = True
                            else:
                                continue

        
        if "round earth theory" in g[x][y][1].activeBuffs:

        #go right to straight left (you're on the right edge and want to appear on left edge)
            #if you're on the very right side
            if y == columns - 1:
                #if it's really high
                if g[x][0][0].tileHeight-1 > g[x][y][0].tileHeight:
                    if "grappling hook" in g[x][y][1].activeBuffs:
                        if g[x][0][0].occupied == True:
                            if g[x][0][1].ownedBy == enemyTurn or "berzerk" in g[x][y][1].activeBuffs:
                                g[x][0][0].highlightRed = True
                        else:
                            g[x][0][0].highlight = True
                #if it's normal height
                else:
                    if g[x][0][0].occupied == True:
                        if g[x][0][1].ownedBy == enemyTurn or "berzerk" in g[x][y][1].activeBuffs:
                            g[x][0][0].highlightRed = True
                    else:
                        g[x][0][0].highlight = True
                        
        #go left straight to the right (you're on the left edge and want to appear on the right edge)
            if y == 0:
                #if it's really high
                if g[x][columns-1][0].tileHeight-1 > g[x][y][0].tileHeight:
                    if "grappling hook" in g[x][y][1].activeBuffs:
                        if g[x][columns-1][0].occupied == True:
                            if g[x][columns-1][1].ownedBy == enemyTurn or "berzerk" in g[x][y][1].activeBuffs:
                                g[x][columns-1][0].highlightRed = True
                        else:
                            g[x][columns-1][0].highlight = True
                #if it's normal height
                else:
                    if g[x][columns-1][0].occupied == True:
                        if g[x][columns-1][1].ownedBy == enemyTurn or "berzerk" in g[x][y][1].activeBuffs:
                            g[x][columns-1][0].highlightRed = True
                    else:
                        g[x][columns-1][0].highlight = True
                        
        #go straight up to the bottom (you're on the top row and want to appear on the bottom)
            if x == 0:
                #if it's really high
                if g[rows-1][y][0].tileHeight-1 > g[x][y][0].tileHeight:
                    if "grappling hook" in g[x][y][1].activeBuffs:
                        if g[rows-1][y][0].occupied == True:
                            if g[rows-1][y][1].ownedBy == enemyTurn or "berzerk" in g[x][y][1].activeBuffs:
                                g[rows-1][y][0].highlightRed = True
                        else:
                            g[rows-1][y][0].highlight = True
                #if it's normal height
                else:
                    if g[rows-1][y][0].occupied == True:
                        if g[rows-1][y][1].ownedBy == enemyTurn or "berzerk" in g[x][y][1].activeBuffs:
                            g[rows-1][y][0].highlightRed = True
                    else:
                        g[rows-1][y][0].highlight = True
                        
        #go straight down to the top (you're on the bottom row and want to reappear on the top)
            if x == rows-1:
                #if it's really high
                if g[0][y][0].tileHeight-1 > g[x][y][0].tileHeight:
                    if "grappling hook" in g[x][y][1].activeBuffs:
                        if g[0][y][0].occupied == True:
                            if g[0][y][1].ownedBy == enemyTurn or "berzerk" in g[x][y][1].activeBuffs:
                                g[0][y][0].highlightRed = True
                        else:
                            g[0][y][0].highlight = True
                #if it's normal height
                else:
                    if g[0][y][0].occupied == True:
                        if g[0][y][1].ownedBy == enemyTurn or "berzerk" in g[x][y][1].activeBuffs:
                            g[0][y][0].highlightRed = True
                    else:
                        g[0][y][0].highlight = True
                        
        #teleport up right (you're on the top row and want to reappear on the bottom row, to the right)
            if "move diagonal" in g[x][y][1].activeBuffs:
                if x == 0 and y+1 < columns:
                    #if it's really high
                    if g[rows-1][y+1][0].tileHeight-1 > g[x][y][0].tileHeight:
                        if "grappling hook" in g[x][y][1].activeBuffs:
                            if g[rows-1][y+1][0].occupied == True:
                                if g[rows-1][y+1][1].ownedBy == enemyTurn or "berzerk" in g[x][y][1].activeBuffs:
                                    g[rows-1][y+1][0].highlightRed = True
                            else:
                                g[rows-1][y+1][0].highlight = True
                    #if it's normal height
                    else:
                        if g[rows-1][y+1][0].occupied == True:
                            if g[rows-1][y+1][1].ownedBy == enemyTurn or "berzerk" in g[x][y][1].activeBuffs:
                                g[rows-1][y+1][0].highlightRed = True
                        else:
                            g[rows-1][y+1][0].highlight = True
                            
                #upright along right edge but not top row            
                elif x >= 0 and x < rows and y == columns-1:
                    if g[x-1][0][0].tileHeight-1 > g[x][y][0].tileHeight:
                        if "grappling hook" in g[x][y][1].activeBuffs:
                            if g[x-1][0][0].occupied == True:
                                if g[x-1][0][1].ownedBy == enemyTurn or "berzerk" in g[x][y][1].activeBuffs:
                                    g[x-1][0][0].highlightRed = True
                            else:
                                g[x-1][0][0].highlight = True
                    #if it's normal height
                    else:
                        if g[x-1][0][0].occupied == True:
                            if g[x-1][0][1].ownedBy == enemyTurn or "berzerk" in g[x][y][1].activeBuffs:
                                g[x-1][0][0].highlightRed = True
                        else:
                            g[x-1][0][0].highlight = True
                            
        #teleport up left (you're on the top row and want to appear on the bottom, slightly to the left)
            if "move diagonal" in g[x][y][1].activeBuffs:
                if x == 0 and y-1>=0:
                    #if it's really high
                    if g[rows-1][y-1][0].tileHeight-1 > g[x][y][0].tileHeight:
                        if "grappling hook" in g[x][y][1].activeBuffs:
                            if g[rows-1][y-1][0].occupied == True:
                                if g[rows-1][y-1][1].ownedBy == enemyTurn or "berzerk" in g[x][y][1].activeBuffs:
                                    g[rows-1][y-1][0].highlightRed = True
                            else:
                                g[rows-1][y-1][0].highlight = True
                    #if it's normal height
                    else:
                        if g[rows-1][y-1][0].occupied == True:
                            if g[rows-1][y-1][1].ownedBy == enemyTurn or "berzerk" in g[x][y][1].activeBuffs:
                                g[rows-1][y-1][0].highlightRed = True
                        else:
                            g[rows-1][y-1][0].highlight = True
                            
                elif x >= 0 and x < rows and y==0:
                    #if it's really high
                    if g[x-1][columns-1][0].tileHeight-1 > g[x][y][0].tileHeight:
                        if "grappling hook" in g[x][y][1].activeBuffs:
                            if g[x-1][columns-1][0].occupied == True:
                                if g[x-1][columns-1][1].ownedBy == enemyTurn or "berzerk" in g[x][y][1].activeBuffs:
                                   g[x-1][columns-1][0].highlightRed = True
                            else:
                                g[x-1][columns-1][0].highlight = True
                    #if it's normal height
                    else:
                        
                        if g[x-1][columns-1][0].occupied == True:
                            if g[x-1][columns-1][1].ownedBy == enemyTurn or "berzerk" in g[x][y][1].activeBuffs:
                                g[x-1][columns-1][0].highlightRed = True
                        else:
                            g[x-1][columns-1][0].highlight = True
                    
                

        #teleport down right (you're on the bottom row and want to appear on the top to the right)
            if "move diagonal" in g[x][y][1].activeBuffs:
                if x == rows-1 and y+1 < columns:
                    #if it's really high
                    if g[0][y+1][0].tileHeight-1 > g[x][y][0].tileHeight:
                        if "grappling hook" in g[x][y][1].activeBuffs:
                            if g[0][y+1][0].occupied == True:
                                if g[0][y+1][1].ownedBy == enemyTurn or "berzerk" in g[x][y][1].activeBuffs:
                                    g[0][y+1][0].highlightRed = True
                            else:
                                g[0][y+1][0].highlight = True
                    #if it's normal height
                    else:
                        if g[0][y+1][0].occupied == True:
                            if g[0][y+1][1].ownedBy == enemyTurn or "berzerk" in g[x][y][1].activeBuffs:
                                g[0][y+1][0].highlightRed = True
                        else:
                            g[0][y+1][0].highlight = True

                #elif x > 0 and x < rows-1 and y== columns - 1:
                elif x >= 0 and x < rows-1 and y== columns - 1:
                    #if it's really high
                    
                    if g[x+1][0][0].tileHeight-1 > g[x][y][0].tileHeight:
                        if "grappling hook" in g[x][y][1].activeBuffs:
                            if g[x+1][0][0].occupied == True:
                                if g[x+1][0][1].ownedBy == enemyTurn or "berzerk" in g[x][y][1].activeBuffs:
                                    g[x+1][0][0].highlightRed = True
                            else:
                                g[x+1][0][0].highlight = True
                    #if it's normal height
                    else:
                        if g[x+1][0][0].occupied == True:
                            if g[x+1][0][1].ownedBy == enemyTurn or "berzerk" in g[x][y][1].activeBuffs:
                                g[x+1][0][0].highlightRed = True
                        else:
                            g[x+1][0][0].highlight = True

                
                            
        #teleport down left (you're on the bottom row and want to appear on the top to your left)
            if "move diagonal" in g[x][y][1].activeBuffs:
                if x == rows-1 and y-1 >= 0:
                    #if it's really high
                    if g[0][y-1][0].tileHeight-1 > g[x][y][0].tileHeight:
                        if "grappling hook" in g[x][y][1].activeBuffs:
                            if g[0][y-1][0].occupied == True:
                                if g[0][y-1][1].ownedBy == enemyTurn or "berzerk" in g[x][y][1].activeBuffs:
                                    g[0][y-1][0].highlightRed = True
                            else:
                                g[0][y-1][0].highlight = True
                    #if it's normal height
                    else:
                        if g[0][y-1][0].occupied == True:
                            if g[0][y-1][1].ownedBy == enemyTurn or "berzerk" in g[x][y][1].activeBuffs:
                                g[0][y-1][0].highlightRed = True
                        else:
                            g[0][y-1][0].highlight = True
                
                elif x >= 0 and x < rows-1 and y == 0:
                    if g[x+1][columns-1][0].tileHeight-1 > g[x][y][0].tileHeight:
                        if "grappling hook" in g[x][y][1].activeBuffs:
                            if g[x+1][columns-1][0].occupied == True:
                                if g[x+1][columns-1][1].ownedBy == enemyTurn or "berzerk" in g[x][y][1].activeBuffs:
                                    g[x+1][columns-1][0].highlightRed = True
                            else:
                                g[x+1][columns-1][0].highlight = True
                    #if it's normal height
                    else:
                        if g[x+1][columns-1][0].occupied == True:
                            if g[x+1][columns-1][1].ownedBy == enemyTurn or "berzerk" in g[x][y][1].activeBuffs:
                                g[x+1][columns-1][0].highlightRed = True
                        else:
                            g[x+1][columns-1][0].highlight = True



            # corner cases
            if "move diagonal" in g[x][y][1].activeBuffs:
                #top left corner
                if x == 0 and y == 0:
                    #if it's really high
                    if g[rows-1][columns-1][0].tileHeight-1 > g[x][y][0].tileHeight:
                        if "grappling hook" in g[x][y][1].activeBuffs:
                            if g[rows-1][columns-1][0].occupied == True:
                                if g[rows-1][columns-1][1].ownedBy == enemyTurn or "berzerk" in g[x][y][1].activeBuffs:
                                    g[rows-1][columns-1][0].highlightRed = True
                            else:
                                g[rows-1][columns-1][0].highlight = True
                    #if it's normal height
                    else:
                        if g[rows-1][columns-1][0].occupied == True:
                            if g[rows-1][columns-1][1].ownedBy == enemyTurn or "berzerk" in g[x][y][1].activeBuffs:
                                g[rows-1][columns-1][0].highlightRed = True
                        else:
                            g[rows-1][columns-1][0].highlight = True

                #top right corner
                if x == 0 and y == columns-1:
                    #if it's really high
                    if g[rows-1][0][0].tileHeight-1 > g[x][y][0].tileHeight:
                        if "grappling hook" in g[x][y][1].activeBuffs:
                            if g[rows-1][0][0].occupied == True:
                                if g[rows-1][0][1].ownedBy == enemyTurn or "berzerk" in g[x][y][1].activeBuffs:
                                    g[rows-1][0][0].highlightRed = True
                            else:
                                g[rows-1][0][0].highlight = True
                    #if it's normal height
                    else:
                        if g[rows-1][0][0].occupied == True:
                            if g[rows-1][0][1].ownedBy == enemyTurn or "berzerk" in g[x][y][1].activeBuffs:
                                g[rows-1][0][0].highlightRed = True
                        else:
                            g[rows-1][0][0].highlight = True
                            
                #bottom left corner
                if x == rows-1 and y == 0:
                    #if it's really high
                    if g[0][columns-1][0].tileHeight-1 > g[x][y][0].tileHeight:
                        if "grappling hook" in g[x][y][1].activeBuffs:
                            if g[0][columns-1][0].occupied == True:
                                if g[0][columns-1][1].ownedBy == enemyTurn or "berzerk" in g[x][y][1].activeBuffs:
                                    g[0][columns-1][0].highlightRed = True
                            else:
                                g[0][columns-1][0].highlight = True
                    #if it's normal height
                    else:
                        if g[0][columns-1][0].occupied == True:
                            if g[0][columns-1][1].ownedBy == enemyTurn or "berzerk" in g[x][y][1].activeBuffs:
                                g[0][columns-1][0].highlightRed = True
                        else:
                            g[0][columns-1][0].highlight = True

                #bottom right corner
                if x == rows-1 and y == columns - 1:
                    #if it's really high
                    if g[0][0][0].tileHeight-1 > g[x][y][0].tileHeight:
                        if "grappling hook" in g[x][y][1].activeBuffs:
                            if g[0][0][0].occupied == True:
                                if g[0][0][1].ownedBy == enemyTurn or "berzerk" in g[x][y][1].activeBuffs:
                                    g[0][0][0].highlightRed = True
                            else:
                                g[0][0][0].highlight = True
                    #if it's normal height
                    else:
                        if g[0][0][0].occupied == True:
                            if g[0][0][1].ownedBy == enemyTurn or "berzerk" in g[x][y][1].activeBuffs:
                                g[0][0][0].highlightRed = True
                        else:
                            g[0][0][0].highlight = True
                            
                
##            if "move diagonal" in g[x][y][1].activeBuffs and y == columns - 1:
##                #if it's really high
##                if g[x][0].tileHeight-1 > g[x][y][0].tileHeight:
##                    if "grappling hook" in g[x][y][1].activeBuffs:
##                        if g[x][0].occupied == True:
##                            if g[x][1].ownedBy == enemyTurn or "berzerk" in g[x][y][1].activeBuffs:
##                                g[x][0].highlightRed = True
##                        else:
##                            g[x][0].highlight = True
##                #if it's normal height
##                else:
##                    if g[x][0].occupied == True:
##                            if g[x][1].ownedBy == enemyTurn or "berzerk" in g[x][y][1].activeBuffs:
##                                g[x][0].highlightRed = True
##                        else:
##                            g[x][0].highlight = True
##                            
##                        
##
##    #trying to go down right
##    elif startLocation[0] == endLocation[0]-1 and startLocation[1] == columns -1 and endLocation[1] == 0 and "move diagonal" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
##        sg.popup("Your piece is attempting to roll to the other side!",keep_on_top=True)
##        return True
##    #trying to go up right
##    elif startLocation[0] == endLocation[0]+1 and startLocation[1] == columns -1 and endLocation[1] == 0 and "move diagonal" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
##        sg.popup("Your piece is attempting to roll to the other side!",keep_on_top=True)
##        return True
    

###trying to go from left to right side
##    #try to go straight left to straight right
##    if startLocation[0] == endLocation[0]:
##        if startLocation[1] == 0 and endLocation[1] == columns -1:
##            sg.popup("Your piece is attempting to roll to the other side!",keep_on_top=True)
##            return True
##    #trying to go down right
##    elif startLocation[0] == endLocation[0]-1 and startLocation[1] == 0  and endLocation[1] == columns -1 and "move diagonal" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
##        sg.popup("Your piece is attempting to roll to the other side!", keep_on_top=True)
##        return True
##    #trying to go up right
##    elif startLocation[0] == endLocation[0]+1 and startLocation[1] == 0 and endLocation[1] == columns -1 and "move diagonal" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
##        sg.popup("Your piece is attempting to roll to the other side!", keep_on_top=True)
##        return True
##
##        
###trying to go from up to down
##    #try to go straight up to straight down
##    if startLocation[1] == endLocation[1]:
##        if startLocation[0] == 0 and endLocation[0] == rows -1:
##            sg.popup("Your piece is attempting to roll to the other side!", keep_on_top=True)
##            return True
##    #trying to go up right
##    elif startLocation[0] == 0 and startLocation[1] == (endLocation[1] +1) and endLocation[0] == rows -1 and "move diagonal" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
##        sg.popup("Your piece is attempting to roll to the other side!", keep_on_top=True)
##        return True
##    #trying to go up right
##    elif startLocation[1] == endLocation[1]-1 and startLocation[0] == 0 and endLocation[0] == rows -1 and "move diagonal" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
##        sg.popup("Your piece is attempting to roll to the other side!", keep_on_top=True)
##        return True
##
###diagonals (only works with diagonal enabled
##    if "move diagonal" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
##        #upleft
##        if startLocation[0] == 0 and startLocation[1] == 0 and endLocation[0] == rows-1 and endLocation[1] == columns-1:
##            sg.popup("Your piece is attempting to roll to the other side!", keep_on_top=True)
##            return True
##        #upright
##        if startLocation[0] == 0 and startLocation[1] == columns-1 and endLocation[0] == rows-1 and endLocation[1] == 0:
##            sg.popup("Your piece is attempting to roll to the other side!", keep_on_top=True)
##            return True
##        #downleft
##        if startLocation[0] == rows-1 and startLocation[1] == 0 and endLocation[0] == 0 and endLocation[1] == columns-1:
##            sg.popup("Your piece is attempting to roll to the other side!", keep_on_top=True)
##            return True
##        #downright
##        if startLocation[0] == rows-1 and startLocation[1] == columns-1 and endLocation[0] == 0 and endLocation[1] == 0:
##            sg.popup("Your piece is attempting to roll to the other side!", keep_on_top=True)
##            return True
##    else:
##        return False






            
        #normal
        
        validLocations = getCross(location, gameBoard)
        for i in validLocations:
            xi = i[0]
            yi = i[1]
            
            #if the floor isn't gone
            if g[xi][yi][0].tileType not in [
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
                if g[xi][yi][0].tileHeight-1 > g[x][y][0].tileHeight:
                    if "grappling hook" not in g[x][y][1].activeBuffs:
                        continue
                    
                #if nothing's there
                if g[xi][yi][0].occupied == False:
                    g[xi][yi][0].highlight = True
                #if someone is there
                elif g[xi][yi][0].occupied == True:
                    if g[xi][yi][1].ownedBy != g[x][y][1].ownedBy:
                        g[xi][yi][0].highlightRed = True
                    if g[xi][yi][1].ownedBy == g[xi][yi][1].ownedBy:
                        if "berzerk" in g[x][y][1].activeBuffs:
                            g[xi][yi][0].highlightRed = True
                        else:
                            continue
                        
            #if the floor is gone, continue
            if g[xi][yi][0].tileType in [
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
                continue
                            
            g[xi][yi][0].highlight = True
                
    if actionType == "all":
        if reachType == "row":
            validLocations = getRow(location, gameBoard)
            for i in validLocations:
                ix = i[0]
                iy = i[1]
                g[ix][iy][0].highlight = True
            return
        if reachType == "column":
            validLocations = getColumn(location, gameBoard)
            for i in validLocations:
                ix = i[0]
                iy = i[1]
                g[ix][iy][0].highlight = True
            return
        if reachType == "radial":
            validLocations = getRadial(location, gameBoard)
            for i in validLocations:
                ix = i[0]
                iy = i[1]
                g[ix][iy][0].highlight = True
            return
        if reachType == "allTrueEmpty":
            validLocations = []
            validLocations = emptySpots(gameBoard, trueEmpty = True)
            for i in validLocations:
                ix = i[0]
                iy = i[1]
                g[ix][iy][0].highlight = True
            return
        if reachType == "allUnoccupied":
            validLocations = []
            validLocations = emptySpots(gameBoard, trueEmpty = True)
            for i in validLocations:
                ix = i[0]
                iy = i[1]
                g[ix][iy][0].highlight = True
            return
##        if reachType == "invert elevation all":
##            for i in gameBoard:
##                for j in i:
##                    if j[0].tileHeight != 0:
##                        j[0].highlightRed = True


    if actionType == "allOccupiedNeutral":
        if reachType == "row":
            validLocations = getRow(location, gameBoard)
            for i in validLocations:
                ix = i[0]
                iy = i[1]
                if g[ix][iy][0].occupied == True:
                    j[0].highlightBrown = True
            return
        if reachType == "column":
            validLocations = getColumn(location, gameBoard)
            for i in validLocations:
                ix = i[0]
                iy = i[1]
                if g[ix][iy][0].occupied == True:
                    j[0].highlightBrown = True
            return
        if reachType == "radial":
            validLocations = getRadial(location, gameBoard)
            for i in validLocations:
                ix = i[0]
                iy = i[1]
                if g[ix][iy][0].occupied == True:
                    j[0].highlightBrown = True
            return
        if reachType == "allOccupied":
            #validLocations = []
            #validLocations = emptySpots(gameBoard, trueEmpty = True)
            for i in gameBoard:
                for j in i:
                    
                    if j[0].occupied == True:
                        j[0].highlightBrown = True
            return
        


    if actionType == "allHurt":
        if reachType == "row":
            validLocations = getRow(location, gameBoard)
            for i in validLocations:
                ix = i[0]
                iy = i[1]
                
                if g[ix][iy][0].occupied == True:
                    g[ix][iy][0].highlightRed = True
                else:
                    g[ix][iy][0].highlight = True
            return
        if reachType == "column":
            validLocations = getColumn(location, gameBoard)
            for i in validLocations:
                ix = i[0]
                iy = i[1]
                if g[ix][iy][0].occupied == True:
                    g[ix][iy][0].highlightRed = True
                else:
                    g[ix][iy][0].highlight = True
            return
        if reachType == "radial":
            validLocations = getRadial(location, gameBoard)
            for i in validLocations:
                ix = i[0]
                iy = i[1]
                if g[ix][iy][0].occupied == True:
                    g[ix][iy][0].highlightRed = True
                else:
                    g[ix][iy][0].highlight = True
            return
        
        if reachType == "allOccupied":
            for i in gameBoard:
                for j in i:
                    
                    if j[0].occupied == True:
                        j[0].highlightBrown = True
            return


        
    if actionType == "enemyHurtOnly":
        if reachType == "row":
            validLocations = getRow(location, gameBoard)
            for i in validLocations:
                ix = i[0]
                iy = i[1]
                if g[ix][iy][0].occupied == True:
                    if g[ix][iy][1].ownedBy == enemyTurn:
                        g[ix][iy][0].highlightRed = True
                    else:
                        g[ix][iy][0].highlight = True
                else:
                    g[ix][iy][0].highlight = True
            return
        if reachType == "column":
            validLocations = getColumn(location, gameBoard)
            for i in validLocations:
                ix = i[0]
                iy = i[1]
                if g[ix][iy][0].occupied == True:
                    if g[ix][iy][1].ownedBy == enemyTurn:
                        g[ix][iy][0].highlightRed = True
                    else:
                        g[ix][iy][0].highlight = True
                else:
                    g[ix][iy][0].highlight = True
            return
        if reachType == "radial":
            validLocations = getRadial(location, gameBoard)
            for i in validLocations:
                ix = i[0]
                iy = i[1]
                if g[ix][iy][0].occupied == True:
                    if g[ix][iy][1].ownedBy == enemyTurn:
                        g[ix][iy][0].highlightRed= True
                    else:
                       g[ix][iy][0].highlight = True 
                else:
                    g[ix][iy][0].highlight = True
            return


    if actionType == "alliesHelpedOnly":
        if reachType == "row":
            validLocations = getRow(location, gameBoard)
            for i in validLocations:
                ix = i[0]
                iy = i[1]
                if g[ix][iy][0].occupied == True:
                    if g[ix][iy][1].ownedBy == playerTurn:
                        g[ix][iy][0].highlightGreen = True
                    else:
                        g[ix][iy][0].highlight = True
                else:
                    g[ix][iy][0].highlight = True
            return
        if reachType == "column":
            validLocations = getColumn(location, gameBoard)
            for i in validLocations:
                ix = i[0]
                iy = i[1]
                if g[ix][iy][0].occupied == True:
                    if g[ix][iy][1].ownedBy == playerTurn:
                        g[ix][iy][0].highlightGreen = True
                    else:
                        g[ix][iy][0].highlight = True
                else:
                    g[ix][iy][0].highlight = True
            return
        if reachType == "radial":
            validLocations = getRadial(location, gameBoard)
            for i in validLocations:
                ix = i[0]
                iy = i[1]
                if g[ix][iy][0].occupied == True:
                    if g[ix][iy][1].ownedBy == playerTurn:
                        g[ix][iy][0].highlightGreen = True
                    else:
                        g[ix][iy][0].highlight = True
                else:
                    g[ix][iy][0].highlight = True
            return



    if actionType == "alliesHurtOnly":
        if reachType == "row":
            validLocations = getRow(location, gameBoard)
            for i in validLocations:
                ix = i[0]
                iy = i[1]
                if g[ix][iy][0].occupied == True:
                    if g[ix][iy][1].ownedBy == playerTurn:
                        g[ix][iy][0].highlightRed = True
                    else:
                        g[ix][iy][0].highlight = True
                else:
                    g[ix][iy][0].highlight = True
            return
        if reachType == "column":
            validLocations = getColumn(location, gameBoard)
            for i in validLocations:
                ix = i[0]
                iy = i[1]
                if g[ix][iy][0].occupied == True:
                    if g[ix][iy][1].ownedBy == playerTurn:
                        g[ix][iy][0].highlightRed = True
                    else:
                        g[ix][iy][0].highlight = True
                else:
                    g[ix][iy][0].highlight = True
            return
        if reachType == "radial":
            validLocations = getRadial(location, gameBoard)
            for i in validLocations:
                ix = i[0]
                iy = i[1]
                if g[ix][iy][0].occupied == True:
                    if g[ix][iy][1].ownedBy == playerTurn:
                        g[ix][iy][0].highlightRed= True
                    else:
                       g[ix][iy][0].highlight = True 
                else:
                    g[ix][iy][0].highlight = True
            return
        if reachType == "all":
            for i in gameBoard:
                for j in i:
                    
                    if j[0].occupied == True:
                        if j[1].ownedBy == playerTurn:
                            j[0].highlightRed = True
                            
            g[x][y][0].highlightRed = False
            g[x][y][0].highlightGreen = True
            return


# for finding the outer ring that surrounds the immediate surrounding pieces
def getOuterRadialOnly(location, gameBoard):
    g = gameBoard
    x = location[0]
    y = location[1]
    rows = len(gameBoard)
    columns = len(gameBoard[0])
    #check for illegal boundaries outside of the playing field
    if x < 0 or x >= rows or y < 0 or y >= columns:
        return -1
    else:
        return (x, y)

#find the corresponding inner ring location for the outer ring.   That is, the top right corner of the outer ring (and the two adjacent tiles) correspond
#to the top right of the inner ring
def mapping(element):
    orientation = element[2]
    x = element[0]
    y = element[1]

    # for top left
    if orientation in ("tll", "tml", "mlt"):
        return (x + 1, y + 1)
    # for top middle
    elif orientation in ("tm"):
        return (x + 1, y)
    # for top right
    elif orientation in ("tmr", "trr", "mrt"):
        return (x + 1, y - 1)
    # for middle left
    elif orientation in ("ml"):
        return (x, y + 1)
    # for middle right
    elif orientation in ("mr"):
        return (x, y - 1)
    # for bottom left
    elif orientation in ("mlb", "bll", "bml"):
        return (x - 1, y + 1)
    # for bottom middle
    elif orientation in ("bm"):
        return (x - 1, y)
    # for bottom right
    elif orientation in ("brr", "bmr", "mrb"):
        return (x - 1, y - 1)

def emptySpots(gameBoard,trueEmpty = False):
    emptySpots = []
    for iIndex, i in enumerate(gameBoard):
        for jIndex,j in enumerate(i):
            if j[0].tileType == "default":
                if trueEmpty == False:
                    emptySpots.append( (iIndex, jIndex) )
                    

                #truly empty spots
                elif trueEmpty == True and True not in (j[0].orbEater, j[0].dumpList, j[0].occupied, j[0].wormHole1, j[0].wormHole2) and j[0].recallTurn == False:
                    emptySpots.append( (iIndex, jIndex) )
    return emptySpots

def cleanTile(tile):
    tile.wormHole1 = False
    tile.wormHole2 = False
    tile.orbEater = False
    tile.purityTile = False
    tile.secretAgent = False

    
def filterEmpty(gameBoard, filterList):
    cleanedList = []
    for i in filterList:
        x = i[0]
        y = i[1]
        if gameBoard[x][y][0].tileType == "default" and gameBoard[x][y][0].occupied == False:
            cleanedList.append((x, y))
    return cleanedList

# determine how far two points are
def getDistance(a, b, c, d):
    verticalDistance = abs(c - a)
    horizontalDistance = abs(d - b)
    distance = verticalDistance + horizontalDistance
    return distance

def getRow(location, gameBoard,grow=False):
    validLocations = []
    if grow == False:
        for i in range(len(gameBoard[0])):
            validLocations.append( (location[0], i))
    return validLocations


def getRadial(location, gameBoard, grow=False):
    validLocations = []
    rows = len(gameBoard)
    columns = len(gameBoard[0])

    if grow == False:
        # check if you can go one row up
        if location[0] - 1 != -1:
            # check if you can also go left after going up (only false if you're in the top left corner)
            if location[1] - 1 != -1:
                validLocations.append((location[0] - 1, location[1] - 1))
            # one row up (guaranteed already)
            validLocations.append((location[0] - 1, location[1] + 0))
            # check if you can also go right after going up (only false if you're in the top right corner)
            if location[1] + 1 != columns:
                validLocations.append((location[0] - 1, location[1] + 1))
        # check if you can go left
        if location[1] - 1 != -1:
            validLocations.append((location[0], location[1] - 1))
        # you are guaranteed to append yourself
        validLocations.append((location[0], location[1]))
        # check if you can go right
        if location[1] + 1 != columns:
            validLocations.append((location[0], location[1] + 1))
        # check if you can go down
        if location[0] + 1 != rows:
            # check bottom left
            if location[1] - 1 != -1:
                validLocations.append((location[0] + 1, location[1] - 1))
            # bottom guaranteed
            validLocations.append((location[0] + 1, location[1]))
            # check bottom right
            if location[1] + 1 != columns:
                validLocations.append((location[0] + 1, location[1] + 1))
    return validLocations


def getCross(location, gameBoard, grow=False, includeSelf=False, trueEmpty = False):
    validLocations = []
    rows = len(gameBoard)
    columns = len(gameBoard[0])
    
    x = location[0]
    y = location[1]
    # check if you can go up one
    if location[0] - 1 != -1:
        g = gameBoard[location[0]-1][y][0]
        # one row up (guaranteed already)
        if trueEmpty == False:
            validLocations.append((location[0] - 1, location[1] + 0))
        elif trueEmpty == True and g.orbEater == False and g.wormHole1 == False and g.tileType == "default" and g.wormHole2 == False and g.occupied == False and g.recallBackup == False and g.secretAgent == False and g.purityTile == False:
            validLocations.append((location[0] - 1, location[1] + 0))
    # check if you can go left
    if location[1] - 1 != -1:
        g = gameBoard[x][location[1]-1][0]
        if trueEmpty == False:
            validLocations.append((location[0], location[1] - 1))
        elif trueEmpty == True and g.orbEater == False and g.wormHole1 == False and g.tileType == "default" and g.wormHole2 == False and g.occupied == False and g.recallBackup == False and g.secretAgent == False and g.purityTile == False:
            validLocations.append((location[0], location[1] -1))
        
    if includeSelf == True:
        if trueEmpty == False:
            validLocations.append((location[0], location[1]))
            
    # check if you can go right
    if location[1] + 1 != columns:
        g = gameBoard[x][location[1] + 1][0]
        if trueEmpty == False:
            validLocations.append((location[0], location[1] + 1))
        elif trueEmpty == True and g.orbEater == False and g.wormHole1 == False and g.tileType == "default" and g.wormHole2 == False and g.occupied == False and g.recallBackup == False and g.secretAgent == False and g.purityTile == False:
            validLocations.append((location[0], location[1]+1))
    # check if you can go down
    if location[0] + 1 != rows:
        g = gameBoard[location[0] + 1][y][0]
        # bottom guaranteed
        if trueEmpty == False:
            validLocations.append((location[0] + 1, location[1]))
        elif trueEmpty == True and g.orbEater == False and g.wormHole1 == False and g.tileType == "default" and g.wormHole2 == False and g.occupied == False and g.recallBackup == False and g.secretAgent == False and g.purityTile == False:
            validLocations.append((location[0] + 1, location[1]))

    #sg.popup(f"Inside function {validLocations}",keep_on_top = True)
    return validLocations
