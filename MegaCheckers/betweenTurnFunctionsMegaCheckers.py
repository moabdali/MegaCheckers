# imported by megaCheckers

import PySimpleGUI as sg
from playsound import playsound
import random
from useItemsMegaCheckers import *


def playSoundExceptionCatcher(fileName, block = True):
    try:
        playsound(fileName, block)
    except:
        print(".")

        
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
        if gameBoard[i[0]][i[1]][0].tileType in ( "itemOrb", "trap orb 1", "trap orb 2", "trap orb 0"):
            #sg.popup("Orbeater was blessed with an orb!")
            gameBoard[i[0]][i[1]][0].tileType = "default"
            #make orbeater fat
            continue
        
        #for each shuffled location that the mouse can move to
        for j in legalLocations:
            #i refers to mice location, j refers to a adjacent location
            #eat an orb
            if gameBoard[j[0]][j[1]][0].tileType in ( "itemOrb", "trap orb 1", "trap orb 2", "trap orb 0"):
                gameBoard[i[0]][i[1]][0].orbEater = False
                gameBoard[j[0]][j[1]][0].tileType = "default"
                gameBoard[j[0]][j[1]][0].orbEater = True
                #change the picture to a fat mouse if he eats an orb; explode the mouse if it's a trap orb.  If he eats too many orbs, maybe make him crazy?
                
                orbsEaten+=1
                ateOrb = True
                #finish working on the current mouse
                break
            
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
                    if gameBoard[secondaryCoordinates[0]][secondaryCoordinates[1]][0].tileType in ( "itemOrb", "trap orb 1", "trap orb 2", "trap orb 0") and gameBoard[location[0]][location[1]][0].orbEater!= True and gameBoard[location[0]][location[1]][0].tileType == "default":
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


#the floor repairs itself a little each turn
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

# after your turn ends, get back your max "move again" turns
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


# function for lowering the timer on the time bomb
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

                        
# reduce the timer on the spooky hand, if it exists
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
                playSoundExceptionCatcher(f"sounds\spookyHand{choice}.mp3", block = False)
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


# the namesake of the AI bomb
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

        #if there is a bomb on a exploded square
        if gameBoard[location[0]][location[1]][0].tileType == "damaged":
            continue
        
        adjacentTiles = getCross(location, gameBoard)
        for i in adjacentTiles:
            if gameBoard[i[0]][i[1]][0].occupied == True:
                #sg.popup("Debug: found a rrigger point", keep_on_top = True)
                if explodeChance > 80:
                    explodeMe = getRadial(location, gameBoard)
                    sg.popup("The AI bomb has been set off!", keep_on_top = True)
                    for j in explodeMe:
                        damageCheck(window, gameBoard, j)
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

# if a berzerk piece exists, it must lower its food count        
def berzerkFunction(window, gameBoard, playerTurn):
    for i in gameBoard:
        for j in i:
            if j[0].occupied == True and j[1].ownedBy == playerTurn and "berzerk" in j[1].activeBuffs:
                j[1].berzerkMeatCount -= 1
                
                j[1].berzerkAttacksLeft = 3
                if j[1].berzerkMeatCount < 0:
                    
                    sg.popup("Your berzerk piece died of hunger.  Being berzerk is energy intensive!", keep_on_top = True)
                    pm(window, "Your berzerk piece died of hunger.  Being berzerk is energy intensive!")
                    playSoundExceptionCatcher("sounds\destroy.mp3",block=False)
                    j[0].occupied = False
                    #explode
                    
# how many pieces does each player have left?
def countPieces(gameBoard, window,PublicStats):
    player1count = 0
    player2count = 0
    for i in gameBoard:
        for j in i:
            if j[1] != 0:
                if j[1].ownedBy == 1:
                    player1count += 1
                elif j[1].ownedBy == 2:
                    player2count += 1
    if player1count == 0:
        #sg.popup("Player one loses",keep_on_top=True)
        gameOverLayout = [
            [sg.T("Congrats to our winner, Player Two")],
            [sg.Button("New Game")],
            [sg.Button("Quit")]
            ]
        window.disable()
        gameOverWindow = sg.Window("Game Over",gameOverLayout,element_justification = "center", keep_on_top = True)
        event = gameOverWindow.read()
        if "New Game" in event:
            window.enable()
            gameOverWindow.close()
            begin(PublicStats.screenSize)
        else:
            gameOverWindow.close()
            window.close()
            raise SystemExit
    if player2count == 0:
        #sg.popup("Player one loses",keep_on_top=True)
        gameOverLayout = [
            [sg.T("Congrats to our winner, Player One")],
            [sg.Button("New game")],
            [sg.Button("Quit")]
            ]
        window.disable()
        gameOverWindow = sg.Window("Game Over",gameOverLayout,element_justification = "center",keep_on_top = True)
        event = gameOverWindow.read()
        if "New Game" in event:
            window.enable()
            gameOverWindow.close()
            begin(PublicStats.screenSize)
        else:
            gameOverWindow.close()
            window.close()
            raise SystemExit

        
    window["player1piececount"].update(f"Player 1 controls: {player1count}\n")
    window["player2piececount"].update(f"Player 2 controls: {player2count}\n")
    window.refresh()
