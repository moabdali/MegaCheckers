import PySimpleGUI as sg
import copy
import math
import random
from time import sleep
from PIL import Image
from io import BytesIO
import base64
from playsound import playsound
import pyautogui

PublicPNGList = []     

def initializeField(columns, rows, window, gameBoard):
    

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
##           gameBoard[i][j][1].activeBuffs.append("move diagonal")
##           gameBoard[i][j][1].activeBuffs.append("jump proof")
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


class PublicStats:
    turnCount = 1
    cycle = 0
    #orbCycleList = [5, 10, 0, 0, 3, 1, 0, 2, 1]
    orbCycleList = [4, 0, 0, 1, 3, 2, 2, 0, 1,0,0]
    spookyHand = False
    spookyHandTurnCount = 5
    hotSpot = []
    recallCount = 0
    def getOrbCount(self):
        cycle = PublicStats.turnCount % 11
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
        self.forcefieldTurn = 0
        self.stickyTimeBomb = False
        self.feralMeatCount = False
        self.feralAttacksLeft = False
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
        self.secretAgent = False
        self.secretAgentList = []
        self.purityTile = False
        self.dumpList = []
        self.snake = False
        self.highlight = False #blue
        self.highlightRed = False #red
        self.highlightGreen = False #green
        self.highlightBrown = False #brown
        

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
            validLocations.append( (i, location[1]) )
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
        sg.popup("Player one loses",keep_on_top=True)
        raise SystemExit
    elif player2count == 0:
        sg.popup("player two loses",keep_on_top=True)
        raise SystemExit
    window["player1piececount"].update(f"Player 1 controls: {player1count}\n")
    window["player2piececount"].update(f"Player 2 controls: {player2count}\n")
    window.refresh()

# the actual loop that is used to progress turns
def gamePlay(playerTurn, window, gameBoard):

    
    countPieces(gameBoard, window)
    createOrbs(window, gameBoard)
    #displayBoard(window, gameBoard)

    movePiece(playerTurn, window, gameBoard)
    PublicStats.turnCount += 1
    repairFloor(window, gameBoard)

# determine how far two points are
def getDistance(a, b, c, d):
    verticalDistance = abs(c - a)
    horizontalDistance = abs(d - b)
    distance = verticalDistance + horizontalDistance
    return distance

def feralFunction(window, gameBoard, playerTurn):
    for i in gameBoard:
        for j in i:
            if j[0].occupied == True and j[1].ownedBy == playerTurn and "feral" in j[1].activeBuffs:
                j[1].feralMeatCount -= 1
                
                j[1].feralAttacksLeft = 3
                if j[1].feralMeatCount < 0:
                    
                    sg.popup("Your feral piece died of hunger.  Being feral is energy intensive!", keep_on_top = True)
                    pm(window, "Your feral piece died of hunger.  Being feral is energy intensive!")
                    playsound("sounds\destroy.wav",block=False)
                    j[0].occupied = False
                    #explode
            
    
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

# see if any pieces are sitting on death spots
def deathCheck(window, gameBoard, move=False):
    for i in gameBoard:
        for j in i:
            # if a regular mine or laser was stepped on
            if (j[0].occupied == True) and (j[0].tileType == "mine" or (j[0].vertLaser == True or j[0].horiLaser == True or j[0].crossLaser == True) ):

                if j[1].shieldTurn == PublicStats.turnCount:
                    j[0].tileType = "default"
                    sg.popup("Forcefield saved you",keep_on_top=True)
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
                            location = (indexI,left)
                            forceFieldCheck = forcefieldCheck(window, gameBoard, location, location)
                            sg.popup(f"Force field check is {forceFieldCheck}")
                            if forceFieldCheck == True:
                                sg.popup("Survived a laser",keep_on_top=True)
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
                                #forceFieldRightStop = True
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
                                #forceFieldLeftStop = True
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
                                sg.popup("The laser killed a piece",keep_on_top=True)

                                
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
                                sg.popup("The laser killed a piece",keep_on_top=True)
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
        "secretAgent", #11
        "purityTile",#12
        "floor0",#13
        "floor1",#14
        "floor2",#15
        "floor-1",#16
        "floor-2",#17
        "recall",#18
        "snake",#19
        "jumpoline",#20
        "mystery box",#21
        "itemDump",#22
        "exploding",#23
        "damaged8",#24
        "damaged7",#25
        "damaged6",#26
        "damaged5",#27
        "damaged4",#28
        "damaged3",#29
        "damaged2",#30
        "damaged",#31
        "highlightBlue",#32
        "highlightRed",#33
        "highlight",#34
        "vile",#35
        "jump proof", #36
        "highlightGreen", #37
        "highlightBrown", #38
        "vampiricism", #39
        ]):

        myImage = Image.open(f"images/{i}.png").convert("RGBA")
        PublicPNGList.append(myImage)
            
       
                        
def cleanTile(tile):
    tile.wormHole1 = False
    tile.wormHole2 = False
    tile.orbEater = False
    tile.purityTile = False
    tile.secretAgent = False

def avatarFunction(window, avatar, gameBoard, i,j):
    g = gameBoard[i][j][0]
    if g.tileHeight == 0:
        window[(i,j)].update(button_color = ("white","grey50"))
    elif g.tileHeight == 1:
        window[(i,j)].update(button_color = ("white","grey65"))
    elif g.tileHeight == 2:
        window[(i,j)].update(button_color = ("white","white"))
    elif g.tileHeight == -1:
        window[(i,j)].update(button_color = ("white","grey25"))
    elif g.tileHeight == -2:
        window[(i,j)].update(button_color = ("white","grey10"))
    elif g.tileType == "destroyed":
        window[(i,j)].update(button_color = ("white","black"))
    
    if gameBoard[i][j][0].highlight == True:
        grey = Image.open("images/highlightBlue.png").convert("RGBA")
        avatar = Image.blend(grey, avatar, 0.50)
    im_file = BytesIO()
    avatar.save(im_file, format="png")

    

        
    im_bytes = im_file.getvalue()
    avatar = base64.b64encode(im_bytes)

    

    window[i, j].update(image_data=avatar)
    
#display the board (update what the tiles/pieces should look like)
def displayBoard(window, gameBoard):

    for i in range(len(gameBoard)):
        for j in range(len(gameBoard[0])):
            # unoccupied spaces

            
            
            if gameBoard[i][j][0].horiLaser == True and gameBoard[i][j][0].vertLaser == False:
                window[i, j].update(image_filename="images/horiLaserBeam.png")
                continue
            if gameBoard[i][j][0].horiLaser == False and gameBoard[i][j][0].vertLaser == True:    
                window[i, j].update(image_filename="images/vertLaserBeam.png")
                continue
            if gameBoard[i][j][0].horiLaser == True and gameBoard[i][j][0].vertLaser == True:
                window[i, j].update(image_filename="images/crossLaserBeam.png")
                continue
            if gameBoard[i][j][0].tileType == "jumpoline":
                
                avatarFunction(window, PublicPNGList[20], gameBoard, i, j)
                continue
            if gameBoard[i][j][0].tileType == "mystery box":
                avatarFunction(window, PublicPNGList[21], gameBoard, i, j)
                continue
            if gameBoard[i][j][0].tileType == "itemDump":
                avatarFunction(window, PublicPNGList[22], gameBoard, i, j)
                continue
            if gameBoard[i][j][0].tileType == "exploding":
                cleanTile(gameBoard[i][j][0])
                avatarFunction(window, PublicPNGList[23], gameBoard, i, j)
                continue
            if gameBoard[i][j][0].tileType == "damaged8":
                gameBoard[i][j][0].tileHeight = 0
                cleanTile(gameBoard[i][j][0])
                avatarFunction(window, PublicPNGList[24], gameBoard, i, j)
                continue
            if gameBoard[i][j][0].tileType == "damaged7":
                cleanTile(gameBoard[i][j][0])
                avatarFunction(window, PublicPNGList[25], gameBoard, i, j)
                continue
            if gameBoard[i][j][0].tileType == "damaged6":
                cleanTile(gameBoard[i][j][0])
                avatarFunction(window, PublicPNGList[26], gameBoard, i, j)
                continue
            if gameBoard[i][j][0].tileType == "damaged5":
                cleanTile(gameBoard[i][j][0])
                avatarFunction(window, PublicPNGList[27], gameBoard, i, j)
                continue
            if gameBoard[i][j][0].tileType == "damaged4":
                cleanTile(gameBoard[i][j][0])
                avatarFunction(window, PublicPNGList[28], gameBoard, i, j)
                continue
            if gameBoard[i][j][0].tileType == "damaged3":
                cleanTile(gameBoard[i][j][0])
                avatarFunction(window, PublicPNGList[29], gameBoard, i, j)
                continue
            if gameBoard[i][j][0].tileType == "damaged2":
                cleanTile(gameBoard[i][j][0])
                avatarFunction(window, PublicPNGList[30], gameBoard, i, j)
                continue
            if gameBoard[i][j][0].tileType == "damaged":
                cleanTile(gameBoard[i][j][0])
                avatarFunction(window, PublicPNGList[31], gameBoard, i, j)
                continue
            #snake
            if gameBoard[i][j][0].snake == True:
                pm(window,"Hiss.")
                avatar = PublicPNGList[19].convert("RGBA")
                avatarFunction(window, avatar, gameBoard, i, j)
                continue
            if gameBoard[i][j][0].tileType == "vile":
                avatar = (PublicPNGList[35]).convert("RGBA")
                avatarFunction(window, avatar, gameBoard, i, j)
                #window[i, j].update(image_filename="images/vile.png")
                continue
            if gameBoard[i][j][0].wormHole1 == True:

                wormHole1 = Image.open("images/wormHole1.png").convert("RGBA")
                avatar.paste(wormHole1, (0, 0), wormHole1)
                avatarFunction(window, wormHole1, gameBoard, i, j)
                if gameBoard[i][j][0].occupied == False:
                    continue
            if gameBoard[i][j][0].wormHole2 == True:
                wormHole2 = Image.open("images/wormHole2.png").convert("RGBA")
                avatar.paste(wormHole2, (0, 0), wormHole1)
                avatarFunction(window, wormHole2, gameBoard, i, j)
                if gameBoard[i][j][0].occupied == False:
                    continue
            
        
            if gameBoard[i][j][0].occupied == False:
                
                #0 default - start with the default floor
                if gameBoard[i][j][0].tileType == "default":
                    avatar = PublicPNGList[0].convert("RGBA")
                    avatarFunction(window, avatar, gameBoard, i, j)
                    
                    #if there's a recall waiting
                    if gameBoard[i][j][0].recallTurn != False:
                        #avatar = PublicPNGList[18].convert("RGBA")
                        window[i, j].update(image_filename="images/recall.png")
                        
                    #if the mouse is here
                    if gameBoard[i][j][0].orbEater == True:
                        window[i, j].update(image_data=PublicPNGList[10])
                    if gameBoard[i][j][0].secretAgent != False:
                        avatarFunction(window, PublicPNGList[11], gameBoard, i, j)
                    if gameBoard[i][j][0].purityTile != False:
                        avatarFunction(window, PublicPNGList[12], gameBoard, i, j)
                    continue
                #7 itemOrb
                if gameBoard[i][j][0].tileType == "itemOrb":
                    avatarFunction(window, PublicPNGList[7], gameBoard, i, j)

   
                    #if the mouse is here
                    if gameBoard[i][j][0].orbEater == True:
                        window[i, j].update(image_data=PublicPNGList[10])
                    
                    continue
                #1 destroyed
                if gameBoard[i][j][0].tileType == "destroyed":
                    gameBoard[i][j][0].tileHeight = -2
                    cleanTile(gameBoard[i][j][0])
                    avatarFunction(window, PublicPNGList[1], gameBoard, i, j)
                    #window[i, j].update(image_data=PublicPNGList[1])
                    continue
                #2 mine
                if gameBoard[i][j][0].tileType == "mine":
                    avatarFunction(window, PublicPNGList[2], gameBoard, i, j)
                    #window[i, j].update(image_data=PublicPNGList[2])
                    continue
                #8 trapOrb
                if gameBoard[i][j][0].tileType in [
                    "trap orb 0",
                    "trap orb 1",
                    "trap orb 2",
                ]:
                    avatarFunction(window, PublicPNGList[8], gameBoard, i, j)
                    #window[i, j].update(image_data=PublicPNGList[8])
                    #if the mouse is here
                    if gameBoard[i][j][0].orbEater == True:
                        cleanTile(gameBoard[i][j][0])
                        avatarFunction(window, PublicPNGList[10], gameBoard, i, j)
                        #window[i, j].update(image_data=PublicPNGList[10])
                    continue
                if gameBoard[i][j][0].tileType in ["hand1","hand2","hand3"]:
                    pass
                
                #3 horiLaserTripod
                if gameBoard[i][j][0].tileType == "horiLaserTripod":
                    #avatar = PublicPNGList[3].convert("RGBA")
                    avatarFunction(window, PublicPNGList[3], gameBoard, i, j)
                    #window[i, j].update(image_data= PublicPNGList[3])
                    continue

                if gameBoard[i][j][0].tileType == "vertLaserTripod":
                    avatarFunction(window, PublicPNGList[9], gameBoard, i, j)
                    #window[i, j].update(image_data= PublicPNGList[9])
                    continue
                if gameBoard[i][j][0].tileType in ("player1default","player2default"):
                    gameBoard[i][j][0].tileType = "default"
                    avatarFunction(window, PublicPNGList[0], gameBoard, i, j)
                    if gameBoard[i][j][0].recallTurn != False:
                        avatarFunction(window, PublicPNGList[7], gameBoard, i, j)
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
                    if g.ownedBy == 2:
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

                    if "jump proof" in g.activeBuffs:

                        jumpProof = (PublicPNGList[36]).convert("RGBA")
                        avatar.paste(jumpProof, (0, 0), jumpProof)
                        avatarFunction(window, avatar, gameBoard, i, j)
                        
                    if "vampiricism" in g.activeBuffs:

                        vampiricism = (PublicPNGList[39]).convert("RGBA")
                        avatar.paste(vampiricism, (0, 0), vampiricism)
                        avatarFunction(window, avatar, gameBoard, i, j)
                
                        #jumpProof = Image.open("images/jumpProof.png").convert("RGBA")
                        #avatar.paste(jumpProof, (0, 0), jumpProof)
                    
                    if "dead man's trigger" in g.activeBuffs:
                        deadmanstrigger = Image.open("images/deadmanstrigger.png").convert("RGBA")
                        avatar.paste(deadmanstrigger, (0, 0), deadmanstrigger)

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
                    if "purified1" in g.activeBuffs:
                        purified1 = Image.open("images/purified1.png").convert("RGBA")
                        avatar.paste(purified1, (0, 0), purified1)
                    if "purified0" in g.activeBuffs:
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
                    if g.moveAgain == 2:
                        step2 = Image.open("images/moveAgain2.png").convert("RGBA")
                        avatar.paste(step2, (0, 0), step2)
                    if g.moveAgain == 3:
                        step3 = Image.open("images/moveAgain3.png").convert("RGBA")
                        avatar.paste(step3, (0, 0), step3)
                    if g.moveAgain > 3:
                        stepMax = Image.open("images/moveAgainMax.png").convert("RGBA")
                        avatar.paste(stepMax, (0, 0), stepMax)

                    if g.feralMeatCount == 1:
                        meat1 = Image.open("images/meat1.png").convert("RGBA")
                        avatar.paste(meat1, (0, 0), meat1)
                    elif g.feralMeatCount == 2:
                        meat2 = Image.open("images/meat2.png").convert("RGBA")
                        avatar.paste(meat2, (0, 0), meat2)
                    elif g.feralMeatCount >= 3:
                        meat3 = Image.open("images/meat3.png").convert("RGBA")
                        avatar.paste(meat3, (0, 0), meat3)
                    
                    if "vile" in g.activeDebuffs:
                        vile = Image.open("images/vile.png").convert("RGBA")
                        avatar.paste(vile, (0, 0), vile)

                    # if it's supposed to be highlighted... then highlight it
                    if g.grey == True:
                        grey = (PublicPNGList[34]).convert("RGBA")
##                        grey = Image.open("images/highlight.png").convert("RGBA")
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
                        
                    #teleport to opposite edges
                    if "round earth theory" in g.activeBuffs:
                        roundEarthTheory = Image.open("images/roundEarthTheory.png").convert("RGBA")
                        avatar.paste(roundEarthTheory, (0, 0), roundEarthTheory)

                    #robs your enemy    
                    if gameBoard[i][j][0].secretAgent != False:
                        secretAgent = Image.open("images/secretAgent.png").convert("RGBA")
                        avatar.paste(secretAgent, (0, 0), secretAgent)
                        window[i, j].update(image_filename="images/secretAgent.png")

                    #pure tile to clean pieces
                    if gameBoard[i][j][0].purityTile != False:
                        purityTile = Image.open("images/purityTile.png").convert("RGBA")
                        avatar.paste(purityTile, (0, 0), purityTile)
                        window[i, j].update(image_filename="images/purityTile.png")
                        
                    #recall logo on PIECE    
                    if gameBoard[i][j][1].recallTurn != False:
                            recall1 = Image.open("images/recall1.png").convert("RGBA")
                            avatar.paste(recall1, (0, 0), recall1)
                            window[i, j].update(image_filename="images/recall1.png")
                            
                    #recall logo on TILE
                    if gameBoard[i][j][0].recallTurn != False:
                        
                        recall = Image.open("images/recall.png").convert("RGBA")
                        avatar.paste(recall, (0, 0), recall)
                        window[i, j].update(image_filename="images/recall.png")


            if gameBoard[i][j][0].highlight == True:
                grey = (PublicPNGList[32]).convert("RGBA")
                #grey = Image.open("images/highlightBlue.png").convert("RGBA")
                avatar = Image.blend(grey, avatar, 0.50)


            if gameBoard[i][j][0].highlightRed == True:
                red = (PublicPNGList[33]).convert("RGBA")
                #grey = Image.open("images/highlightBlue.png").convert("RGBA")
                avatar = Image.blend(red, avatar, 0.50)

            if gameBoard[i][j][0].highlightGreen == True:
                green = (PublicPNGList[37]).convert("RGBA")
                #grey = Image.open("images/highlightBlue.png").convert("RGBA")
                avatar = Image.blend(green, avatar, 0.50)
                
            if gameBoard[i][j][0].highlightBrown == True:
                #sg.popup("Brown activated")
                brown = (PublicPNGList[38]).convert("RGBA")
                #grey = Image.open("images/highlightBlue.png").convert("RGBA")
                avatar = Image.blend(brown, avatar, 0.50)


                #g[ix][iy][0].highlightGreen = True

                
            avatarFunction(window, avatar, gameBoard, i ,j)


            



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


# the item list
def pickUpItemOrb(gameBoard=0, x=0, y=0, introOnly = False, window = None, getItemsList = False):
    # items = ["suicideBomb Row","Energy Forcefield","suicideBomb Column","Haphazard Airstrike","suicideBomb Radial","jumpProof","smartBombs"]
    items = [
        "berzerk",
        "bernie sanders",
        "bowling ball",
        "canyon column",
        "canyon radial",
        "canyon row",
        "care package drop",
        "charity",
        "dead man's trigger",
        "dump items",
        "elevate tile",
        "Energy Forcefield",
        "floor restore",
        "haphazard airstrike",
        "haymaker",
        "heir",
        "jump proof",
        "jumpoline",
        "laser column",
        "laser row",
        "magnet",
        "move again",
        "move diagonal",
        "mutual treason column",
        "mutual treason radial",
        "mutual treason row",
        "mystery box",
        "napalm column",
        "napalm radial",
        "napalm row",
        "orb eater",
        "place mine",
        "purify radial",
        "purity tile",
        "recall",
        "reproduce",
        "round earth theory",
        "secretAgent",
        "seismic activity",
        "shuffle column",
        "shuffle item orbs",
        "shuffle radial",
        "shuffle row",
        "sink tile",
        "smart bombs",
        "snake tunneling",
        "spooky hand",
        "steal items column",
        "steal items radial",
        "steal items row",
        "steal powers column",
        "steal powers radial",
        "steal powers row",
        "sticky time bomb",
        #"study column",
        #"study radial",
        "study row",
        "suicide bomb column",
        "suicide bomb radial",
        "suicide bomb row",
        "teach column",
        "teach radial",
        "teach row",
        "trap orb",
        "trump",
        #"trip mine column",
        "trip mine radial",
        #"trip mine row",
        "vile radial",
        "warp",
        #"wololo column",
        "wololo radial",
        #"wololo row",
        "worm hole",
    ]
    if introOnly == True:
        return random.choice(items)
    if getItemsList == True:
        return items

    #pick an item at random; should eventually have biases on the items by separating them into different lists that have different odds of being chosen
    randItem = random.choice(items)
    gameBoard[x][y][1].storedItems.append(randItem)
    playerOwned = gameBoard[x][y][1].ownedBy
    #modifies your avatar to signify the player is holding an item(s)
    gameBoard[x][y][1].avatar = f"player{playerOwned}stored"
    explanation = itemExplanation(randItem)
    #randItemName = randItem.center(35)
    youFoundA = "You found a".center(len(randItem*2))
    pickupFrame = [ [sg.Image(f"images/{randItem}.png",tooltip = explanation) ],
        [sg.T(youFoundA, font = "Cambria 30")],
        [sg.T(randItem, font = "Cambria 50", text_color = "Blue")],
        [sg.T("(Hover over the picture to read about the item)")],
        [sg.Button("SWEET", key = "Affirmative")]
                    ]
        
    pickUpLayout = [
            [sg.Frame("GET ITEM", pickupFrame,element_justification = "center")]
        ]
    window.disable()
    affirmativeList = ("Sweet", "Nice!", "Thanks", "Woot!", "Ok", "K.", "I see...", "Neat.")
    randomChoice = random.choice(affirmativeList)
    
    pickUpWindow = sg.Window("Get item.", pickUpLayout,keep_on_top = True).finalize()
    pickUpWindow["Affirmative"].update(randomChoice)
    a = pickUpWindow.read()
    

    
    if a[0] == "Affirmative":
        pickUpWindow.close()
    window.enable()
    
    
    #sg.PopupAnimated(f"images/{randItem}.png",no_titlebar = False, font = "cambria 20",message = f"Picked up an item orb containing \n[{randItemName}]!")


def jumpoline(window, gameBoard, location, playerTurn):
    validLocations = emptySpots(gameBoard, trueEmpty = True)
    if len(validLocations) == 0:
        sg.popup("Nowhere valid for you to jumpoline to. :(",keep_on_top=True)
        return
    choice = random.choice(validLocations)
    x=choice[0]
    y=choice[1]
    return x,y

def disableEverything(window, turnOn = False):
    if turnOn == False:
        window["exit"].update(disabled = True)
        #window["itemButton"].update(disabled=True)
        window["examineItem"].update(disabled=True)
        ###window["readItems"].update(disabled=True)
        window["cheetz"].update(disabled=True)
    else:
        window["exit"].update(disabled = False)
        #window["itemButton"].update(disabled=False)
        window["examineItem"].update(disabled=False)
        ###window["readItems"].update(disabled=False)
        window["cheetz"].update(disabled=True)



#####################################################################
#  Adding an item:  note that each item you add has a
#  few dependencies.  You must add the item logic in this section,
#  add the name of the file to the function pickUpItemOrbs,
#  add an explanation to the def itemExplanation, add a 75x75 .png
#  to the images folder that matches the item name, and also add a
#  picture, if needed, to def displayBoard if the item has any
#  pictures that need to show up on the board.
#####################################################################
        
# using an item
def useItems(gameBoard, x, y, window):



    gameBoard[x][y][1].storedItems.sort()
    layout = []
    listData = [[sg.T("Item Menu", justification="center", font="Calibri 30")]]
    itemsLength = len(gameBoard[x][y][1].storedItems)
    playerTurn = gameBoard[x][y][1].ownedBy
    updateToolTips(window, gameBoard, playerTurn)
    startLocation = (x,y)
    for i in gameBoard[x][y][1].storedItems:
        picture = f"images/{i}.png"

        #send out the item's name to get an explanation
        explanation = itemExplanation(i)


        if itemsLength < 5:
            listData += [
                [
                    sg.Button(
                        i,
                        key=i,
                        image_filename=picture,
                        tooltip=explanation,
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
                        image_filename=picture,
                        tooltip=explanation,
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
                        image_filename=picture,
                        tooltip=explanation,
                        font="Arial 20",
                        size=(30, 1),
                        button_color=("pink", "grey"),
                        image_size=(400, 30),
                    )
                ]
            ]
            
        
    listData += [[sg.Button("CANCEL")]]

    layout += [[sg.Column(listData, justification="center")]]


    
    itemsMenu = sg.Window("Items Menu", layout,  no_titlebar = True,keep_on_top = True).finalize()
    
    #disable_close=True,
    #grab_anywhere=True
    #keep_on_top=True,
    enemyTurn = 0
    playerTurn = gameBoard[x][y][1].ownedBy
    if playerTurn == 1:
        enemyTurn = 2
    elif playerTurn == 2:
        enemyTurn = 1
    else:
        pm(window, "An error occured in the turn assignment in items")
    rows = len(gameBoard)
    columns = len(gameBoard[0])
    location = (x, y)

    eventList = []
    eventNotReceived = True
    focusOutFlag = False
    itemsMenu.bind('<FocusOut>', '+FOCUS OUT+')

    for i,idata in enumerate(gameBoard):
        for j,jdata in enumerate(idata):
            window[(i,j)].update(disabled = True)
    while True:
        playsound("sounds/click2.wav",block=False)
        event = (itemsMenu.read()) 
        try:
            i = event[0]
            for inum,idata in enumerate(gameBoard):
                for jnum,jdata in enumerate(idata):
                    window[(inum,jnum)].update(disabled = False)
                
            if i == None:
                itemsMenu.close()
                return "earlyBreak"
            if i == "CANCEL":
                itemsMenu.close()
                return "earlyBreak"
            if i == '+FOCUS OUT+':
                itemsMenu.close()
                return "earlyBreak"
                
            
            if i in (0,1,2,3,4,5,6,7,8,9):
                break
        except:
            break

        itemsMenu.close()
        
#all, allHurt, enemiesHurtOnly, alliesHelpedOnly, allOccupiedNeutral, alliesHurtOnly
#def highlightValidDistance(gameBoard, window, startLocation, actionType = "walk", reachType = "cross", turnOff = False):
        
# suicidebomb row
        if str.find(i, "suicide bomb row") >= 0:
            itemsMenu.close()
            gameBoard[x][y][1].grey = False
            highlightValidDistance(gameBoard, window, startLocation, actionType = "allHurt", reachType = "row" )
            displayBoard(window, gameBoard)
            window.refresh()
            yesno = sg.popup_yes_no("Use?",keep_on_top=True)
            if yesno == "No":
                continue

            gameBoard[x][y][1].grey = False
            gameBoard[x][y][1].storedItems.remove("suicide bomb row")
            # for each item inside the specific gameBoard row
            for j in gameBoard[x]:
                if isinstance(j[1], Piece):
                    if "Energy Forcefield" in j[1].activeBuffs:
                        sg.popup("Your shield activated and protected you from damage.", keep_on_top = True)
                        j[1].activeBuffs.remove("Energy Forcefield")
                        continue
                    if j[1].forcefieldTurn == PublicStats.turnCount:
                        sg.popup("Your shield continues to protect you.",keep_on_top = True)
                        continue
                    else:
                        # set the tile to be empty
                        j[0].occupied = False
                        j[1] = 0
                        j[0].tileType = "default"


# canyon row
        elif str.find(i, "canyon row") >= 0:
            itemsMenu.close()
            gameBoard[x][y][1].grey = False
            highlightValidDistance(gameBoard, window, startLocation, actionType = "all", reachType = "row" )
            displayBoard(window, gameBoard)
            window.refresh()
            yesno = sg.popup_yes_no("Lower all affected tiles?",keep_on_top=True)
            if yesno == "No":
                continue
            gameBoard[x][y][1].storedItems.remove("canyon row")
            playsound("sounds/building.mp3",block=False)
            for i in gameBoard[x]:
                i[0].tileHeight = -2
            sg.popup("A canyon row was created.", keep_on_top = True)
            pm(window, "A canyon row was created.")

# canyon column
        elif str.find(i, "canyon column") >= 0:
            itemsMenu.close()
            gameBoard[x][y][1].grey = False
            highlightValidDistance(gameBoard, window, startLocation, actionType = "all", reachType = "column" )
            displayBoard(window, gameBoard)
            window.refresh()
            yesno = sg.popup_yes_no("Lower all affected tiles?",keep_on_top=True)
            if yesno == "No":
                continue
            gameBoard[x][y][1].storedItems.remove("canyon column")
            playsound("sounds/building.mp3",block=False)
            for i in gameBoard:
                i[y][0].tileHeight = -2
            sg.popup("A canyon column was created.", keep_on_top = True)
            pm(window, "A canyon column was created.")

#canyon radial
        elif str.find(i, "canyon radial") >= 0:
            itemsMenu.close()
            gameBoard[x][y][1].grey = False
            highlightValidDistance(gameBoard, window, startLocation, actionType = "all", reachType = "radial" )
            displayBoard(window, gameBoard)
            window.refresh()
            yesno = sg.popup_yes_no("Lower all affected tiles?",keep_on_top=True)
            if yesno == "No":
                continue
            gameBoard[x][y][1].storedItems.remove("canyon radial")
            playsound("sounds/building.mp3",block=False)
            validLocations = getRadial(location, gameBoard)
            for i in validLocations:
                ix = i[0]
                iy = i[1]
                gameBoard[ix][iy][0].tileHeight = -2
            sg.popup("A canyon radial was created.", keep_on_top = True)
            pm(window, "A canyon radial was created.")

            
#elevate tile
        elif str.find(i, "elevate tile") >= 0:
            itemsMenu.close()
            yesno = sg.popup_yes_no("Elevate the tile you're on?",keep_on_top=True)
            if yesno == "No":
                continue
            elevateTileLayout = [
                [ sg.T(f"What level would you like to increase the elevation to? (CurrentElevation: {gameBoard[x][y][0].tileHeight})") ],
                [ sg.Button(f"Elevation {elevation}",key = f"elevation{elevation}")for elevation in range(-1,3)],[sg.Button("Cancel")]
                ]
            elevateWindow = sg.Window("Choose an elevation", elevateTileLayout,keep_on_top = True)
            while True:
                window.disable()
                event = elevateWindow.read()
                window.enable()
                if event[0] == f"elevation-1":
                    raiseTile = -1
                elif event[0] == f"elevation0":
                    raiseTile = 0
                elif event[0] == f"elevation1":
                    raiseTile = 1
                elif event[0] == f"elevation2":
                    raiseTile = 2
                elif event[0] == "Cancel":
                    elevateWindow.close()
                    break
                if raiseTile <= gameBoard[x][y][0].tileHeight:
                    sg.popup("You must pick a height greater than the current height.", keep_on_top = True)
                    pm(window,"You must pick a height greater than the current height.")
                    continue
                if raiseTile > gameBoard[x][y][0].tileHeight:
                    gameBoard[x][y][0].tileHeight = raiseTile
                    sg.popup("The tile was raised up!  Look down upon the peons.", keep_on_top = True)
                    pm(window,"The tile was raised up!  Look down upon the peons.")
                    elevateWindow.close()
                    break


#sink tile
        elif str.find(i, "sink tile") >= 0:
            itemsMenu.close()
            yesno = sg.popup_yes_no("Lower the tile you're on?",keep_on_top=True)
            if yesno == "No":
                continue
            elevateTileLayout = [
                [ sg.T(f"What level would you like to decrease the elevation to? (CurrentElevation: {gameBoard[x][y][0].tileHeight})") ],
                [ sg.Button(f"Elevation {elevation}",key = f"elevation{elevation}")for elevation in range(-2,2)],[sg.Button("Cancel")]
                ]
            elevateWindow = sg.Window("Choose an elevation", elevateTileLayout,keep_on_top = True)
            while True:
                window.disable()
                event = elevateWindow.read()
                window.enable()
                if event[0] == f"elevation-2":
                    lowerTile = -2
                elif event[0] == f"elevation-1":
                    lowerTile = -1
                elif event[0] == f"elevation0":
                    lowerTile = 0
                elif event[0] == f"elevation1":
                    lowerTile = 1
                elif event[0] == "Cancel":
                    elevateWindow.close()
                    break
                if lowerTile >= gameBoard[x][y][0].tileHeight:
                    sg.popup("You must pick a height lower than the current height.", keep_on_top = True)
                    pm(window,"You must pick a height lower than the current height.")
                    continue
                if lowerTile < gameBoard[x][y][0].tileHeight:
                    gameBoard[x][y][0].tileHeight = lowerTile
                    sg.popup("The tile was lowered down!  I guess you like looking up to others?", keep_on_top = True)
                    pm(window,"The tile was lowered down!  I guess you like looking up to other?")
                    elevateWindow.close()
                    break
                
##            if gameBoard[x][y][0].tileHeight == 2:
##                sg.popup("Tile is already at maximum elevation; it can't be raised further", keep_on_top = True)
##                pm(window, "Tile is already at maximum elevation; it can't be raised further")
##                continue
##            else:
##                gameBoard[x][y][0].tileHeight+=1
##                if gameBoard[x][y][0].tileHeight > 2:
##                    gameBoard[x][y][0].tileHeight = 2
##                gameBoard[x][y][1].storedItems.remove("elevate tile")
##                sg.popup(f"The tile was raised to a height of {gameBoard[x][y][0].tileHeight}", keep_on_top = True)
##                continue

#sink tile
        elif str.find(i, "sink tile") >= 0:
            itemsMenu.close()
            yesno = sg.popup_yes_no("Sink this tile?",keep_on_top=True)
            if yesno == "No":
                continue
            if gameBoard[x][y][0].tileHeight == 2:
                sg.popup("Tile is already at maximum elevation; it can't be raised further", keep_on_top = True)
                pm(window, "Tile is already at maximum elevation; it can't be raised further")
                continue
            else:
                gameBoard[x][y][0].tileHeight+=1
                if gameBoard[x][y][0].tileHeight > 2:
                    gameBoard[x][y][0].tileHeight = 2
                gameBoard[x][y][1].storedItems.remove("elevate tile")
                sg.popup(f"The tile was raised to a height of {gameBoard[x][y][0].tileHeight}", keep_on_top = True)
                continue
#seismic activity
        elif str.find(i, "seismic activity") >= 0:
            itemsMenu.close()
            yesno = sg.popup_yes_no("Induce an earthquake?  This will cause random elevation changes to the field.  Pieces will not be harmed.",keep_on_top=True)
            if yesno == "No":
                continue
            magnitude = random.randint(1,10)
            gameBoard[x][y][1].storedItems.remove("seismic activity")
            if magnitude in (1,2,3,4):
                raiseLower = (-1,0,0,0,0,1)
                playsound("sounds/earthquake.wav",block=False)
                for j in gameBoard:
                    for i in j:
                        change = random.choice(raiseLower)
                        i[0].tileHeight = i[0].tileHeight + change
                        if i[0].tileHeight < -2:
                            i[0].tileHeight = -2
                        elif i[0].tileHeight > 2:
                            i[0].tileHeight = 2
                sg.popup(f"A minor magnitude {magnitude} earthquake hit.",keep_on_top = True)
            if magnitude in (5,6,7,8):
                raiseLower = (-2,-1,-1,0,0,0,0,1,1,1,2)
                playsound("sounds/earthquake.wav",block=False)
                for j in gameBoard:
                    for i in j:
                        change = random.choice(raiseLower)
                        i[0].tileHeight = i[0].tileHeight + change
                        
                        if i[0].tileHeight < -2:
                            i[0].tileHeight = -2
                        elif i[0].tileHeight > 2:
                            i[0].tileHeight = 2
                        
                sg.popup(f"A high magnitude {magnitude} earthquake hit.",keep_on_top = True)
            if magnitude in (9,10):
                raiseLower = (-2,-1,1,+2)
                playsound("sounds/earthquake.wav",block=False)
                for j in gameBoard:
                    for i in j:
                        change = random.choice(raiseLower)
                        i[0].tileHeight = i[0].tileHeight + change
                        if i[0].tileHeight < -2:
                            i[0].tileHeight = -2
                        elif i[0].tileHeight > 2:
                            i[0].tileHeight = 2
                sg.popup(f"An extreme magnitude {magnitude} earthquake hit!  The playing field has been altered significantly.",keep_on_top = True)


#invert elevation all
        elif str.find(i, "invert elevation all") >= 0:
            itemsMenu.close()
##            highlightValidDistance(gameBoard, window, startLocation, actionType = "all", reachType = "invert elevation all" )
##            displayBoard(window, gameBoard)
##            window.refresh()
            yesno = sg.popup_yes_no("Do you want to invert all the heights of tiles on the field to their opposites? (low -> high, high -> low, neutral height tiles will be unaffected)",keep_on_top=True)
            if yesno == "No":
                continue

            for i in gameBoard:
                for j in i:
                    j[0].tileHeight *= -1
            sg.popup("The field's topology has been inverted.  All highs are lows, and all lows are highs.", keep_on_top = True)
            pm(window,"The field's topology has been inverted.  All highs are lows, and all lows are highs.")
            gameBoard[x][y][1].storedItems.remove("invert elevation all")
        
#trump
        elif str.find(i, "trump") >= 0:
            itemsMenu.close()
            yesno = sg.popup_yes_no("Do you want to build a wall and make your opponent pay for it?* (*The wall is free and no one will actually pay for it)",keep_on_top=True)
            if yesno == "No":
                continue

            wallWindowLayout = [
                [ sg.T(f"The wall can be built in either your row or your column.  The wall will raise all existing tiles in range, but will not repair any broken tiles.  Any pieces that are on the tiles will not be affected other than being elevated.") ],
                [ sg.Button(f"Build Row Wall",key = "row wall"), sg.Button(f"Build Column Wall", key = "column wall"),sg.Button("Cancel")]
                ]
            wallWindow = sg.Window("Do you want to build a wall?", wallWindowLayout)
            while True:
                event = wallWindow.read()
                if event[0] == "Cancel":
                    wallWindow.close()
                    break
                if event[0] == "row wall":
                    for i in gameBoard[x]:
                        wallWindow.close()
                        i[0].tileHeight = 2
                    gameBoard[x][y][1].storedItems.remove("trump")
                    playsound("sounds\\building.mp3",block = False)
                    sg.popup("The wall was built with the most covfefe of engineering.  Congrats!", keep_on_top = True)
                    pm(window, "The wall was built with the most covfefe of engineering.  Congrats!")
                    break
                if event[0] == "column wall":
                    for i in gameBoard:
                        wallWindow.close()
                        i[y][0].tileHeight = 2
                    playsound("sounds\\building.mp3",block = False)
                    gameBoard[x][y][1].storedItems.remove("trump")
                    sg.popup("The wall was built with the most covfefe of engineering.  Congrats!", keep_on_top = True)
                    pm(window, "The wall was built with the most covfefe of engineering.  Congrats!")
                    break
# steal items column
        elif str.find(i, "steal items column") >= 0:
            itemsMenu.close()
            highlightValidDistance(gameBoard, window, startLocation, actionType = "enemiesHurtOnly", reachType = "column" )
            displayBoard(window, gameBoard)
            window.refresh()
            yesno = sg.popup_yes_no("Use?",keep_on_top=True)
            if yesno == "No":
                continue
            stolenItems = 0
            namesOfStolenItems = ""
            for iIndex, i in enumerate(gameBoard):
                if i[y][0].occupied == True:
                    if i[y][1].ownedBy == enemyTurn:
                        for items in i[y][1].storedItems:
                            gameBoard[x][y][1].storedItems.append(items)
                            stolenItems+=1
                            namesOfStolenItems+=items+"\n"
                        i[y][1].storedItems.clear()
            if stolenItems > 0:
                playsound("sounds\yoink.mp3",block = False)
                sg.popup(f"You've stolen {stolenItems} items:\n"+namesOfStolenItems, keep_on_top = True)
            
            gameBoard[x][y][1].storedItems.remove("steal items column")


# steal items row
        elif str.find(i, "steal items row") >= 0:
            itemsMenu.close()
            highlightValidDistance(gameBoard, window, startLocation, actionType = "enemiesHurtOnly", reachType = "row" )
            displayBoard(window, gameBoard)
            window.refresh()
            yesno = sg.popup_yes_no("Use?",keep_on_top=True)
            if yesno == "No":
                continue
            stolenItems = 0
            namesOfStolenItems = ""
            for iIndex, i in enumerate(gameBoard[x]):
                if i[0].occupied == True:
                    if i[1].ownedBy == enemyTurn:
                        for items in i[1].storedItems:
                            gameBoard[x][y][1].storedItems.append(items)
                            stolenItems+=1
                            namesOfStolenItems+=items+"\n"
                        i[1].storedItems.clear()
            if stolenItems > 0:
                playsound("sounds\yoink.mp3",block = False)
                sg.popup(f"You've stolen {stolenItems} items:\n"+namesOfStolenItems, keep_on_top = True)
            
            gameBoard[x][y][1].storedItems.remove("steal items row")

# steal items radial
        elif str.find(i, "steal items radial") >= 0:
            itemsMenu.close()
            highlightValidDistance(gameBoard, window, startLocation, actionType = "enemiesHurtOnly", reachType = "radial" )
            displayBoard(window, gameBoard)
            window.refresh()
            yesno = sg.popup_yes_no("Use?",keep_on_top=True)
            if yesno == "No":
                continue
            stolenItems = 0
            namesOfStolenItems = ""

            validCoordinates = getRadial(location, gameBoard)
            
            for i in (validCoordinates):
                ix = i[0]
                iy = i[1]
                g = gameBoard[ix][iy]
                if g[0].occupied == True:
                    if g[1].ownedBy == enemyTurn:
                        for items in g[1].storedItems:
                            gameBoard[x][y][1].storedItems.append(items)
                            stolenItems+=1
                            namesOfStolenItems+=items+"\n"
                        g[1].storedItems.clear()
            if stolenItems > 0:
                playsound("sounds\yoink.mp3",block = False)
                sg.popup(f"You've stolen {stolenItems} items:\n"+namesOfStolenItems, keep_on_top = True)
            
            gameBoard[x][y][1].storedItems.remove("steal items radial")
            
# steal powers column
        elif str.find(i, "steal powers column") >= 0:
            itemsMenu.close()
            highlightValidDistance(gameBoard, window, startLocation, actionType = "enemiesHurtOnly", reachType = "column" )
            displayBoard(window, gameBoard)
            window.refresh()
            yesno = sg.popup_yes_no("Use?",keep_on_top=True)
            if yesno == "No":
                continue
            stolenPowers = 0
            namesOfStolenPowerss = ""
            for iIndex, i in enumerate(gameBoard):
                if i[y][0].occupied == True:
                    if i[y][1].ownedBy == enemyTurn:
                        for powers in i[y][1].activeBuffs:
                            if powers != "bowling ball":
                                gameBoard[x][y][1].activeBuffs.append(powers)
                                stolenpowers+=1
                                namesOfStolenpowers+=powers+"\n"
                        i[y][1].activeBuffs.clear()
            if stolenPowers > 0:
                playsound("sounds\yoink.mp3",block = False)
                sg.popup(f"You've stolen {stolenPowers} powers:\n"+namesOfStolenPowers, keep_on_top = True)
            
            gameBoard[x][y][1].itemsStored.remove("steal powers column")


# steal powers row
        elif str.find(i, "steal powers row") >= 0:
            itemsMenu.close()
            highlightValidDistance(gameBoard, window, startLocation, actionType = "enemiesHurtOnly", reachType = "row" )
            displayBoard(window, gameBoard)
            window.refresh()
            yesno = sg.popup_yes_no("Use?",keep_on_top=True)
            if yesno == "No":
                continue
            stolenpowers = 0
            namesOfStolenpowers = ""
            for iIndex, i in enumerate(gameBoard[x]):
                if i[0].occupied == True:
                    if i[1].ownedBy == enemyTurn:
                        for powers in i[1].activeBuffs:
                            if powers != "bowling ball":
                                gameBoard[x][y][1].activeBuffs.append(powers)
                                stolenpowers+=1
                                namesOfStolenpowers+=powers+"\n"
                        i[1].activeBuffs.clear()
            if stolenpowers > 0:
                playsound("sounds\yoink.mp3",block = False)
                sg.popup(f"You've stolen {stolenpowers} powers:\n"+namesOfStolenpowers, keep_on_top = True)
            
            gameBoard[x][y][1].itemsStored.remove("steal powers row")

# steal powers radial
        elif str.find(i, "steal powers radial") >= 0:
            itemsMenu.close()
            highlightValidDistance(gameBoard, window, startLocation, actionType = "enemiesHurtOnly", reachType = "radial" )
            displayBoard(window, gameBoard)
            window.refresh()
            yesno = sg.popup_yes_no("Use?",keep_on_top=True)
            if yesno == "No":
                continue
            stolenpowers = 0
            namesOfStolenpowers = ""

            validCoordinates = getRadial(location, gameBoard)
            
            for i in (validCoordinates):
                ix = i[0]
                iy = i[1]
                g = gameBoard[ix][iy]
                if g[0].occupied == True:
                    if g[1].ownedBy == enemyTurn:
                        for powers in g[1].activeBuffs:
                            if powers != "bowling ball":
                                gameBoard[x][y][1].activeBuffs.append(powers)
                                stolenpowers+=1
                                namesOfStolenpowers+=powers+"\n"
                        g[1].activeBuffs.clear()
            if stolenpowers > 0:
                playsound("sounds\yoink.mp3",block = False)
                sg.popup(f"You've stolen {stolenpowers} powers:\n"+namesOfStolenpowers, keep_on_top = True)
            
            gameBoard[x][y][1].itemsStored.remove("steal powers radial")                              

# teach column
        elif str.find(i, "teach column") >= 0:
            itemsMenu.close()
            highlightValidDistance(gameBoard, window, startLocation, actionType = "all", reachType = "column" )
            displayBoard(window, gameBoard)
            window.refresh()
            yesno = sg.popup_yes_no("Use?",keep_on_top=True)
            if yesno == "No":
                continue
            
            gameBoard[x][y][1].grey = False
            #if there is fewer than one item in the list
            if len(gameBoard[x][y][1].activeBuffs) < 1:
                sg.popup("You won't have any buffs to teach.  Aborted.",keep_on_top=True)
                continue
            gameBoard[x][y][1].storedItems.remove("teach column")
            taughtPieces = 0
            taughtString = ""
            for k in gameBoard[x][y][1].activeBuffs:
                    
                    taughtString += k + "\n"
            sg.popup("Teaching:\n"+taughtString,keep_on_top=True)
            # for every row in gameBoard
            for iIndex, i in enumerate(gameBoard):
                #if the x'th item belongs to you, and it's not the same item that's sharing the items
                
                if i[y][0].occupied == True and "bowling ball" not in i[y][1].activeBuffs and i[y][1].ownedBy == playerTurn and iIndex != x and "burdened" not in i[y][1].activeDebuffs:
                    #for every item in the active buffs list
                    i[y][1].grey = True
                    
                    displayBoard(window,gameBoard)
                    window.refresh()
                    taughtPieces += 1
                    for k in gameBoard[x][y][1].activeBuffs:
                        
                        i[y][1].activeBuffs.append(k)
                        
                        
                    i[y][1].grey = False
                    
                else:
                    continue
            sg.popup(f"Taught buffs to {taughtPieces} piece(s).",keep_on_top=True)
            pm(window,f"Taught buffs to {taughtPieces} piece(s).")
            
        elif str.find(i, "heir") >= 0:
            itemsMenu.close()
            highlightValidDistance(gameBoard, window, startLocation, actionType = "alliesHurtOnly", reachType = "all" )
            displayBoard(window, gameBoard)
            window.refresh()
            yesno = sg.popup_yes_no("Use?",keep_on_top=True)
            if yesno == "No":
                continue

            if "burdened" in gameBoard[x][y][1].activeDebuffs:
                sg.popup("This piece cannot acquire item orbs as it is burdened by an effect.")
                pm(window, "This piece cannot acquire item orbs as it is burdened by an effect.")
                continue

            itemsCount = 0
            for i in gameBoard:
                for j in i:
                    if j[0].occupied and j[1].ownedBy == playerTurn and j[1]!= gameBoard[x][y][1]:
                        for items in j[1].storedItems:
                            gameBoard[x][y][1].storedItems.append(items)
                            itemsCount+=1
                        j[1].storedItems.clear()
            if itemsCount > 0:
                sg.popup(f"You've inherited {itemsCount} items from your allies.  Don't get yourself killed, now.",keep_on_top = True)
                pm(window,f"You've inherited {itemsCount} items from your allies.  Don't get yourself killed, now.")
                
            updateToolTips(window, gameBoard, playerTurn)
            sleep(2)

#vampiricism
        elif str.find(i, "vampiricism") >= 0:
                itemsMenu.close()
                yesno = sg.popup_yes_no("Use?",keep_on_top=True)
                if yesno == "Apply the vampricism buff to yourself?  (Jump killing an enemy allows you to steal (most) powers from them)":
                    continue
                playsound("sounds/vampire.mp3",block=False)
                gameBoard[x][y][1].activeBuffs.append("vampiricism")
                gameBoard[x][y][1].storedItems.remove("vampiricism")
                    
                        
            
#bernie sanders   
        elif str.find(i, "bernie sanders") >= 0:
            itemsMenu.close()
            highlightValidDistance(gameBoard, window, startLocation, actionType = "allOccupiedNeutral", reachType = "all" )
            displayBoard(window, gameBoard)
            window.refresh()
            yesno = sg.popup_yes_no("Use?",keep_on_top=True)
            if yesno == "No":
                continue
            
            itemsCollected = []
            validPieces = []
            gameBoard[x][y][1].storedItems.remove("bernie sanders")
            count = 0
            
            for iIndex, iData in enumerate(gameBoard):
                for jIndex,j in enumerate(iData):
                    #if there is a piece
                    if j[0].occupied == True:
                        #grab (a copy of) all its items
                        for k in j[1].storedItems:
                            itemsCollected.append(k)
                        #delete the original items
                        j[1].storedItems.clear()
                        if "burdened" not in j[1].activeDebuffs and "bowling ball" not in j[1].activeBuffs:
                            validPieces.append( (iIndex, jIndex) )
                            count+=1
            displayBoard(window, gameBoard)
            window.refresh()
            sg.popup("Bernie has taken everyone's wealth",keep_on_top = True)
            for i in itemsCollected:
                luckyRecipient = random.choice(validPieces)
                xi = luckyRecipient[0]
                yi = luckyRecipient[1]
                gameBoard[xi][yi][1].storedItems.append(i)
            itemsRedistributed = len(itemsCollected)
            itemsCollected.clear()
            updateToolTips(window, gameBoard,playerTurn)
            sg.popup(f"{itemsRedistributed} items have been redistributed!",keep_on_top = True)
            pm(window,f"{itemsRedistributed} items have been redistributed!")

# care package drop
        # care package drop
        elif str.find(i, "care package drop") >= 0:
            itemsMenu.close()
            sg.popup("Choose an enemy to center the item airdrop on",keep_on_top=True)

            event = window.read()
            location = event[0]
            x1 = location[0]
            y1 = location[1]

            if gameBoard[x1][y1][0].occupied == False:
                sg.popup("There's no one there; the package drop requires you choose an enemy",keep_on_top=True)
                continue
            elif gameBoard[x1][y1][1].ownedBy == playerTurn:
                sg.popup("You cannot center the airdrop on your own piece.",keep_on_top=True)
                continue
            else:
                gameBoard[x][y][1].storedItems.remove("care package drop")
                validLocations = getRadial(location, gameBoard)
                
                for i in validLocations:
                    dropX = i[0]
                    dropY = i[1]
                    gameBoard[dropX][dropY][0].tileType = "itemOrb"
                    gameBoard[dropX][dropY][0].grey = True
                    isOccupied = False
                    if gameBoard[dropX][dropY][0].occupied == True:
                        isOccupied = True
                    gameBoard[dropX][dropY][0].occupied = False
                    displayBoard(window,gameBoard)
                    window.refresh()
                    sleep(.3)
                    gameBoard[dropX][dropY][0].grey = False
                    if isOccupied == True:
                        gameBoard[dropX][dropY][0].occupied = True
                    window.refresh()
                    sleep(.3)



    
# dump items
        elif str.find(i, "dump items") >= 0:
            itemsMenu.close()
            if len(gameBoard[x][y][1].storedItems) < 2:
                sg.popup("There won't be any items to dump.  Canceling.",keep_on_top=True)
                continue
            validLocations = emptySpots(gameBoard, trueEmpty = True)
            sg.popup("Pick any empty spot to drop all of your items into.  Anyone can pick it up.  Click yourself if you don't wish to use this.",keep_on_top=True)
            disableEverything(window)
            event = window.read()
            
            if event[0] == (location):
                sg.popup("Canceled the dump",keep_on_top=True)
                disableEverything(window,turnOn = True)
                continue
            elif event[0] in validLocations:
                x1 = event[0][0]
                y1 = event[0][1]
                dumpCount = 0
                gameBoard[x][y][1].storedItems.remove("dump items")
                for i in gameBoard[x][y][1].storedItems:
                    
                    gameBoard[x1][y1][0].dumpList.append(i)
                    dumpCount +=1
                 
                gameBoard[x][y][1].storedItems.clear()
                sg.popup(f"Dumped {dumpCount} item(s)",keep_on_top=True)
                disableEverything(window,turnOn = True)
                gameBoard[x1][y1][0].tileType = "itemDump"
                
            #updateToolTips(window, gameBoard, playerTurn)
# charity            
        elif str.find(i, "charity") >= 0:
            itemsMenu.close()
            validLocations = emptySpots(gameBoard)
            if len(validLocations) < 1:
                sg.popup("There's no space to gift an extra piece to your opponent.",keep_on_top=True)
            else:
                sg.popup("Pick any unoccupied space on the board to spawn a free basic piece for your opponent.  How charitable!",keep_on_top=True)
                pm(window, "Pick any unoccupied space on the board to spawn a free basic piece for your opponent.  How charitable!")
                window["exit"].update(disabled = False)
                #window["itemButton"].update(disabled=True)
                window["examineItem"].update(disabled=True)
                ###window["readItems"].update(disabled=True)
                event = window.read()
                x1 = event[0][0]
                y1 = event[0][1]
                if "exit" in event[0]:
                    
                    quityesno = sg.popup_yes_no("You seriously want to quit?!",keep_on_top=True)
                    
                    if quityesno == "Yes":
                        sg.popup("Whatever.  Get lost.",keep_on_top=True)
                        window.close()
                        raise SystemExit
                    else:
                        continue
                else:
                    if not event[0] in validLocations:
                        sg.popup("That's not a valid spot.  Canceling",keep_on_top=True)
                    else:
                        
                        gameBoard[x][y][1].storedItems.remove("charity")
                        #set the location as active
                        gameBoard[x1][y1][0].occupied = True
                        #we need to find the enemy's number to provide it to the piece class below
                        if playerTurn == 1:
                            enemy = 2
                        elif playerTurn ==2:
                            enemy = 1
                        #create a new basic piece at the location given, and under the control of the enemy
                        gameBoard[x1][y1][1] = Piece(x1,y1,enemy)
            
           
                

# teach radial
        elif str.find(i, "teach radial") >= 0:
            itemsMenu.close()
            gameBoard[x][y][1].grey = False
            #if there is fewer than one item in the list
            if len(gameBoard[x][y][1].activeBuffs) < 1:
                sg.popup("You won't have any buffs to teach.  Aborted.",keep_on_top=True)
                continue
            gameBoard[x][y][1].storedItems.remove("teach radial")
            taughtPieces = 0
            taughtString = ""
            for k in gameBoard[x][y][1].activeBuffs:
                    
                    taughtString += k + "\n"
            sg.popup("Teaching:\n"+taughtString,keep_on_top=True)
            # for every row in gameBoard
            location = (x,y)
            validLocations = getRadial(location,gameBoard)
            for i in validLocations:
                ix = i[0]
                iy = i[1]
                #if the x'th item belongs to you, and it's not the same item that's sharing the items
                
                if gameBoard[ix][iy][0].occupied == True and "bowling ball" not in gameBoard[ix][iy][1].activeBuffs and gameBoard[ix][iy][1].ownedBy == playerTurn and (ix,iy) != (x,y) and "burdened" not in gameBoard[ix][iy][1].activeDebuffs:
                    #for every item in the active buffs list
                    gameBoard[ix][iy][1].grey = True
                    
                    displayBoard(window,gameBoard)
                    window.refresh()
                    taughtPieces += 1
                    for k in gameBoard[x][y][1].activeBuffs:
                        
                        gameBoard[ix][iy][1].activeBuffs.append(k)
                        
                        
                    gameBoard[ix][iy][1].grey = False
                    
                else:
                    continue
            sg.popup(f"Taught buffs to {taughtPieces} piece(s).",keep_on_top=True)
            pm(window,f"Taught buffs to {taughtPieces} piece(s).")

#study row            
        elif str.find(i, "study row") >= 0:            
            itemsMenu.close()
            gameBoard[x][y][1].grey = False
            if "inert" in gameBoard[x][y][1].activeDebuffs:
                sg.popup("This piece is inert and can't learn anything",keep_on_top=True)
                continue
            learnedFromPieces = 0
            learnedString = ""
            bowlingBallRejected = False
            # for every column in gameBoard
            for iIndex, i in enumerate(gameBoard[x]):
                #if the x'th item belongs to you, and it's not the same item that's sharing the items
                
                if i[0].occupied == True and i[1].ownedBy == playerTurn and iIndex != y and len(i[1].activeBuffs)>0:
                    #for every item in the active buffs list
                    i[1].grey = True
                    pm(window,"Learning")
                    displayBoard(window,gameBoard)
                    window.refresh()
                    learnedFromPieces += 1
                    for k in gameBoard[x][iIndex][1].activeBuffs:
                        if k != "bowling ball":
                            gameBoard[x][y][1].activeBuffs.append(k)
                        else:
                            bowlingBallRejected = True
                    i[1].grey = False
                else:
                    continue
            if bowlingBallRejected == True:
                sg.popup("You attempted to learn bowling ball from at least one piece, but it proved to be too difficult.",keep_on_top=True)
            sg.popup(f"Learned buffs from {learnedFromPieces} piece(s).", keep_on_top = True)
            pm(window,f"Learned buffs from {learnedFromPieces} piece(s).")

            
# teach row
        elif str.find(i, "teach row") >= 0:
            itemsMenu.close()


            highlightValidDistance(gameBoard, window, startLocation, actionType = "alliesHelpedOnly", reachType = "row" )
            displayBoard(window, gameBoard)
            window.refresh()
            yesno = sg.popup_yes_no("Use?",keep_on_top=True)
            if yesno == "No":
                continue
            gameBoard[x][y][1].grey = False
            #if there is fewer than one item in the list
            if len(gameBoard[x][y][1].activeBuffs) < 1:
                sg.popup("You won't have any buffs to teach.  Aborted.",keep_on_top=True)
                continue
            gameBoard[x][y][1].storedItems.remove("teach row")
            taughtPieces = 0
            taughtString = ""
            for k in gameBoard[x][y][1].activeBuffs:
                    
                    taughtString += k + "\n"
            sg.popup("Teaching:\n"+taughtString,keep_on_top=True)
            # for every column in gameBoard
            for iIndex, i in enumerate(gameBoard[x]):
                #if the x'th item belongs to you, and it's not the same item that's sharing the items
                
                if i[0].occupied == True and "bowling ball" not in i[1].activeBuffs and i[1].ownedBy == playerTurn and iIndex != y and "burdened" not in i[1].activeDebuffs:
                    #for every item in the active buffs list
                    i[1].grey = True
                    
                    displayBoard(window,gameBoard)
                    window.refresh()
                    taughtPieces += 1
                    for k in gameBoard[x][y][1].activeBuffs:
                        
                        i[1].activeBuffs.append(k)
                        
                        
                    i[1].grey = False
                    
                else:
                    continue
            sg.popup(f"Taught buffs to {taughtPieces} piece(s).",keep_on_top=True)
            pm(window,f"Taught buffs to {taughtPieces} piece(s).")
            
            
# deadman's trigger                        
        elif str.find(i,"dead man's trigger") >= 0:
            itemsMenu.close()
            gameBoard[x][y][1].storedItems.remove("dead man's trigger")
            gameBoard[x][y][1].activeBuffs.append("dead man's trigger")
            sg.popup("This piece has applied a dead man's trigger to itself.  If he is jumped by an enemy, they will die as well.",keep_on_top=True)

# mutual treason row  
        elif str.find(i,"mutual treason row") >=0 or str.find(i,"mutual treason column")>=0 or str.find(i,"mutual treason radial")>=0:
            itemsMenu.close()
            validList = []
            if i == "mutual treason row":
                validList = getRow(location, gameBoard)
                gameBoard[x][y][1].storedItems.remove("mutual treason row")
            elif i == "mutual treason radial":
                validList = getRadial(location, gameBoard)
                gameBoard[x][y][1].storedItems.remove("mutual treason radial")
            elif i == "mutual treason column":
                validList = getColumn(location, gameBoard)
                gameBoard[x][y][1].storedItems.remove("mutual treason column")

            for i in validList:
                x1 = i[0]
                y1 = i[1]
                if gameBoard[x1][y1][0].occupied == True:
                    if gameBoard[x1][y1][1].ownedBy == 1:
                        gameBoard[x1][y1][1].ownedBy = 2
                    elif gameBoard[x1][y1][1].ownedBy == 2:
                        gameBoard[x1][y1][1].ownedBy = 1
            sg.popup("All affected pieces have changed their allegiances",keep_on_top=True)
# jumpoline
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
                    sg.popup("Must pick an empty spot",keep_on_top=True)
                    pm(window, "Must pick an empty spot")
                    break
                elif g[0].tileType != "default":
                    sg.popup("Must be a valid tile",keep_on_top=True)
                    pm(window, "Must be a valid tile")
                    break
                else:
                    gameBoard[x][y][1].storedItems.remove("jumpoline")
                    g[0].tileType = "jumpoline"
            else:
                sg.popup("Invalid location",keep_on_top=True)
                break

# mystery box
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
                    sg.popup("Must pick an empty spot",keep_on_top=True)
                    pm(window, "Must pick an empty spot")
                    break
                elif g[0].tileType != "default":
                    sg.popup("Must be a valid tile",keep_on_top=True)
                    pm(window, "Must be a valid tile")
                    break
                else:
                    gameBoard[x][y][1].storedItems.remove("mystery box")
                    #g[0].secretAgent = playerTurn
                    g[0].tileType = "mystery box"

            else:
                sg.popup("Invalid location",keep_on_top=True)
                break
            
# floor restore            
        elif str.find(i,"floor restore") >= 0:
            itemsMenu.close()
            gameBoard[x][y][1].storedItems.remove("floor restore")
            for i in gameBoard:
                for j in i:
                    if j[0].tileType in(
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
                        j[0].tileType = "default"
            sg.popup("Any damaged floors are back to brand new condition",keep_on_top=True)

# secretAgent          
        elif str.find(i,"secretAgent") >= 0:
            itemsMenu.close()
            validTargets = getCross((x, y), gameBoard, trueEmpty = True)
            
            pm(window, "Pick an adjacent location to place the secretAgent.")
            event = window.read()
            if event[0] in validTargets:
                x1 = event[0][0]
                y1 = event[0][1]
                g = gameBoard[x1][y1]
                if g[0].occupied == True:
                    sg.popup("Must pick an empty spot",keep_on_top=True)
                    pm(window, "Must pick an empty spot")
                    break
                elif g[0].tileType != "default":
                    sg.popup("Must be a valid tile",keep_on_top=True)
                    pm(window, "Must be a valid tile")
                    break
                else:
                    gameBoard[x][y][1].storedItems.remove("secretAgent")
                    g[0].secretAgent = playerTurn
                    

            else:
                sg.popup("Invalid location",keep_on_top=True)
                break
# purity tile
        elif str.find(i,"purity tile") >= 0:
            itemsMenu.close()
            validTargets = getCross((x, y), gameBoard, trueEmpty = True)
            
            pm(window, "Pick an adjacent location to place the purity tile.")
            event = window.read()
            if event[0] in validTargets:
                x1 = event[0][0]
                y1 = event[0][1]
                g = gameBoard[x1][y1]
                if g[0].occupied == True:
                    sg.popup("Must pick an empty spot",keep_on_top=True)
                    pm(window, "Must pick an empty spot")
                    break
                elif g[0].tileType != "default":
                    sg.popup("Must be a valid tile",keep_on_top=True)
                    pm(window, "Must be a valid tile")
                    break
                else:
                    gameBoard[x][y][1].storedItems.remove("purity tile")
                    g[0].purityTile = playerTurn
                    

            else:
                sg.popup("Invalid location",keep_on_top=True)
                break
            
# reproduce            
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
                    sg.popup("Must pick an empty spot",keep_on_top=True)
                    pm(window, "Must pick an empty spot")
                    break
                elif g[0].tileType != "default":
                    sg.popup("Must be a valid tile",keep_on_top=True)
                    pm(window, "Must be a valid tile")
                    break
                else:
                    g[1] = Piece(playerTurn = playerTurn)
                    g[0].occupied = True
                    g[0].tileType = f"player{playerTurn}default"
                    g[1].avatar = "default"
                    
                    sg.popup("Congrats on your newborn piece.",keep_on_top=True)
                    gameBoard[x][y][1].storedItems.remove("reproduce")
                    return
            else:
                sg.popup("Invalid location",keep_on_top=True)
                break
# recall            
        elif str.find(i, "recall") >= 0:
            
            turnCountRecall = 10
            g = gameBoard[x][y]
            if g[0].recallBackup != False:
                sg.popup("This tile is awaiting the arrival of another recall piece.  It cannot be used until the recall is complete.",keep_on_top=True)
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
            
            
# laser row            
        elif str.find(i, "laser row") >= 0:
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
                    gameBoard[x][y][1].storedItems.remove("laser row")
                    pm(window,"horizontal laser tripod placed")
                    g[0].tileType = "horiLaserTripod"
                    g[0].horiLaser = False
                    g[0].vertLaser = False
                    g[0].crossLaser = False
                    laserCheck(window,gameBoard)
            else:
                sg.popup("Pick something in range (default range is one up/down/left/right)!", keep_on_top=True)
# worm hole
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
                        sg.popup("An error occurred trying to place the worm hole",keep_on_top=True)
                        break
                    displayBoard(window, gameBoard)
                    gameBoard[x][y][1].storedItems.remove("worm hole")
                    window.refresh()
                    break
                else:
                    pm(window, "You must pick an empty adjacent location (up/down/left/right)")
                    sleep(1)
            except:
                sg.popup("An error occurred trying to place the worm hole",keep_on_top=True)
                break
                    
                    
                    
# orb eater            
        elif str.find(i, "orb eater") >= 0:
            itemsMenu.close()
            emptyList = emptySpots(gameBoard)
            pm(window, "Where do you want to deliver the orb eater to?")
            event = window.read()
            try:
                if event[0] in emptyList and gameBoard[event[0][0]][event[0][1]][0].orbEater == False:
                    gameBoard[x][y][1].storedItems.remove("orb eater")
                    gameBoard[event[0][0]][event[0][1]][0].orbEater = True
                    fileNum = random.randint(1,4)
                    playsound(f"sounds/squeak{fileNum}.mp3", block = False)
                elif gameBoard[event[0][0]][event[0][1]][0].orbEater == True:
                    sg.popup("There's already an orb eater here... get your mind out of the gutter, that's not going to happen.",keep_on_top=True)
                    pm(window, "There's already an orb eater here... get your mind out of the gutter, that's not going to happen.")
                else:
                    sg.popup("You need to select an emty space.  The orb eater will find nearby orbs to eat on his own.",keep_on_top=True)
                    continue
            except:
                sg.popup(f"Error. {event[0]} {emptyList}",keep_on_top=True)
                continue
# warp            
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
                sg.popup("Nowhere to teleport to",keep_on_top=True)
                break
            
# round earth theory        
        elif str.find(i, "round earth theory") >= 0:
            itemsMenu.close()
            pm(window,"This piece can now 'wrap' around the edges of the map to appear on the opposite side.")
            gameBoard[x][y][1].storedItems.remove("round earth theory")
            gameBoard[x][y][1].activeBuffs.append("round earth theory")
            
            
# laser column            
        elif str.find(i, "laser column") >= 0:
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
                    gameBoard[x][y][1].storedItems.remove("laser column")
                    pm(window,"vertical laser tripod placed")
                    g[0].tileType = "vertLaserTripod"
                    g[0].horiLaser = False
                    g[0].vertLaser = False
                    g[0].crossLaser = False
                    laserCheck(window,gameBoard)
            else:
                sg.popup("Pick something in range (default range is one up/down/left/right)!", keep_on_top=True)    

# spooky hand       
        elif str.find(i, "spooky hand") >= 0:
            itemsMenu.close()
            gameBoard[x][y][1].storedItems.remove("spooky hand")
            sg.popup("A spooky hand has gone under the field.  When will he strike?  Nobody knows...", keep_on_top = True)
            pm(window,"A spooky hand has gone under the field.  When will he strike?  Nobody knows...")
            sleep(1)
            PublicStats.spookyHand = True

# bowling ball
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
# shuffle item orbs             
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
            
# magnet            
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
                    playsound("sounds/getItem.wav",block=False)
                    pickUpItemOrb(gameBoard, x, y, window = window)
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
                            pm(window, "An item was picked up by your piece.")
                            playsound("sounds/getItem.wav",block=False)
                            pickUpItemOrb(gameBoard, ix, iy, window = window)

                        elif (
                            g[ix][iy][1].ownedBy == enemyTurn
                            and "stunned" not in g[ix][iy][1].activeDebuffs
                        ):
                            pm(window, "Your opponent picked up an item")
                            pickUpItemOrb(gameBoard, ix, iy, window = window)

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
                    if "Energy Forcefield" in j[1].activeBuffs:
                        sg.popup("Your shield activated and protected you from damage.", keep_on_top = True)
                        j[1].activeBuffs.remove("Energy Forcefield")
                        continue
                    if j[1].forcefieldTurn == PublicStats.turnCount:
                        sg.popup("Your shield continues to protect you.",keep_on_top = True)
                        continue

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
                    if "Energy Forcefield" in j[1].activeBuffs:
                        sg.popup("Your shield activated and protected you from damage.", keep_on_top = True)
                        j[1].activeBuffs.remove("Energy Forcefield")
                        continue
                    
                    if j[1].forcefieldTurn == PublicStats.turnCount:
                        sg.popup("Your shield continues to protect you.",keep_on_top = True)
                        continue

                    else:
                        # set the tile to be empty
                        gameBoard[x][y][0].occupied = False
                        gameBoard[x][y][1] = 0
                        gameBoard[x][y][0].tileType = "default"

# napalm row
        elif str.find(i, "napalm row") >= 0:

            itemsMenu.close()
            highlightValidDistance(gameBoard, window, startLocation, actionType = "enemiesHurtOnly", reachType = "row")
            displayBoard(window, gameBoard)
            window.refresh()
            yesno = sg.popup_yes_no("Use?",keep_on_top=True)
            if yesno == "No":
                continue
            
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


# shuffle row
        elif str.find(i, "shuffle row") >= 0:
            itemsMenu.close()
            g = gameBoard
            if g[x][y][1].grey == True:
                g[x][y][1].currentTurnPiece = True
                g[x][y][1].grey = False
            cg = []
            locations = []
            g[x][y][1].storedItems.remove("shuffle row")
            laserCheck(window, gameBoard, resetOnly = True)
            
            #for pieces in the row
            for iIndex,i in enumerate(g[x]):
                # copy the row's tiles to cg    
                cg.append(copy.deepcopy(i))
                locations.append((x, iIndex))
                g[x][iIndex][0].tileType = "default"
                g[x][iIndex][0].occupied = False
                displayBoard(window, g)
                window.refresh()
                sleep(0.1)


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

# berzerk
        elif str.find(i, "berzerk") >= 0:
            itemsMenu.close
            yesno = sg.popup_yes_no("Using this item will make this piece go berzerk and allow it to eat enemies and allies alike, enraging it and allowing it to attack again after each kill (up to three times per turn), but at the cost of dying if it goes any turns without eating (it stores leftovers from each enemy killed so it can eat on subsequent turns without attacking). Use?",keep_on_top=True)
            if yesno == "No":
                continue
            g = gameBoard
            g[x][y][1].storedItems.remove("berzerk")
            g[x][y][1].activeBuffs.append("feral")
            g[x][y][1].feralMeatCount = 0
            g[x][y][1].feralAttacksLeft = 3
            
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
            
# sticky time bomb
        elif str.find(i, "sticky time bomb") >= 0:
            itemsMenu.close()
            validLocations = getCross(location, gameBoard, includeSelf = True)
            turnsToArm = 5
            pm(window, "What piece would you like to attach the bomb to?")
            event = window.read()
            if (event[0][0], event[0][1]) in validLocations:

                if gameBoard[event[0][0]][event[0][1]][0].occupied == True and "resistant" not in gameBoard[event[0][0]][event[0][1]][1].activeBuffs and "sticky time bomb" not in gameBoard[event[0][0]][event[0][1]][1].activeDebuffs:
                    gameBoard[event[0][0]][event[0][1]][1].activeDebuffs.append("sticky time bomb")
                    gameBoard[x][y][1].storedItems.remove("sticky time bomb")
                    gameBoard[event[0][0]][event[0][1]][1].stickyTimeBomb = PublicStats.turnCount + turnsToArm
                    sg.popup("Attached the sticky time bomb.  It'll explode in 5 turns, destroying the piece and all surrounding tiles.",keep_on_top=True)
                    
                    displayBoard(window, gameBoard)
                    window.refresh()
                    continue
                elif gameBoard[event[0][0]][event[0][1]][0].occupied == False:
                    sg.popup("There's no one there to attach the bomb to.", keep_on_top = True)
                    continue
                elif "sticky time bomb" in gameBoard[event[0][0]][event[0][1]][0].activeDebuffs:
                    sg.popup("This piece already has a sticky time bomb attached to it, you can't put a second one on it",keep_on_top=True)
                    continue
                else:
                    sg.popup("That piece is unaffected due to an item effect",keep_on_top=True)
                    continue
            else:
                pm(window, "Can't place mine there.  Must attach it to a nearby piece (including yourself).")
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
                                g[1].activeDebuffs.append("vile")
                                displayBoard(window, gameBoard)
                                window.refresh()
                                g[1].activeDebuffs.remove("vile")
                                
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
        elif str.find(i, "wololo radial") >= 0:

            
            itemsMenu.close()
            highlightValidDistance(gameBoard, window, startLocation, actionType = "enemiesHurtOnly", reachType = "radial")
            displayBoard(window, gameBoard)
            window.refresh()
            yesno = sg.popup_yes_no("Use?",keep_on_top=True)
            if yesno == "No":
                continue
            validList = []
            validList = getRadial(location, gameBoard)
            player = gameBoard[x][y][1].ownedBy
            converted = 0
            if player == 1:
                enemy = 2
            elif player == 2:
                enemy = 1
            for i in validList:
                ix = i[0]
                iy = i[1]
                if gameBoard[ix][iy][0].occupied == True:
                    if gameBoard[ix][iy][1].ownedBy == enemy:
                        gameBoard[ix][iy][1].ownedBy = player
                        converted+=1
            gameBoard[x][y][1].storedItems.remove("wololo radial")

            if converted > 0:
                sg.popup(f"WOLOLO!  You've converted {converted} pieces to your side!", keep_on_top = True)
                pm(window, f"WOLOLO!  You've converted {converted} pieces to your side!")
                
            
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
                        sleep(.5)
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
        elif str.find(i, "snake tunneling") >= 0:
            gameBoard[x][y][1].storedItems.remove("snake tunneling")
            itemsMenu.close()
            i = 10
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

                gameBoard[s1][s2][0].snake = True
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
                        sleep(.5)
                        gameBoard[s1][s2][0].tileType = "default"
                        displayBoard(window, gameBoard)
                        window.refresh()
                        sleep(.5)

                        gameBoard[s1][s2][0].tileHeight = 2
                    else:
                        gameBoard[s1][s2][0] = copy.deepcopy(tileVictim)
                        gameBoard[s1][s2][0].tileHeight = 2
                else:
                    gameBoard[s1][s2][0] = copy.deepcopy(tileVictim)
                    gameBoard[s1][s2][0].tileHeight = 2
                gameBoard[s1][s2][0].snake = False
                displayBoard(window, gameBoard)
                window.refresh()
                sleep(.5)

            updateToolTips(window, gameBoard, playerTurn)
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


def forcefieldCheck(window, gameBoard, startLocation = 0, endLocation = 0):
    g = gameBoard[endLocation[0]][endLocation[1]]
    gs = gameBoard[startLocation[0]][startLocation[1]]
    if g[0].horiLaser or g[0].vertLaser or g[0].crossLaser or g[0].tileType == "mine":
    #if g[0].horiLaser or g[0].vertLaser or g[0].crossLaser or g[0].tileType == "mine" or (g[0].occupied == True and g[1].ownedBy != playerTurn and "dead man's trigger" in g[0].activeBuffsList):
        
        if "Energy Forcefield" in g[1].activeBuffs:
            g[1].shieldTurn = PublicStats.turnCount
            g[1].activeBuffs.remove("Energy Forcefield")
            sg.popup("The forcefield activated and will protect you from energy until the end of this turn",keep_on_top=True)
            return True
        elif g[1].shieldTurn == PublicStats.turnCount:
            sg.popup("A forcefield is still active until the end of this turn.  It has saved you again.",keep_on_top=True)
            return True
        else:
            #DEATH
            return False

    else:
        return False
    
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
    for i in gameBoard:
        columnIndex = 0
        for j in i:
            
            if j[0].occupied == True:
                
                if j[0].currentTurnPiece == True:
                    return (rowIndex,columnIndex)
            columnIndex +=1
            
        rowIndex +=1

def itemExplanation(i):


        
        if i == "bowling ball":
            explanation = "Your piece loses all of its powers and negative effects... but becomes a crazy bowling ball on a rampage."
        elif i == "berzerk":
            explanation = "MUST RIP AND TEAR!  BERZERK MAKE PIECE GO ANGRY.  PIECE GO HUNGRY.  PIECE EAT ENEMY AND FOE ALIKE! IF PIECE EAT A PIECE, PIECE MOVE AGAIN!  \nIF PIECE EAT AGAIN ON THIS BONUS MOVE, THEN PIECE GO AGAIN ONE MORE TIME!  THAT THREE TIME MAX!  PIECE MUST EAT MEAT FROM DEAD ENEMY EVERY TURN!  \nPIECE STORE MEAT FROM EACH KILL!  IF PIECE HAVE NO MEAT STORED TO EAT, PIECE DIE!  PIECE NO LIKE DIE UNLESS HE MAKE OTHERS DIE!"
        elif i in ("canyon row","canyon column","canyon radial"):
            explanation = "Dig a canyon that lowers all the pieces in the affected area.  The tiles are only lowered; the pieces on the tiles are not affected in any way."
        elif i == "care package drop":
            explanation = "A plane drops off some item orbs near the selected opponent"
        elif i == "charity":
            explanation = "Gift your opponent a brand new piece.  How charitable!"
        elif i == "dead man's trigger":
            explanation = "Strap a bomb to yourself and activate the trigger.  If you die, you release the trigger, and the enemy that jumped on you dies as well."
        elif i == "dump items":
            explanation = "After activating this item, your other unused items clump together into a giant item orb and then get dumped on any empty tile on the field.  \nAny piece that is capable of picking up items - including your enemy's pieces - can then grab this wad of powers."
        elif i == "elevate tile":
            explanation = "Spontaneously cause the tile that you're standing on to rise up to a chosen height.  Let the other pieces know you are above them, in more ways than one."
        elif i == "Energy Forcefield":
            explanation = "A forcefield that will protect you from an explosion or energy attack; the shield remains active for one turn, shielding you from further explosions."
        elif i == "floor restore":
            explanation = "Repair all damaged/missing floor tiles and replace them with pristine ones."
        elif i == "haphazard airstrike":
            explanation = "Call in an airstrike from an underfunded army.  The plane doesn't have targeting systems installed, so it will carpet bomb the field at random."
        elif i == "haymaker":
            explanation = "Unleash a strong punch that sends a piece flying."
        elif i == "heir":
            explanation = "Looks like you're going to have a good heir day!  There is luck in the heir today!  Because this item lets you grab every single item that your allies carry onto this specific piece.  Become an army of one!"
        elif i == "jump proof":
            explanation = "Your piece dons a dapper hard hat, naturally making you immune to being jumped on.  It does not provide any other forms of protection."
        elif i == "jumpoline":
            explanation = "Spawns a jumpoline, which is what they used to call those devices consisting of a piece of taut, strong fabric stretched between a steel frame using many \ncoiled springs, at least until your mom jumped on one.  If a piece belonging to either player jumps onto a jumpoline, they'll be tossed to another random empty square."
        elif i in ("laser column","laser row"):
            explanation = "Place a laser turret that will shoot out an infinite range beam that'll destroy any pieces it hits (including your own).  Laser turrets are immune to other \nlaser turrets, but are affected by pieces and other items."
        elif i == "magnet":
            explanation = "Uses Science (tm) to create a powerful magnet that pulls in nearby lightweight objects, then proceeds to pull in slightly farther items if there is room to pull them in."
        elif i == "move again":
            explanation = "Activate this to gain the move again shoes, which allow this piece to permanently move twice in one turn. This effect stacks if it uses multiple move agains."
        elif i == "move diagonal":
            explanation = "Activate this piece to gain a cool diagonal arrows logo, which allow this piece to permanently move diagonal (while still having access to normal movement)"
        elif i == "secretAgent":
            explanation = "Activate this to reveal a secret agent in a neighboring square.  This creepy guy will steal items from your opponents if they visit his square, and will give those items to you if you visit him."
        elif i in ("mutual treason column", "mutual treason row", "mutual treason radial"):
            explanation = "You and your opponent both utilize some excellent propoganda... any affected pieces permanently switch their allegiances."
        elif i == "mystery box":
            explanation = "Summon a mysterious box.  A random effect will occur for any piece that steps in, from gaining items, getting buffs, being cleansed, losing buffs, getting a\n random negative effect, or even spontaneously exploding!"
        elif i in ("napalm radial", "napalm column", "napalm row"):
            explanation = "Fire off a stream of fire and sticky substances at your opponents.  Any opponent hit by it will burn to a crisp and leave a hole in the ground.  Allies are unaffected thanks to your sweet aiming skills."
        elif i == "orb eater":
            explanation = "Summon a hungry orb eater (totally not a mouse) on any empty spot in the field.  It will move around in between turns and eat up any item orbs it finds. Legend has \nit that you shouldn't let an orb eater eat too many..."
        elif i == "place mine":
            explanation = "Place a mine down on an adjacent square.  Any player stepping on it goes boom."
        elif i in ("purify radial", "purify column", "purify row"):
            explanation = "Clear out all negative effects from all of your allies within range.  Who needs a medical degree when you have this?!"
        elif i == "purity tile":
            explanation = "Step into this tile to remove all negative effects from your piece.  Rinse, lather, repeat. (I mean, you can if you want, but you'd just be wasting your time if you're already purified, y'know?)"
        elif i == "recall":
            explanation = "at the earlier time no matter what.  Activate this and your tile will be marked with a recall logo, which in 10 turns will whisk you back to the exact snapshot you were at the earlier time no matter what.\n Activate this and your tile will be marked with a recall logo, which in 10 turns will whisk you back to the exact snapshot you were"
        elif i == "reproduce":
            explanation = "Use this to create a baby piece within range.  It will be a brand new simple piece.  How do non-sentient pieces have babies?  Life... uh... finds a way."
        elif i == "seismic activity":
            explanation = "Induce an earthquake.  A random magnitude earthquake will occur: the higher the magnitude, the more drastically the field will be altered.  Random elevations and depressions will occur throughout the field.  Surprisingly, no pieces will be harmed."
        elif i == "round earth theory":
            explanation = "The scientists called us insane, but thanks to the power of pseudoscience, you prove the earth is totally round, so if you can totally wrap around the playing field.  \nThat is, if you wanted to, you can move from the right edge of the map straight to the left edge.  Or from the top straight to the bottom.  Pac man style."
        elif i in ("shuffle column", "shuffle radial", "shuffle row"):
            explanation = "All tiles in the affected area get shuffled around randomly."
        elif i == "shuffle item orbs":
            explanation = "All item orbs (and trap orbs) get removed from the field and then are randomly redistributed on empty spots of the field."
        elif i == "sink tile":
            explanation = "Use sheer will to lower the tile to a chosen elevation."
        elif i == "smart bombs":
            explanation = "A well funded military sends in a precision bomber to shoot bombs on the field and will make sure to avoid hitting your pieces."
        elif i == "snake tunneling":
            explanation = "A robotic snake starts digging around from the summoning point.  It burrows around and pushes the ground up (to an elevation of 2), killing enemies but sparing your pieces."
        elif i == "spooky hand":
            explanation = "A scary hand that will periodically grab a random piece from the field, permanently removing it from play.  \nAfter claiming a victim, it takes its time doing whatever it is that spooky hands do, before looking for a new victim."
        elif i in ("steal items column","steal items radial","steal items row"):
            explanation = "Steal all unactivated items from all enemies in range.  POSSESSION IS 9/10 OF THE LAW, YO!"
        elif i in ("steal powers column","steal powers radial","steal powers row"):
            explanation = "Steal (almost) all active buffs from all enemies in range.  Finders keepers! (exceptions exist for some buffs, such as bowling ball)"
        elif i == "sticky time bomb":
            explanation = "Attach a bomb to any in-range piece (including your own).  After five turns, it explodes, killing all surrounding pieces."
        elif i in ("study column", "study row", "study radial"):
            explanation = "Copy any activated buffs from your in-range allies (aside for special cases such as recall and bowling ball)"
        elif i in ("suicide bomb column", "suicide bomb row", "suicide bomb radial"):
            explanation = "Kills every piece within range - yours and your enemy's.  Terrorism is not cool, but I guess it's ok if non-sentient pieces do it to each other."
        elif i in ("teach column", "teach radial", "teach row"):
            explanation = "Become a master tutor and teach your in-range allies whatever buffs you have."
        elif i == "trap orb":
            explanation = "Put a bomb disguised as an item orb that will explode on your enemy if they touch it.  The trap orb looks exactly like a normal item orb, \nso there's no way to tell it apart.  However, your pieces will be aware that it's a trap and will be unaffected by them (stepping on them leaves the trap as-is so that your opponent still has a shot at getting tricked by it"
        elif i in ("trip mine radial", "trip mine row", "trip mine column"):
            explanation = "Set up a bomb on all in-range enemies that can detect when the piece moves.  Upon moving, the piece will trigger the bomb, causing it to explode upon finishing its action.  \nA piece that has a trip mine set up on it can still use most items (including teleporting items) safely without setting the bomb off. However, items that are linked to moving will still set it off."
        elif i == ("trump"):
            explanation = "We're gonna build a great wall, a wall greater than what the enemy team ever built, and we're gonna make them pay for it!  The wall will be built by taking all of the affected tiles and raising them to max height.  The wall can either be built as a row or a column."
        elif i in ("vile radial", "vile column", "vile row"):
            explanation = "Apply the 'vile' debuff to all enemies within range. This nasty effect stops affected pieces from being able to apply buffs to themselves.  \nThey can still pick up any items normally, and use items that don't apply positive effects to themselves."
        elif i == "warp" :
            explanation = "Your piece is randomly whisked away to an empty spot in the field. Where you end up is completely random, so don't bother whining about \n'boo hoo how come I always end up in the worst position possible everytime I use this item', because that's your fault for being unlucky."
        elif i in ("wololo radial", "wololo column", "wololo row"):
            explanation = "Your piece uses the ancient incantatation of the ancient Ayoh Eetoo religion, which convinces all in-range pieces that hear the word of truth to join your \nside.  It somehow changes their color to match your team's color, too.  Weird how that works."
        elif i == "worm hole":
            explanation = "Set up a worm hole at an adjacent tile.  As long as your pieces are not on the warp tile, you can use your move to teleport to that worm hole from anywhere."
        elif i == "vampiricism":
            explanation = "Pounce and feed on a piece's essence, gaining its power.  Sorry, the piece doesn't come back from the dead as your lover, nor do you get to sparkle in the sun.  Well, you do, because you're made of metal, but whatever."
        elif i == "bernie sanders":
            explanation = "Taxes all pieces on the field and gathers up all of your unactivated items and all of your opponent's unactivated items.  Shuffles the items around and randomly redistributes the wealth \namong all pieces that are capable of receiving items.  DO YOU FEEL THE BURN?  If so... that might be a napalm row...  uh oh."
        else:
            #z = "images/default.png"
            explanation = "no explanation supplied... yet"

        return explanation
     
##    if itemName == "orb eater":
##        if introOnly:
##            return "A mouse spawns.  After each player's turn, the mouse will eat a close by item orb or trap orb that he finds.  If he doesn't find one, he will walk in a random direction."
##        sg.popup("A mouse spawns.  After each player's turn, the mouse will eat a close by item orb or trap orb that he finds.  If he doesn't find one, he will walk in a random direction.", keep_on_top = True)
##    elif itemName == "laser row":
##        if introOnly:
##            return "Set up a laser emitter.  The laser will shoot all the way left and right, destroying any pieces it finds.  It does not affect item orbs or other non-player entities. It will not affect any other laser emitters."
##        sg.popup("Set up a laser emitter.  The laser will shoot all the way left and right, destroying any pieces it finds.  It does not affect item orbs or other non-player entities. It will not affect any other laser emitters.", keep_on_top = True)
##    elif itemName == "magnet":
##        if introOnly:
##            return"Suck in any adjacent item orbs or bombs.  Afterwards, it'll suck in anything in the 4x4 square that is surrounding the adjacent 3x3 into the 3x3 if there is space."
##        sg.popup("Suck in any adjacent item orbs or bombs.  Afterwards, it'll suck in anything in the 4x4 square that is surrounding the adjacent 3x3 into the 3x3 if there is space.", keep_on_top = True)
##    elif itemName == "trap orb":
##        if introOnly:
##            return "An explosive trap designed to look like an item orb.  They are indistinguishable.  Luckily, your traps will not affect you."
##        sg.popup("An explosive trap designed to look like an item orb.  They are indistinguishable.  Luckily, your traps will not affect you.", keep_on_top = True)
##    elif itemName == "place mine":
##        if introOnly:
##            return "Place a mine next to you.  If either player steps on it, BOOM."
##        sg.popup("Place a mine next to you.  If either player steps on it, BOOM.", keep_on_top = True)
##    elif itemName ==  "move again":
##        if introOnly:
##            return "After you activate this permanent buff, your piece will get to move again after moving."
##        sg.popup("After you activate this permanent buff, your piece will get to move again after moving.", keep_on_top = True)
##    elif itemName ==  "suicide bomb row":
##        if introOnly:
##            return "Blow yourself up, killing everyone in the same row as you - including your allies."
##        sg.popup("Blow yourself up, killing everyone in the same row as you - including your allies.", keep_on_top = True)
##    elif itemName == "Energy Forcefield":
##        if introOnly:
##            return "After activating it, you'll be surrounded by a forcefield. Protects you one time from most energy/explosive type attacks. It has no effect against modifiers, or against blunt attacks such as being jumped on or crushed, and will not protect you if the floor disappears."
##        sg.popup("After activating it, you'll be surrounded by a forcefield. Protects you one time from most energy/explosive type attacks. It has no effect against modifiers, or against blunt attacks such as being jumped on or crushed, and will not protect you if the floor disappears.", keep_on_top = True)
##    elif itemName == "suicide bomb column":
##        if introOnly:
##            return "Blow yourself up, killing everyone in the column."
##        sg.popup("Blow yourself up, killing everyone in the column.", keep_on_top = True)
##    elif itemName == "haphazard airstrike":
##        if introOnly:
##            return "Call in an airstrike from a poorly funded army.  The plane cannot aim and will blow holes into the ground randomly, killing anything that was on the tile, including the floor itself"
##        sg.popup("Call in an airstrike from a poorly funded army.  The plane cannot aim and will blow holes into the ground randomly, killing anything that was on the tile, including the floor itself", keep_on_top = True)
##    elif itemName == "suicide bomb radial":
##        if introOnly:
##            return "Blow yourself up, killing you and anyone or anything next to you."
##        sg.popup("Blow yourself up, killing you and anyone or anything next to you.", keep_on_top = True)
##    elif itemName == "jump proof":
##        if introOnly:
##            return "Enemies cannot jump on you.  You may still be affected by anything else."
##        sg.popup("Enemies cannot jump on you.  You may still be affected by anything else.", keep_on_top = True)
##    elif itemName == "smart bombs":
##        if introOnly:
##            return "Call in an airstrike conducted by a sophisticated bomber. It will not hurt any of your pieces.  Leaves holes in the ground, destroying its targets."
##        sg.popup("Call in an airstrike conducted by a sophisticated bomber. It will not hurt any of your pieces.  Leaves holes in the ground, destroying its targets.", keep_on_top = True)
##    elif itemName == "move diagonal":
##        if introOnly:
##            return "After activating this buff, in addition to your usual spots, your piece can move to diagonal locations."
##        sg.popup("After activating this buff, in addition to your usual spots, your piece can move to diagonal locations.", keep_on_top = True)
##    elif itemName == "trip mine radial":
##        if introOnly:
##            return "Set mines on all surrounding enemies.  If they move, they blow up.  They can still safely use items that don't require them to move.  Teleporting is not considered moving."
##        sg.popup("Set mines on all surrounding enemies.  If they move, they blow up.  They can still safely use items that don't require them to move.  Teleporting is not considered moving.", keep_on_top = True)
##    elif itemName == "purify radial":
##        if introOnly:
##            return "Remove all negative effects from surrounding allies."
##        sg.popup("Remove all negative effects from surrounding allies.", keep_on_top = True)
##    elif itemName == "napalm radial":
##        if introOnly:
##            return"Set all enemies in the surrounding area on fire.  This kills them and burns a hole in the ground."
##        sg.popup("Set all enemies in the surrounding area on fire.  This kills them and burns a hole in the ground.", keep_on_top = True)
##    elif itemName == "vile radial":
##        if introOnly:
##            return "Remove all beneficial powers that your surrounding enemies possess."
##        sg.popup("Remove all beneficial powers that your surrounding enemies possess.", keep_on_top = True)
##    elif itemName == "haymaker":
##        if introOnly:
##            return "Punch an adjacent piece really hard.  The flying piece will keep going until it either slams into a piece/wall and stuns itself and the piece it collided into, or if it dies by moving into a danger location (laser beam/hole/mine/etc).  The piece will not be able to pick up any items as it passes over. "
##        sg.popup("Punch an adjacent piece really hard.  The flying piece will keep going until it either slams into a piece/wall and stuns itself and the piece it collided into, or if it dies by moving into a danger location (laser beam/hole/mine/etc).  The piece will not be able to pick up any items as it passes over. ", keep_on_top = True)
##    elif itemName == "bowling ball":
##        if introOnly:
##            return"Turn your piece into a feral bowling ball.  The bowling ball loses all effects that it has (positive and negative).  It can no longer pick up any items.  It no longer has access to normal movement.  Instead, if you select it, it will only allow you to choose a direction.  The bowling bar will fly toward that direction with sheer rage and be unaffected by most negative effects, including bombs or mines.  It can still die by falling into holes.  It will continue going in a given direction until it slams into a wall or a piece.  If it hits a piece, it stuns allies and kills the enemy."
##        sg.popup("Turn your piece into a feral bowling ball.  The bowling ball loses all effects that it has (positive and negative).  It can no longer pick up any items.  It no longer has access to normal movement.  Instead, if you select it, it will only allow you to choose a direction.  The bowling bar will fly toward that direction with sheer rage and be unaffected by most negative effects, including bombs or mines.  It can still die by falling into holes.  It will continue going in a given direction until it slams into a wall or a piece.  If it hits a piece, it stuns allies and kills the enemy.", keep_on_top = True)
##    elif itemName == "laser column":
##        if introOnly:
##            return "Set up a laser emitter.  The laser will shoot all the way up and down, destroying any pieces it finds.  It does not affect item orbs or other non-player entities and will not affect any other laser emitters."
##        sg.popup("Set up a laser emitter.  The laser will shoot all the way up and down, destroying any pieces it finds.  It does not affect item orbs or other non-player entities and will not affect any other laser emitters.", keep_on_top = True)
##    elif itemName == "shuffle column":
##        if introOnly:
##            return "Shuffle everything in the column randomly.  This does not set off tripmines as the pieces themselves are not actually moving - the tiles are, along with their tripmines."
##        sg.popup("Shuffle everything in the column randomly.  This does not set off tripmines as the pieces themselves are not actually moving - the tiles are, along with their tripmines.", keep_on_top = True)
##    elif itemName == "shuffle radial":
##        if introOnly:
##            return "Shuffle everything in the surrounding randomly.  This does not set off tripmines as the pieces themselves are not actually moving - the tiles are, along with their tripmines."
##        sg.popup("Shuffle everything in the surrounding randomly.  This does not set off tripmines as the pieces themselves are not actually moving - the tiles are, along with their tripmines.", keep_on_top = True)
##    elif itemName == "spooky hand":
##        if introOnly:
##            return "After using this, a creepy hand will lurk under the playing field for the rest of the game.  Once every handful (see what I did there?) of turns, it'll pop up and abduct one piece from either player, taking the floor with it."
##        sg.popup("After using this, a creepy hand will lurk under the playing field for the rest of the game.  Once every handful (see what I did there?) of turns, it'll pop up and abduct one piece from either player, taking the floor with it.", keep_on_top = True)
##    elif itemName == "reproduce":
##        if introOnly:
##            return "Your piece spawns a cute baby.  The baby is a generic piece that has no powerups and is just like any other normal piece."
##        sg.popup("Your piece spawns a cute baby.  The baby is a generic piece that has no powerups and is just like any other normal piece.", keep_on_top = True)
##    elif itemName == "worm hole":
##        if introOnly:
##            return "Choose an empty location.  A worm hole replaces the tile.  As long as no on is on that tile, any of your pieces can teleport to there from anywhere."
##        sg.popup("Choose an empty location.  A worm hole replaces the tile.  As long as no on is on that tile, any of your pieces can teleport to there from anywhere.", keep_on_top = True)
##    elif itemName == "warp":
##        if introOnly:
##            return "Your piece is randomly whisked away to an empty location.  Careful, it can make you end up in enemy territory... or just move you one space away... or anything in between."
##        sg.popup("Your piece is randomly whisked away to an empty location.  Careful, it can make you end up in enemy territory... or just move you one space away... or anything in between.", keep_on_top = True)
##    elif itemName == "recall":
##        if introOnly:
##            return "After a piece uses recall, it creates an unbreakable bond with the tile it cast it on and gets a snapshot of how it is in that exact moment.  In 10 turns, the piece will, no matter what, return to that tile in the state that it was at, even if it died.  If the tile is moved by any items before the recall occurs, the piece will appear in the location the tile was moved to."
##
##        sg.popup("After a piece uses recall, it creates an unbreakable bond with the tile it cast it on and gets a snapshot of how it is in that exact moment.  In 10 turns, the piece will, no matter what, return to that tile in the state that it was at, even if it died.  If the tile is moved by any items before the recall occurs, the piece will appear in the location the tile was moved to.", keep_on_top = True)


def roundEarthTheoryFunction(gameBoard,startLocation,endLocation,columns,rows):
#trying to go from right side to left side
    #try to go straight right to straight left
    if startLocation[0] == endLocation[0]:
        if startLocation[1] == columns-1 and endLocation[1] == 0:
            sg.popup("Your piece rolled around to the other side!",keep_on_top=True)
            return True
    #trying to go down right
    elif startLocation[0] == endLocation[0]-1 and startLocation[1] == columns -1 and endLocation[1] == 0 and "move diagonal" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
        sg.popup("Your piece rolled around to the other side!",keep_on_top=True)
        return True
    #trying to go up right
    elif startLocation[0] == endLocation[0]+1 and startLocation[1] == columns -1 and endLocation[1] == 0 and "move diagonal" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
        sg.popup("Your piece rolled around to the other side!",keep_on_top=True)
        return True
    

#trying to go from left to right side
    #try to go straight left to straight right
    if startLocation[0] == endLocation[0]:
        if startLocation[1] == 0 and endLocation[1] == columns -1:
            sg.popup("Your piece rolled around to the other side!",keep_on_top=True)
            return True
    #trying to go down right
    elif startLocation[0] == endLocation[0]-1 and startLocation[1] == 0  and endLocation[1] == columns -1 and "move diagonal" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
        sg.popup("Your piece rolled around to the other side!", keep_on_top=True)
        return True
    #trying to go up right
    elif startLocation[0] == endLocation[0]+1 and startLocation[1] == 0 and endLocation[1] == columns -1 and "move diagonal" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
        sg.popup("Your piece rolled around to the other side!", keep_on_top=True)
        return True

        
#trying to go from up to down
    #try to go straight up to straight down
    if startLocation[1] == endLocation[1]:
        if startLocation[0] == 0 and endLocation[0] == rows -1:
            sg.popup("Your piece rolled around to the other side!", keep_on_top=True)
            return True
    #trying to go up right
    elif startLocation[0] == 0 and startLocation[1] == (endLocation[1] +1) and endLocation[0] == rows -1 and "move diagonal" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
        sg.popup("Your piece rolled around to the other side!", keep_on_top=True)
        return True
    #trying to go up right
    elif startLocation[1] == endLocation[1]-1 and startLocation[0] == 0 and endLocation[0] == rows -1 and "move diagonal" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
        sg.popup("Your piece rolled around to the other side!", keep_on_top=True)
        return True

#diagonals (only works with diagonal enabled
    if "move diagonal" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
        #upleft
        if startLocation[0] == 0 and startLocation[1] == 0 and endLocation[0] == rows-1 and endLocation[1] == columns-1:
            sg.popup("Your piece rolled around to the other side!", keep_on_top=True)
            return True
        #upright
        if startLocation[0] == 0 and startLocation[1] == columns-1 and endLocation[0] == rows-1 and endLocation[1] == 0:
            sg.popup("Your piece rolled around to the other side!", keep_on_top=True)
            return True
        #downleft
        if startLocation[0] == rows-1 and startLocation[1] == 0 and endLocation[0] == 0 and endLocation[1] == columns-1:
            sg.popup("Your piece rolled around to the other side!", keep_on_top=True)
            return True
        #downright
        if startLocation[0] == rows-1 and startLocation[1] == columns-1 and endLocation[0] == 0 and endLocation[1] == 0:
            sg.popup("Your piece rolled around to the other side!", keep_on_top=True)
            return True
    else:
        return False


def highlightValidDistance(gameBoard, window, startLocation, actionType = "walk", reachType = "cross", turnOff = False):
    x = startLocation[0]
    y = startLocation[1]
    g = gameBoard

    if g[x][y][0].occupied == True:
        playerTurn = g[x][y][1].ownedBy

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
                #print("Testing")
                #print(f" {iIndex,jIndex} j0w1 {j[0].wormHole1}")
                if j[0].wormHole1 == True and playerTurn == 1:
                    
                    #if the location of the warp is empty
                    if j[0].occupied == False:
                        print("highlighted worm hole")
                        #highlight it
                        j[0].highlight = True
                    #if you're there, don't allow movement there, unless feral
                    elif j[1].ownedBy == playerTurn and "feral" not in j[1].activeBuffs:
                        continue
                    else:
                        j[0].highlight = True
                #print("Testing")
                #print(f" j0w2 {j[0].wormHole2}")
                if j[0].wormHole2 == True and playerTurn==2:
                    #if it's empty
                    
                    if j[0].occupied == False:
                        #highlight it
                        
                        j[0].highlight = True
                    #if you're there, don't allow movement there, unless feral
                    elif j[1].ownedBy == playerTurn and "feral" not in j[1].activeBuffs:
                        continue
                    else:
                        j[0].highlight = True
                        
        if "move diagonal" in g[x][y][1].activeBuffs:
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
                    #if nothing's there
                    if g[xi][yi][0].occupied == False:
                        g[xi][yi][0].highlight = True
                    #if someone is there
                    elif g[xi][yi][0].occupied == True:
                        if g[xi][yi][1].ownedBy != g[x][y][1].ownedBy:
                            g[xi][yi][0].highlightRed = True
                        if g[xi][yi][1].ownedBy == g[xi][yi][1].ownedBy:
                            if "feral" in g[x][y][1].activeBuffs:
                                g[xi][yi][0].highlightRed = True
                            else:
                                continue

        #placeholder for around the world
        #elif around the world
        #normal
        else:
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
                    
                    #if nothing's there
                    if g[xi][yi][0].occupied == False:
                        g[xi][yi][0].highlight = True
                    #if someone is there
                    elif g[xi][yi][0].occupied == True:
                        if g[xi][yi][1].ownedBy != g[x][y][1].ownedBy:
                            print("Enemy highlighted")
                            g[xi][yi][0].highlightRed = True
                        if g[xi][yi][1].ownedBy == g[xi][yi][1].ownedBy:
                            if "feral" in g[x][y][1].activeBuffs:
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


        
    if actionType == "enemiesHurtOnly":
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
            g[x][y][0].hightlightGreen = True
            return
            

def movePiece(playerTurn, window, gameBoard):
    #pyautogui.moveTo(10, 10)
    # a small list that is used to make sure a player that gets a second turn for a piece can only use that specific piece twice
    repeatRestrictor = [False, (-1, -1)]
    pieceTeleported = False
    #startLocation = [0,0]
    startLocation = []
    roundEarthTheory = False
    rows = len(gameBoard)
    columns = len(gameBoard[0])
    #displayBoard(window, gameBoard)
##    #currentMouseX, currentMouseY = pyautogui.position()  
##    sleep(4)
##    #pyautogui.moveTo(currentMouseX, currentMouseY)
##    window.refresh()
##    updateToolTips(window, gameBoard,playerTurn)
##    updateToolTips(window, gameBoard, playerTurn)
##    window.refresh()

    while True:
        
        
        updateToolTips(window, gameBoard,playerTurn)
        highlightValidDistance(gameBoard, window, (0,0),turnOff = True)
        #flag for keeping track of pieces that were teleported
        if pieceTeleported == True:
            startLocation[0],startLocation[1] = findCurrentTurnPiece(window, gameBoard)
            gameBoard[startLocation[0]][startLocation[1]][1].currentTurnPiece = True
        displayBoard(window, gameBoard)
        #Picked up item is used to show a message if a piece is picked up automatically at the end of the turn
        pickedUpItem = False
        window["exit"].update(disabled=False)
        usedItem = False
        #window["itemButton"].update(disabled=True)
        window["examineItem"].update(disabled=False)
        ###window["readItems"].update(disabled=False)
        window["cheetz"].update(disabled=False)
        
        window.refresh()
        
        window["playerTurn"].update(f"{playerTurn}")
        window["information"].update(text_color="white")

        # message for pick your piece to move
        pm(window, f"Pick a piece to move.")



        ##########################################
        #   IF FIRST TURN                        #
        ##########################################

        
        # check to see if this is your second+ turn (you don't get to choose a new piece).  False means this isn't your second move (so if False, it's your first turn)
        if repeatRestrictor[0] == False:

            ###########################
            #FIRST PIECE PICKED HERE  #
            ###########################
            
            # This is your initial selection option for choosing a piece
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
                highlightValidDistance(gameBoard, window, (0,0),turnOff = True)
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
                ###window["readItems"].update(disabled=False)
                continue

##            #if the player wants to read about items
##            if "readItems" in event:
##                    highlightValidDistance(gameBoard, window, (0,0),turnOff = True)
##                #readItems()
##                    learnItemsLayout = []
##                    itemList = [
##                    "<QUIT>",
##                    "orb eater",
##                    "magnet",
##                    "trap orb",
##                    "place mine",
##                    "move again",
##                    "suicide bomb row",
##                    "Energy Forcefield",
##                    "suicide bomb column",
##                    "haphazard airstrike",
##                    "suicide bomb radial",
##                    "jump proof",
##                    "smart bombs",
##                    "move diagonal",
##                    "trip mine radial",
##                    "purify radial",
##                    "napalm radial",
##                    "vile radial",
##                    "haymaker",
##                    "bowling ball",
##                    "laser column",
##                    "laser row",
##                    "shuffle column",
##                    "shuffle radial",
##                    "spooky hand",
##                    "reproduce",
##                    "worm hole",
##                    "warp"
##                    ]
##                    itemList.sort()
##                    disableEverything(window)
##                    for i in itemList:
##                        learnItemsLayout+= [ [sg.Button(f"{i}",key = i)] ]
##                    learnItems = sg.Window("Title",learnItemsLayout,keep_on_top = True).finalize()
##                    #window.disable()
##                    learnItems.bind('<FocusOut>', '+FOCUS OUT+')
##                    
##                    event = learnItems.read()
##                    
##                    
##                    
##                    while event[0]!="<QUIT>" and event[0]!=None and event[0]!= '+FOCUS OUT+':
##                    
##                        itemExplanation(event[0])
##                        event = learnItems.read()
##                        if event[0] == None:
##                            break
##                    #disableEverything(window, turnOn = True)
##                    learnItems.close()
##                    
##                    disableEverything(window, turnOn = True)
##                    #window.enable()
##                    continue
                
        #disable the exit button to avoid issues
        window["exit"].update(disabled=True)
        window["cheetz"].update(disabled=True)
        ###window["readItems"].update(disabled=True)
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
            sg.popup("An exception error has occurred during piece selection.  Attempting to recover.  Please try again.",keep_on_top = True)
            continue

            
       
        
        #IS THE PIECE A BOWLING BALL?  
        if gameBoard[event[0][0]][event[0][1]][0].occupied == True and "bowling ball" in gameBoard[event[0][0]][event[0][1]][1].activeBuffs:
            highlightValidDistance(gameBoard, window, startLocation,turnOff = True)
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

        #force the piece to be last moved piece
        elif repeatRestrictor[0] == True:
            event = []
            #repeat restrictor keeps track of where the player was last and forces the event to equal that location
            event.append(repeatRestrictor[1])
            

            #if an error occurs, try from the beginning
            if event[0] == (-1,- 1):
                sg.popup("An error has occurred while determining last known location of a move again piece.  Please try again.", keep_on_top=True)
                repeatRestrictor = False
                continue
            
        #allow player to read about items, but not view tiles; helps avoid glitches
        #window["itemButton"].update(disabled=False)
        #window["itemButton"].update(disabled=True)
        window["examineItem"].update(disabled=True)


        #sL = startLocation; this is where the player started; keep track of this for calculations
        
        startLocation = event[0]
        startLocationBackup = startLocation

        if gameBoard[startLocation[0]][startLocation[1]][0].occupied == True:
            highlightValidDistance(gameBoard, window, startLocation)

        #if the person is trying to move a piece that isn't the same piece they just moved
        if (repeatRestrictor[0] == True) and (event[0] != repeatRestrictor[1]):
            getChoice = sg.popup_yes_no(
                "You can only move the same piece twice.  Move again? Click yes to force that piece to be selected.  Otherwise choose no to end your turn.",
                keep_on_top=True,
            )
            if getChoice == "Yes":
                startLocation = repeatRestrictor[1]
                highlightValidDistance(gameBoard, window, startLocation)
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



##########################################################
# NO PIECES EXISTS ON THE STARTING TILE THAT WAS CLICKED #                          
##########################################################

        # if there's no piece on that square
        if gameBoard[event[0][0]][event[0][1]][0].occupied == False:
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

        # Totherwise, if a tile is picked and a piece exists on it
        elif gameBoard[event[0][0]][event[0][1]][0].occupied == True:

            # if that piece is stunned and it's your piece
            if (
                playerTurn == gameBoard[event[0][0]][event[0][1]][1].ownedBy
                and "stunned" in gameBoard[event[0][0]][event[0][1]][1].activeDebuffs
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
                playerTurn == gameBoard[event[0][0]][event[0][1]][1].ownedBy
                and len(gameBoard[event[0][0]][event[0][1]][1].storedItems) > 0
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
            elif playerTurn != gameBoard[event[0][0]][event[0][1]][1].ownedBy:
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
        if gameBoard[startLocation[0]][startLocation[1]][1] != 0:
            gameBoard[startLocation[0]][startLocation[1]][1].grey = True
            gameBoard[startLocation[0]][startLocation[1]][1].currentTurnPiece = True


            highlightValidDistance(gameBoard, window, startLocation)
            
        # update the board (to show highlighting)
        displayBoard(window, gameBoard)
        window.refresh()


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
                sleep(.4)
                continue

            # if the piece has no items
            elif len(gameBoard[startLocation[0]][startLocation[1]][1].storedItems) < 1:
                gameBoard[startLocation[0]][startLocation[1]][1].grey = False
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
            gameBoard[startLocation[0]][startLocation[1]][1].currentTurnPiece = False
            playsound("sounds/wrong.wav",block=False) 
            pm(window, f"Nothing exists on the initial square!")
            window.refresh
            continue

        # if the piece no longer exists on the original point, ungrey it
        if gameBoard[startLocation[0]][startLocation[1]][1] != 0:
            gameBoard[startLocation[0]][startLocation[1]][1].grey = False
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
                if gameBoard[endLocation[0]][endLocation[1]][0].occupied == False and gameBoard[endLocation[0]][endLocation[1]][0].wormHole1 == True and playerTurn == 1:
                    wormHole = True
                elif gameBoard[endLocation[0]][endLocation[1]][0].occupied == False and gameBoard[endLocation[0]][endLocation[1]][0].wormHole2 == True and playerTurn == 2:
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
                        window.refresh
                        continue
                
                ##################################################
                # if it's close enough:  (DESTINATION/LEGAL MOVE)#
                ##################################################



                
                if (gameBoard[startLocation[0]][startLocation[1]][0].tileHeight+1 < gameBoard[endLocation[0]][endLocation[1]][0].tileHeight) and ("climb tile" not in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs):
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
                    window["information"].update(f"Can't move here!")
                    pm(window, "Can't move here!")
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
                    
                    # set the original location as being empty; delete the class; set a default tile
                    gameBoard[startLocation[0]][startLocation[1]][0].occupied = False
                    gameBoard[startLocation[0]][startLocation[1]][1] = 0


                    
                    
                    #secretAgent check
                    usedShield = forcefieldCheck(window, gameBoard, startLocation, endLocation)
                    if usedShield == True:
                        sg.popup("A shield was used",keep_on_top = True)
                    secretAgentCheck(window, gameBoard, startLocation, endLocation, playerTurn)




                    #purity tile check
                    if gameBoard[endLocation[0]][endLocation[1]][0].purityTile == True:
                        for iIndex,i in enumerate(gameBoard):
                            for jIndex,j in enumerate(i):
                                if j[0].occupied == True:
                                    if j[1].stickyTimeBomb != False:
                                        j[1].stickyTimeBomb = False
                        sg.popup("Any negative effects on this piece have been cleared.",keep_on_top = True)
                        gameBoard[endLocation[0]][endLocation[1]][1].activeDebuffs.clear()
                        
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
                        sg.popup("You monster!  You killed an orb eater!")
                        gameBoard[endLocation[0]][endLocation[1]][0].orbEater = False

                     

                    playsound("sounds/thump.mp3",block=False)    
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
                        window.disable()
                        moveAgainCheck = sg.popup_yes_no(
                            "This piece gets to go again. Would you like to use it again?", keep_on_top=True
                        )
                        window.enable()
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
                elif gameBoard[endLocation[0]][endLocation[1]][1].ownedBy == playerTurn and "feral" not in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
                    playsound("sounds/wrong.wav",block=False) 
                    pm(window, "You can't jumpkill your own piece.")
                    window.refresh
                    continue

                # kill enemy piece; elif enemy owns the ending location
                elif gameBoard[endLocation[0]][endLocation[1]][1].ownedBy != playerTurn or "feral" in gameBoard[startLocation[0]][startLocation[1]][1].activeBuffs:
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
                    if "feral" in gameBoard[endLocation[0]][endLocation[1]][1].activeBuffs:
                        playsound("sounds/destroy.wav",block=False)
                        pm(window, f"THE BEZERKER KILLED A PIECE AND ENRAGED!  IT HAS EATEN PART OF THE VICTIM AND IS STORING THE REST FOR LATER!")
                        displayBoard(window, gameBoard)
                        window.refresh()
                        gameBoard[endLocation[0]][endLocation[1]][1].feralAttacksLeft -=1
                        gameBoard[endLocation[0]][endLocation[1]][1].feralMeatCount +=1
                        sg.popup(f"THE BEZERKER KILLED A PIECE AND ENRAGED!  IT HAS EATEN PART OF THE VICTIM AND IS STORING THE REST FOR LATER!",keep_on_top = True)
                        
                        if gameBoard[endLocation[0]][endLocation[1]][1].feralAttacksLeft > 0:
                            sleep(1)
                            window["information"].update(f"THE BEZERKER IS STILL ENRAGED AND HAS {gameBoard[endLocation[0]][endLocation[1]][1].feralAttacksLeft} ATTACKS LEFT, AND HAS STORED {gameBoard[endLocation[0]][endLocation[1]][1].feralMeatCount} MEATS")
                            sg.popup(f"THE BEZERKER IS STILL ENRAGED AND HAS {gameBoard[endLocation[0]][endLocation[1]][1].feralAttacksLeft} ATTACKS LEFT, AND HAS STORED {gameBoard[endLocation[0]][endLocation[1]][1].feralMeatCount} MEATS",keep_on_top = True)
                            repeatRestrictor[0] = True
                            repeatRestrictor[1] = (endLocation[0], endLocation[1])
                            continue
                        else:
                            return
                        #


                    else:
                        playsound("sounds/destroy.wav",block=False)
                        window["information"].update(f"Jumpkilled an enemy piece!")
                        pm(window, "Jumpkilled an enemy piece!")

                    secretAgentCheck(window, gameBoard, startLocation, endLocation, playerTurn)
                    

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


##def updateToolTips(window, gameBoard,playerTurn):
##    
##    for i in range(0,len(gameBoard)):
##        for j in range(0,len(gameBoard[0])):
##            print(f"i and j are {i} {j}")
##            if gameBoard[i][j][0].occupied == True:
##                buffs = f"[BUFFS] x{len(gameBoard[i][j][1].activeBuffs)}"+"\n"
##                debuffs = "\n"+f"[DEBUFFS] x{len(gameBoard[i][j][1].activeDebuffs)} "+"\n"
##                storedItems = "\n"+f"[ITEMS] x{len(gameBoard[i][j][1].storedItems)}"+"\n"
##                for b in gameBoard[i][j][1].activeBuffs:
##                    buffs+=b+"\n"
##                for d in gameBoard[i][j][1].activeDebuffs:
##                    debuffs+=d+"\n"
##                if gameBoard[i][j][1].ownedBy == playerTurn:
##                    for s in  gameBoard[i][j][1].storedItems:
##                        storedItems += s+"\n"
##                else:
##
##                    for s in  gameBoard[i][j][1].storedItems:
##                        storedItems += "???"+"\n"
##                toolTipData = buffs+debuffs+storedItems
##            else:
##                toolTipData = ""
##                specialConditions = "Special Conditions:\n"
##                
##                tileType = f"Tile Type: {gameBoard[i][j][0].tileType}"+"\n"
##                tileHeight = f"Tile Height: {gameBoard[i][j][0].tileHeight}"+"\n"
##                if gameBoard[i][j][0].horiLaser or gameBoard[i][j][0].vertLaser or gameBoard[i][j][0].crossLaser:
##                    specialConditions += "Being lasered\n"
##                if gameBoard[i][j][0].orbEater:
##                    specialConditions += "Has an orb eater\n"
##                if gameBoard[i][j][0].wormHole1:
##                    specialConditions += "Has a worm hole (player 1)\n"
##                if gameBoard[i][j][0].wormHole2:
##                    specialConditions += "Has a worm hole (player 2)\n"
##                if gameBoard[i][j][0].recallTurn != False:
##                    specialConditions += "Has a recall slated"
##                if gameBoard[i][j][0].secretAgent:
##                    specialConditions += "Has a secret agent"
##                if gameBoard[i][j][0].purityTile:
##                    specialConditions += "Has a purity tile"
##                if len(gameBoard[i][j][0].dumpList)>0:
##                    specialConditions += "This item dump contains: \n"
##                    for i in gameBoard[i][j][0].dumpList:
##                        specialConditions += i+"\n"
##                toolTipData += tileType + tileHeight + specialConditions
##            try:
##                window[(i,j)].SetTooltip(toolTipData)
##            except:
##                pm(window, "oops, an error occurred with trying to set a new tooltip")




def updateToolTips(window, gameBoard,playerTurn):
    #debug attempt

    
    #window.disappear()

    

    
    for iIndex, iData in enumerate(gameBoard):
        for j, jData in enumerate(iData):
            
            if gameBoard[iIndex][j][0].occupied == True:
                buffs = f"[BUFFS] x{len(gameBoard[iIndex][j][1].activeBuffs)}"+"\n"
                debuffs = "\n"+f"[DEBUFFS] x{len(gameBoard[iIndex][j][1].activeDebuffs)} "+"\n"
                storedItems = "\n"+f"[ITEMS] x{len(gameBoard[iIndex][j][1].storedItems)}"+"\n"
                for b in gameBoard[iIndex][j][1].activeBuffs:
                    if b == None:
                        b = ""
                    if b == "feral":
                        b = f"berzerk - [{gameBoard[iIndex][j][1].feralMeatCount} meats stored]"
                    buffs+=b+"\n"
                for d in gameBoard[iIndex][j][1].activeDebuffs:
                    if d == None:
                        d = ""
                    debuffs+=d+"\n"
                if gameBoard[iIndex][j][1].ownedBy == playerTurn:
                    for s in  gameBoard[iIndex][j][1].storedItems:
                        storedItems += s+"\n"
                else:

                    for s in  gameBoard[iIndex][j][1].storedItems:
                        storedItems += "???"+"\n"
                toolTipData = buffs+debuffs+storedItems+f"\nTILE HEIGHT: {gameBoard[iIndex][j][0].tileHeight}"
            else:
                toolTipData = ""
                specialConditions = "Special Conditions:\n"

                
                tileType = f"Tile Type: {gameBoard[iIndex][j][0].tileType}"+"\n"
                tileHeight = f"Tile Height: {gameBoard[iIndex][j][0].tileHeight}"+"\n"
                if gameBoard[iIndex][j][0].horiLaser or gameBoard[iIndex][j][0].vertLaser or gameBoard[iIndex][j][0].crossLaser:
                    specialConditions += "Being lasered\n"
                if gameBoard[iIndex][j][0].orbEater:
                    specialConditions += "Has an orb eater\n"
                if gameBoard[iIndex][j][0].wormHole1:
                    specialConditions += "Has a worm hole (player 1)\n"
                if gameBoard[iIndex][j][0].wormHole2:
                    specialConditions += "Has a worm hole (player 2)\n"
                if gameBoard[iIndex][j][0].recallTurn != False:
                    specialConditions += "Has a recall slated"
                if gameBoard[iIndex][j][0].secretAgent:
                    specialConditions += "Has a secret agent"
                if gameBoard[iIndex][j][0].purityTile:
                    specialConditions += "Has a purity tile"
                if len(gameBoard[iIndex][j][0].dumpList)>0:
                    specialConditions += "This item dump contains: \n"
                    for i in gameBoard[iIndex][j][0].dumpList:
                        specialConditions += i+"\n"
                toolTipData += tileType + tileHeight + specialConditions
            try:
                window[(iIndex,j)].SetTooltip(toolTipData)
            except:
                pm(window, "oops, an error occurred with trying to set a new tooltip")
    #debug attempt
##    window.disappear()
##    window.reappear()
    #debug attempt
                

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
                
                sg.popup("A piece has recalled",keep_on_top = True)


        
            
def stickyTimeBomb(window,gameBoard):
    validLocations = []
    for iIndex,i in enumerate(gameBoard):
        for jIndex,j in enumerate(i):
            if j[0].occupied == True:
                if j[1].stickyTimeBomb != False:
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
                        sg.popup("The sticky time bomb went off!",keep_on_top())
                        #validLocations.clear()
                                
def itemOrbForecast(window):
    #print each member of the orb list (used for balancing)
    for iIndex, i in enumerate(PublicStats.orbCycleList):
        window[f"Orb{iIndex}"].update(i,text_color = "grey30",font = "Cambria 20")
        
    
    index = (PublicStats.turnCount+1)%len(PublicStats.orbCycleList)
    
    if index >= len(PublicStats.orbCycleList):
        index = 0
    window[f"Orb{index}"].update(f"{PublicStats.orbCycleList[index]}",text_color = ("orange"), font = "Cambria 30")

        
def begin():

    # variables
    columns = 10
    rows = 10
    gameBoard = []


    buttonSize = (75,75)
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
        [sg.Button("Toggle Item Guide", size = (50,10), disabled = True)]



    ]
    frame_turnsPassed = [
        [sg.T(f"{1:3}",font = "Cambria, 30",text_color = "Black",key = 'turnspassed',size = (3,1))]
        ]

    frame_itemOrbForecast =[
        [sg.T(f"123:>3",key = f"Orb{i}",size = (4,1),pad = (0,0),font = "Cambria, 30")for i in range(0,len(PublicStats.orbCycleList))]
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
    #item info is in this frame
    frame_layout = [
        [sg.Image("images/up.png", key="turn", visible=True)],
        [
            sg.T(f"Player:", font="Cambria 30", pad=(4, 4)),
            sg.T(f"", key="playerTurn", font="Cambria 30", pad=(4, 4)),
        ],
        [sg.T(f" " * 50, key="information", size=(25, 3), font="Cambria 30")],
        [sg.Frame("Pieces Remaining", frame_remaining), sg.Frame("Item Info",frame_itemInfo)],
        [sg.Frame("Current Turn", frame_turnsPassed), sg.Frame("Item Orb Forecast (expected number of orbs that will spawn after your turn ends):",frame_itemOrbForecast)],
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
        #keep_on_top = True,
        disable_close=False,
        
        location=(0, 0),
    ).finalize()
    
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
        gamePlay(playerTurn, window, gameBoard)
        x = -1
        y = -1
        # end player one's turn, begin player two's turn, switch players
        if playerTurn == 1:
            
            window["turn"].update(filename="images/down.png")
            window['turnspassed'].update(f"{PublicStats.turnCount:>3}")
            itemOrbForecast(window)
            #check for recalled pieces
            if PublicStats.recallCount > 0:
                recallFunction(window,gameBoard)

            #check for sticky bombs
            stickyTimeBomb(window,gameBoard)
            
                
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
            laserCheck(window, gameBoard)
            if orbsEaten > 0:
                pm(window, f"Orbs eaten by the orb eaters: {orbsEaten}")
                fileNum = random.randint(1,4)
                playsound(f"sounds/squeak{fileNum}.mp3", block = False)
            feralFunction(window, gameBoard, playerTurn)



            
        # end player two's turn, begin player one's turn
        else:
            window["turn"].update(filename="images/up.png")
            window['turnspassed'].update(f"{PublicStats.turnCount:>3}")
            itemOrbForecast(window)
            #check for recalled pieces
            if PublicStats.recallCount > 0:
                recallFunction(window,gameBoard)

            #check for sticky time bomb
            stickyTimeBomb(window,gameBoard)
            
            
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
            laserCheck(window, gameBoard)    
            resetMoveAgain(gameBoard)
            if orbsEaten > 0:
                pm(window, f"Orbs eaten by the orb eaters: {orbsEaten}")
                fileNum = random.randint(1,4)
                playsound(f"sounds/squeak{fileNum}.mp3", block = False)
            feralFunction(window, gameBoard, playerTurn)


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
        #[sg.Button("Getting info on pieces", key="info")],
        [sg.Button("EXIT", key="EXIT")],
        
    ]
    frame_2 = [
        [
            sg.Button(
                image_filename="images/default.png",
                key=(i, j),
                size=(20, 20),
                tooltip="tooltip",
                #pad=(10, 10),
            )
            for j in range(columns)
        ]
        for i in range(0, rows)
    ]
    frame_3 = [[sg.T(" " * 100, key="tutorialInfo", font="Cambria 13", size=(50, 10))]]
    frame_4 = [[sg.T(" " * 100, key="information", font="Cambria 13", size=(88, 20))]]

    layout = [
        [
            sg.T("MegaCheckers", font="Cambria 50", key="title"),
            #sg.Button("use item", image_filename="images/backpack.png", visible=False),
        ],
    ]
    layout += [
        [
            sg.Frame("Main screen", frame_1, key="options", visible=True),
            sg.Frame("Game Play", frame_2, key="gamePlay", visible=True),
            sg.Frame("Tutorial Info", frame_3)
            
        ],
        [ sg.Frame("Information", frame_4)]
        
    ]
    #layout += [[sg.Frame("Tutorial Info", frame_3), sg.Frame("Information", frame_4)]]

    # gameBoard for logic
    gameBoard = []
    line = []
    for i in range(columns):
        line.append([Tile(), 0])
        gameBoard.append(0)

    for j in range(rows):
        gameBoard[j] = copy.deepcopy(line)

    window = sg.Window("MegaCheckers", layout, location=(0, 0)).finalize()
    window.maximize()

    initializeField(columns, rows, window, gameBoard)

    window["options"].update(visible=True)

    while True:
        event = window.read()
        if event[0] == "EXIT":
            # QUIT
            window.close()
            main()
            raise SystemExit
        if event[0] == "object":
            window["gamePlay"].update(visible=True)
            myText = """OBJECT: The object of the game is to destroy all of your opponent's pieces or make it impossible for them to take a turn.  Your main method to do this will be by jumping on enemy pieces to kill them (don't worry, the pieces aren't sentient, so no one is getting hurt).  You will also be able to employ items that you find on the field to either protect yourself from your enemies or to blow them up someway or another.  Pick another topic from the menu on the left."""
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
                                    #window["use item"].update(visible=True)
                                    myText = "Click on the same piece twice to see the item menu."

                                    event = window.read()
                                    window["tutorialInfo"].update(myText)

                                    if event[0] == (2, 4):
                                        myText = "Click on the same piece again to see the item menu."
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
                                        window.close()
                                        tutorial()

                                    else:
                                        sg.popup("Nope, try again", keep_on_top=True)
                                        continue

        else:
            myText = "Invalid choice.  There are no tutorials in progress. Try clicking something on the menu on the left."
            window["tutorialInfo"].update(myText)

def popupItemExplanation():
    itemsList = pickUpItemOrb(getItemsList = True)
        
    text = "THIS IS A TEMPORARY SOLUTION TO SHOWING ALL THE ITEMS.  IT'LL BE REPLACED BY SOMETHING PRETTIER... EVENTUALLY.\n\n\n"
    for i in itemsList:
        explanation = itemExplanation(i)
        text+= f"{i}: {explanation}"
        text+="\n\n\n"
    sg.PopupScrolled(text)
    

def main():
    publicPNGloader()
    introLayout = [[sg.Text("Mega\nCheckers", font="Cambria 100", justification = "center")]]
    frame_1 = [
        [sg.Button("Begin game", key="begin", size = (20,5))],
        [sg.Button("How to play", key="tutorial", size = (20,2))],
        [sg.Button("Read about items")]
    ]
    frame_2 = [
        #name of item
        [sg.T(f"",key="itemName",text_color = "blue",font = "Cambria, 40",size = (20,1))],
        #address of item picture
        [sg.Image("",size=(400,400),key="itemPic"),],
        [sg.T(f"(No description)",key = "itemDescription",size = (75,7),font = "Cambria 20")]
        ]
    introLayout += [[sg.Frame("Choose an option", frame_1, key="options"),sg.Frame("Items Spotlight:",frame_2,key="itemBlurb")]]
    introWindow = sg.Window("MegaCheckers", introLayout).finalize()
    introWindow.disappear()
    while True:
        
            itemName = pickUpItemOrb(introOnly = True)
            
            introWindow["itemPic"].update(filename = f"images/{itemName}.png")
            
            introWindow["itemName"].update(itemName)
            
            description = itemExplanation(itemName)
            
            introWindow["itemDescription"].update(description)
            introWindow.reappear()
            
            
            break
        
            sg.popup("Error in introwindow")
            continue
    event = introWindow.read()
    if event[0] == "tutorial":
        introWindow.close()
        tutorial()
    if event[0] == "begin":
        introWindow.close()
        begin()
    if event[0] == "Read about items":
        introWindow.close()
        popupItemExplanation()
        main()

# delete me after debug
#begin()
# delete me



main()
