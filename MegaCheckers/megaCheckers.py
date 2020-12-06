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


#contains:
# func begin: starts the game
# func createOrbs: create orbs between turns
# func gamePlay: the root game loop
# func initializeField: set up the player pieces and create board
# func itemOrbForecast: forecast how many item orbs are appearing
# func orbEater: the "AI" for the mice that eat item orbs
# func recallFunction: saves state of a tile and returns it to that state in X turns
# func repairFloor: slowly repairs the ground by one phase each turn
# func roundEarthTheory: allows applicable pieces to roll to opposite side of the field
# func secretAgentCheck: runs the logic for the secretAgent item
# func spookyHand: runs the logic for the spooky hand item
# func stickyTimeBomb: runs the logic for the sticky bomb item
# func tutorial: show the tutorial gifs
# func popupItemExplanation: deprecated
# func main: start the preparations for the game loop

#############################
# starts the game           #
#############################
def begin(screenSize):
    
    columns = 10
    rows = 10
    # list of rows
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
        if os.path.exists(f"{workingDirectoryName}/images"):
            shutil.rmtree(f"{workingDirectoryName}/images")
            
        shutil.copytree(workingDirectoryName+"/imagesNormal", workingDirectoryName+"/images")
    else:
        buttonSize = (40,40)
        sg.popup("Note that this mode is a backup mode designed for rarer laptops that don't have normal 1900x1080 resolutions. Enough development time does not exist for focused changes to this mode, so things may look weird.  I recommend you get a normal sized monitor in order to enjoy the game properly.",keep_on_top = True)
        if os.path.exists(f"{workingDirectoryName}/images"):
            shutil.rmtree(f"{workingDirectoryName}/images")
        shutil.copytree(workingDirectoryName+"/imagesSmall", workingDirectoryName+"/images")

    # safety clear in case the PNG still has data left over from a previous game or something
    PublicPNGList.clear()
    #loads .png files from harddrive to RAM; lowers the disk usage
    publicPNGloader()
    
    # create the main window 
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

    # "read about items" frame
    frame_itemInfo = [
        [sg.Button("Read Items", size = (50,10))]

    ]

    # show the elevation map legend
    frame_elevation = [
            [sg.Image(filename = "images/elevation.png", tooltip = "Each shade represents the height of a given tile.  A piece can jump down safely from any height to any tile that is lower than it.\nHowever, it cannot climb a tile that is more than one elevation unit taller.")]

        ]
    # how many turns have passed
    frame_turnsPassed = [
        [sg.T(f"{1:3}",font = "Cambria, 30",text_color = "Black",key = 'turnspassed',size = (3,1))]
        ]
    # how many items are expected to spawn next turn
    frame_itemOrbForecast =[
        [sg.T(f"xx:>3",key = f"Orb{i}",size = (4,1),pad = (0,0),font = "Cambria, 30", )for i in range(0,len(PublicStats.orbCycleList))]
    ]

    # how any pieces each player has remaining
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

    # which items the current player has
    top_right_frame = [  [ sg.Button("",key = f"itemList{i}{j}",disabled = True, size = (15,1)) for i in range(0,3)]for j in range(0,15)  ]

    # whose turn is it?
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

    
        
    # layout of the main window
    layout = [
        [
            # game's title
            sg.T("MegaCheckers", font="Cambria 50"),
            # get more information about a tile
            sg.Button(
                "Look",
                button_color=("Blue", "White"),
                tooltip="Examine",
                font="Cambria 20",
                key="examineItem",
                image_filename="images/examine.png",
            ),
            #exit game
            sg.Button("Exit", size=(20,4), key="exit"),
            # cheat in items by typing their name; consider a more fun way,
            # maybe by changing it to a phrase related to the item than
            # the name of the item itself.  For example, napalm might be replaced
            # by "imfiredup" or spookyhand might be replaced by "donttouchme"
            sg.Button("cheetz"),
            sg.Button("Surrender")
        ]
    ]
    #add the game itself
    layout += [
        [
            sg.Frame("Playing Field", frame_main),
            sg.Frame(
                "Information:", frame_layout, font="Calibri 20", title_color="blue"
            ),
        ],
    ]
    
    window = sg.Window(
        "MegaCheckers",
        layout,
        #no_titlebar=True,
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

    
    #flag to show quick start once
    showQuickStartOnce = True
    #Between turns
    playerTurn = 1
    
    while True:
        if showQuickStartOnce == True:
            sg.popup("""QUICK GUIDE:\n- Starting out, pieces can move up, down, left, right\n- Pick up items by stepping on them\n- Kill enemies by stepping on them or using items\n- Use items by double clicking your piece\n""", keep_on_top = True, title = "Quick Start")
        showQuickStartOnce = False
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
                                    playSoundExceptionCatcher("sounds/getItem.wav",block=False)
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
                playSoundExceptionCatcher(f"sounds/squeak{fileNum}.wav", block = False)
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
                                    playSoundExceptionCatcher("sounds/getItem.wav",block=False)
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
                playSoundExceptionCatcher(f"sounds/squeak{fileNum}.wav", block = False)
            berzerkFunction(window, gameBoard, playerTurn)


# neat little function I made to get around the glitchy module - instead of a memory leak error, it just skips it
def playSoundExceptionCatcher(fileName, block = True):
    try:
        playsound(fileName, block)
    except:
        print(".")


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


# the actual loop that is used to progress turns
def gamePlay(playerTurn, window, gameBoard):

    
    countPieces(gameBoard, window, PublicStats)
    createOrbs(window, gameBoard)
    giveUpFlag = movePiece(playerTurn, window, gameBoard)
    if giveUpFlag == "give up":
        giveUpFlag = "continue"
        window.close()
        main()
    else:
        PublicStats.turnCount += 1
        repairFloor(window, gameBoard)

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
            

def itemOrbForecast(window):
    #print each member of the orb list (used for balancing)
    for iIndex, i in enumerate(PublicStats.orbCycleList):
        window[f"Orb{iIndex}"].update(i,text_color = "grey30",font = "Cambria 20")
        
    
    index = (PublicStats.turnCount+1)%len(PublicStats.orbCycleList)
    
    if index >= len(PublicStats.orbCycleList):
        index = 0
    window[f"Orb{index}"].update(f"{PublicStats.orbCycleList[index]}",text_color = ("orange"), font = "Cambria 30")

def main():
    workingDirectoryName = os.getcwd()
    if os.path.exists(f"{workingDirectoryName}/images"):
        shutil.rmtree(f"{workingDirectoryName}/images")
    shutil.copytree(workingDirectoryName+"/imagesNormal", workingDirectoryName+"/images")

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


main()
