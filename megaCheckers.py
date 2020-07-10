import PySimpleGUI as sg
import copy
import math
import random
from time import sleep
from PIL import Image
from io import BytesIO
import base64
from playsound import playsound

PublicPNGList = []     

def initializeField(columns, rows, window, gameBoard):
    publicPNGloader()

    for i in range(2):
        for j in range(columns):
            gameBoard[i][j][0] = Tile(occupied=True)
            piece = Piece(playerTurn=1)
            gameBoard[i][j][1] = piece
            gameBoard[i][j][1].location = (i, j)
            gameBoard[i][j][0].tileType = "player1default"
            gameBoard[i][j][1].avatar = "default"
    for i in range(2):
        for j in range(columns):
            gameBoard[rows - i - 1][j][0] = Tile(occupied=True)
            piece = Piece(playerTurn=2)
            gameBoard[rows - i - 1][j][1] = piece
            gameBoard[rows - i - 1][j][1].location = (rows - i - 1, j)
            gameBoard[rows - i - 1][j][0].tileType = "player2default"
            gameBoard[rows - i - 1][j][1].avatar = "default"

 ###### DELETE ME ##########
    for i in range(2):
        for j in range(columns):
            #middle row generator
            rows = 6
            gameBoard[rows - i - 1][j][0] = Tile(occupied=True)
            piece = Piece(playerTurn=2)



            #give items to main row
            gameBoard[i][j][1].storedItems.append("mystery box")
            gameBoard[i][j][1].storedItems.append("shuffle radial")
            gameBoard[i][j][1].storedItems.append("jumpoline")
            gameBoard[i][j][1].storedItems.append("mugger")
            gameBoard[i][j][1].storedItems.append("shuffle item orbs")
            gameBoard[i][j][1].storedItems.append("row laser")
            gameBoard[i][j][1].storedItems.append("column laser")
            gameBoard[i][j][1].storedItems.append("shuffle column")
            gameBoard[i][j][1].storedItems.append("reproduce")
            gameBoard[i][j][1].storedItems.append("haymaker")
            gameBoard[i][j][1].storedItems.append("haphazard airstrike")
            gameBoard[i][j][1].storedItems.append("row laser")
            gameBoard[i][j][1].storedItems.append("warp")
            
            
            gameBoard[i][j][1].activeBuffs.append("move diagonal")
            gameBoard[i][j][1].activeBuffs.append("jump proof")
            

            #the middle row
            gameBoard[rows - i - 1][j][1] = piece
            gameBoard[rows - i - 1][j][1].location = (rows - i - 1, j)
            gameBoard[rows - i - 1][j][0].tileType = "player2default"
            gameBoard[rows - i - 1][j][1].avatar = "default"
            gameBoard[rows - i - 1][j][1].storedItems.append("haphazard airstrike")
            gameBoard[rows - i - 1][j][1].activeBuffs.append("haymaker")



            #give items to middle row
            gameBoard[rows - i - 1][j][1].storedItems.append("shuffle radial")
            gameBoard[rows - i - 1][j][1].storedItems.append("worm hole")
            gameBoard[rows - i - 1][j][1].storedItems.append("orbEater")
            gameBoard[rows - i - 1][j][1].storedItems.append("shuffle item orbs")
            gameBoard[rows - i - 1][j][1].storedItems.append("row laser")
            gameBoard[rows - i - 1][j][1].storedItems.append("warp")
            gameBoard[rows - i - 1][j][1].storedItems.append("column laser")
            gameBoard[rows - i - 1][j][1].storedItems.append("place mine")
            gameBoard[rows - i - 1][j][1].storedItems.append("haymaker")
            gameBoard[rows - i - 1][j][1].storedItems.append("haphazard airstrike")
            gameBoard[rows - i - 1][j][1].storedItems.append("row laser")
            gameBoard[rows - i - 1][j][1].activeBuffs.append("move diagonal")
            gameBoard[rows - i - 1][j][1].storedItems.append("bowling ball")


####### END DELETE ME###########


class PublicStats:
    turnCount = 1
    cycle = 0
    #orbCycleList = [5, 10, 0, 0, 3, 1, 0, 2, 1]
    orbCycleList = [5, 0, 0, 1, 3, 3, 2, 2, 1]
    spookyHand = False
    spookyHandTurnCount = 5
    hotSpot = []
    recallCount = 0
    def getOrbCount(self):
        cycle = PublicStats.turnCount % 9
        return PublicStats.orbCycleList[cycle]
    

class Piece:
    def __init__(self, row=None, column=None, playerTurn=None):
        # where the piece is currently residing
        self.location = (row, column)
        # what bonuses the player has
        self.activeBuffs = []
        # what maluses the player has
        self.activeDebuffs = []
        # what the player is holding (need a max; 5?)
        self.storedItems = []
        # what it looks like
        self.avatar = "default"
        self.ownedBy = playerTurn
        self.distanceMax = 1
        self.grey = False
        self.currentTurnPiece = False
        self.moveAgain = 0
        self.standingOnSelfOrb = False
        self.recallTurn = False
    def determineAvatar(self):
        pass


class Tile:
    def __init__(self, occupied=False):
        self.tileHeight = 0
        self.tileType = "default"
        self.occupied = occupied
        self.horiLaser = False
        self.vertLaser = False
        self.crossLaser = False
        self.orbEater = False
        self.wormHole1 = False
        self.wormHole2 = False
        self.recallTurn = False
        self.recallBackup = False
        self.mugger = False
        self.muggerList = []

    def describeSelf(self):

        if self.tileType == "default":
            sg.popup(
                #f"This is a regular tile with an elevation of {self.tileHeight}",
                f"""This is a regular tile with an elevation of {self.tileHeight}.
Horizontal Laser Beam: {self.horiLaser}, Vertical Laser Beam: {self.vertLaser}, Cross Laser Beam: {self.crossLaser}
Orb Eater on tile? {self.orbEater}
Player one's worm hole? {self.wormHole1}
Player two's worm hole? {self.wormHole2}
""",
                keep_on_top=True,
            )
            return f"This is a regular tile with an elevation of {self.tileHeight}"
        elif self.tileType == "itemOrb":
            sg.popup(
                f"This is an item orb tile with an elevation of {self.tileHeight}",
                keep_on_top=True,
            )
            return f"This is an item orb tile with an elevation of {self.tileHeight}"
        elif self.tileType == "destroyed":
            sg.popup(
                f"This tile has been destroyed!  But don't worry, it'll come back in 5 turns.",
                keep_on_top=True,
            )
            return f"This tile has been destroyed!  But don't worry, it'll come back in 5 turns."
        elif self.tileType == "damaged4":
            sg.popup(
                f"This tile is being repaired.  It'll be ready for business in 4 turns.",
                keep_on_top=True,
            )
            return (
                f"This tile is being repaired.  It'll be ready for business in 4 turns."
            )
        elif self.tileType == "damaged3":
            sg.popup(
                f"This tile is being repaired.  It'll be up and at 'em in 3 turns.",
                keep_on_top=True,
            )
            return f"This tile is being repaired.  It'll be up and at 'em in 3 turns."
        elif self.tileType == "damaged2":
            sg.popup(
                f"This tile is being repaired.  It'll be repaired in 2 turns.",
                keep_on_top=True,
            )
            return f"This tile is being repaired.  It'll be repaired in 2 turns."
        elif self.tileType == "damaged":
            sg.popup(
                f"This tile is almost ready!  It'll be ready on the next turn!",
                keep_on_top=True,
            )
            return f"This tile is almost ready!  It'll be ready on the next turn!"
        elif self.tileType == "mine":
            sg.popup(
                f"There's an obvious booby trap on this tile.  Don't move here without protection! It has an elevation of {self.tileHeight}",
                keep_on_top=True,
            )
            return f"There's an obvious booby trap on this tile.  Don't move here without protection! It has an elevation of {self.tileHeight}"
        elif self.tileType in ["trap orb 0", "trap orb 1", "trap orb 2"]:
            sg.popup(
                f"This is an item orb tile with an elevation of {self.tileHeight}",
                keep_on_top=True,
            )
            return f"This is an item orb tile with an elevation of {self.tileHeight}"


def getColumn(location, gameBoard, grow=False, emptyOnly=False):
    validLocations = []
    if grow == False:
        for i in range(len(gameBoard)):
            validLocations.append(i, location[1])
    return validLocations


def filterEmpty(gameBoard, filterList):
    cleanedList = []
    for i in filterList:
        x = i[0]
        y = i[1]
        if gameBoard[x][y][0].tileType == "default":
            cleanedList.append((x, y))
    return cleanedList


def getRow(location, gameBoard,grow=False):
    validLocations = []
    if grow == False:
        for i in range(len(gameBoard[0])):
            validLocations.append(location[0], i)
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
    g = gameBoard[location[0]][location[1]]
    # check if you can go up one
    if location[0] - 1 != -1:
        # one row up (guaranteed already)
        if trueEmpty == False:
            validLocations.append((location[0] - 1, location[1] + 0))
        elif trueEmpty == True and g[0].orbEater == False and g[0].wormHole1 == False and g[0].wormHole2 == False:
            validLocations.append((location[0] - 1, location[1] + 0))
    # check if you can go left
    if location[1] - 1 != -1:
        if trueEmpty == False:
            validLocations.append((location[0], location[1] - 1))
        elif trueEmpty == True and g[0].orbEater == False and g[0].wormHole1 == False and g[0].wormHole2 == False:
            validLocations.append((location[0], location[1] -1))
        
    if includeSelf == True:
        if trueEmpty == False:
            validLocations.append((location[0], location[1]))
        elif trueEmpty == True and g[0].orbEater == False and g[0].wormHole1 == False and g[0].wormHole2 == False:
            validLocations.append((location[0], location[1]))
    # check if you can go right
    if location[1] + 1 != columns:
        if trueEmpty == False:
            validLocations.append((location[0], location[1] + 1))
        elif trueEmpty == True and g[0].orbEater == False and g[0].wormHole1 == False and g[0].wormHole2 == False:
            validLocations.append((location[0], location[1]+1))
    # check if you can go down
    if location[0] + 1 != rows:
        # bottom guaranteed
        if trueEmpty == False:
            validLocations.append((location[0] + 1, location[1]))
        elif trueEmpty == True and g[0].orbEater == False and g[0].wormHole1 == False and g[0].wormHole2 == False:
            validLocations.append((location[0] + 1, location[1]))
    return validLocations


# print out messages to both the window and console
def pm(window, message):
    window["information"].update(message)
    print(message)

# how many pieces does each player have left?
def countPieces(gameBoard, window):
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
        sg.popup("Player one loses")
        raise SystemExit
    elif player2count == 0:
        sg.popup("player two loses")
        raise SystemExit
    window["player1piececount"].update(f"Player 1 controls: {player1count}\n")
    window["player2piececount"].update(f"Player 2 controls: {player2count}\n")
    window.refresh()

# the actual loop that is used to progress turns
def gamePlay(playerTurn, window, gameBoard):
    countPieces(gameBoard, window)
    createOrbs(window, gameBoard)
    displayBoard(window, gameBoard)
    movePiece(playerTurn, window, gameBoard)
    PublicStats.turnCount += 1
    repairFloor(window, gameBoard)

# determine how far two points are
def getDistance(a, b, c, d):
    verticalDistance = abs(c - a)
    horizontalDistance = abs(d - b)
    distance = verticalDistance + horizontalDistance
    return distance

# generate item orbs
def createOrbs(window, gameBoard):
    dangerTurn = 30
    #dangerTurn = 1
    emptySpots = 0
    if PublicStats.turnCount == dangerTurn:
        sg.popup(
            "Warning: mines disguised as item orbs may spawn from now on!  They will explode if either player steps on them.",
            keep_on_top=True,
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
            sg.popup("Space is at a premium for orb generation.  Aborting.")
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

# see if any pieces are sitting on death spots
def deathCheck(window, gameBoard, move=False):
    for i in gameBoard:
        for j in i:
            # if a regular mine or laser was stepped on
            if (j[0].occupied == True) and (j[0].tileType == "mine" or (j[0].vertLaser == True or j[0].horiLaser == True or j[0].crossLaser == True) ):

                if "forceField" in j[1].activeBuffs:
                    j[1].activeBuffs.remove("forcefield")
                    sg.popup(
                        "You were protected from certain death by your forcefield",
                        keep_on_top=True,
                    )
                    j[0].tileType = "default"
                else:

                    j[0].tileType = "exploding"
                    j[1] = 0
                    j[0].occupied = False
                    displayBoard(window, gameBoard)
                    
                    window.refresh()
                    playsound("sounds/grenade.mp3", block = False)
                    j[0].tileType = "default"
                    displayBoard(window, gameBoard)
                    window.refresh()
                    sg.popup("A piece died!", keep_on_top=True)
                    return "death"

            # if a trap belonging to your enemy was set
            elif j[0].occupied == True and (
                (j[0].tileType == "trap orb 1" and j[1].ownedBy != 1)
                or (j[0].tileType == "trap orb 2" and j[1].ownedBy != 2)
            ):
                if "forceField" in j[1].activeBuffs:
                    j[1].activeBuffs.remove("forcefield")
                    playsound("sounds/grenade.mp3", block = False)
                    sg.popup(
                        "You were protected from certain death by your forcefield",
                        keep_on_top=True,
                    )
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
                    
                    sg.popup("A piece died!", keep_on_top=True)
                    return "death"

            # if a neutral trap was stepped on
            elif j[0].occupied == True and ((j[0].tileType == "trap orb 0")):
                if "forceField" in j[1].activeBuffs:
                    j[1].activeBuffs.remove("forecefield")
                    sg.popup(
                        "You were protected from certain death by your forcefield",
                        keep_on_top=True,
                    )
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
                    sg.popup("A piece died!", keep_on_top=True)
                    return "death"
            # do something for holes

def laserCheck(window, gameBoard, resetOnly = False):
    rows = len(gameBoard)
    columns = len(gameBoard[0])
    #turn off all lasers
    for i in gameBoard:
        for j in i:
            j[0].horiLaser = False
            j[0].vertLaser = False
            j[0].crossLaser = False
    
    if resetOnly == True:
        return
    #find a laser emitter
    while True:
        
        left = 0
        right = 0
        forceFieldLeft = False
        forceFieldRight = False

        
        for indexI, i in enumerate(gameBoard):
            for indexJ,j in enumerate(i):

                #work on horizontal lasers
                if j[0].tileType == "horiLaserTripod":
                    
                    left = indexJ
                    right = indexJ

                    # LEFT CHECK from the laser emitter, keep going left
                    while left > 0:
                        left-=1

                        #if there is a piece where the laser is burning
                        if gameBoard[indexI][left][0].occupied == True:


                            #forcefield check
                            if "Energy Forcefield" in gameBoard[indexI][left][1].activeBuffs:
                                forceFieldLeftStop = True
                                forceFieldDeletedList = True #turn into a list
                                break
                            
                            #if it doesn't have a forcefield
                            else:
                                
                                gameBoard[indexI][left][0].occupied = False
                                gameBoard[indexI][left][1] = 0
                                #gameBoard[indexI][left][0].horiLaser = False
                                tileBackup = gameBoard[indexI][left][0].tileType
                                if tileBackup in ("player1default", "player2default"):
                                    tileBackup = "default"
                                gameBoard[indexI][left][0].tileType = "exploding"
                                displayBoard(window, gameBoard)
                                window.refresh()

                                gameBoard[indexI][left][0].tileType = tileBackup
                                sg.popup("The laser killed a piece",keep_on_top=True)

                                if gameBoard[indexI][left][0].tileType == "horiLaserTripod":
                                    gameBoard[indexI][left][0].horiLaser = False
                                else:
                                    gameBoard[indexI][left][0].horiLaser = True
                                window.refresh()
                        #if there isn't a piece there
                                
                        else:
                            #if there's a tripod there, don't burn it
                            if gameBoard[indexI][left][0].tileType in ( "horiLaserTripod", "vertLaserTripod") :
                                gameBoard[indexI][left][0].horiLaser = False
                                gameBoard[indexI][left][0].vertLaser = False
                                gameBoard[indexI][left][0].crossLaser = False
                                                                        
                            else:
                                gameBoard[indexI][left][0].horiLaser = True
                                if gameBoard[indexI][left][0].vertLaser == True:
                                    gameBoard[indexI][left][0].crossLaser = True


                    #RIGHT CHECK as long as we haven't gone past the right wall
                    while right < columns-1:
                        
                        right += 1
                       


                        #if there's a piece to the right
                        if gameBoard[indexI][right][0].occupied == True:

                            #if there's a forcefield on the piece
                            if "Energy Forcefield" in gameBoard[indexI][right][1].activeBuffs:
                                forceFieldLeftStop = True
                                break

                            #if there isn't a forcefield on the piece
                            else:
                                
                                gameBoard[indexI][right][0].occupied = False
                                gameBoard[indexI][right][1] = 0
                                #gameBoard[indexI][right][0].horiLaser = False
                                tileBackup = gameBoard[indexI][right][0].tileType
                                if tileBackup in ("player1default", "player2default"):
                                    tileBackup = "default"
                                gameBoard[indexI][right][0].tileType = "exploding"
                                displayBoard(window, gameBoard)
                                window.refresh()

                                gameBoard[indexI][right][0].tileType = tileBackup
                                sg.popup("The laser killed a piece",keep_on_top=True)
                                if gameBoard[indexI][right][0].tileType == "horiLaserTripod":
                                    gameBoard[indexI][right][0].horiLaser = False
                                else:
                                    gameBoard[indexI][right][0].horiLaser = True
                                displayBoard(window, gameBoard)
                                window.refresh()
                        #if there isn't a piece there
                        else:
                            if gameBoard[indexI][right][0].tileType == "horiLaserTripod":
                                gameBoard[indexI][right][0].horiLaser = False
                                gameBoard[indexI][right][0].vertLaser = False
                                gameBoard[indexI][right][0].crossLaser = False
                            else:
                                gameBoard[indexI][right][0].horiLaser = True
                                if gameBoard[indexI][left][0].vertLaser == True:
                                    gameBoard[indexI][left][0].crossLaser = True
                                
                    left = indexJ
                    right = indexJ




                #work on vertical lasers
                    
                if j[0].tileType == "vertLaserTripod":
                    #as long as you have space left to above you
                    up = indexI
                    down = indexI
                    
                    while up > 0:
                        
                        up-=1
                        if gameBoard[up][indexJ][0].occupied == True:
                            
                            if "Energy Forcefield" in gameBoard[up][indexJ][1].activeBuffs:
                                forceFieldLeftStop = True
                                break
                            
                            else:
                                
                                gameBoard[up][indexJ][0].occupied = False
                                gameBoard[up][indexJ][1] = 0
                                #gameBoard[up][indexJ][0].horiLaser = False
                                tileBackup = gameBoard[up][indexJ][0].tileType
                                if tileBackup in ("player1default", "player2default"):
                                    tileBackup = "default"
                                gameBoard[up][indexJ][0].tileType = "exploding"
                                displayBoard(window, gameBoard)
                                window.refresh()

                                gameBoard[up][indexJ][0].tileType = tileBackup
                                sg.popup("The laser killed a piece")

                                
                                if gameBoard[up][indexJ][0].tileType in( "horiLaserTripod" , "vertLaserTripod"):
                                    gameBoard[up][indexJ][0].vertLaser = False
                                    gameBoard[up][indexJ][0].horiLaser = False
                                    gameBoard[up][indexJ][0].crossLaser = False
                                else:
                                    
                                    gameBoard[up][indexJ][0].vertLaser = True
                                    
                                displayBoard(window, gameBoard)
                                window.refresh()
                        else:
                            
                            if gameBoard[up][indexJ][0].tileType in ("horiLaserTripod" , "vertLaserTripod"):
                                gameBoard[up][indexJ][0].vertLaser = False
                                gameBoard[up][indexJ][0].horiLaser = False
                                gameBoard[up][indexJ][0].crossLaser = False
                            else:
                                gameBoard[up][indexJ][0].vertLaser = True
                                if gameBoard[up][indexJ][0].horiLaser == True:
                                    gameBoard[up][indexJ][0].crossLaser = True
                    
                    while down < rows-1:
                        
                        down += 1
                       


                        #if there's a piece bottom
                        if gameBoard[down][indexJ][0].occupied == True:

                            #if there's a forcefield on the piece
                            if "Energy Forcefield" in gameBoard[down][indexJ][1].activeBuffs:
                                forceFieldLeftStop = True
                                break

                            #if there isn't a forcefield on the piece
                            else:
                                
                                gameBoard[down][indexJ][0].occupied = False
                                gameBoard[down][indexJ][1] = 0
                                #gameBoard[down][indexJ][0].horiLaser = False
                                tileBackup = gameBoard[down][indexJ][0].tileType
                                if tileBackup in ("player1default", "player2default"):
                                    tileBackup = "default"
                                gameBoard[down][indexJ][0].tileType = "exploding"
                                displayBoard(window, gameBoard)
                                window.refresh()

                                gameBoard[down][indexJ][0].tileType = tileBackup
                                sg.popup("The laser killed a piece")
                                if gameBoard[down][indexJ][0].tileType in ( "horiLaserTripod" , "vertLaserTripod"):
                                    gameBoard[down][indexJ][0].vertLaser = False
                                    gameBoard[down][indexJ][0].horiLaser = False
                                    gameBoard[down][indexJ][0].crossLaser = False
                                else:
                                    gameBoard[down][indexJ][0].vertLaser = True
                                displayBoard(window, gameBoard)
                                window.refresh()
                        #if there isn't a piece there
                        else:
                            if gameBoard[down][indexJ][0].tileType in ("horiLaserTripod" , "vertLaserTripod"):
                                gameBoard[down][indexJ][0].vertLaser = False
                            else:
                                gameBoard[down][indexJ][0].vertLaser = True
                                if gameBoard[up][indexJ][0].horiLaser == True:
                                    gameBoard[up][indexJ][0].crossLaser = True
                    left = indexJ
                    right = indexJ
                    up = indexI
                    down = indexI
                        
        return
def publicPNGloader():
    #PublicPNGList
    for indexI, i in enumerate( [
        "default", #0
        "destroyed", #1
        "mine", #2
        "horiLaserTripod", #3
        "p1", #4
        "p2", #5
        "items",#6
        "itemOrb",#7
        "trapOrb",#8
        "vertLaserTripod",#9
        "orbEater", #10
        ]):
        if i == "p1":
            myImage = Image.open("images/p1.png").convert("RGBA")
            PublicPNGList.append(myImage)
            continue
        elif i == "p2":
            myImage = Image.open("images/p2.png").convert("RGBA")
            PublicPNGList.append(myImage)
            continue
        if i == "items":
            myImage = Image.open("images/items.png").convert("RGBA")
            PublicPNGList.append(myImage)
            continue
        myImage = Image.open(f"images/{i}.png").convert("RGBA")
        im_file = BytesIO()
        myImage.save(im_file, format="png")
        im_bytes = im_file.getvalue()
        PublicPNGList.append(base64.b64encode(im_bytes))        
                        
def cleanTile(tile):
    tile.wormHole1 = False
    tile.wormHole2 = False
    tile.orbEater = False
    
#display the board (update what the tiles/pieces should look like)
def displayBoard(window, gameBoard):

    for i in range(len(gameBoard)):
        for j in range(len(gameBoard[0])):
            # unoccupied spaces
            
                
            if gameBoard[i][j][0].horiLaser == True and gameBoard[i][j][0].vertLaser == False:
                window[i, j].update(image_filename="images/horiLaserBeam.png")
                continue
            elif gameBoard[i][j][0].horiLaser == False and gameBoard[i][j][0].vertLaser == True:    
                window[i, j].update(image_filename="images/vertLaserBeam.png")
                continue
            elif gameBoard[i][j][0].horiLaser == True and gameBoard[i][j][0].vertLaser == True:
                window[i, j].update(image_filename="images/crossLaserBeam.png")
                continue
            if gameBoard[i][j][0].tileType == "jumpoline":
                window[i, j].update(image_filename="images/jumpoline.png")
                continue
            
            if gameBoard[i][j][0].tileType == "mystery box":
                window[i, j].update(image_filename="images/mystery box.png")
                continue

            if gameBoard[i][j][0].tileType == "mugger":
                window[i, j].update(image_filename="images/mugger.png")
                continue
            
            if gameBoard[i][j][0].tileType == "exploding":
                cleanTile(gameBoard[i][j][0])
                window[i, j].update(image_filename="images/exploding.png")
                continue

            elif gameBoard[i][j][0].tileType == "damaged4":
                cleanTile(gameBoard[i][j][0])
                window[i, j].update(image_filename="images/damaged4.png")
                continue

            elif gameBoard[i][j][0].tileType == "damaged3":
                cleanTile(gameBoard[i][j][0])
                window[i, j].update(image_filename="images/damaged3.png")
                continue

            elif gameBoard[i][j][0].tileType == "damaged2":
                cleanTile(gameBoard[i][j][0])
                window[i, j].update(image_filename="images/damaged2.png")
                continue

            elif gameBoard[i][j][0].tileType == "damaged":
                cleanTile(gameBoard[i][j][0])
                window[i, j].update(image_filename="images/damaged.png")
                continue

            elif gameBoard[i][j][0].tileType == "snake":
                window[i, j].update(image_filename="images/snake.png")
                continue

            elif gameBoard[i][j][0].tileType == "abolished":
                window[i, j].update(image_filename="images/abolished.png")
                continue
            elif gameBoard[i][j][0].wormHole1 == True:
                window[i, j].update(image_filename="images/wormHole1.png")
                if gameBoard[i][j][0].occupied == False:
                    continue
            elif gameBoard[i][j][0].wormHole2 == True:
                window[i, j].update(image_filename="images/wormHole2.png")
                if gameBoard[i][j][0].occupied == False:
                    continue
            
        
            if gameBoard[i][j][0].occupied == False:

                #0 default
                if gameBoard[i][j][0].tileType == "default":
                    window[i, j].update(image_data=PublicPNGList[0])
                    #if the mouse is here
                    if gameBoard[i][j][0].recallTurn != False:
                
                        window[i, j].update(image_filename="images/recall.png")
                    if gameBoard[i][j][0].orbEater == True:
                        window[i, j].update(image_data=PublicPNGList[10])
                    continue
                #7 itemOrb
                elif gameBoard[i][j][0].tileType == "itemOrb":
                    window[i, j].update(image_data=PublicPNGList[7])
                    #if the mouse is here
                    if gameBoard[i][j][0].orbEater == True:
                        window[i, j].update(image_data=PublicPNGList[10])
                    continue
                #1 destroyed
                elif gameBoard[i][j][0].tileType == "destroyed":
                    cleanTile(gameBoard[i][j][0])
                    window[i, j].update(image_data=PublicPNGList[1])
                    continue
                #2 mine
                elif gameBoard[i][j][0].tileType == "mine":
                    window[i, j].update(image_data=PublicPNGList[2])
                    continue
                #8 trapOrb
                elif gameBoard[i][j][0].tileType in [
                    "trap orb 0",
                    "trap orb 1",
                    "trap orb 2",
                ]:
                    window[i, j].update(image_data=PublicPNGList[8])
                    #if the mouse is here
                    if gameBoard[i][j][0].orbEater == True:
                        cleanTile(gameBoard[i][j][0])
                        window[i, j].update(image_data=PublicPNGList[10])
                    continue
                elif gameBoard[i][j][0].tileType in ["hand1","hand2","hand3"]:
                    pass
                
                #3 horiLaserTripod
                elif gameBoard[i][j][0].tileType == "horiLaserTripod":
                    window[i, j].update(image_data= PublicPNGList[3])
                    continue

                elif gameBoard[i][j][0].tileType == "vertLaserTripod":
                    window[i, j].update(image_data= PublicPNGList[9])
                    continue
                elif gameBoard[i][j][0].tileType in ("player1default","player2default"):
                    gameBoard[i][j][0].tileType = "default"
                    window[i, j].update(image_data= PublicPNGList[0])
                    if gameBoard[i][j][0].recallTurn != False:
                
                        window[i, j].update(image_filename="images/recall1.png")
                    continue
                else:
                    sg.popup(
                        f"A tile error has occurred, with type {gameBoard[i][j][0].tileType}",
                        keep_on_top=True,
                    )
                    window[i, j].update(image_filename="images/glitch.png")
                    continue
            else:
                if gameBoard[i][j][0].occupied:
                    g = gameBoard[i][j][1]
                    
                    if "bowling ball" in g.activeBuffs:
                        avatar = Image.open(f"images/bowling ball {g.ownedBy}.png").convert("RGBA")
                        im_file = BytesIO()
                        avatar.save(im_file, format="png")
                        im_bytes = im_file.getvalue()
                        im_b64 = base64.b64encode(im_bytes)

                        window[i, j].update(image_data=im_b64)
                        continue
                    
                    # set the center color
                    if g.ownedBy == 1:
                        #4 p1
                        avatar = (PublicPNGList[4]).convert("RGBA")
                    elif g.ownedBy == 2:
                        #5 p2
                        avatar = (PublicPNGList[5]).convert("RGBA")
                    

                    # set the meat of the piece
                    #6 items
                    if len(g.storedItems) > 0:
                        
                        items = (PublicPNGList[6]).convert("RGBA")
                        avatar.paste(items, (0, 0), items)
                    else:
                        donut = Image.open("images/donut.png").convert("RGBA")
                        avatar.paste(donut, (0, 0), donut)

                    if "jumpProof" in g.activeBuffs:
                        jumpProof = Image.open("images/jumpProof.png").convert("RGBA")
                        avatar.paste(jumpProof, (0, 0), jumpProof)

                    # set a forcefield if it exists
                    if "Energy Forcefield" in g.activeBuffs:
                        forcefield = Image.open("images/forcefield.png").convert("RGBA")
                        avatar.paste(forcefield, (0, 0), forcefield)

                    if "trip mine" in g.activeDebuffs:
                        tripmine = Image.open("images/tripmine.png").convert("RGBA")
                        avatar.paste(tripmine, (0, 0), tripmine)
                    # if the piece is stunned
                    if "stunned" in g.activeDebuffs:
                        stunned = Image.open("images/stunned.png").convert("RGBA")
                        avatar.paste(stunned, (0, 0), stunned)

                    if "purified2" in g.activeBuffs:
                        purified2 = Image.open("images/purified2.png").convert("RGBA")
                        avatar.paste(purified2, (0, 0), purified2)
                    elif "purified1" in g.activeBuffs:
                        purified1 = Image.open("images/purified1.png").convert("RGBA")
                        avatar.paste(purified1, (0, 0), purified1)
                    elif "purified0" in g.activeBuffs:
                        purified0 = Image.open("images/purified0.png").convert("RGBA")
                        avatar.paste(purified0, (0, 0), purified0)

                    # if move diagonal exists:
                    if "move diagonal" in g.activeBuffs:
                        diagonal = Image.open("images/diagonal.png").convert("RGBA")
                        avatar.paste(diagonal, (0, 0), diagonal)

                    # see which type of shoe icon needs to be applied
                    if g.moveAgain == 1:
                        step1 = Image.open("images/moveAgain1.png").convert("RGBA")
                        avatar.paste(step1, (0, 0), step1)
                    elif g.moveAgain == 2:
                        step2 = Image.open("images/moveAgain2.png").convert("RGBA")
                        avatar.paste(step2, (0, 0), step2)
                    elif g.moveAgain == 3:
                        step3 = Image.open("images/moveAgain3.png").convert("RGBA")
                        avatar.paste(step3, (0, 0), step3)
                    elif g.moveAgain > 3:
                        stepMax = Image.open("images/moveAgainMax.png").convert("RGBA")
                        avatar.paste(stepMax, (0, 0), stepMax)

                    if "abolished" in g.activeDebuffs:
                        abolished = Image.open("images/abolished.png").convert("RGBA")
                        avatar.paste(abolished, (0, 0), abolished)

                    # if it's supposed to be highlighted... then highlight it
                    if g.grey == True:
                        grey = Image.open("images/highlight.png").convert("RGBA")
                        avatar = Image.blend(grey, avatar, 0.50)

                    if gameBoard[i][j][0].tileType == "hand1":
                        hand1 = Image.open("images/hand1.png").convert("RGBA")
                        avatar.paste(hand1, (0, 0), hand1)
                        
                    if gameBoard[i][j][0].tileType == "hand2":
                        hand2 = Image.open("images/hand2.png").convert("RGBA")
                        avatar.paste(hand2, (0, 0), hand2)
                        
                    if gameBoard[i][j][0].tileType == "hand3":
                        hand3 = Image.open("images/hand3.png").convert("RGBA")
                        avatar.paste(hand3, (0, 0), hand3)

                    if "round earth theory" in g.activeBuffs:
                        roundEarthTheory = Image.open("images/roundEarthTheory.png").convert("RGBA")
                        avatar.paste(roundEarthTheory, (0, 0), roundEarthTheory)
                        
                    if gameBoard[i][j][1].recallTurn != False:
                            recall1 = Image.open("images/recall1.png").convert("RGBA")
                            avatar.paste(recall1, (0, 0), recall1)
                            window[i, j].update(image_filename="images/recall1.png")
                            
                    #if gameBoard[i][j][0].recallTurn != False or gameBoard[i][j][1].recallTurn != False:
                    if gameBoard[i][j][0].recallTurn != False:
                        
                        recall = Image.open("images/recall.png").convert("RGBA")
                        avatar.paste(recall, (0, 0), recall)
                        window[i, j].update(image_filename="images/recall.png")
                    
            im_file = BytesIO()
            avatar.save(im_file, format="png")
            im_bytes = im_file.getvalue()
            avatar = base64.b64encode(im_bytes)

            window[i, j].update(image_data=avatar)



# for finding the outer ring that surrounds the immediate surrounding pieces
def getOuterRadialOnly(location, gameBoard):
    g = gameBoard
    x = location[0]
    y = location[1]
    rows = len(gameBoard)
    columns = len(gameBoard[0])
    #check for illegal boundaries outside of the playing field
    if x < 0 or x > rows or y < 0 or y > columns:
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
                elif trueEmpty == True and True not in (j[0].orbEater, j[0].occupied, j[0].wormHole1, j[0].wormHole2) and j[0].recallTurn == False:
                    emptySpots.append( (iIndex, jIndex) )
                    
            
    return emptySpots
# the item list
def pickUpItemOrb(gameBoard, x, y):
    # items = ["suicideBomb Row","Energy Forcefield","suicideBomb Column","Haphazard Airstrike","suicideBomb Radial","jumpProof","smartBombs"]
    items = [
        "orb eater",
        "row laser",
        "magnet",
        "trap orb",
        "place mine",
        "move again",
        "suicide bomb row",
        "Energy Forcefield",
        "suicide bomb column",
        "haphazard airstrike",
        "suicide bomb radial",
        "jump proof",
        "smart bombs",
        "move diagonal",
        "trip mine radial",
        "purify radial",
        "napalm radial",
        "vile radial",
        "haymaker",
        "bowling ball",
        "column laser",
        "row laser",
        "shuffle column",
        "shuffle radial",
        "spooky hand",
        "reproduce",
        "worm hole",
        "warp",
        "recall",
        "jumpoline",
        "mystery box"
    ]
    # items = ["magnet"]

    #pick an item at random; should eventually have biases on the items by separating them into different lists that have different odds of being chosen
    randItem = random.choice(items)
    gameBoard[x][y][1].storedItems.append(randItem)
    playerOwned = gameBoard[x][y][1].ownedBy
    #modifies your avatar to signify the player is holding an item(s)
    gameBoard[x][y][1].avatar = f"player{playerOwned}stored"
    sg.popup("Picked up an item!")


def jumpoline(window, gameBoard, location, playerTurn):
    validLocations = emptySpots(gameBoard, trueEmpty = True)
    if len(validLocations) == 0:
        sg.popup("Nowhere valid for you to jumpoline to. :(")
        return
    choice = random.choice(validLocations)
    x=choice[0]
    y=choice[1]
    return x,y


# using an item
def useItems(gameBoard, x, y, window):
    layout = []
    listData = [[sg.T("Item Menu", justification="center", font="Calibri 30")]]
    itemsLength = len(gameBoard[x][y][1].storedItems)
    for i in gameBoard[x][y][1].storedItems:
        z = f"images/{i}.png"
        if z == "images/move again.png":
            z = "images/moveAgainMax.png"
            zz = "Move an extra space"
        elif z == "images/trip mine radial.png":
            z = "images/tripMine.png"
            zz = "set up a trip mine"
        elif z == "images/place mine.png":
            z = "images/mine.png"
            zz = "place a mine"
        elif z == "images/vile radial.png":
            z = "images/vile.png"
            zz = "removes all buffs (beneficial effects) from surrounding enemies."
        elif z == "images/purify radial.png":
            z = "images/purified1.png"
            zz = "removes all debuffs (negative effects) from all surrounding allies and this piece."
        elif z == "images/jumpProof.png":
            z = "images/jumpProof.png"
            zz = "This piece is wearing a hardhat, so naturally, he can't be jumped on by a 3 ton block of metal machinery."
        elif z == "images/shuffle column.png":
            z = "images/shuffleColumn.png"
            zz = "Randomly shuffle a column."
        elif z == "images/shuffle radial.png":
            z = "images/shuffleRadial.png"
            zz = "Shuffle your piece and all surrounding tiles around."
        elif z == "images/spooky hand.png":
            z = "images/Hand3.png"
            zz = "A scary hand that will periodically grab a random piece from the field."
        elif z == "images/haymaker.png":
            z = "images/haymaker.png"
            zz = "A strong punch that will send a piece flying until it smashes into something."
        elif z == "images/Energy Forcefield.png":
            z = "images/Forcefield.png"
            zz = "removes all buffs (beneficial effects) from surrounding enemies."
        elif z == "images/bowling ball.png":
            z = "images/bowling ball.png"
            zz = "Your piece loses all of its effects and items... but turns into a crazy bowling ball."
        else:
            z = "images/default.png"
            zz = "no explanation supplied... yet"

        if itemsLength < 5:
            listData += [
                [
                    sg.Button(
                        i,
                        key=i,
                        image_filename=z,
                        tooltip=zz,
                        font="Arial 20",
                        size=(30, 1),
                        button_color=("pink", "grey"),
                        image_size=(400, 100),
                    )
                ]
            ]
        elif itemsLength <10:
            listData += [
                [
                    sg.Button(
                        i,
                        key=i,
                        image_filename=z,
                        tooltip=zz,
                        font="Arial 20",
                        size=(30, 1),
                        button_color=("pink", "grey"),
                        image_size=(400, 75),
                    )
                ]
            ]
        else:
            listData += [
                [
                    sg.Button(
                        i,
                        key=i,
                        image_filename=z,
                        tooltip=zz,
                        font="Arial 20",
                        size=(30, 1),
                        button_color=("pink", "grey"),
                        image_size=(400, 50),
                    )
                ]
            ]
            
        
    listData += [[sg.Button("CANCEL")]]

    layout += [[sg.Column(listData, justification="center")]]
    #no_titlebar=True,

    
    itemsMenu = sg.Window("Items Menu", layout, disable_close=True, grab_anywhere=True,keep_on_top=True).finalize()
    
    # event = itemsMenu.read()
    enemyTurn = 0
    playerTurn = gameBoard[x][y][1].ownedBy
    if playerTurn == 1:
        enemyTurn = 2
    elif playerTurn == 2:
        enemyTurn = 1
    else:
        pm(window, "An error occurs in the turn assignment in items")
    rows = len(gameBoard)
    columns = len(gameBoard[0])
    location = (x, y)
    while True:
        window.disable()
        event = itemsMenu.read()
        window.enable()
        i = event[0]

        if i == None:
            break

        # suicidebomb row
        if str.find(i, "suicide bomb row") >= 0:
            gameBoard[x][y][1].storedItems.remove("suicide bomb row")
            # for each item inside the specific gameBoard row
            for j in gameBoard[x]:
                if isinstance(j[1], Piece):
                    if "Energy Forcefield" in j[1].activeBuffs:

                        j[1].activeBuffs.remove("Energy Forcefield")

                    else:
                        # set the tile to be empty
                        j[0].occupied = False
                        j[1] = 0
                        j[0].tileType = "default"

        elif str.find(i,"jumpoline") >= 0:
            itemsMenu.close()
            validTargets = getCross((x, y), gameBoard, trueEmpty = True)
            pm(window, "Pick an adjacent location to place the jumpoline.")
            event = window.read()
            if event[0] in validTargets:
                x1 = event[0][0]
                y1 = event[0][1]
                g = gameBoard[x1][y1]
                if g[0].occupied == True:
                    sg.popup("Must pick an empty spot")
                    pm(window, "Must pick an empty spot")
                    break
                elif g[0].tileType != "default":
                    sg.popup("Must be a valid tile")
                    pm(window, "Must be a valid tile")
                    break
                else:
                    gameBoard[x][y][1].storedItems.remove("jumpoline")
                    g[0].tileType = "jumpoline"
            else:
                sg.popup("Invalid location")
                break
            
        elif str.find(i,"mystery box") >= 0:
            itemsMenu.close()
            validTargets = getCross((x, y), gameBoard, trueEmpty = True)
            pm(window, "Pick an adjacent location to place the mystery box.")
            event = window.read()
            if event[0] in validTargets:
                x1 = event[0][0]
                y1 = event[0][1]
                g = gameBoard[x1][y1]
                if g[0].occupied == True:
                    sg.popup("Must pick an empty spot")
                    pm(window, "Must pick an empty spot")
                    break
                elif g[0].tileType != "default":
                    sg.popup("Must be a valid tile")
                    pm(window, "Must be a valid tile")
                    break
                else:
                    gameBoard[x][y][1].storedItems.remove("mystery box")
                    g[0].mugger = playerTurn
                    g[0].tileType = "mystery box"

            else:
                sg.popup("Invalid location")
                break

        elif str.find(i,"mugger") >= 0:
            itemsMenu.close()
            validTargets = getCross((x, y), gameBoard, trueEmpty = True)
            sg.popup(validTargets)
            pm(window, "Pick an adjacent location to place the .")
            event = window.read()
            if event[0] in validTargets:
                x1 = event[0][0]
                y1 = event[0][1]
                g = gameBoard[x1][y1]
                if g[0].occupied == True:
                    sg.popup("Must pick an empty spot")
                    pm(window, "Must pick an empty spot")
                    break
                elif g[0].tileType != "default":
                    sg.popup("Must be a valid tile")
                    pm(window, "Must be a valid tile")
                    break
                else:
                    gameBoard[x][y][1].storedItems.remove("mugger")
                    g[0].mugger = playerTurn
                    g[0].tileType = "mugger"

            else:
                sg.popup("Invalid location")
                break
            
            
        elif str.find(i,"reproduce") >= 0:
            itemsMenu.close()
            validTargets = getCross((x, y), gameBoard)
            pm(window, "Pick an adjacent location for your baby to be spawned. You can only spawn on empty spots.")
            event = window.read()
            if event[0] in validTargets:
                x1 = event[0][0]
                y1 = event[0][1]
                g = gameBoard[x1][y1]
                if g[0].occupied == True:
                    sg.popup("Must pick an empty spot")
                    pm(window, "Must pick an empty spot")
                    break
                elif g[0].tileType != "default":
                    sg.popup("Must be a valid tile")
                    pm(window, "Must be a valid tile")
                    break
                else:
                    g[1] = Piece(playerTurn = playerTurn)
                    g[0].occupied = True
                    g[0].tileType = f"player{playerTurn}default"
                    g[1].avatar = "default"
                    
                    sg.popup("Congrats on your newborn piece.")
                    gameBoard[x][y][1].storedItems.remove("reproduce")
                    return
            else:
                sg.popup("Invalid location")
                break
            
        elif str.find(i, "recall") >= 0:
            
            turnCountRecall = 10
            g = gameBoard[x][y]
            if g[0].recallBackup != False:
                sg.popup("This tile is awaiting the arrival of another recall piece.  It cannot be used until the recall is complete.")
                break
            gameBoard[x][y][1].storedItems.remove("recall")
            gameBoard[x][y][1].grey = False
            #backup the gameTile and gamePiece as one blob into the tile itself
            g[0].recallBackup = copy.deepcopy(g)
            g[1].recallTurn = PublicStats.turnCount + turnCountRecall

            #make note of the turn that the tile will be reverted, into the tile itself
            g[0].recallTurn = PublicStats.turnCount + turnCountRecall
            #increase the number of pieces awaiting recall by one
            PublicStats.recallCount +=1
            
            
            sg.popup(f"This piece will be returned to its current location and in its current state in {turnCountRecall} turns.",keep_on_top = True)
            
            
            
        elif str.find(i, "row laser") >= 0:
            itemsMenu.close()
            validTargets = getCross((x, y), gameBoard)
            pm(window, "Where do you want to deploy the laser emitter?  Pick an empty spot that is either one space up/down/left/right")
            event = window.read()

            # if the target is within range
            if event[0] in validTargets:

                #attempted laser location
                lx= event[0][0]
                ly = event[0][1]
                g = gameBoard[lx][ly]
                if g[0].occupied == True or g[0].tileType not in ("default","player1default","player2default"):
                    sg.popup("You must put the laser tripod in an empty spot!",keep_on_top=True)
                    continue
                if g[0].tileType == "default":
                    gameBoard[x][y][1].storedItems.remove("row laser")
                    pm(window,"horizontal laser tripod placed")
                    g[0].tileType = "horiLaserTripod"
                    g[0].horiLaser = False
                    g[0].vertLaser = False
                    g[0].crossLaser = False
                    laserCheck(window,gameBoard)
            else:
                sg.popup("Pick something in range (default range is one up/down/left/right)!", keep_on_top=True)

        elif str.find(i, "worm hole") >= 0:
            g = gameBoard
            itemsMenu.close()
            emptyList = getCross((x,y),gameBoard, trueEmpty = True)
            pm(window, "Choose an empty cross spot to deploy the wormhole")
            event = window.read()
            try:
                
                if event[0] in emptyList:
                    x1 = event[0][0]
                    y1 = event[0][1]
                    
                    if playerTurn == 1:
                        g[x1][y1][0].wormHole1 = True
                        pm(window, "worm hole placed")
                        
                    elif playerTurn == 2:
                        g[x1][y1][0].wormHole2 = True
                        pm(window, "worm hole placed")
                        
                    else:
                        sg.popup("An error occurred trying to place the worm hole")
                        break
                    displayBoard(window, gameBoard)
                    gameBoard[x][y][1].storedItems.remove("worm hole")
                    window.refresh()
                    break
                else:
                    pm(window, "You must pick an empty adjacent location (up/down/left/right)")
                    sleep(1)
            except:
                sg.popup("An error occurred trying to place the worm hole")
                break
                    
                    
                    
            
        elif str.find(i, "orbEater") >= 0:
            itemsMenu.close()
            emptyList = emptySpots(gameBoard)
            pm(window, "Where do you want to deliver the orb eater to?")
            event = window.read()
            try:
                if event[0] in emptyList and gameBoard[event[0][0]][event[0][1]][0].orbEater == False:
                    gameBoard[x][y][1].storedItems.remove("orbEater")
                    gameBoard[event[0][0]][event[0][1]][0].orbEater = True
                    fileNum = random.randint(1,4)
                    playsound(f"sounds/squeak{fileNum}.mp3", block = False)
                elif gameBoard[event[0][0]][event[0][1]][0].orbEater == True:
                    sg.popup("There's already an orb eater here... get your mind out of the gutter, that's not going to happen.")
                    pm(window, "There's already an orb eater here... get your mind out of the gutter, that's not going to happen.")
                else:
                    sg.popup("You need to select an emty space.  The orb eater will find nearby orbs to eat on his own.")
                    continue
            except:
                sg.popup(f"Error. {event[0]} {emptyList}")
                continue
            
        elif str.find(i, "warp") >= 0:
            itemsMenu.close()
            emptyList = emptySpots(gameBoard)
            g = gameBoard[x][y]
            if len(emptyList)>0:
                g[1].storedItems.remove("warp")
                window.disable()
                copyPiece = copy.deepcopy(g)
                g[0].occupied = False
                g[0].tileType = "default"
                g[1] = 0
                choice = random.choice(emptyList)
                x1 = choice[0]
                y1 = choice[1]

                #test this
                gameBoard[x1][y1][1] = copy.deepcopy(copyPiece[1])
                
                displayBoard(window, gameBoard)
                window.refresh()
                sleep(.5)
                gameBoard[x1][y1][0].occupied = False
                displayBoard(window, gameBoard)
                window.refresh()
                sleep(.5)
                gameBoard[x1][y1][0].occupied = True
                gameBoard[x1][y1][1].grey = False
                window.enable()
                pm(window,"Piece was teleported")
                break
            else:
                sg.popup("Nowhere to teleport to")
                break
        
        elif str.find(i, "round earth theory") >= 0:
            itemsMenu.close()
            pm(window,"This piece can now 'wrap' around the edges of the map to appear on the opposite side.")
            gameBoard[x][y][1].storedItems.remove("round earth theory")
            gameBoard[x][y][1].activeBuffs.append("round earth theory")
            
            
            
        elif str.find(i, "column laser") >= 0:
            itemsMenu.close()
            validTargets = getCross((x, y), gameBoard)
            pm(window, "Where do you want to deploy the laser emitter?  Pick an empty spot that is either one space up/down/left/right.  Careful - you can be burned by your own laser.")
            event = window.read()

            # if the target is within range
            if event[0] in validTargets:

                #attempted laser location
                lx= event[0][0]
                ly = event[0][1]
                g = gameBoard[lx][ly]
                if g[0].occupied == True or g[0].tileType not in ("default","player1default","player2default"):
                    sg.popup("You must put the laser tripod in an empty spot!",keep_on_top=True)
                    continue
                if g[0].tileType == "default":
                    gameBoard[x][y][1].storedItems.remove("column laser")
                    pm(window,"vertical laser tripod placed")
                    g[0].tileType = "vertLaserTripod"
                    g[0].horiLaser = False
                    g[0].vertLaser = False
                    g[0].crossLaser = False
                    laserCheck(window,gameBoard)
            else:
                sg.popup("Pick something in range (default range is one up/down/left/right)!", keep_on_top=True)    
                
        elif str.find(i, "spooky hand") >= 0:
            itemsMenu.close()
            gameBoard[x][y][1].storedItems.remove("spooky hand")
            sg.popup("A spooky hand has gone under the field.  When will he strike?  Nobody knows...", keep_on_top = True)
            pm(window,"A spooky hand has gone under the field.  When will he strike?  Nobody knows...")
            sleep(1)
            PublicStats.spookyHand = True
            
        elif str.find(i, "bowling ball") >= 0:
            
            yesno = sg.popup_yes_no("Warning: using bowling ball will make your piece permanently transform into a rabid bowling ball, and will lose all items and effects. Are you sure you want to use this?",keep_on_top=True)
            itemsMenu.close()
            if yesno == "Yes":
                gameBoard[x][y][1].storedItems.remove("bowling ball")
                gameBoard[x][y][1].activeDebuffs.clear()
                gameBoard[x][y][1].activeBuffs.clear()
                gameBoard[x][y][1].storedItems.clear()
                gameBoard[x][y][1].activeBuffs.append("bowling ball")
                pm(window,"You now have a bowling ball")
            if yesno == "No":
                break
            
        elif str.find(i, "shuffle item orbs") >= 0:
            itemsMenu.close()
            gameBoard[x][y][1].storedItems.remove("shuffle item orbs")
            
            orbList = []
            for i in gameBoard:
                for j in i:
                    if j[0].tileType == "itemOrb":
                        orbList.append("itemOrb")
                        j[0].tileType = "default"
                        displayBoard(window, gameBoard)
                        window.refresh()
                    elif j[0].tileType == "trap Orb 0":
                        orbList.append("trap Orb 0")
                        j[0].tileType = "default"
                        displayBoard(window, gameBoard)
                        window.refresh()
                    elif j[0].tileType == "trap Orb 1":
                        orbList.append("trap Orb 1")
                        j[0].tileType = "default"
                        displayBoard(window, gameBoard)
                        window.refresh()
                    elif j[0].tileType == "trap Orb 2":
                        orbList.append("trap Orb 2")
                        j[0].tileType = "default"
                        displayBoard(window, gameBoard)
                        window.refresh()
                    else:
                        continue
                    
            emptyList = emptySpots(gameBoard)
            random.shuffle(emptyList)
            random.shuffle(orbList)

            for iIndex,i in enumerate(orbList):
                emptyX = emptyList[iIndex][0]
                emptyY = emptyList[iIndex][1]
                gameBoard[emptyX][emptyY][0].tileType = i
                displayBoard(window, gameBoard)
                window.refresh()
            window["information"].update(text_color = "Blue")
            
            pm(window,"All orbs (including any potential trap orbs) have been shuffled.")
            window.refresh()
            sleep(2)
            window["information"].update(text_color = "white")
            
            
        elif str.find(i, "magnet") >= 0:
            gameBoard[x][y][1].storedItems.remove("magnet")
            itemsMenu.close()
            g = gameBoard
            playerTurn = gameBoard[x][y][1].ownedBy
            innerRadial = getRadial(location, gameBoard)
            legalOuterList = []
            # each coordinate corresponds to a part of the outer ring.  tb = top/bottom, m = middle, lr = left/right
            coordList = [
                (x - 2, y - 2, "tll"),
                (x - 2, y - 1, "tml"),
                (x - 2, y, "tm"),
                (x - 2, y + 1, "tmr"),
                (x - 2, y + 2, "trr"),
                (x - 1, y - 2, "mlt"),
                (x - 1, y + 2, "mrt"),
                (x, y - 2, "ml"),
                (x, y + 2, "mr"),
                (x + 1, y - 2, "mlb"),
                (x + 1, y + 2, "mrb"),
                (x + 2, y - 2, "bll"),
                (x + 2, y - 1, "bml"),
                (x + 2, y, "bm"),
                (x + 2, y + 1, "bmr"),
                (x + 2, y + 2, "brr"),
            ]
            for i in coordList:
                radValue = getOuterRadialOnly(i, gameBoard)
                if radValue == -1:
                    continue
                else:
                    legalOuterList.append(i)
        
            forceFieldUsed = False
            death = False
            itemOrbDeath = False
            for i in innerRadial:
                ix = i[0]
                iy = i[1]
                # explosive list
                # if the tile has a mine or trap orb
                if g[ix][iy][0].tileType in [
                    "mine",
                    "AI bomb",
                    "trap Orb 0",
                    f"trap Orb {enemyTurn}",
                ]:
                    if g[ix][iy][0].tileType in ["trap Orb 0", f"trap Orb {enemyTurn}"]:
                        itemOrbDeath = True
                    if "Energy Forcefield" in g[x][y][1].activeBuffs:
                        forceFieldUsed = True
                    else:
                        death = True
                    # set the tile as empty
                    g[ix][iy][0].tileType = "default"
                    displayBoard(window, gameBoard)
                    sleep(0.1)
                    window.refresh()

                # if an item orb exists in the inner circle, pick it up
                if (
                    g[ix][iy][0].tileType == "itemOrb"
                    and "stunned" not in g[x][y][1].activeDebuffs
                ):
                    g[ix][iy][0].tileType = "default"
                    pickUpItemOrb(gameBoard, x, y)
                    pm(window, "You picked up an item")
                    displayBoard(window, gameBoard)
                    sleep(0.1)
                    window.refresh()

            if itemOrbDeath == True:
                pm(window, "A hostile trap orb was sucked in!")
            if forceFieldUsed == True:
                pm(window, "You were saved from explosives by your forcefield")
                g[x][y][1].activeBuffs.remove("Energy Forcefield")
                displayBoard(window, gameBoard)
                sleep(0.1)
                window.refresh()
            if death == True:
                g[x][y][0].tileType = "mine"
                deathCheck(window, gameBoard)

            #for every spot that exists in the outer ring that isn't off the playing field
            for i in legalOuterList:
                mappedValue = mapping(i)
                #out (x/y) = outer x/y
                outx = i[0]
                outy = i[1]
                #i(x/y) means inner x/y
                ix = mappedValue[0]
                iy = mappedValue[1]

                # if the inner slot is empty
                if g[ix][iy][0].occupied == False:
                    # copy the outer location into the center
                    g[ix][iy] = copy.deepcopy(g[outx][outy])
                    g[outx][outy][0].occupied = False
                    g[outx][outy][0].tileType = "default"
                    g[outx][outy][1] = 0
                    displayBoard(window, gameBoard)
                    sleep(0.3)
                    window.refresh()
                
                if g[ix][iy][0].occupied == True:
                    if g[outx][outy][0].tileType == "itemOrb":

                        g[ix][iy][0].tileType = "itemOrb"

                        if (
                            g[ix][iy][1].ownedBy == playerTurn
                            and "stunned" not in g[ix][iy][1].activeDebuffs
                        ):
                            pm(window, "You picked up an item")
                            pickUpItemOrb(gameBoard, ix, iy)

                        elif (
                            g[ix][iy][1].ownedBy == enemyTurn
                            and "stunned" not in g[ix][iy][1].activeDebuffs
                        ):
                            pm(window, "Your opponent picked up an item")
                            pickUpItemOrb(gameBoard, ix, iy)

                        g[outx][outy][0].tileType = "default"

                    if g[outx][outy][0].tileType in [
                        "mine",
                        "trap orb 1",
                        "trap orb 0",
                        "trap orb 2",
                        
                    ] or True in (g[outx][outy][0].horiLaser,g[outx][outy][0].vertLaser,g[outx][outy][0].crossLaser) :

                        g[ix][iy][0].tileType = g[outx][outy][0].tileType
                        death = deathCheck(window, gameBoard)
                        if death == "death":
                            displayBoard(window, gameBoard)
                            sleep(0.1)
                            window.refresh()
                        return

            displayBoard(window, gameBoard)
            sleep(0.1)
            window.refresh()

        # trip mine radial
        elif str.find(i, "trip mine radial") >= 0:
            gameBoard[x][y][1].storedItems.remove("trip mine radial")
            validTargets = getRadial((x, y), gameBoard)

            for i in validTargets:
                g = gameBoard[i[0]][i[1]]

                if g[0].occupied == True:

                    if g[1].ownedBy != playerTurn:
                        g[1].activeDebuffs.append("trip mine")
                        pm(window, "Trip mine has been placed")
                        window.refresh()
                        sleep(0.5)
                        # add code for graphics

        # suicide bomb column
        elif str.find(i, "suicide bomb column") >= 0:
            gameBoard[x][y][1].storedItems.remove("suicide bomb column")
            # for each item inside the specific gameBoard row
            for j in gameBoard:
                if isinstance(j[y][1], Piece):
                    if "Energy Forcefield" in j[y][1].activeBuffs:

                        j[y][1].activeBuffs.remove("Energy Forcefield")

                    else:
                        # set the tile to be empty
                        j[y][0].occupied = False
                        j[y][1] = 0
                        j[y][0].tileType = "default"

        # suicide bomb radial
        elif str.find(i, "suicide bomb radial") >= 0:
            gameBoard[x][y][1].storedItems.remove("suicide bomb radial")
            validTargets = getRadial((x, y), gameBoard)

            for i in validTargets:
                x = i[0]
                y = i[1]

                if isinstance(gameBoard[x][y][1], Piece):
                    if "Energy Forcefield" in gameBoard[x][y][1].activeBuffs:

                        gameBoard[x][y][1].activeBuffs.remove("Energy Forcefield")

                    else:
                        # set the tile to be empty
                        gameBoard[x][y][0].occupied = False
                        gameBoard[x][y][1] = 0
                        gameBoard[x][y][0].tileType = "default"

        # napalm row
        elif str.find(i, "napalm row") >= 0:
            gameBoard[x][y][1].storedItems.remove("napalm row")
            # for each column inside the row
            for j in gameBoard[x]:
                if isinstance(j[1], Piece):

                    # if there is a piece
                    if j[0].occupied == True:

                        # if it's the enemy's piece
                        if j[1].ownedBy != playerTurn:
                            # test for forcefield
                            if "Energy Forcefield" in j[1].activeBuffs:
                                backupTile = j[0].tileType
                                j[0].tileType = "exploding"
                                displayBoard(window, gameBoard)
                                window.refresh()
                                sleep(1)
                                j[0].tileType = backupTile
                                j[1].activeBuffs.remove("Energy Forcefield")
                                continue
                            # if no forcefield, kill
                            else:

                                j[0].occupied = False
                                j[1] = 0
                                j[0].tileType = "exploding"
                                displayBoard(window, gameBoard)
                                window.refresh()
                                sleep(1)
                                j[0].tileType = "destroyed"
                                continue
                    # if there isn't a piece
                    else:
                        formerTileType = j[0].tileType
                        j[0].tileType = "exploding"
                        displayBoard(window, gameBoard)
                        window.refresh()
                        sleep(1)

                        j[0].tileType = formerTileType
                        displayBoard(window, gameBoard)
                        window.refresh()
                        sleep(1)

        # napalm column
        elif str.find(i, "napalm column") >= 0:
            gameBoard[x][y][1].storedItems.remove("napalm column")
            # for each item inside the specific gameBoard row
            for j in gameBoard:
                if isinstance(j[y][1], Piece):

                    # if there is a piece
                    if j[y][0].occupied == True:

                        # if it's the enemy's piece
                        if j[y][1].ownedBy != playerTurn:
                            # test for forcefield
                            if "Energy Forcefield" in j[y][1].activeBuffs:
                                backupTile = gameBoard[j][y][0].tileType
                                j[y][0].tileType = "exploding"
                                displayBoard(window, gameBoard)
                                window.refresh()
                                sleep(1)
                                j[y][0].tileType = backupTile
                                j[y][1].activeBuffs.remove("Energy Forcefield")
                                continue
                            # if no forcefield, kill
                            else:
                                j[y][0].occupied = False
                                j[y][1] = 0
                                j[y][0].tileType = "exploding"
                                displayBoard(window, gameBoard)
                                window.refresh()
                                sleep(1)
                                j[y][0].tileType = "destroyed"
                                continue
                    # if there isn't a piece
                    else:
                        formerTileType = gameBoard[x][y][0].tileType
                        gameBoard[x][y][0].tileType = "exploding"
                        displayBoard(window, gameBoard)
                        window.refresh()
                        sleep(1)

                        gameBoard[x][y][0].tileType = formerTileType
                        displayBoard(window, gameBoard)
                        window.refresh()
                        sleep(1)

        # napalm Radial
        elif str.find(i, "napalm radial") >= 0:
            gameBoard[x][y][1].storedItems.remove("napalm radial")
            validSpots = getRadial((x, y), gameBoard)
            for i in validSpots:

                g = gameBoard[i[0]][i[1]]

                # if there's a piece
                if g[0].occupied == True:

                    if g[1].ownedBy != playerTurn:
                        # test for forcefield
                        if "Energy Forcefield" in g[1].activeBuffs:
                            backupTile = g[0].tileType
                            g[0].tileType = "exploding"
                            displayBoard(window, gameBoard)
                            window.refresh()
                            sleep(1)
                            g[0].tileType = backupTile
                            g[1].activeBuffs.remove("Energy Forcefield")
                            continue
                        # if no forcefield, kill
                        else:
                            g[0].occupied = False
                            g[1] = 0
                            g[0].tileType = "exploding"
                            displayBoard(window, gameBoard)
                            window.refresh()
                            sleep(1)
                            g[0].tileType = "destroyed"
                            continue
                    # if there isn't a piece
                    else:
                        formerTileType = g[0].tileType
                        g[0].tileType = "exploding"
                        displayBoard(window, gameBoard)
                        window.refresh()
                        sleep(1)

                        g[0].tileType = formerTileType
                        displayBoard(window, gameBoard)
                        window.refresh()
                        sleep(1)

        # shuffle column
        elif str.find(i, "shuffle column") >= 0:
            itemsMenu.close()
            g = gameBoard
            if g[x][y][1].grey == True:
                g[x][y][1].currentTurnPiece = True
                g[x][y][1].grey = False
            cg = []
            locations = []
            g[x][y][1].storedItems.remove("shuffle column")
            # for rows called i, in gameboard
            x = 0

            laserCheck(window, gameBoard, resetOnly = True)
            for i in g:
                # copy the column's tiles to cg    
                cg.append(copy.deepcopy(i[y]))
                locations.append((x, y))
                g[x][y][0].tileType = "default"
                g[x][y][0].occupied = False
                displayBoard(window, g)
                window.refresh()
                sleep(0.1)
                x += 1

            # shuffle locations to look cooler?
            random.shuffle(locations)
            # shuffle locations to look cooler?

            displayBoard(window, gameBoard)
            window.refresh()
            
            while len(locations) > 0:
                
                randCoord = random.choice(locations)
                randTileInfo = random.choice(cg)
                g[randCoord[0]][randCoord[1]] = randTileInfo
                locations.remove(randCoord)
                cg.remove(randTileInfo)
                #laserChecks
                g[randCoord[0]][randCoord[1]][0].horiLaser = False
                displayBoard(window, g)
                window.refresh()
                sleep(0.1)
            laserCheck(window, gameBoard)
            displayBoard(window, g)

        # shuffle radial
        elif str.find(i, "shuffle radial") >= 0:
            itemsMenu.close()
            g = gameBoard
            if g[x][y][1].grey == True:
                g[x][y][1].currentTurnPiece = True
                g[x][y][1].grey = False
            #cg is copiedGameBoard
            cg = []
            locations = getRadial((x, y), gameBoard)

            # shuffle the locations to look cooler?
            random.shuffle(locations)
            # shuffle the locations to look cooler?

            g[x][y][1].storedItems.remove("shuffle radial")
            storedWarpLocations = []
            storedWarpTurns = []
            laserCheck(window, gameBoard, resetOnly = True)
            for i in locations:
                x = i[0]
                y = i[1]
                #if g[x][y][0].recallTurn == True:
                cg.append(copy.deepcopy(g[x][y]))
                #might cause crashes; disabled to make recall work with shuffle
                g[x][y][0].tileType = "default"
                g[x][y][0].occupied = False
                displayBoard(window, g)
                window.refresh()
                sleep(0.1)

            while len(locations) > 0:
                randCoord = random.choice(locations)
                randTileInfo = random.choice(cg)
                g[randCoord[0]][randCoord[1]] = randTileInfo
                
                locations.remove(randCoord)
                cg.remove(randTileInfo)
                g[randCoord[0]][randCoord[1]][0].horiLaser = False
                g[randCoord[0]][randCoord[1]][0].vertLaser = False
                g[randCoord[0]][randCoord[1]][0].crossLaser = False
                
                displayBoard(window, g)
                window.refresh()
                sleep(0.1)
            laserCheck(window, gameBoard)    
            displayBoard(window, g)

        # purify radial
        elif str.find(i, "purify radial") >= 0:
            gameBoard[x][y][1].storedItems.remove("purify radial")
            validSpots = getRadial((x, y), gameBoard)
            cleanCheck = False
            itemsMenu.close()
            for i in validSpots:

                g = gameBoard[i[0]][i[1]]

                # if there's a piece
                if g[0].occupied == True:

                    if g[1].ownedBy == playerTurn:

                        if len(g[1].activeDebuffs) > 0:
                            pm(window, "Purifying...")
                            for i in g[1].activeDebuffs:
                                cleanCheck = True
                                previousTile = g[0].tileType
                                g[1].activeBuffs.append("purified0")
                                displayBoard(window, gameBoard)
                                window.refresh()
                                # sleep(.01)
                                g[1].activeBuffs.append("purified1")
                                displayBoard(window, gameBoard)
                                window.refresh()
                                # sleep(.01)
                                g[1].activeBuffs.append("purified2")
                                displayBoard(window, gameBoard)
                                window.refresh()
                                # sleep(.01)
                                g[1].activeBuffs.remove("purified0")
                                g[1].activeBuffs.remove("purified1")
                                g[1].activeBuffs.remove("purified2")
                                listOfDebuffs = ""
                                for j in g[1].activeDebuffs:
                                    listOfDebuffs += j + "\n"
                                pm(window, f"Removed:  {listOfDebuffs}")
                                g[1].activeDebuffs.clear()
                                # check this for deletions on window information

                                window["information"].update(text_color="blue")
                                window.refresh()
                                # sleep(.5)
                                window["information"].update(text_color="white")
                                g[0].tileType = previousTile
                                displayBoard(window, gameBoard)
                                window.refresh()
                                # sleep(.5)

            if cleanCheck == False:

                window["information"].update(text_color="red")
                pm(
                    window,
                    f"No corrupted allies were in range. Nothing happened. Well, that was a pointless waste.",
                )
                window.refresh()
                sleep(1)
                window["information"].update(text_color="white")

        # move diagonal
        elif str.find(i, "move diagonal") >= 0:
            gameBoard[x][y][1].storedItems.remove("move diagonal")
            gameBoard[x][y][1].activeBuffs.append("move diagonal")

        # place mine
        elif str.find(i, "place mine") >= 0:
            itemsMenu.close()
            validLocations = getRadial(location, gameBoard)
            validLocations = filterEmpty(gameBoard, validLocations)

            pm(window, "Where would you like to place the mine?")
            event = window.read()
            if (event[0][0], event[0][1]) in validLocations:

                pm(window, f"mine placed at {event[0][0],event[0][1]}")
                gameBoard[event[0][0]][event[0][1]][0].tileType = "mine"
                gameBoard[x][y][1].storedItems.remove("place mine")
                displayBoard(window, gameBoard)
                window.refresh()
                continue
            else:
                pm(window, "Can't place mine there.  Only in an ampty space in range.")
                continue

        # trap orb
        elif str.find(i, "trap orb") >= 0:
            itemsMenu.close()
            validLocations = getRadial(location, gameBoard)
            validLocations = filterEmpty(gameBoard, validLocations)

            pm(window, "Where would you like to place the trap?")
            event = window.read()
            if (event[0][0], event[0][1]) in validLocations:

                pm(window, "Done.")
                gameBoard[event[0][0]][event[0][1]][
                    0
                ].tileType = f"trap orb {playerTurn}"
                gameBoard[x][y][1].storedItems.remove("trap orb")
                displayBoard(window, gameBoard)
                window.refresh()
                continue
            else:
                pm(window, "Can't place that there.  Only in an ampty space in range.")
                continue

        # vile radial
        elif str.find(i, "vile radial") >= 0:
            gameBoard[x][y][1].storedItems.remove("vile radial")
            validSpots = getRadial((x, y), gameBoard)
            abolishCheck = False
            itemsMenu.close()
            for i in validSpots:

                g = gameBoard[i[0]][i[1]]

                # if there's a piece
                if g[0].occupied == True:

                    if g[1].ownedBy != playerTurn:
                        if len(g[1].activeBuffs) > 0:
                            pm(window, "abolishing")
                            
                            for i in g[1].activeBuffs:
                                abolishCheck = True
                                previousTile = g[0].tileType
                                g[1].activeDebuffs.append("abolished")
                                displayBoard(window, gameBoard)
                                window.refresh()
                                g[1].activeDebuffs.remove("abolished")
                                
                                listOfBuffs = ""
                                for j in g[1].activeBuffs:
                                    listOfBuffs += j + "\n"
                                pm(window, f"Removed\n{listOfBuffs}")
                                g[1].activeBuffs.clear()
                                window["information"].update(text_color="blue")
                                window.refresh()
                                
                                window["information"].update(text_color="white")
                                g[0].tileType = previousTile
                                displayBoard(window, gameBoard)
                                window.refresh()
                                

            if abolishCheck == False:
                pm(
                    window,
                    f"No powered enemies were in range. Nothing happened. Well, that was a pointless waste.",
                )
                window["information"].update(text_color="red")
                window.refresh()
                sleep(1)
                window["information"].update(text_color="white")

        # energy forcefield
        elif str.find(i, "Energy Forcefield") >= 0:
            gameBoard[x][y][1].storedItems.remove("Energy Forcefield")
            gameBoard[x][y][1].activeBuffs.append("Energy Forcefield")
            displayBoard(window, gameBoard)

        # move again
        elif str.find(i, "move again") >= 0:
            gameBoard[x][y][1].storedItems.remove("move again")
            gameBoard[x][y][1].activeBuffs.append("move again")
            gameBoard[x][y][1].moveAgain += 1

            pm(
                window,
                f"Activated move again.  Bonus moves per turn: {gameBoard[x][y][1].moveAgain}",
            )
            displayBoard(window, gameBoard)

        # haymaker
        elif str.find(i, "haymaker") >= 0:
            itemsMenu.close()
            validTargets = getCross((x, y), gameBoard)
            pm(window, "Pick a target that is within range.")
            event = window.read()

            # if the target is within range
            if event[0] in validTargets:
                

                # s1 is the victim's start row, compare to x
                s1 = event[0][0]

                # s2 is the victim's start column, compare to y
                s2 = event[0][1]
                if gameBoard[s1][s2][0].occupied == False:
                    pm(window, "There's no one to punch at that location!")
                    itemsMenu.close()
                    return

                gameBoard[x][y][1].storedItems.remove("haymaker")
                direction = 0
                # if they are in the same row:
                if x == s1:
                    # if x is to the left of the target
                    if y < s2:
                        direction = "push right"
                    # if it's to the right:
                    else:
                        direction = "push left"
                # if they're in the same column
                elif y == s2:
                    # if the target is below:
                    if x < s1:
                        
                        direction = "push down"
                    # if the target is above
                    else:
                        direction = "push up"

                else:
                    sg.popup(
                        "ERROR IN HAYMAKER DIRECTION CALCULATION", keep_on_top=True
                    )

                if direction == "push down":
                    
                    #######TRIPMINE FORCEFIELD CHECK NEEDED#####

                    # copy the original piece
                    tempCopyVictim = copy.deepcopy(gameBoard[s1][s2][1])
                    tempCopyTileType = "default"
                    lastTurnTileType = "default"
                    while True:
                        # check for lower wall

                        if s1 == rows - 1:
                            gameBoard[s1][s2][1].activeDebuffs.append("stunned")
                            #######TRIPMINE FORCEFIELD CHECK NEEDED#####
                            break

                        # if the next block is empty
                        elif gameBoard[s1 + 1][s2][0].occupied == False:

                            # if the next location is a hole
                            if gameBoard[s1 + 1][s2][0].tileType in [
                                "destroyed",
                                "damaged4",
                                "damaged3",
                                "damaged2",
                                "damaged",
                            ]:
                                # kill the piece
                                gameBoard[s1][s2][1] = 0
                                gameBoard[s1][s2][0].tileType = "default"
                                gameBoard[s1][s2][0].occupied = False
                                
                                pm(
                                    window,
                                    "Brutal!  You just pushed that piece into the void.",
                                )
                                break

                            # if the next location is safe to spawn in (as in it won't break the game; might still be deadly to the piece)
                            else:
                                #copy the tile type
                                g = gameBoard
                                sx = s1
                                sy = s2
                                ex = sx+1
                                ey = sy
                                
                                tempPrevTileType = g[sx][sy][0].tileType
                                tempPrevPiece = copy.deepcopy(g[sx][sy][1])

                                
                                startBoard = g[sx][sy]
                                endBoard = g[ex][ey]

                                startBoard[0].occupied = False
                                startBoard[0].tileType = lastTurnTileType

                                
                                lastTurnTileType = endBoard[0].tileType
                                endBoard[0].occupied = True
                                endBoard[1] = copy.deepcopy(tempPrevPiece)
                                
                                #check to see if dead
                                death = deathCheck(window, gameBoard, move=True)
                                if death != "death":
                                    death2 = tripMineCheck(
                                        window, gameBoard, s1 + 1, s2
                                    )
                                if death == "death" or death2 == "death":
                                    return

                                displayBoard(window, gameBoard)
                                window.refresh()
                                s1 += 1
                                

                        elif gameBoard[s1 + 1][s2][0].occupied == True:

                            gameBoard[s1][s2][1].activeDebuffs.append("stunned")
                            gameBoard[s1 + 1][s2][1].activeDebuffs.append("stunned")
                            pm(window, "Both of the collided pieces are stunned.")
                            break
                    
                
                elif direction == "push up":
                    #######TRIPMINE FORCEFIELD CHECK NEEDED#####

                    # copy the original piece
                    tempCopyVictim = copy.deepcopy(gameBoard[s1][s2][1])

                    tempCopyTileType = "default"
                    lastTurnTileType = "default"
                    while True:
                        # check for upper wall

                        if s1 == 0:
                            gameBoard[s1][s2][1].activeDebuffs.append("stunned")
                            #######TRIPMINE FORCEFIELD CHECK NEEDED#####
                            break

                        # if the next block is empty
                        elif gameBoard[s1 - 1][s2][0].occupied == False:

                            # do laser or land mine check here

                            # end laser or land mine check here

                            # if the next location is a hole
                            if gameBoard[s1 - 1][s2][0].tileType in [
                                "destroyed",
                                "damaged4",
                                "damaged3",
                                "damaged2",
                                "damaged",
                            ]:
                                # kill the piece
                                gameBoard[s1][s2][1] = 0
                                gameBoard[s1][s2][0].tileType = "default"
                                gameBoard[s1][s2][0].occupied = False
                                pm(
                                    window,
                                    "Brutal!  You just pushed that piece into the void.",
                                )
                                break

                            # if the next location is safe
                            else:






                                #copy the tile type
                                g = gameBoard
                                sx = s1
                                sy = s2
                                ex = sx-1
                                ey = sy
                                
                                tempPrevTileType = g[sx][sy][0].tileType
                                tempPrevPiece = copy.deepcopy(g[sx][sy][1])

                                
                                startBoard = g[sx][sy]
                                endBoard = g[ex][ey]

                                startBoard[0].occupied = False
                                startBoard[0].tileType = lastTurnTileType
                                startBoard[1] = 0

                                
                                lastTurnTileType = endBoard[0].tileType
                                endBoard[0].occupied = True
                                endBoard[1] = copy.deepcopy(tempPrevPiece)
                                
                                #check to see if dead
                                death = deathCheck(window, gameBoard, move=True)
                                if death != "death":
                                    death2 = tripMineCheck(
                                        window, gameBoard, s1 - 1, s2
                                    )
                                if death == "death" or death2 == "death":
                                    return

                                displayBoard(window, gameBoard)
                                window.refresh()
                                s1 -= 1


                        elif gameBoard[s1 - 1][s2][0].occupied == True:

                            gameBoard[s1][s2][1].activeDebuffs.append("stunned")
                            gameBoard[s1 - 1][s2][1].activeDebuffs.append("stunned")
                            pm(window, "Both of the collided pieces are stunned.")
                            break

                elif direction == "push right":

                    #######TRIPMINE FORCEFIELD CHECK NEEDED#####

                    # copy the piece that you are punching
                    tempCopyVictim = copy.deepcopy(gameBoard[s1][s2][1])
                    tempCopyTileType = "default"
                    lastTurnTileType = "default"
                    while True:
                        # check for right wall

                        if s2 == columns - 1:
                            gameBoard[s1][s2][1].activeDebuffs.append("stunned")
                            #######TRIPMINE FORCEFIELD CHECK NEEDED#####
                            break

                        # if the next block is empty
                        elif gameBoard[s1][s2 + 1][0].occupied == False:

                            # do laser or land mine check here

                            # end laser or land mine check here

                            # if the next location is a hole
                            if gameBoard[s1][s2 + 1][0].tileType in [
                                "destroyed",
                                "damaged4",
                                "damaged3",
                                "damaged2",
                                "damaged",
                            ]:
                                # kill the piece
                                gameBoard[s1][s2][1] = 0
                                gameBoard[s1][s2][0].tileType = "default"
                                gameBoard[s1][s2][0].occupied = False
                                pm(
                                    window,
                                    "Brutal!  You just pushed that piece into the void.",
                                )
                                break

                            # if the next location is safe
                            else:

                                #copy the tile type
                                g = gameBoard
                                sx = s1
                                sy = s2
                                ex = sx
                                ey = sy+1
                                
                                tempPrevTileType = g[sx][sy][0].tileType
                                tempPrevPiece = copy.deepcopy(g[sx][sy][1])

                                
                                startBoard = g[sx][sy]
                                endBoard = g[ex][ey]

                                startBoard[0].occupied = False
                                startBoard[0].tileType = lastTurnTileType
                                startBoard[1] = 0

                                
                                lastTurnTileType = endBoard[0].tileType
                                endBoard[0].occupied = True
                                endBoard[1] = copy.deepcopy(tempPrevPiece)
                                
                                #check to see if dead
                                death = deathCheck(window, gameBoard, move=True)
                                if death != "death":
                                    death2 = tripMineCheck(
                                        window, gameBoard, s1, s2+1
                                    )
                                if death == "death" or death2 == "death":
                                    return

                                displayBoard(window, gameBoard)
                                window.refresh()
                                s2 += 1

                        elif gameBoard[s1][s2 + 1][0].occupied == True:

                            gameBoard[s1][s2][1].activeDebuffs.append("stunned")
                            gameBoard[s1][s2 + 1][1].activeDebuffs.append("stunned")
                            pm(window, "Both of the collided pieces are stunned.")
                            break

                elif direction == "push left":

                    #######TRIPMINE FORCEFIELD CHECK NEEDED#####

                    # copy the original piece
                    tempCopyVictim = copy.deepcopy(gameBoard[s1][s2][1])
                    tempCopyTileType = "default"
                    lastTurnTileType = "default"
                    while True:
                        # check for left

                        if s2 == 0:
                            gameBoard[s1][s2][1].activeDebuffs.append("stunned")
                            #######TRIPMINE FORCEFIELD CHECK NEEDED#####
                            break

                        # if the next block is empty
                        elif gameBoard[s1][s2 - 1][0].occupied == False:

                            # do laser or land mine check here

                            # end laser or land mine check here

                            # if the next location is a hole
                            if gameBoard[s1][s2 - 1][0].tileType in [
                                "destroyed",
                                "damaged4",
                                "damaged3",
                                "damaged2",
                                "damaged",
                            ]:
                                # kill the piece
                                gameBoard[s1][s2][1] = 0
                                gameBoard[s1][s2][0].tileType = "default"
                                gameBoard[s1][s2][0].occupied = False
                                pm(
                                    window,
                                    "Brutal!  You just pushed that piece into the void.",
                                )
                                break

                            # if the next location is safe
                            else:

                                #copy the tile type
                                g = gameBoard
                                sx = s1
                                sy = s2
                                ex = sx
                                ey = sy-1
                                
                                tempPrevTileType = g[sx][sy][0].tileType
                                tempPrevPiece = copy.deepcopy(g[sx][sy][1])

                                
                                startBoard = g[sx][sy]
                                endBoard = g[ex][ey]

                                startBoard[0].occupied = False
                                startBoard[0].tileType = lastTurnTileType

                                
                                lastTurnTileType = endBoard[0].tileType
                                endBoard[0].occupied = True
                                endBoard[1] = copy.deepcopy(tempPrevPiece)
                                
                                #check to see if dead
                                death = deathCheck(window, gameBoard, move=True)
                                if death != "death":
                                    death2 = tripMineCheck(
                                        window, gameBoard, s1, s2-1
                                    )
                                if death == "death" or death2 == "death":
                                    return

                                displayBoard(window, gameBoard)
                                window.refresh()
                                s2 -= 1

                        elif gameBoard[s1][s2 - 1][0].occupied == True:

                            gameBoard[s1][s2][1].activeDebuffs.append("stunned")
                            gameBoard[s1][s2 - 1][1].activeDebuffs.append("stunned")
                            pm(window, "Both of the collided pieces are stunned.")
                            break
            else:
                sg.popup("Pick something in range!", keep_on_top=True)
        # jump proof
        elif str.find(i, "jump proof") >= 0:
            gameBoard[x][y][1].storedItems.remove("jump proof")
            gameBoard[x][y][1].activeBuffs.append("jump proof")
            displayBoard(window, gameBoard)
            pm(window, "Congrats; your piece can't be jumped on.")

        # wololo
        elif str.find(i, "Wololo (convert to your side)") >= 0:
            itemsMenu.close()
            pm(window, "Choose an enemy to recruit")

            event = window.read()
            player = gameBoard[x][y][1].ownedBy
            if player == 1:
                enemy = 2
            elif player == 2:
                enemy = 1
            if gameBoard[event[0][0]][event[0][1]][1] == 0:
                pm(window, "Choose an enemy, not a vacant tile...")
                continue
            elif gameBoard[event[0][0]][event[0][1]][1].ownedBy == enemy:
                gameBoard[event[0][0]][event[0][1]][1].ownedBy = player
                gameBoard[x][y][1].storedItems.remove("Wololo (convert to your side)")
            else:
                pm(window, "Wololo only works on enemies.")
                sleep(1)
            displayBoard(window, gameBoard)
            window.refresh()

        # haphazard airstrike
        elif str.find(i, "haphazard airstrike") >= 0:

            gameBoard[x][y][1].storedItems.remove("haphazard airstrike")
            i = 5
            itemsMenu.close()
            while i > 0:
                i -= 1

                x = random.randint(0, len(gameBoard) - 1)
                y = random.randint(0, len(gameBoard[0]) - 1)

                # if someone is on the spot
                if gameBoard[x][y][0].occupied == True:
                    # if someone has a forcefield there, don't kill them
                    if "Energy Forcefield" in gameBoard[x][y][1].activeBuffs:
                        backupTile = gameBoard[x][y][0].tileType
                        gameBoard[x][y][0].tileType = "exploding"
                        displayBoard(window, gameBoard)
                        window.refresh()
                        sleep(1)
                        gameBoard[x][y][0].tileType = backupTile
                        gameBoard[x][y][1].activeBuffs.remove("Energy Forcefield")
                        continue
                    else:
                        gameBoard[x][y][0].occupied = False
                        gameBoard[x][y][1] = 0
                        gameBoard[x][y][0].tileType = "exploding"
                        displayBoard(window, gameBoard)
                        window.refresh()
                        sleep(1)
                        gameBoard[x][y][0].tileType = "destroyed"
                        continue

                else:
                    gameBoard[x][y][0].occupied = False
                    gameBoard[x][y][1] = 0
                    gameBoard[x][y][0].tileType = "exploding"
                    displayBoard(window, gameBoard)
                    window.refresh()
                    sleep(1)
                    gameBoard[x][y][0].tileType = "destroyed"

        # smartBombs
        elif str.find(i, "smart bombs") >= 0:
            attempts = 0
            gameBoard[x][y][1].storedItems.remove("smart bombs")
            i = 3
            itemsMenu.close()
            while i > 0:
                i -= 1
                # a check to make sure the plane doesn't get stuck in a pseudo infinite loop in case of special scenarios where pretty much the entire field is full of allied squares
                attempts += 1
                if attempts > 100:
                    sg.popup(
                        "The plane had trouble finding targets, so it flew away early.",
                        keep_on_top=True,
                    )
                    pm(
                        window,
                        "The plane had trouble finding targets, so it flew away early.",
                    )
                    if itemsMenu:
                        itemsMenu.close()
                    break

                # generate a random target location on the field
                x = random.randint(0, len(gameBoard) - 1)
                y = random.randint(0, len(gameBoard[0]) - 1)

                # if someone is on the spot
                if gameBoard[x][y][0].occupied == True:

                    # if the piece belongs to you, don't attack
                    if gameBoard[x][y][1].ownedBy == playerTurn:
                        # continue the loop by incrementing the conditional
                        i += 1
                        continue
                    # if someone has a forcefield there, don't kill them
                    if "Energy Forcefield" in gameBoard[x][y][1].activeBuffs:
                        backupTile = gameBoard[x][y][0].tileType
                        gameBoard[x][y][0].tileType = "exploding"
                        displayBoard(window, gameBoard)
                        window.refresh()
                        sleep(1)
                        gameBoard[x][y][0].tileType = backupTile
                        gameBoard[x][y][1].activeBuffs.remove("Energy Forcefield")
                        continue
                    # if the enemy is targeted and doesn't have a force field, kill them and the block
                    else:
                        gameBoard[x][y][0].occupied = False
                        gameBoard[x][y][1] = 0
                        gameBoard[x][y][0].tileType = "exploding"
                        displayBoard(window, gameBoard)
                        window.refresh()
                        sleep(1)
                        gameBoard[x][y][0].tileType = "destroyed"
                        continue

                # attack an unoccupied area
                else:
                    # smart bombs have a 20% chance of not hitting empty spaces.  If the 80% check succeeds, try a new spot.
                    redo = random.randint(0, 10)
                    if redo < 8:
                        i += 1
                        continue
                    # destroy the piece and the floor
                    gameBoard[x][y][0].occupied = False
                    gameBoard[x][y][1] = 0
                    gameBoard[x][y][0].tileType = "exploding"
                    displayBoard(window, gameBoard)
                    window.refresh()
                    sleep(1)
                    gameBoard[x][y][0].tileType = "destroyed"

        # snake tunneling
        elif str.find(i, "Snake Tunneling") >= 0:
            gameBoard[x][y][1].storedItems.remove("Snake Tunneling")

            i = 5
            lastSpace = (x, y)
            while i > 0:
                i -= 1

                validPoints = getCross((lastSpace[0], lastSpace[1]), gameBoard)
                attackSquare = random.choice(validPoints)
                s1 = attackSquare[0]
                s2 = attackSquare[1]
                if attackSquare == lastSpace:
                    i += 1
                    continue
                lastSpace = attackSquare
                pieceVictim = gameBoard[s1][s2][1]
                # tileVictim = gameBoard[s1][s2][0].tileType
                tileVictim = copy.deepcopy(gameBoard[s1][s2][0])
                # tileVictim = gameBoard[s1][s2][0]

                gameBoard[s1][s2][0].tileType = "snake"
                displayBoard(window, gameBoard)
                window.refresh()
                sleep(1)

                if gameBoard[s1][s2][0].occupied == True:
                    if gameBoard[s1][s2][1].ownedBy != playerTurn:
                        gameBoard[s1][s2][0].occupied = False
                        gameBoard[s1][s2][1] = 0
                        gameBoard[s1][s2][0].tileType = "exploding"
                        displayBoard(window, gameBoard)
                        window.refresh()
                        sleep(1)
                        gameBoard[s1][s2][0].tileType = "default"
                        displayBoard(window, gameBoard)
                        window.refresh()
                        sleep(1)

                        gameBoard[s1][s2][0].tileHeight = 3
                    else:
                        gameBoard[s1][s2][0] = copy.deepcopy(tileVictim)
                        gameBoard[s1][s2][0].tileHeight = 3
                else:
                    gameBoard[s1][s2][0] = copy.deepcopy(tileVictim)
                    gameBoard[s1][s2][0].tileHeight = 3

                displayBoard(window, gameBoard)
                window.refresh()
                sleep(1)

        # after using the menu, close it
        if itemsMenu:
            itemsMenu.close()
        
        if event[0] == "CANCEL":
            itemsMenu.close()
            return
        
def orbEater(gameBoard):
    listOfMice = []
    legalLocations = []
    orbsEaten = 0
    for iIndex,i in enumerate(gameBoard):
        for jIndex, j in enumerate(i):
            if j[0].orbEater == True:
                listOfMice.append( (iIndex,jIndex) )
    for i in listOfMice:
        ateOrb = False
        legalLocations.clear()
        legalLocations = getCross(i,gameBoard) #dang it, TJ!
        
        random.shuffle(legalLocations)
        if gameBoard[i[0]][i[1]][0].tileType in ( "itemOrb", "trap Orb 1", "trap Orb 2", "trap Orb 0"):
            #sg.popup("Orbeater was blessed with an orb!")
            gameBoard[i[0]][i[1]][0].tileType = "default"
            #make orbeater fat
            continue
        for j in legalLocations:

            #eat an orb
            if gameBoard[j[0]][j[1]][0].tileType in ( "itemOrb", "trap Orb 1", "trap Orb 2", "trap Orb 0"):
                gameBoard[i[0]][i[1]][0].orbEater = False
                gameBoard[j[0]][j[1]][0].tileType = "default"
                gameBoard[j[0]][j[1]][0].orbEater = True
                #change the picture to a fat mouse if he eats an orb; explode the mouse if it's a trap orb.  If he eats too many orbs, maybe make him crazy?
                
                orbsEaten+=1
                ateOrb = True
                break
            
        #if there wasn't a nearby orb, go somewhere else, if possible
        if ateOrb == False:
            random.shuffle(legalLocations)
            for j in legalLocations:
                if gameBoard[j[0]][j[1]][0].tileType == "default" and gameBoard[j[0]][j[1]][0].occupied == False:
                    gameBoard[i[0]][i[1]][0].orbEater = False
                    gameBoard[j[0]][j[1]][0].tileType = "default"
                    gameBoard[j[0]][j[1]][0].orbEater = True
                    break
                else:
                    continue
        
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
                        if gameBoard[curRow+1][curCol][0].tileType not in ("destroyed", "damaged4", "damaged3", "damaged2", "damaged"):

                            
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
                        if gameBoard[curRow-1][curCol][0].tileType not in ("destroyed", "damaged4", "damaged3", "damaged2", "damaged"):

                            
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
                        if gameBoard[curRow][curCol-1][0].tileType not in ("destroyed", "damaged4", "damaged3", "damaged2", "damaged"):

                            
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
                    
                    sg.popup("Slammed into wall?",keep_on_top=True)
                    return
    if direction == "Right":
        while True:
                #if the next spot is legal
                if curCol+1 < columns:

                    
                    # if there are no pieces on the next row
                    if gameBoard[curRow][curCol+1][0].occupied == False:

                        
                        #if the floor exists in the next row
                        if gameBoard[curRow][curCol+1][0].tileType not in ("destroyed", "damaged4", "damaged3", "damaged2", "damaged"):

                            
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
                        
                       
def repairFloor(window, gameBoard):
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

def findCurrentTurnPiece(window, gameBoard, reset = False):
    rowIndex = 0
    columnIndex = 0
    for i in gameBoard:
        columnIndex = 0
        for j in i:
            
            if j[0].occupied == True:
                
                if j[0].currentTurnPiece == True:
                    return (rowIndex,columnIndex)
            columnIndex +=1
            
        rowIndex +=1

def itemExplanation(itemName): 
     
    if itemName == "orb eater":
        sg.popup("A mouse spawns.  After each player's turn, the mouse will eat a close by item orb or trap orb that he finds.  If he doesn't find one, he will walk in a random direction.", keep_on_top = True)
    elif itemName == "row laser":
        sg.popup("Set up a laser emitter.  The laser will shoot all the way left and right, destroying any pieces it finds.  It does not affect item orbs or other non-player entities. It will not affect any other laser emitters.", keep_on_top = True)
    elif itemName == "magnet":
        sg.popup("Suck in any adjacent item orbs or bombs.  Afterwards, it'll suck in anything in the 4x4 square that is surrounding the adjacent 3x3 into the 3x3 if there is space.", keep_on_top = True)
    elif itemName == "trap orb":
        sg.popup("An explosive trap designed to look like an item orb.  They are indistinguishable.  Luckily, your traps will not affect you.", keep_on_top = True)
    elif itemName == "place mine":
        sg.popup("Place a mine next to you.  If either player steps on it, BOOM.", keep_on_top = True)
    elif itemName ==  "move again":
        sg.popup("After you activate this permanent buff, your piece will get to move again after moving.", keep_on_top = True)
    elif itemName ==  "suicide bomb row":
        sg.popup("Blow yourself up, killing everyone in the same row as you - including your allies.", keep_on_top = True)
    elif itemName == "Energy Forcefield":
        sg.popup("After activating it, you'll be surrounded by a forcefield. Protects you one time from most energy/explosive type attacks. It has no effect against modifiers, or against blunt attacks such as being jumped on or crushed, and will not protect you if the floor disappears.", keep_on_top = True)
    elif itemName == "suicide bomb column":
        sg.popup("Blow yourself up, killing everyone in the column.", keep_on_top = True)
    elif itemName == "haphazard airstrike":
        sg.popup("Call in an airstrike from a poorly funded army.  The plane cannot aim and will blow holes into the ground randomly, killing anything that was on the tile, including the floor itself", keep_on_top = True)
    elif itemName == "suicide bomb radial":
        sg.popup("Blow yourself up, killing you and anyone or anything next to you.", keep_on_top = True)
    elif itemName == "jump proof":
        sg.popup("Enemies cannot jump on you.  You may still be affected by anything else.", keep_on_top = True)
    elif itemName == "smart bombs":
        sg.popup("Call in an airstrike conducted by a sophisticated bomber. It will not hurt any of your pieces.  Leaves holes in the ground, destroying its targets.", keep_on_top = True)
    elif itemName == "move diagonal":
        sg.popup("After activating this buff, in addition to your usual spots, your piece can move to diagonal locations.", keep_on_top = True)
    elif itemName == "trip mine radial":
        sg.popup("Set mines on all surrounding enemies.  If they move, they blow up.  They can still safely use items that don't require them to move.  Teleporting is not considered moving.", keep_on_top = True)
    elif itemName == "purify radial":
        sg.popup("Remove all negative effects from surrounding allies.", keep_on_top = True)
    elif itemName == "napalm radial":
        sg.popup("Set all enemies in the surrounding area on fire.  This kills them and burns a hole in the ground.", keep_on_top = True)
    elif itemName == "vile radial":
        sg.popup("Remove all beneficial powers that your surrounding enemies possess.", keep_on_top = True)
    elif itemName == "haymaker":
        sg.popup("Punch an adjacent piece really hard.  The flying piece will keep going until it either slams into a piece/wall and stuns itself and the piece it collided into, or if it dies by moving into a danger location (laser beam/hole/mine/etc).  The piece will not be able to pick up any items as it passes over. ", keep_on_top = True)
    elif itemName == "bowling ball":
        sg.popup("Turn your piece into a feral bowling ball.  The bowling ball loses all effects that it has (positive and negative).  It can no longer pick up any items.  It no longer has access to normal movement.  Instead, if you select it, it will only allow you to choose a direction.  The bowling bar will fly toward that direction with sheer rage and be unaffeced by most negative effects, including bombs or mines.  It can still die by falling into holes.  It will continue going in a given direction until it slams into a wall or a piece.  If it hits a piece, it stuns allies and kills the enemy.", keep_on_top = True)
    elif itemName == "column laser":
        sg.popup("Set up a laser emitter.  The laser will shoot all the way up and down, destroying any pieces it finds.  It does not affect item orbs or other non-player entities and will not affect any other laser emitters.", keep_on_top = True)
    elif itemName == "shuffle column":
        sg.popup("Shuffle everything in the column randomly.  This does not set off tripmines as the pieces themselves are not actually moving - the tiles are, along with their tripmines.", keep_on_top = True)
    elif itemName == "shuffle radial":
        sg.popup("Shuffle everything in the surrounding randomly.  This does not set off tripmines as the pieces themselves are not actually moving - the tiles are, along with their tripmines.", keep_on_top = True)
    elif itemName == "spooky hand":
        sg.popup("After using this, a creepy hand will lurk under the playing field for the rest of the game.  Once every handful (see what I did there?) of turns, it'll pop up and abduct one piece from either player, taking the floor with it.", keep_on_top = True)
    elif itemName == "reproduce":
        sg.popup("Your piece spawns a cute baby.  The baby is a generic piece that has no powerups and is just like any other normal piece.", keep_on_top = True)
    elif itemName == "worm hole":
        sg.popup("Choose an empty location.  A worm hole replaces the tile.  As long as no on is on that tile, any of your pieces can teleport to there from anywhere.", keep_on_top = True)
    elif itemName == "warp":
        sg.popup("Your piece is randomly whisked away to an empty location.  Careful, it can make you end up in enemy territory... or just move you one space away... or anything in between.", keep_on_top = True)
    elif itemName == "recall":
        sg.popup("After a piece uses recall, it creates an unbreakable bond with the tile it cast it on and gets a snapshot of how it is in that exact moment.  In 10 turns, the piece will, no matter what, return to that tile in the state that it was at, even if it died.  If the tile is moved by any items before the recall occurs, the piece will appear in the location the tile was moved to.", keep_on_top = True)

    
def movePiece(playerTurn, window, gameBoard):
    # a small list that is used to make sure a player that gets a second turn for a piece can only use that specific piece twice
    repeatRestrictor = [False, (-1, -1)]
    pieceTeleported = False
    #startLocation = [0,0]
    startLocation = []
    roundEarthTheory = False
    rows = len(gameBoard)
    columns = len(gameBoard[0])
    while True:
        #flag for keeping track of pieces that were teleported
        if pieceTeleported == True:
            startLocation[0],startLocation[1] = findCurrentTurnPiece(window, gameBoard)
            gameBoard[startLocation[0]][startLocation[1]][1].currentTurnPiece = True
        displayBoard(window, gameBoard)
        pickedUpItem = False
        window["exit"].update(disabled=False)
        usedItem = False
        window["itemButton"].update(disabled=True)
        window["examineItem"].update(disabled=False)
        window["readItems"].update(disabled=False)
        window.refresh()
        
        window["playerTurn"].update(f"{playerTurn}")
        window["information"].update(text_color="white")

        # message for pick your piece to move
        pm(window, f"Pick a piece to move.")
        
        # check to see if this is your second (or higher) turn (you don't get to choose a new piece).  False means this isn't your second move
        if repeatRestrictor[0] == False:


            #FIRST PIECE PICK HERE - this is your initial selection option for choosing a piece
            event = window.read()


            #if you wanna cheat
            if "cheetz" in event:
                buffs = sg.popup_get_text("",keep_on_top = True)
                for i in gameBoard:
                    for j in i:
                        if j[0].occupied == True:
                            j[1].storedItems.append(buffs)
                continue


            #if exit is clicked
            if "exit" in event:
                a = sg.popup_yes_no(
                    "Seriously, you want to exit this awesome game?", keep_on_top=True
                )
                pm(window, "You're a fool if you're wanting to quit this game.")
                if a == "Yes":
                    sg.popup("Wow, your loss.", keep_on_top=True)
                    window.close()
                    raise SystemExit
                else:
                    continue

            #if player wants to examine a tile/piece
            if "examineItem" in event:
                window["examineItem"].update(disabled=True)
                window["information"].update(
                    f"What do you want to examine?", text_color="red"
                )
                event = window.read()
                window["information"].update(text_color="white")
                # if no pieces exist here:
                if gameBoard[event[0][0]][event[0][1]][0].occupied == False:
                    pm(window, gameBoard[event[0][0]][event[0][1]][0].describeSelf())
                # if there is a piece:
                else:
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
                    sg.popup(f"The piece here belongs to {owner}.\nIt currently holds {len(gameBoard[event[0][0]][event[0][1]][1].storedItems)} inactive items.\nIt has the following buffs:\n{buffslist}\nIt has the current debuffs:\n{debuffslist}",)
                    pm(
                        window,
                        f"The piece here belongs to {owner}.\nIt currently holds {len(gameBoard[event[0][0]][event[0][1]][1].storedItems)} inactive items.\nIt has the following buffs:\n{buffslist}\nIt has the current debuffs:\n{debuffslist}",
                    )
                window["examineItem"].update(disabled=False)
                window["readItems"].update(disabled=False)
                continue

            #if the player wants to read about items
            if "readItems" in event:
                    learnItemsLayout = []
                    itemList = [
                            "<QUIT>",
                            "orb eater",
                            "row laser",
                            "magnet",
                            "trap orb",
                            "place mine",
                            "move again",
                            "suicide bomb row",
                            "Energy Forcefield",
                            "suicide bomb column",
                            "haphazard airstrike",
                            "suicide bomb radial",
                            "jump proof",
                            "smart bombs",
                            "move diagonal",
                            "trip mine radial",
                            "purify radial",
                            "napalm radial",
                            "vile radial",
                            "haymaker",
                            "bowling ball",
                            "column laser",
                            "row laser",
                            "shuffle column",
                            "shuffle radial",
                            "spooky hand",
                            "reproduce",
                            "worm hole",
                            "warp"
                        ]
                    for i in itemList:
                        learnItemsLayout+= [ [sg.Button(f"{i}",key = i)] ]
                    learnItems = sg.Window("Title",learnItemsLayout,keep_on_top = True)
                    window.disable()
                    
                    event = learnItems.read()
                    
                
                    while event[0]!="<QUIT>" and event[0]!=None :
                        itemExplanation(event[0])
                        event = learnItems.read()
                        if event[0] == None:
                            break
                    learnItems.close()
                    window.enable()
                    continue
        #disable the exit button to avoid issues
        window["exit"].update(disabled=True)

            
        #if the piece is a bowling ball    
        if gameBoard[event[0][0]][event[0][1]][0].occupied == True and "bowling ball" in gameBoard[event[0][0]][event[0][1]][1].activeBuffs:
            #if it's your enemy's bowling ball
            if gameBoard[event[0][0]][event[0][1]][1].ownedBy != playerTurn:
                pm(window,"That's not your piece!")
                continue

            #x/y values of the bowling ball
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

        #if it's the person's second (or more) turn
        elif repeatRestrictor[0] == True:
            event = []
            #repeat restrictor keeps track of where the player was last
            event.append(repeatRestrictor[1])
            if event[0] == (-1.0 - 1):
                sg.popup(
                    "An error has occurred in repeat Restrictor's (-1,-1)",
                    keep_on_top=True,
                )
                repeatRestrictor = False
                return
        #allow player to read about items, but not view tiles; helps avoid glitches
        window["itemButton"].update(disabled=False)
        window["examineItem"].update(disabled=True)


        #this is where the player started; keep track of this for calculations
        startLocation = event[0]


        #if the person is trying to move a piiece that isn't the same piece they just moved
        if (repeatRestrictor[0] == True) and (startLocation != repeatRestrictor[1]):
            getChoice = sg.popup_yes_no(
                "You can only move the same piece twice.  Click yes to force that piece to be selected.  Otherwise choose no to end your turn.",
                keep_on_top=True,
            )
            if getChoice == "Yes":
                startLocation = repeatRestrictor[1]
            else:
                return

        #if it's the same piece they moved earlier, make it grey.  If the piece isn't there, find it using the currentTurnPiece function
        if (repeatRestrictor[0] == True) and (startLocation == repeatRestrictor[1]):
            try:
                gameBoard[startLocation[0]][startLocation[1]][1].grey = True
                gameBoard[startLocation[0]][startLocation[1]][1].currentTurnPiece = True
            except:
                startLocation[0],startLocation[1] = findCurrentTurnPiece(window, gameBoard)
            displayBoard(window, gameBoard)

        # if a square is picked and a piece exists on it
        if gameBoard[event[0][0]][event[0][1]][0].occupied == True:

            # if that piece is stunned
            if (
                playerTurn == gameBoard[event[0][0]][event[0][1]][1].ownedBy
                and "stunned" in gameBoard[event[0][0]][event[0][1]][1].activeDebuffs
            ):
                window["information"].update(
                    f"You cannot use a stunned/sleeping piece."
                )
                pm(window, f"Pick a piece to move.")
                window["information"].update(text_color="red")
                window.refresh()
                continue

            # if the piece belongs to you and it has items (and isn't stunned)
            elif (
                playerTurn == gameBoard[event[0][0]][event[0][1]][1].ownedBy
                and len(gameBoard[event[0][0]][event[0][1]][1].storedItems) > 0
            ):
                window["information"].update(
                    f"Selection made, pick a destination or click the same piece again to access items."
                )
                pm(
                    window,
                    f"Selection made, pick a destination or click the same piece again to access items.",
                )

                window["readItems"].update(disabled=True)
            # if the piece doesn't belong to you
            elif playerTurn != gameBoard[event[0][0]][event[0][1]][1].ownedBy:
                window["information"].update(f"That's not your piece...")
                pm(window, f"That's not your piece...")
                window["information"].update(text_color="red")
                window.refresh()
                continue
            # if the piece belongs to you but doesn't have items
            else:
                window["information"].update(f"Selection made, pick a destination.")
                pm(window, f"Selection made, pick a destination.")

        # if there's no piece on that square
        else:
            window["information"].update(text_color="red")
            window["information"].update(
                f"You can't interact directly with unoccupied spaces."
            )
            pm(window, f"You can't interact directly with unoccupied spaces.")
            window.refresh()

            sleep(0.25)
            continue

        # if there is a piece there and it belongs to you, highlight it to show you selected it
        if gameBoard[startLocation[0]][startLocation[1]][1] != 0:
            gameBoard[startLocation[0]][startLocation[1]][1].grey = True
            gameBoard[startLocation[0]][startLocation[1]][1].currentTurnPiece = True
        # update the board (to show highlighting)
        displayBoard(window, gameBoard)

        # get the next location
        event = window.read()

        window["examineItem"].update(disabled=True)

        # this is where we're attempting to move
        endLocation = event[0]

        # trying to use item
        if (
            "itemButton" in event
            and gameBoard[startLocation[0]][startLocation[1]][0].occupied == True
        ) or (
            startLocation == endLocation
            and gameBoard[startLocation[0]][startLocation[1]][0].occupied == True
        ):

            # check to see if it's legal to use item
            if len(
                gameBoard[startLocation[0]][startLocation[1]][1].storedItems
            ) > 0 and (
                gameBoard[startLocation[0]][startLocation[1]][1].ownedBy == playerTurn
            ):

                useItems(gameBoard, startLocation[0], startLocation[1], window)

                if gameBoard[startLocation[0]][startLocation[1]][0].occupied == True:
                    gameBoard[startLocation[0]][startLocation[1]][1].grey = False
                    gameBoard[startLocation[0]][startLocation[1]][1].currentTurnPiece = False
                #check to see if any piece counts changed
                countPieces(gameBoard, window)
                displayBoard(window, gameBoard)
                continue
            # if the piece isn't yours
            elif gameBoard[startLocation[0]][startLocation[1]][1].ownedBy != playerTurn:
                gameBoard[startLocation[0]][startLocation[1]][1].grey = False
                gameBoard[startLocation[0]][startLocation[1]][1].currentTurnPiece = False
                pm(window, "That's not your piece")
                continue

            # if the piece has no items
            elif len(gameBoard[startLocation[0]][startLocation[1]][1].storedItems) < 1:
                gameBoard[startLocation[0]][startLocation[1]][1].grey = False
                gameBoard[startLocation[0]][startLocation[1]][1].currentTurnPiece = False
                pm(window, "There are no items on this piece.")
                continue
            # shouldn't get to here
            else:
                pm(window, "An error occurred in item lookups")

        # if there isn't any piece on the square
        if gameBoard[startLocation[0]][startLocation[1]][0].occupied == False:
            gameBoard[startLocation[0]][startLocation[1]][1].currentTurnPiece = False
            pm(window, f"Nothing exists on the initial square!")
            window.refresh
            continue

        # if the piece no longer exists on the original point, ungrey it
        if gameBoard[startLocation[0]][startLocation[1]][1] != 0:
            gameBoard[startLocation[0]][startLocation[1]][1].grey = False
            gameBoard[startLocation[0]][startLocation[1]][1].currentTurnPiece = False
        displayBoard(window, gameBoard)

        # if the spot you're moving from contains a piece (which it should)
        if gameBoard[startLocation[0]][startLocation[1]][0].occupied:
            # if the piece is yours
            if gameBoard[startLocation[0]][startLocation[1]][1].ownedBy == playerTurn:




                #BEGIN REAL MOVE ATTEMPT


                #worm hole override

                #test for tripmine trip mine

                #if player 1's turn and there's a worm hole there
                if gameBoard[endLocation[0]][endLocation[1]][0].occupied == False and gameBoard[endLocation[0]][endLocation[1]][0].wormHole1 == True and playerTurn == 1:
                    roundEarthTheory = True
                elif gameBoard[endLocation[0]][endLocation[1]][0].occupied == False and gameBoard[endLocation[0]][endLocation[1]][0].wormHole2 == True and playerTurn == 2:
                    roundEarthTheory = True

                

                
                # assume the player isn't trying to move diagonally at first
                diagonalCheck = False
                if "round earth theory" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:

                    
                    
                #trying to go from right side to left side

                    #try to go straight right to straight left
                    if startLocation[0] == endLocation[0]:
                        if startLocation[1] == columns-1 and endLocation[1] == 0:
                            sg.popup("Teleport to left")
                            roundEarthTheory = True
                    #trying to go down right
                    elif startLocation[0] == endLocation[0]-1 and startLocation[1] == columns -1 and endLocation[1] == 0 and "move diagonal" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
                        sg.popup("Teleport down right")
                        roundEarthTheory = True
                    #trying to go up right
                    elif startLocation[0] == endLocation[0]+1 and startLocation[1] == columns -1 and endLocation[1] == 0 and "move diagonal" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
                        sg.popup("Teleport up right")
                        roundEarthTheory = True
                    

                #trying to go from left to right side
                    #try to go straight left to straight right
                    if startLocation[0] == endLocation[0]:
                        if startLocation[1] == 0 and endLocation[1] == columns -1:
                            sg.popup("Teleport to right")
                            roundEarthTheory = True
                    #trying to go down right
                    elif startLocation[0] == endLocation[0]-1 and startLocation[1] == 0  and endLocation[1] == columns -1 and "move diagonal" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
                        sg.popup("Teleport down left")
                        roundEarthTheory = True
                    #trying to go up right
                    elif startLocation[0] == endLocation[0]+1 and startLocation[1] == 0 and endLocation[1] == columns -1 and "move diagonal" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
                        sg.popup("Teleport up left")
                        roundEarthTheory = True

                        
                #trying to go from up to down
                    #try to go straight up to straight down
                    if startLocation[1] == endLocation[1]:
                        if startLocation[0] == 0 and endLocation[0] == rows -1:
                            sg.popup("Teleport to bottom")
                            roundEarthTheory = True
                    #trying to go up right
                    elif startLocation[0] == 0 and startLocation[1] == (endLocation[1] +1) and endLocation[0] == rows -1 and "move diagonal" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
                        sg.popup("Teleport up left")
                        roundEarthTheory = True
                    #trying to go up right
                    elif startLocation[1] == endLocation[1]-1 and startLocation[0] == 0 and endLocation[0] == rows -1 and "move diagonal" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
                        sg.popup("Teleport up right")
                        roundEarthTheory = True
                
                #diagonals (only works with diagonal enabled
                    if "move diagonal" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
                        #upleft
                        if startLocation[0] == 0 and startLocation[1] == 0 and endLocation[0] == rows-1 and endLocation[1] == columns-1:
                            sg.popup("teleport to bottom right")
                            roundEarthTheory = True
                        #upright
                        if startLocation[0] == 0 and startLocation[1] == columns-1 and endLocation[0] == rows-1 and endLocation[1] == 0:
                            sg.popup("teleport to bottom left")
                            roundEarthTheory = True
                        #downleft
                        if startLocation[0] == rows-1 and startLocation[1] == 0 and endLocation[0] == 0 and endLocation[1] == columns-1:
                            sg.popup("teleport top right")
                            roundEarthTheory = True
                        #downright
                        if startLocation[0] == rows-1 and startLocation[1] == columns-1 and endLocation[0] == 0 and endLocation[1] == 0:
                            sg.popup("teleport top left")
                            roundEarthTheory = True


                
                # if it's too far...
                # ...but you have a move diagonal and it turns out you're actually within range:
                if roundEarthTheory == False:
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
                        window["information"].update(
                            f"That location is too far for you to move to!"
                        )
                        pm(window, f"That location is too far for you to move to!")
                        window.refresh

                        continue
                
                #
                # if it's close enough:  (DESTINATION/LEGAL MOVE)
                #

                # if the landing spot is an item Orb:
                if gameBoard[endLocation[0]][endLocation[1]][0].tileType == "itemOrb":

                    pickUpItemOrb(gameBoard, startLocation[0], startLocation[1])
                    pm(window, "Picked up an item")
                    pickedUpItem = True

                if gameBoard[endLocation[0]][endLocation[1]][0].tileType in [
                    "destroyed",
                    "damaged4",
                    "damaged3",
                    "damaged2",
                    "damaged",
                ]:
                    window["information"].update(f"Can't move here!")
                    pm(window, "Can't move here!")
                    continue
                
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
                        sg.popup("Bounced to a new spot!")
                        pm(window,"Bounced to a new spot!")


                   

                    #mugger check
                    if gameBoard[endLocation[0]][endLocation[1]][0].tileType == "mugger":
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
                            return
                            
                        
                        if gameBoard[endLocation[0]][endLocation[1]][0].mugger == playerTurn:
                            sg.popup("The mugger has left.")
                            gameBoard[endLocation[0]][endLocation[1]][0].mugger = False
                        elif gameBoard[endLocation[0]][endLocation[1]][0].mugger != playerTurn:
                                
                                if gameBoard[startLocation[0]][startLocation[1]][0].occupied == True:
                                    
                                    if len(gameBoard[startLocation[0]][startLocation[1]][1].storedItems) > 0:
                                        gameBoard[startLocation[0]][startLocation[1]][1].storedItems.clear()
                                        sg.popup("The mugger stole all your held items")
                                        gameBoard[endLocation[0]][endLocation[1]][0].mugger = False
                                    

                        
                    # copy the actual piece object over from the old address to the new one (deepcopy needed?)
                    gameBoard[endLocation[0]][endLocation[1]][1] = gameBoard[
                        startLocation[0]
                    ][startLocation[1]][1]

                    # set the original location as being empty; delete the class; set a default tile
                    gameBoard[startLocation[0]][startLocation[1]][0].occupied = False
                    gameBoard[startLocation[0]][startLocation[1]][1] = 0



                    #mystery box
                    
                    if gameBoard[endLocation[0]][endLocation[1]][0].tileType == "mystery box":
                        sg.popup("Mystery box")
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
                        
                        randomEvent = random.choice( ["getItems", "lose items", "die"])
                        if randomEvent == "getItems":
                            #get three items
                            for i in range(1,4):
                                pickUpItemOrb(gameBoard, endLocation[0], endLocation[1])
                        elif randomEvent == "lose items":
                            gameBoard[endLocation[0]][endLocation[1]][1].storedItems.clear()
                            sg.popup("You've lost all your held items")
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
                            gameBoard[endLocation[0]][endLocation[1]][0].tileType = "default"
                            return
                        
                    if (
                        gameBoard[endLocation[0]][endLocation[1]][1].standingOnSelfOrb
                        == True
                    ):
                        gameBoard[startLocation[0]][startLocation[1]][
                            0
                        ].tileType = f"trap orb {playerTurn}"
                    else:
                        if gameBoard[startLocation[0]][startLocation[1]][0].tileType == "mugger":
                            pass
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
                        sg.popup("You monster!  You killed an orb eater!")
                        gameBoard[endLocation[0]][endLocation[1]][0].orbEater = False

                     

                        
                    pm(window, "Moved successfully")
                    window.refresh

                    # go again if you have moveAgain equipped

                    if (
                        gameBoard[endLocation[0]][endLocation[1]][1] != 0
                        and gameBoard[endLocation[0]][endLocation[1]][1].moveAgain > 0
                    ):

                        window["information"].update(
                            f"This piece gets to move again; {gameBoard[ endLocation[0] ] [ endLocation[1] ][1].moveAgain} remaining!"
                        )
                        displayBoard(window, gameBoard)
                        moveAgainCheck = sg.popup_yes_no(
                            "This piece gets to go again. Would you like to use it again?", keep_on_top=True
                        )
                        if moveAgainCheck == "Yes":
                            gameBoard[endLocation[0]][endLocation[1]][1].moveAgain -= 1
                            repeatRestrictor[0] = True
                            repeatRestrictor[1] = (endLocation[0], endLocation[1])
                            continue
                        else:
                            return

                    else:
                        return 1

                # killing own piece (illegal)
                elif gameBoard[endLocation[0]][endLocation[1]][1].ownedBy == playerTurn:
                    pm(window, "You can't jumpkill your own piece.")
                    window.refresh
                    continue

                # kill enemy piece; elif enemy owns the ending location
                elif gameBoard[endLocation[0]][endLocation[1]][1].ownedBy != playerTurn:
                    # test to see if the piece can be jumped
                    if (
                        "jumpProof"
                        in gameBoard[endLocation[0]][endLocation[1]][1].activeBuffs
                    ):
                        pm(window, "No!  This opponent is jump proof!")
                        window.refresh()
                        sleep(1)
                        continue

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
                        if gameBoard[startLocation[0]][startLocation[1]][0].tileType == "mugger":
                            gameBoard[startLocation[0]][startLocation[1]][0].tileType = "mugger"
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
                    window["information"].update(f"Jumpkilled an enemy piece!")
                    pm(window, "Jumpkilled an enemy piece!")

                    # go again if you have moveAgain equipped
                    if (
                        gameBoard[endLocation[0]][endLocation[1]][1] != 0
                        and gameBoard[endLocation[0]][endLocation[1]][1].moveAgain > 0
                    ):


                        window["information"].update(
                            f"This piece gets to move again; {gameBoard[ endLocation[0] ] [ endLocation[1] ][1].moveAgain} remaining!"
                        )
                        # sleep(1)
                        moveAgainCheck = sg.popup_yes_no(
                            "Would you like to move it again?", keep_on_top=True
                        )

                        if moveAgainCheck == "Yes":

                            gameBoard[endLocation[0]][endLocation[1]][1].moveAgain -= 1
                            repeatRestrictor[0] = True
                            repeatRestrictor[1] = (endLocation[0], endLocation[1])
                            continue
                        else:
                            return
                    return 2
            
            else:
                window["information"].update(f"That's not your piece!")
                pm(window, "That's not your piece!")
                window.refresh
                continue

        else:
            window["information"].update(f"Nothing here to move!")
            pm(window, "Nothing here to move!")
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

                
                gameBoard[xrand][yrand][0].tileType = "hand1"
                displayBoard(window, gameBoard)
                window.refresh()
                
                gameBoard[xrand][yrand][0].tileType = "hand2"
                displayBoard(window, gameBoard)
                window.refresh()

                gameBoard[xrand][yrand][0].tileType = "hand3"
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
                
                sg.popup("A piece has recalled")
                
            

                                

def begin():

    # variables
    columns = 10
    rows = 10
    gameBoard = []

    # window
    frame_main = [
        [
            sg.Button(
                image_filename="images/default.png",
                key=(i, j),
                size=(75, 75),
                button_color=("white", "grey"),
                tooltip="square",
                pad=(2, 2),
            )
            for j in range(columns)
        ]
        for i in range(0, rows)
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

    frame_layout = [
        [sg.Image("images/up.png", key="turn", visible=True)],
        [
            sg.T(f"Player:", font="Cambria 30", pad=(4, 4)),
            sg.T(f"", key="playerTurn", font="Cambria 30", pad=(4, 4)),
        ],
        [sg.T(f" " * 50, key="information", size=(37, 3), font="Cambria 30")],
        [sg.Frame("Pieces Remaining", frame_remaining)],
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
            sg.Button(
                "USE ITEMS", key="itemButton", image_filename="images/backpack.png"
            ),
            sg.Button(
                "Look",
                button_color=("Blue", "White"),
                tooltip="Examine",
                font="Cambria 20",
                key="examineItem",
                image_filename="images/examine.png",
            ),
            sg.Button("Learn about items",key="readItems",size=(40,4)),
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
        
        disable_close=False,
        grab_anywhere=True,
        location=(0, 0),
    ).finalize()

    # window.maximize()

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

        
        ##copy a deepcopy of the entry in gameBoard[x][y], the currentLocation of the spot, and the number of turns 
        
##        #if there's any entries in the recall list
##        if len(PublicStats.recallPieces)>0:
##            
##            #recall is the entire list in recall
##            recallData = PublicStats.recallPieces
##            
##            for iIndex, i in enumerate(PublicStats.recallPieces):
##                changed = False
##                #i[0] is the tilepiece combo, i[1] is the location with i[1][0] being the x and i[1][1] being the y, i[2] is turns left
##                #if the current entry of the recall list isn't 0 (0 means it's been taken care of)
##                if i!=0:
##                    if changed == True:
##                        continue
##                    sg.popup(f"i2 is {i[2]}")
##                    recX = i[1][0]
##                    recY = i[1][1]
##                    #if the turns left isn't zero
##                    if i[2] > 0:
##                        #reduce the number of turns left
##                        recallData[iIndex][2]-=1
##                        sg.popup(f"i2 is {i[2]}")
##                        #check the next entry if a recall piece was changed
##                        changed = True
##                        continue
##                    
##                    #if it is zero turns now
##                    elif i[2] == 0:
##                        #for each row in gameBoard
##                        for sx, j in enumerate(gameBoard):
##                            #for each column in j
##                            if changed == True:
##                                break
##                            for sy,k in enumerate(j):
##                                if changed == True:
##                                    break
##                                #if there is a piece inside of that column
##                                #k is the gameBoard tilePiece (k0 is tile k1 is piece) where the piece is right now
##                                if k[0].occupied == True:
##                                    print(f"I is {i} and i[0] is {i[0]}")
##                                    print(f"k[1].recall is {k[1].recall}")
##                                    #if the .recall data variable integer is equal to the current iIndex of recallPieces
##                                    if k[1] != 0 and k[1].recall == iIndex:
##                                        sg.popup("teleport back")
##                                        sg.popup(f"k1 is {k[1]}")
##                                        gameBoard [recX] [recY] [0]= copy.deepcopy(i[0][0])
##                                        gameBoard [recX] [recY] [1]= copy.deepcopy(i[0][1])
##                                        k[0].occupied = False
##                                        k[0].tileType = "default"
##                                        k[1] = 0
##                                        #set the array value to 0
##                                        recallData[iIndex] = 0
##                                        sg.popup(f"The array is {recallData}")
##                                        displayBoard(window, gameBoard)
##                                        changed = True
##                                        continue
                                        
                        
                    

        
        
        gamePlay(playerTurn, window, gameBoard)
        x = -1
        y = -1
        # end player one's turn, begin player two's turn, switch players
        if playerTurn == 1:
            
            window["turn"].update(filename="images/down.png")

            #check for recalled pieces
            if PublicStats.recallCount > 0:
                recallFunction(window,gameBoard)

                
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
                                    pickUpItemOrb(gameBoard, x, y)
                y = -1
            playerTurn = 2





            #End player 1's turn
            
            if PublicStats.spookyHand == True:
                spookyHand(window,gameBoard)

            orbsEaten = orbEater(gameBoard)    
            resetMoveAgain(gameBoard)
            laserCheck(window, gameBoard)
            if orbsEaten > 0:
                pm(window, f"Orbs eaten by the orb eaters: {orbsEaten}")
                fileNum = random.randint(1,4)
                playsound(f"sounds/squeak{fileNum}.mp3", block = False)




            
        # end player two's turn, begin player one's turn
        else:
            window["turn"].update(filename="images/up.png")

            #check for recalled pieces
            if PublicStats.recallCount > 0:
                recallFunction(window,gameBoard)
                
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
                                    pickUpItemOrb(gameBoard, x, y)
                y = -1
            playerTurn = 1

            
            
            if PublicStats.spookyHand == True:
                spookyHand(window,gameBoard)
            orbsEaten = orbEater(gameBoard)
            laserCheck(window, gameBoard)    
            resetMoveAgain(gameBoard)
            if orbsEaten > 0:
                pm(window, f"Orbs eaten by the orb eaters: {orbsEaten}")
                fileNum = random.randint(1,4)
                playsound(f"sounds/squeak{fileNum}.mp3", block = False)
            


def tutorial():

    # variables
    columns = 10
    rows = 10
    gameBoard = []

    frame_1 = [
        [sg.Button("Object of the game", key="object")],
        [sg.Button("How to select a piece", key="select")],
        [sg.Button("How to move", key="move")],
        [sg.Button("Items", key="items")],
        [sg.Button("Getting info on pieces", key="info")],
        [sg.Button("EXIT", key="EXIT")],
        
    ]
    frame_2 = [
        [
            sg.Button(
                image_filename=".\\default.png",
                key=(i, j),
                size=(20, 20),
                tooltip="tooltip",
                pad=(10, 10),
            )
            for j in range(columns)
        ]
        for i in range(0, rows)
    ]
    frame_3 = [[sg.T(" " * 100, key="tutorialInfo", font="Cambria 20", size=(50, 5))]]
    frame_4 = [[sg.T(" " * 100, key="information", font="Cambria 20", size=(88, 20))]]

    layout = [
        [
            sg.T("MegaCheckers", font="Cambria 50", key="title"),
            sg.Button("use item", image_filename="./backpack.png", visible=False),
        ],
    ]
    layout += [
        [
            sg.Frame("Main screen", frame_1, key="options", visible=True),
            sg.Frame("Game Play", frame_2, key="gamePlay", visible=True),
        ]
    ]
    layout += [[sg.Frame("Tutorial Info", frame_3), sg.Frame("Information", frame_4)]]

    # gameBoard for logic
    gameBoard = []
    line = []
    for i in range(columns):
        line.append([Tile(), 0])
        gameBoard.append(0)

    for j in range(rows):
        gameBoard[j] = copy.deepcopy(line)

    window = sg.Window("MegaCheckers", layout, location=(0, 0)).finalize()

    initializeField(columns, rows, window, gameBoard)

    window["options"].update(visible=True)

    while True:
        event = window.read()
        if event[0] == "EXIT":
            # QUIT
            window.close()
            raise SystemExit
        if event[0] == "object":
            window["gamePlay"].update(visible=True)
            myText = """OBJECT: The object of the game is to destroy all of your opponent's pieces or make it impossible for them to take a turn.  Your main method to do this will be by jumping on enemy pieces to kill them (don't worry, the pieces aren't sentient, so no one is getting hurt).  You will also be able to employ items that you find on the field to either protect yourself from your enemies or to blow them up someway or another."""
            window["tutorialInfo"].update(myText)

        elif event[0] == "select":
            window["gamePlay"].update(visible=True)
            while True:
                myText = """SELECTING A PIECE: to select your piece, simply left click on it.  Try it now!  Left click a blue piece."""
                window["tutorialInfo"].update(myText)
                displayBoard(window, gameBoard)

                event = window.read()

                if event[0] in ["object", "select", "move", "items", "info", "cancel"]:
                    sg.popup("Restarting tutorial", keep_on_top=True)
                    window.close()
                    tutorial()
                if event[0] == "EXIT":
                    sg.popup("Exiting to main screen.", keep_on_top=True)
                    window.close()
                    main()

                x = int(event[0][0])
                y = int(event[0][1])
                if (
                    gameBoard[event[0][0]][event[0][1]][1] != 0
                    and gameBoard[x][y][1].ownedBy == 1
                ):
                    myText = "Great job!  You've selected a piece.  Move onto a different topic."
                    window["tutorialInfo"].update(myText)
                    break
                else:
                    myText = "Sorry, that's not right.  Left click on a blue piece."
                    window["tutorialInfo"].update(myText, text_color="red")
                    window.refresh()
                    sleep(1)
                    window["tutorialInfo"].update(myText, text_color="white")

        elif event[0] == "move":
            window["gamePlay"].update(visible=True)
            outOfRangeTutorialIncomplete = True
            while True:

                while True:
                    notValidSelection = True
                    myText = """MOVING: normally you can move once per turn, and can only move one piece per turn.  Unless they have specific items, pieces can only move one space forward/back/sideways.  Let's try moving a piece now!  Start by selecting a blue piece on the second row from the top."""
                    window["tutorialInfo"].update(myText)
                    displayBoard(window, gameBoard)
                    while notValidSelection:
                        event = window.read()

                        if event[0][0] == 1:
                            validSelection = False
                            myText = (
                                "Good work!  Now we can continue on to the next step."
                            )
                            rowOrig = event[0][0]
                            colOrig = event[0][1]
                            window["tutorialInfo"].update(myText)
                            window.refresh()
                            sleep(1.5)
                            break
                        else:
                            myText = "That's not correct.  You'll have to select a blue piece on the second row before we can continue."
                            window["tutorialInfo"].update(myText, text_color="red")
                            window.refresh()
                            sleep(1)
                            window["tutorialInfo"].update(myText, text_color="white")

                    window["information"].update(
                        f"Piece selected!  Choose a destination tile within range."
                    )
                    window.refresh
                    if outOfRangeTutorialIncomplete == True:
                        myText = """Now that we have clicked on one of your pieces, we can move it.  Notice that the information window lets you know that your piece was selected.  It's asking you to choose a location within range.  HOWEVER - try clicking on any empty space EXCEPT the one that's right in front of your selected piece."""
                    else:
                        myText = """Now that you know what it looks like when you try to move to an invalid space, let's do a valid space.  Choose the spot right in front of your selected piece."""

                    window["tutorialInfo"].update(myText)
                    window.refresh()
                    event = window.read()

                    if (
                        (event[0][0] < 2)
                        or (event[0][0]) > (rows - 2)
                        and outOfRangeTutorialIncomplete == True
                    ):
                        myText = """That's not right.  For this tutorial, we need you to click on an empty space.  You clicked on a space that's occupied.  No worries, let's start over."""
                        window["tutorialInfo"].update(myText, text_color="red")
                        sleep(2)
                        window["tutorialInfo"].update(myText, text_color="white")
                        break
                    if (
                        (event[0][0] == rowOrig + 1)
                        and (event[0][1] == colOrig)
                        and outOfRangeTutorialIncomplete == True
                    ):
                        myText = """You're getting ahead of yourself.  Normally this would be the right move, but trust me...  Just do what the tutorial says and pick any empty spot except for this one."""
                        window["tutorialInfo"].update(myText, text_color="red")
                        window["information"].update("")
                        window.refresh()
                        sleep(4)
                        window["tutorialInfo"].update(myText, text_color="white")
                        continue
                    if (
                        outOfRangeTutorialIncomplete == False
                        and event[0][0] == rowOrig + 1
                        and event[0][1] == colOrig
                    ):
                        myText = "Good job!  You've successfully moved a piece!  If you move onto a enemy in this way, you kill it!  Click on the items tutorial next!"

                        window["tutorialInfo"].update(myText, text_color="white")
                        playerBackup = gameBoard[rowOrig][colOrig][1]
                        gameBoard[rowOrig][colOrig][1] = 0
                        gameBoard[event[0][0]][event[0][1]][1] = playerBackup

                        gameBoard[rowOrig][colOrig][0].occupied = False
                        gameBoard[rowOrig][colOrig][0].tileType = "default"
                        gameBoard[rowOrig + 1][colOrig][0].occupied = True
                        displayBoard(window, gameBoard)
                        window.refresh()
                        window.read()
                        window.close()
                        tutorial()
                    else:
                        if outOfRangeTutorialIncomplete == True:
                            window["information"].update(
                                f"That location is too far for you to move to!"
                            )
                            myText = (
                                "Good work!  Notice the error message in the information box.  During normal gameplay, you can keep an eye out on it to see what you can do.  Alright, now that you know what happens if you try to move out of range, let's try doing an actual move.  Choose a blue piece and then move it one square forward."
                                ""
                            )
                            window["tutorialInfo"].update(myText, text_color="white")
                            window.refresh()
                            sleep(4)
                            window["information"].update("")
                            outOfRangeTutorialIncomplete = False
                            window.refresh
                            sleep(2)
                            break
                        else:
                            myText = """That's not a valid choice.  Let's try again."""
                            window["tutorialInfo"].update(myText, text_color="white")
                            window.refresh()
                            sleep(1)

        elif event[0] == "items":
            myText = "This part of the tutorial assumes you've mastered selecting your pieces and moving around.  If you're still not familiar with that, please practice that some more before doing this next part.  Please grab the power tile in the middle: do this by selecting your blue tile that's next to it."
            window["gamePlay"].update(visible=True)
            window["tutorialInfo"].update(myText)
            gameBoard[2][4][0].tileType = "itemOrb"
            displayBoard(window, gameBoard)

            # click the thingy
            while True:
                event = window.read()
                if event[0] != (1, 4):
                    myText = "You have to select the piece that's right next to the item orb tile"
                    window["tutorialInfo"].update(myText)
                    window.refresh()
                    continue
                else:

                    while True:
                        myText = "Now that you've selected your piece, we need to click on the item orb to have your piece grab it."
                        window["tutorialInfo"].update(myText)
                        event = window.read()
                        if event[0] != (2, 4):
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
                            gameBoard[rowOrig + 1][colOrig][0].occupied = True
                            gameBoard[rowOrig + 1][colOrig][1].storedItems.append(
                                "Energy Forcefield"
                            )
                            gameBoard[rowOrig + 1][colOrig][1].determineAvatar()

                            displayBoard(window, gameBoard)
                            window.refresh()

                            sleep(1)
                            while True:
                                myText = "Alright, click on the powered up piece"

                                event = window.read()
                                window["tutorialInfo"].update(myText)
                                if event[0] != (2, 4):
                                    sg.popup(
                                        "Click on the piece that you just moved",
                                        keep_on_top=True,
                                    )
                                    continue
                                else:
                                    window["use item"].update(visible=True)
                                    myText = "There are two ways to use an item.  You can either click on the selected piece again, or you can click on the Use Item icon near the top.  Do either one."

                                    event = window.read()
                                    window["tutorialInfo"].update(myText)

                                    if event[0] == "use item" or event[0] == (2, 4):
                                        myText = "There are two ways to use an item.  You can either click on the selected piece again, or you can click on the Use Item icon near the top.  Do either one."
                                        explodeLayout = [
                                            [
                                                sg.Button(
                                                    "Cheater's Instawin Item of Instant Winning"
                                                )
                                            ]
                                        ]
                                        x = sg.Window("Items", explodeLayout)

                                        event = x.read()
                                        window["tutorialInfo"].update(myText)

                                        if (
                                            event[0]
                                            == "Cheater's Instawin Item of Instant Winning"
                                        ):
                                            x.close()
                                            myText = "Congrats, you cheater.  This weapon (which only exists in this tutorial mode) will instantly destroy any enemy pieces on the field.  You now know pretty much everything you need to know to win.  Go out there and start playing with a friend."

                                            window["tutorialInfo"].update(myText)
                                            window.refresh()
                                            sleep(1)

                                            for i in range(2):
                                                for j in range(columns):
                                                    window[rows - i - 1, j].update(
                                                        image_filename="images/exploding.png"
                                                    )
                                            window.refresh()
                                            sleep(1)

                                            for i in range(2):
                                                for j in range(columns):
                                                    window[rows - i - 1, j].update(
                                                        image_filename="images/destroyed.png"
                                                    )
                                            window.refresh()
                                            sleep(1)

                                            for i in range(2):
                                                for j in range(columns):
                                                    window[rows - i - 1, j].update(
                                                        image_filename="images/exploding.png"
                                                    )
                                            window.refresh()
                                            sleep(1)

                                            for i in range(2):
                                                for j in range(columns):
                                                    window[rows - i - 1, j].update(
                                                        image_filename="images/default.png"
                                                    )
                                            window.refresh()
                                            sleep(5)
                                        sg.popup(
                                            "Restarting the tutorial", keep_on_top=True
                                        )
                                        tutorial()

                                    else:
                                        sg.popup("Nope, try again", keep_on_top=True)
                                        continue

        else:
            myText = "Invalid choice.  Try clicking something on the menu."
            window["tutorialInfo"].update(myText)


def main():
    introLayout = [[sg.Text("MegaCheckers", font="Cambria 100")]]
    frame_1 = [
        [sg.Button("Begin game", key="begin")],
        [sg.Button("How to play", key="tutorial")],
    ]
    introLayout += [[sg.Frame("Choose an option", frame_1, key="options")]]
    introWindow = sg.Window("MegaCheckers", introLayout)
    event = introWindow.read()
    if event[0] == "tutorial":
        introWindow.close()
        tutorial()
    if event[0] == "begin":
        introWindow.close()
        begin()


# delete me after debug
#begin()
# delete me


main()
