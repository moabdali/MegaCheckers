#imported by megaCheckers

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
from itemExplanationMegaCheckers import *
from displayBoardMegaCheckers import *

#########################################################################################
# FUNCTION: PICK UP ITEM ORB: the item list; it contains a list of the names of every   #
# single item, and allows it to spawn upon picking up an item orb.  If it's not in the  #
# list, the item cannot be spawned (even with cheats).  So make sure any items that are #
# added are added to this list.                                                         #
#########################################################################################
def pickUpItemOrb(gameBoard=0, x=0, y=0, introOnly = False, window = None, getItemsList = False):
    # items = ["suicideBomb Row","Energy Forcefield","suicideBomb Column","Haphazard Airstrike","suicideBomb Radial","jumpProof","smartBombs"]
    items = [
        "AI bomb", #walking bomb
        "auto win", #win in 50 turns
        "bernie sanders", #redistribute inactive items
        "berzerk", #if you kill a piece, go again. But die if you haven't eaten lately
        "bowling ball", #out of control bowling ball
        "canyon column", #create a trench
        "canyon radial",
        "canyon row",
        "care package drop", #drop item orbs near an opponent
        "charity",#10 Give an opponent a piece
        "dead man's trigger", #if your piece is jumped on, the enemy dies, too
        "dump items", #dump your items anywhere on the field
        "elevate tile", #raise a tile
        "Energy Forcefield", #create a defensive shield on your piece
        "floor restore", #restore all tiles
        "grappling hook", #hook your way up a tall tile
        "haphazard airstrike", #indiscriminately bomb the playing field
        "haymaker", #punch a piece away
        "heir", #forcefully take all of your allied pieces' powers
        "invert elevation all",#20 lower tall tiles, raise low tiles
        "invert elevation column",
        "invert elevation radial",
        "invert elevation row",
        "jump proof", #piece cannot be jumped on
        "jumpoline", #jump onto this tile in order to be bounced elsewhere
        "laser column", #create a laser that burns all units in range
        "laser row",
        "magnet", #"suck in" all nearby pieces
        "move again", #get an extra move with this piece
        "move diagonal",#30 move diagonally
        "mutual treason column", #swap ownership of all pieces in range
        "mutual treason radial",
        "mutual treason row",
        "mystery box", # a mystery effect occurs
        "napalm column", #burn all enemy pieces in range, the floor melts away
        "napalm radial",
        "napalm row",
        "orb eater", # summon a mouse that eats orbs
        "place mine", # drop a mine
        "purify column",#40 remove all negative effects from your pieces in range
        "purify radial",
        "purify row",
        "purity tile", # create a reusable tile that heals any piece that steps on it
        "recall", # return a piece to the condition it was in at the time of use, in 10 turns
        "reproduce", # create a brand new piece next to the current piece
        "round earth theory", # ignore boundaries of the playing field - loop around
        "secretAgent", #steals your enemy's items and gives them to you
        "seismic activity", #earthquake that randomly changes the elevation of the tiles
        "shuffle all", #move tiles around randomly
        "shuffle column",#50
        "shuffle item orbs", #move item orbs around randomly
        "shuffle radial",
        "shuffle row",
        "sink tile", # lower the tile
        "smart bombs", # shoot the playing field with no threat of damage to your pieces
        "snake tunneling", # a snake randomly moves nearby tiles up randomly; killing enemies
        "spooky hand", #a scary hand that will stay resident under the field and kidnap enemies
        "steal items column", #steal items from the enemy
        "steal items radial",
        "steal items row",#60
        "steal powers column", #steal activated powers from the enemies
        "steal powers radial",
        "steal powers row",
        "sticky time bomb", #attach a time bomb to any piece, it will blow up in a few turns
        "study column", #copy powers from your allies
        "study radial",
        "study row",
        "suicide bomb column", #kill yourself and your enemies
        "suicide bomb radial",
        "suicide bomb row",#70
        "teach column", #copy powers TO your allies
        "teach radial",
        "teach row",
        "trap orb", #set a trap that blows up your enemy if they step on it.  Looks like an item orb
        "trip mine column", #set a mine on your enemies.  If they move, they die.
        "trip mine radial",
        "trip mine row",
        "trump", #build a wall (raise the tiles)
        "vampiricism", #steal powers from your enemy
        "vile radial",#80 enemy can't activate items
        "warp", #teleport randomly
        "wololo column", #steal enemy pieces
        "wololo radial",
        "wololo row",
        "worm hole", #set a  worm hole; any of YOUR pieces can jump straight to it as long as it's not occupied
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
    youFoundA = "You found a".center(len(randItem*2))
    pickupFrame = [
        [sg.Image(f"images/{randItem}.png",tooltip = explanation) ],
        [sg.T(explanation,visible = True,key="showExplanation", font = "cambria, 15")],
        [sg.Button("Hide/Show explanations")],
        [sg.T(youFoundA, font = "Cambria 30")],
        [sg.T(randItem, font = "Cambria 50", text_color = "Blue")],
        #[sg.T("(Hover over the picture to read about the item)")],
        [sg.Button("          ", key = "Affirmative", font = "Cambria 30")]
                    ]
        
    pickUpLayout = [
            [sg.Frame("GET ITEM", pickupFrame,element_justification = "center")]
        ]
    window.disable()

    #list of cutesy ways to say OK (feel free to add more)
    affirmativeList = ("Sweet", "Nice!", "Thanks", "Woot!", "Ok", "K.", "I see...", "Neat.")
    randomChoice = random.choice(affirmativeList)
    
    pickUpWindow = sg.Window("Get item.", pickUpLayout,keep_on_top = True, no_titlebar = True).finalize()
    pickUpWindow["Affirmative"].update(randomChoice)
    
    

    while True:
        if PublicStats.showItemExplanations:
            pickUpWindow["showExplanation"].update(visible = True)
        else:
            pickUpWindow["showExplanation"].update(visible = False)
        a = pickUpWindow.read()
        if a[0] == "Affirmative":
            pickUpWindow.close()
            break
        if a[0] == "Hide/Show explanations":
            if PublicStats.showItemExplanations:
                PublicStats.showItemExplanations = False
            else:
                PublicStats.showItemExplanations = True
                
    window.enable()
    
    
    #sg.PopupAnimated(f"images/{randItem}.png",no_titlebar = False, font = "cambria 20",message = f"Picked up an item orb containing \n[{randItemName}]!")



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


def updateToolTips(window, gameBoard,playerTurn):
 
    for iIndex, iData in enumerate(gameBoard):
        for j, jData in enumerate(iData):
            
            if gameBoard[iIndex][j][0].occupied == True:
                buffs = f"[BUFFS] x{len(gameBoard[iIndex][j][1].activeBuffs)}"+"\n"
                debuffs = "\n"+f"[DEBUFFS] x{len(gameBoard[iIndex][j][1].activeDebuffs)} "+"\n"
                storedItems = "\n"+f"[ITEMS] x{len(gameBoard[iIndex][j][1].storedItems)}"+"\n"
                for b in gameBoard[iIndex][j][1].activeBuffs:
                    if b == None:
                        b = ""
                    if b == "berzerk":
                        b = f"berzerk - [{gameBoard[iIndex][j][1].berzerkMeatCount} meats stored]"
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
                if playerTurn == 1:
                    
                    if jData[0].tileType in ("itemOrb", "trap orb 0", "trap orb 2"):
                        tileType += "\nThis tile will give you an item if you land on it!\n(Or on rare occasions, it might actually be a trap orb and blow you up)\n\n"
                elif playerTurn == 2:
                    if jData[0].tileType in ("itemOrb", "trap orb 0", "trap orb 1"):
                        tileType += "\nThis tile will give you an item if you land on it!\n(Or on rare occasions, it might actually be a trap orb and blow you up)\n\n"
                if jData[0].tileType == "mystery box":
                    tileType+= "\n A random event will occur when you step on this tile (can be bad or good)!\n\n"
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

    #disable tile buttons so they can't be clicked
    #currently disabling this feature because it looks ugly
##    for i,idata in enumerate(gameBoard):
##        for j,jdata in enumerate(idata):
##            window[(i,j)].update(disabled = True)

    
    while True:
        #window.disable()
        playsound("sounds/click2.mp3",block=False)
        #itemsMenu.UnHide()
        event = (itemsMenu.read())
        
        try:
            i = event[0]
            for inum,idata in enumerate(gameBoard):
                for jnum,jdata in enumerate(idata):
                    window[(inum,jnum)].update(disabled = False)
            #window.enable()
            if i == None:
                itemsMenu.close()
                return "earlyBreak"
            if i == "CANCEL":
                itemsMenu.close()
                return "earlyBreak"
            if i == '+FOCUS OUT+':
                itemsMenu.close()
                return "earlyBreak"
                
            
            if i in range(0,len(gameBoard)):
                window.enable()
                break
        except:
            #window.enable()
            break

        itemsMenu.Hide()
        
#all, allHurt, enemyHurtOnly, alliesHelpedOnly, allOccupiedNeutral, alliesHurtOnly
#def highlightValidDistance(gameBoard, window, startLocation, actionType = "walk", reachType = "cross", turnOff = False):
        
# suicidebomb row
        if str.find(i, "suicide bomb row") >= 0:
            itemsMenu.Hide()
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
                if j[0].occupied == True:
                    death = forcefieldCheck(window, gameBoard, endLocation = j ,danger ="both")
                    #if you didn't die, then start looking in a different direction
                    if death == False:
                        continue



                    #if it doesn't have a forcefield
                    else:
                        
                        j[0].occupied = False
                        j[1] = 0
                        tileBackup = j[0].tileType
                        if tileBackup in ("player1default", "player2default"):
                            tileBackup = "default"
                        j[0].tileType = "exploding"
                        displayBoard(window, gameBoard)
                        window.refresh()
                        j[0].tileType = tileBackup
                        displayBoard(window, gameBoard)
                        window.refresh()


# auto win
        elif str.find(i, "auto win") >= 0:
            itemsMenu.Hide()

            if PublicStats.playerAutoWin != 0:
                sg.popup("Sorry buddy, someone else has already used an auto win, so you're outta luck this time", keep_on_top = True)
            else:
                PublicStats.playerAutoWin = playerTurn
                PublicStats.playerAutoWinTurn = PublicStats.turnCount + 100
                gameBoard[x][y][1].storedItems.remove("auto win")
                window.disable()
                layoutWin = [ [sg.T("CONGRATULATIONS, YOU WIN", font = "Cambria, 50", text_color = "Silver")], [sg.T("in 100 turns.", font = "Cambria 12")], [sg.Button("AWESOME I AM AMAZING",size = (100,2))] ]
                winWindow = sg.Window("YOU WIN", layoutWin,keep_on_top = True).finalize()
                winWindow.read()
                window.enable()
                winWindow.close()
                
# grappling hook
        elif str.find(i, "grappling hook") >= 0:
            itemsMenu.Hide()

            if "burdened" in gameBoard[x][y][1].activeDebuffs:
                
                sg.popup("This piece has been hit by the burdened debuff and can't equip the grappling hook.  Try finding a purifying item or tile.", keep_on_top = True)
                continue
            else:
                gameBoard[x][y][1].storedItems.remove("grappling hook")
                gameBoard[x][y][1].activeBuffs.append("grappling hook")
                pm(window,"Your piece now has a grappling hook and can climb even the tallest of tiles.", )
                sg.popup("Your piece now has a grappling hook and can climb even the tallest of tiles.",keep_on_top=True)
                continue
                
# canyon row
        elif str.find(i, "canyon row") >= 0:
            itemsMenu.Hide()
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
            itemsMenu.Hide()
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
            itemsMenu.Hide()
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
            itemsMenu.Hide()
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
            itemsMenu.Hide()
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
            itemsMenu.Hide()
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
            itemsMenu.Hide()
            yesno = sg.popup_yes_no("Induce an earthquake?  This will cause random elevation changes to the field.  Pieces will not be harmed.",keep_on_top=True)
            if yesno == "No":
                continue
            magnitude = random.randint(1,10)
            gameBoard[x][y][1].storedItems.remove("seismic activity")
            if magnitude in (1,2,3,4):
                raiseLower = (-1,0,0,0,0,1)
                playsound("sounds/earthquake.mp3",block=False)
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
                playsound("sounds/earthquake.mp3",block=False)
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
                playsound("sounds/earthquake.mp3",block=False)
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
            itemsMenu.Hide()
            yesno = sg.popup_yes_no("Do you want to invert all the heights of tiles on the field to their opposites? (low -> high, high -> low, neutral height tiles will be unaffected)",keep_on_top=True)
            if yesno == "No":
                continue

            for i in gameBoard:
                for j in i:
                    j[0].tileHeight *= -1
            sg.popup("The field's topology has been inverted.  All highs are lows, and all lows are highs.", keep_on_top = True)
            pm(window,"The field's topology has been inverted.  All highs are lows, and all lows are highs.")
            gameBoard[x][y][1].storedItems.remove("invert elevation all")

#invert elevation column
        elif str.find(i, "invert elevation column") >= 0:
            itemsMenu.Hide()
            yesno = sg.popup_yes_no("Do you want to invert all the heights of tiles in this column to their opposites? (low -> high, high -> low, neutral height tiles will be unaffected)",keep_on_top=True)
            if yesno == "No":
                continue

            for i in gameBoard:
                i[y][0].tileHeight *= -1
            sg.popup("The column's topology has been inverted.  All highs are lows, and all lows are highs.", keep_on_top = True)
            pm(window,"The columns's topology has been inverted.  All highs are lows, and all lows are highs.")
            gameBoard[x][y][1].storedItems.remove("invert elevation column")
            
#invert elevation row
        elif str.find(i, "invert elevation row") >= 0:
            itemsMenu.Hide()
            yesno = sg.popup_yes_no("Do you want to invert all the heights of tiles in this row to their opposites? (low -> high, high -> low, neutral height tiles will be unaffected)",keep_on_top=True)
            if yesno == "No":
                continue

            for i in gameBoard[x]:
                i[0].tileHeight *= -1
            sg.popup("The row's topology has been inverted.  All highs are lows, and all lows are highs.", keep_on_top = True)
            pm(window,"The row's topology has been inverted.  All highs are lows, and all lows are highs.")
            gameBoard[x][y][1].storedItems.remove("invert elevation row")

#invert elevation radial
        elif str.find(i, "invert elevation radial") >= 0:
            itemsMenu.Hide()
            yesno = sg.popup_yes_no("Do you want to invert all the heights of tiles in this row to their opposites? (low -> high, high -> low, neutral height tiles will be unaffected)",keep_on_top=True)
            if yesno == "No":
                continue

            radialList = getRadial(location, gameBoard)
            for i in radialList:
                x1 = i[0]
                y1 = i[1]
                gameBoard[x1][y1][0].tileHeight *= -1
                
            sg.popup("The radial's topology has been inverted.  All highs are lows, and all lows are highs.", keep_on_top = True)
            pm(window,"The radial's topology has been inverted.  All highs are lows, and all lows are highs.")
            gameBoard[x][y][1].storedItems.remove("invert elevation radial")
            
#trump
        elif str.find(i, "trump") >= 0:
            itemsMenu.Hide()
            yesno = sg.popup_yes_no("Do you want to build a wall and make your opponent pay for it?* (*The wall is free and no one will actually pay for it)",keep_on_top=True)
            if yesno == "No":
                continue

            wallWindowLayout = [
                [ sg.T(f"The wall can be built in either your row or your column.  The wall will raise all existing tiles in range, but will not repair any broken tiles.  Any pieces that are on the tiles will not be affected other than being elevated.") ],
                [ sg.Button(f"Build Row Wall",key = "row wall"), sg.Button(f"Build Column Wall", key = "column wall"),sg.Button("Cancel")]
                ]
            wallWindow = sg.Window("Do you want to build a wall?", wallWindowLayout, keep_on_top = True)
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

#shuffle all
        elif str.find(i, "shuffle all") >= 0:
            itemsMenu.Hide()
            yesno = sg.popup_yes_no("Ya sure you want to shuffle the entire field around?",keep_on_top=True)
            if yesno == "No":
                continue
            gameBoard[x][y][1].storedItems.remove("shuffle all")
            gameBoard[x][y][1].currentTurnPiece = True
            gameBoard[x][y][1].grey = False
            random.shuffle(gameBoard)
            coords = []
            gameBoardCopy = []
            vertical = []
            
            for i in range(0,len(gameBoard)):
                for j in range(0,len(gameBoard)):
                    coords.append( (i,j) )
            for i in range(0,len(coords)):
                while True:
                    xy = random.choice(coords)
                    if xy == None:
                        continue
                    else:
                        x = xy[0]
                        y = xy[1]
                        gameBoardCopy.append(copy.deepcopy(gameBoard[x][y]))
                        coords[coords.index( xy)] = None
                        break
                    
            coords2 = []
            for i in range(0,len(gameBoard)):
                for j in range(0,len(gameBoard)):
                    coords2.append( (i,j) )
            random.shuffle(gameBoardCopy)
            for i in coords2:
                x = i[0]
                y = i[1]
                
                gameBoard[x][y] = copy.deepcopy(gameBoardCopy[0])
                gameBoardCopy.remove(gameBoardCopy[0])
            laserCheck(window, gameBoard, resetOnly = True)
            laserCheck(window, gameBoard)
            displayBoard(window,gameBoard)
            
# steal items column
        elif str.find(i, "steal items column") >= 0:
            itemsMenu.Hide()
            highlightValidDistance(gameBoard, window, startLocation, actionType = "enemyHurtOnly", reachType = "column" )
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
            itemsMenu.Hide()
            highlightValidDistance(gameBoard, window, startLocation, actionType = "enemyHurtOnly", reachType = "row" )
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
            itemsMenu.Hide()
            highlightValidDistance(gameBoard, window, startLocation, actionType = "enemyHurtOnly", reachType = "radial" )
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
            itemsMenu.Hide()
            highlightValidDistance(gameBoard, window, startLocation, actionType = "enemyHurtOnly", reachType = "column" )
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
            
            gameBoard[x][y][1].storedItems.remove("steal powers column")


# steal powers row
        elif str.find(i, "steal powers row") >= 0:
            itemsMenu.Hide()
            highlightValidDistance(gameBoard, window, startLocation, actionType = "enemyHurtOnly", reachType = "row" )
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
            
            gameBoard[x][y][1].storedItems.remove("steal powers row")

# steal powers radial
        elif str.find(i, "steal powers radial") >= 0:
            itemsMenu.Hide()
            highlightValidDistance(gameBoard, window, startLocation, actionType = "enemyHurtOnly", reachType = "radial" )
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
            
            gameBoard[x][y][1].storedItems.remove("steal powers radial")                              

# teach column
        elif str.find(i, "teach column") >= 0:
            itemsMenu.Hide()
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
# heir            
        elif str.find(i, "heir") >= 0:
            itemsMenu.Hide()
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
                itemsMenu.Hide()
                yesno = sg.popup_yes_no("Use?",keep_on_top=True)
                if yesno == "Apply the vampricism buff to yourself?  (Jump killing an enemy allows you to steal (most) powers from them)":
                    continue
                playsound("sounds/vampire.mp3",block=False)
                gameBoard[x][y][1].activeBuffs.append("vampiricism")
                gameBoard[x][y][1].storedItems.remove("vampiricism")
                    
                        
            
#bernie sanders   
        elif str.find(i, "bernie sanders") >= 0:
            itemsMenu.Hide()
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
        elif str.find(i, "care package drop") >= 0:
            itemsMenu.Hide()
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
            itemsMenu.Hide()
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
            itemsMenu.Hide()
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
            itemsMenu.Hide()
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

#study column           
        elif str.find(i, "study column") >= 0:            
            itemsMenu.Hide()
            gameBoard[x][y][1].grey = False
            if "inert" in gameBoard[x][y][1].activeDebuffs:
                sg.popup("This piece is inert and can't learn anything",keep_on_top=True)
                continue
            learnedFromPieces = 0
            learnedString = ""
            bowlingBallRejected = False
            # for every column in gameBoard
            for iIndex, i in enumerate(gameBoard):
                #if the x'th item belongs to you, and it's not the same item that's sharing the items
                c = i[y]
                if c[0].occupied == True and c[1].ownedBy == playerTurn and iIndex != x and len(c[1].activeBuffs)>0:
                    #for every item in the active buffs list
                    c[1].grey = True
                    pm(window,"Learning")
                    displayBoard(window,gameBoard)
                    window.refresh()
                    learnedFromPieces += 1
                    for k in c[1].activeBuffs:
                        if k != "bowling ball":
                            learnedString += k + "\n"
                            gameBoard[x][y][1].activeBuffs.append(k)
                        else:
                            bowlingBallRejected = True
                    c[1].grey = False
                else:
                    continue
            if bowlingBallRejected == True:
                sg.popup("You attempted to learn bowling ball from at least one piece, but it proved to be too difficult.",keep_on_top=True)
            sg.popup(f"Learned buffs from {learnedFromPieces} piece(s): \n{learnedString}", keep_on_top = True)
            pm(window,f"Learned buffs from {learnedFromPieces} piece(s): \n{learnedString}")

# study radial
        elif str.find(i, "study radial") >= 0:
            itemsMenu.Hide()
            highlightValidDistance(gameBoard, window, startLocation, actionType = "alliesHelpedOnly", reachType = "radial" )
            displayBoard(window, gameBoard)
            window.refresh()
            if "burdened" in gameBoard[x][y][1].activeDebuffs:
                sg.popup("This piece can't learn anything because it's got a 'burdened' debuff.  Try clearing it with a purify item or tile first.")
                pm(window,"This piece can't learn anything because it's got a 'burdened' debuff.  Try clearing it with a purify item or tile first.")
                continue
            yesno = sg.popup_yes_no("Learn buffs from allied pieces in range?  (You cannot learn some buffs, including bowling buff and berzerk.)",keep_on_top=True)
            if yesno == "No":
                continue
            gameBoard[x][y][1].grey = False
            gameBoard[x][y][1].storedItems.remove("study radial")
            validList = getRadial(location, gameBoard)
            buffsCount = 0
            buffsName = "\nLearned the following:\n"
            for i in validList:
                ix = i[0]
                iy = i[1]
                
                if gameBoard[ix][iy][0].occupied and (x,y) != (ix,iy):
                    if gameBoard[ix][iy][1].ownedBy == playerTurn:
                        for buffs in gameBoard[ix][iy][1].activeBuffs:
                            if buffs not in ("bowling ball","berzerk"):
                                #sg.popup(f"adding {buffs}", keep_on_top = True)
                                gameBoard[x][y][1].activeBuffs.append(buffs)
                                buffsCount += 1
                                buffsName += buffs.center(25)+"\n"
            
            if buffsCount > 0:
                # took a surprising amount of work to get it to center properly
                # apparently you can't just center the whole thing in one fell swoop
                text = f"Learned {buffsCount} skills!".center(25)
                text += f"{buffsName}"
                sg.popup(text, font = "Cambria, 20",keep_on_top = True)
            else:
                sg.popup("You didn't learn anything!  What a waste!", keep_on_top = True)
            

            
#study row            
        elif str.find(i, "study row") >= 0:            
            itemsMenu.Hide()
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
            itemsMenu.Hide()


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
            itemsMenu.Hide()
            gameBoard[x][y][1].storedItems.remove("dead man's trigger")
            gameBoard[x][y][1].activeBuffs.append("dead man's trigger")
            sg.popup("This piece has applied a dead man's trigger to itself.  If he is jumped by an enemy, they will die as well.",keep_on_top=True)

# mutual treason row  
        elif str.find(i,"mutual treason row") >=0 or str.find(i,"mutual treason column")>=0 or str.find(i,"mutual treason radial")>=0:
            itemsMenu.Hide()
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
            itemsMenu.Hide()
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
            itemsMenu.Hide()
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
            itemsMenu.Hide()
            gameBoard[x][y][1].storedItems.remove("floor restore")
            for i in gameBoard:
                for j in i:
                    if j[0].tileType in(PublicStats.damagedFloor):
                        j[0].tileType = "default"
            sg.popup("Any damaged floors are back to brand new condition",keep_on_top=True)

# secretAgent          
        elif str.find(i,"secretAgent") >= 0:
            itemsMenu.Hide()
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
            itemsMenu.Hide()
            validTargets = getCross((x, y), gameBoard, trueEmpty = True)
            
            startLocation = (x,y)
            for i in validTargets:
                ix = i[0]
                iy = i[1]
                gameBoard[ix][iy][0].highlight= True
                
            displayBoard(window, gameBoard)
            window.refresh()
            pm(window, "Pick an adjacent location to place the purity tile.")
            event = window.read()
            for i in validTargets:
                ix = i[0]
                iy = i[1]
                gameBoard[ix][iy][0].highlight = False
            displayBoard(window, gameBoard)
            window.refresh()
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
                    g[0].purityTile = True
                    

            else:
                sg.popup("Invalid location",keep_on_top=True)
                break
            
# reproduce            
        elif str.find(i,"reproduce") >= 0:
            itemsMenu.Hide()
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
            itemsMenu.Hide()
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
            itemsMenu.Hide()
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
            itemsMenu.Hide()
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
            itemsMenu.Hide()
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
            itemsMenu.Hide()
            pm(window,"This piece can now 'wrap' around the edges of the map to appear on the opposite side.")
            gameBoard[x][y][1].storedItems.remove("round earth theory")
            gameBoard[x][y][1].activeBuffs.append("round earth theory")
            
            
# laser column            
        elif str.find(i, "laser column") >= 0:
            itemsMenu.Hide()
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
            itemsMenu.Hide()
            gameBoard[x][y][1].storedItems.remove("spooky hand")
            sg.popup("A spooky hand has gone under the field.  When will he strike?  Nobody knows...", keep_on_top = True)
            pm(window,"A spooky hand has gone under the field.  When will he strike?  Nobody knows...")
            sleep(1)
            PublicStats.spookyHand = True

# bowling ball
        elif str.find(i, "bowling ball") >= 0:
            
            yesno = sg.popup_yes_no("Warning: using bowling ball will make your piece permanently transform into a rabid bowling ball, and will lose all items and effects. Are you sure you want to use this?",keep_on_top=True)
            itemsMenu.Hide()
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
            itemsMenu.Hide()
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
            itemsMenu.Hide()
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
                    playsound("sounds/getItem.mp3",block=False)
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
                            playsound("sounds/getItem.mp3",block=False)
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
            itemsMenu.Hide()
            highlightValidDistance(gameBoard, window, startLocation, actionType = "enemyHurtOnly", reachType = "radial")
            displayBoard(window, gameBoard)
            window.refresh()
            yesno = sg.popup_yes_no("Use?",keep_on_top=True)
            if yesno == "No":
                continue
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

# trip mine row
        elif str.find(i, "trip mine row") >= 0:
            itemsMenu.Hide()
            highlightValidDistance(gameBoard, window, startLocation, actionType = "enemyHurtOnly", reachType = "row")
            displayBoard(window, gameBoard)
            window.refresh()
            yesno = sg.popup_yes_no("Use?",keep_on_top=True)
            if yesno == "No":
                continue
            
            gameBoard[x][y][1].storedItems.remove("trip mine row")
            validTargets = getRow(location, gameBoard)

            for i in validTargets:
                g = gameBoard[i[0]][i[1]]

                if g[0].occupied == True:

                    if g[1].ownedBy != playerTurn:
                        g[1].activeDebuffs.append("trip mine")
                        pm(window, "Trip mine has been placed")
                        window.refresh()
                        sleep(0.5)
                        # add code for graphics

# trip mine column
        elif str.find(i, "trip mine column") >= 0:
            itemsMenu.Hide()
            highlightValidDistance(gameBoard, window, startLocation, actionType = "enemyHurtOnly", reachType = "column")
            displayBoard(window, gameBoard)
            window.refresh()
            yesno = sg.popup_yes_no("Use?",keep_on_top=True)
            if yesno == "No":
                continue
            validTargets = getColumn(location, gameBoard)

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
            itemsMenu.Hide()
            highlightValidDistance(gameBoard, window, startLocation, actionType = "allHurt", reachType = "column")
            displayBoard(window, gameBoard)
            window.refresh()
            yesno = sg.popup_yes_no("Use?",keep_on_top=True)
            if yesno == "No":
                continue
            gameBoard[x][y][1].storedItems.remove("suicide bomb column")
            # for each item inside the specific gameBoard row
            for j in gameBoard:
                if j[y][0].occupied == True:
                    death = forcefieldCheck(window, gameBoard, endLocation = j[y] ,danger ="both")
                    #if you didn't die, then start looking in a different direction
                    if death == False:
                        continue

                    #if it doesn't have a forcefield
                    else:
                        
                        j[y][0].occupied = False
                        j[y][1] = 0
                        tileBackup = j[y][0].tileType
                        if tileBackup in ("player1default", "player2default"):
                            tileBackup = "default"
                        j[y][0].tileType = "exploding"
                        displayBoard(window, gameBoard)
                        window.refresh()
                        j[y][0].tileType = tileBackup
                        displayBoard(window, gameBoard)
                        window.refresh()
                

# suicide bomb radial
        elif str.find(i, "suicide bomb radial") >= 0:
            itemsMenu.Hide()
            highlightValidDistance(gameBoard, window, startLocation, actionType = "allHurt", reachType = "radial")
            displayBoard(window, gameBoard)
            window.refresh()
            yesno = sg.popup_yes_no("Use?",keep_on_top=True)
            if yesno == "No":
                continue
            
            gameBoard[x][y][1].storedItems.remove("suicide bomb radial")
            validTargets = getRadial((x, y), gameBoard)

            for i in validTargets:
                x = i[0]
                y = i[1]
                
                
                j = gameBoard[x][y]
                if j[0].occupied == True:
                    death = forcefieldCheck(window, gameBoard, endLocation = j ,danger ="both")
                    #if you didn't die, then start looking in a different direction
                    if death == False:
                        continue

                    #if it doesn't have a forcefield
                    else:
                        
                        j[0].occupied = False
                        j[1] = 0
                        tileBackup = j[0].tileType
                        if tileBackup in ("player1default", "player2default"):
                            tileBackup = "default"
                        j[0].tileType = "exploding"
                        displayBoard(window, gameBoard)
                        window.refresh()
                        j[0].tileType = tileBackup
                        displayBoard(window, gameBoard)
                        window.refresh()
                        

# napalm row
        elif str.find(i, "napalm row") >= 0:

            itemsMenu.Hide()
            highlightValidDistance(gameBoard, window, startLocation, actionType = "enemyHurtOnly", reachType = "row")
            displayBoard(window, gameBoard)
            window.refresh()
            yesno = sg.popup_yes_no("Use?",keep_on_top=True)
            if yesno == "No":
                continue
            
            gameBoard[x][y][1].storedItems.remove("napalm row")
            # for each column inside the row
            for j in gameBoard[x]:
                

                    # if there is a piece
                
                    #sg.popup(f"TEST", keep_on_top = True)        
                    if j[0].occupied == True and j[1].ownedBy == enemyTurn:
                        death = forcefieldCheck(window, gameBoard, endLocation = j ,danger ="enemyHurtOnly")
                        #if you didn't die, then start looking in a different direction
                        if death == False:
                            continue

                        #if it doesn't have a forcefield
                        else:
                            
                            j[0].occupied = False
                            j[1] = 0
                            tileBackup = j[0].tileType
                            if tileBackup in ("player1default", "player2default"):
                                tileBackup = "default"
                            j[0].tileType = "exploding"
                            displayBoard(window, gameBoard)
                            window.refresh()
                            j[0].tileType = "default"
                            displayBoard(window, gameBoard)
                            window.refresh()
                            j[0].tileType = "exploding"
                            displayBoard(window, gameBoard)
                            window.refresh()
                            j[0].tileType = "default"
                            displayBoard(window, gameBoard)
                            window.refresh()
                            j[0].tileType = "exploding"
                            displayBoard(window, gameBoard)
                            window.refresh()
                            sleep(.3)
                            j[0].tileType = "destroyed"
                            displayBoard(window, gameBoard)
                            window.refresh()

# napalm column 
        elif str.find(i, "napalm column") >= 0:
            itemsMenu.Hide()
            highlightValidDistance(gameBoard, window, startLocation, actionType = "enemyHurtOnly", reachType = "column")
            displayBoard(window, gameBoard)
            window.refresh()
            yesno = sg.popup_yes_no("Use?",keep_on_top=True)
            if yesno == "No":
                continue
            gameBoard[x][y][1].storedItems.remove("napalm column")
            # for each item inside the specific gameBoard row
            for j in gameBoard:
                if j[y][0].occupied == True and j[y][1].ownedBy == enemyTurn:
                        death = forcefieldCheck(window, gameBoard, endLocation = j[y] ,danger ="enemyHurtOnly")
                        #if you didn't die, then start looking in a different direction
                        if death == False:
                            continue

                        #if it doesn't have a forcefield
                        else:
                            
                            j[y][0].occupied = False
                            j[y][1] = 0
                            tileBackup = j[y][0].tileType
                            if tileBackup in ("player1default", "player2default"):
                                tileBackup = "default"
                            j[y][0].tileType = "exploding"
                            displayBoard(window, gameBoard)
                            window.refresh()
                            j[y][0].tileType = "default"
                            displayBoard(window, gameBoard)
                            window.refresh()
                            j[y][0].tileType = "exploding"
                            displayBoard(window, gameBoard)
                            window.refresh()
                            j[y][0].tileType = "default"
                            displayBoard(window, gameBoard)
                            window.refresh()
                            j[y][0].tileType = "exploding"
                            displayBoard(window, gameBoard)
                            window.refresh()
                            sleep(.3)
                            j[y][0].tileType = "destroyed"
                            displayBoard(window, gameBoard)
                            window.refresh()


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
                            g[1].forceFieldTurn = PublicStats.turnCount
                            continue
                        if g[1].forceFieldTurn == PublicStats.turnCount:
                                backupTile = g[0].tileType
                                g[0].tileType = "exploding"
                                displayBoard(window, gameBoard)
                                window.refresh()
                                sleep(1)
                                g[0].tileType = backupTile
                                sg.popup("A piece was protected by a force field.", keep_on_top = True)
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
            itemsMenu.Hide()
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
            itemsMenu.Hide()
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
            itemsMenu.Hide()
            yesno = sg.popup_yes_no("Using this item will make this piece go berzerk and allow it to eat enemies and allies alike, enraging it and allowing it to attack again after each kill (up to three times per turn), but at the cost of dying if it goes any turns without eating (it stores leftovers from each enemy killed so it can eat on subsequent turns without attacking). Use?",keep_on_top=True)
            if yesno == "No":
                continue
            g = gameBoard
            g[x][y][1].storedItems.remove("berzerk")
            g[x][y][1].activeBuffs.append("berzerk")
            g[x][y][1].berzerkMeatCount = 0
            g[x][y][1].berzerkAttacksLeft = 3
            
# shuffle radial
        elif str.find(i, "shuffle radial") >= 0:
            itemsMenu.Hide()
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


# purify column
        elif str.find(i, "purify column") >= 0:

            itemsMenu.Hide()
            highlightValidDistance(gameBoard, window, startLocation, actionType = "alliesHelpedOnly", reachType = "column")
            displayBoard(window, gameBoard)
            window.refresh()
            yesno = sg.popup_yes_no("Use?",keep_on_top=True)
            if yesno == "No":
                continue
            cleanCheck = False
            gameBoard[x][y][1].storedItems.remove("purify column")


            # for each row in the column
            for rows in gameBoard:
                g = rows[y]
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

                                

# purify row
        elif str.find(i, "purify row") >= 0:

            itemsMenu.Hide()
            highlightValidDistance(gameBoard, window, startLocation, actionType = "alliesHelpedOnly", reachType = "row")
            displayBoard(window, gameBoard)
            window.refresh()
            yesno = sg.popup_yes_no("Use?",keep_on_top=True)
            if yesno == "No":
                continue
            cleanCheck = False
            gameBoard[x][y][1].storedItems.remove("purify row")
            
            # for each column inside the row
            for g in gameBoard[x]:
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
                        

# purify radial
        elif str.find(i, "purify radial") >= 0:

            itemsMenu.Hide()
            highlightValidDistance(gameBoard, window, startLocation, actionType = "alliesHelpedOnly", reachType = "radial")
            displayBoard(window, gameBoard)
            window.refresh()
            yesno = sg.popup_yes_no("Use?",keep_on_top=True)
            if yesno == "No":
                continue
            
            gameBoard[x][y][1].storedItems.remove("purify radial")
            validSpots = getRadial((x, y), gameBoard)
            cleanCheck = False
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
                                sleep(.5)
                                window["information"].update(text_color="white")
                                g[0].tileType = previousTile
                                displayBoard(window, gameBoard)
                                window.refresh()
                                sleep(.5)

            if cleanCheck == False:

                window["information"].update(text_color="red")
                pm(
                    window,
                    f"No corrupted allies were in range. Nothing happened. Well, that was a pointless waste.",
                )
                window.refresh()
                sleep(2)
                window["information"].update(text_color="white")

# move diagonal
        elif str.find(i, "move diagonal") >= 0:
            gameBoard[x][y][1].storedItems.remove("move diagonal")
            gameBoard[x][y][1].activeBuffs.append("move diagonal")

# place mine
        elif str.find(i, "place mine") >= 0:
            itemsMenu.Hide()
            validLocations = getRadial(location, gameBoard)
            validLocations = filterEmpty(gameBoard, validLocations)

            pm(window, "Where would you like to place the mine?")
            event = window.read()
            if (event[0][0], event[0][1]) in validLocations:

                pm(window, f"Mine placed.")
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
            itemsMenu.Hide()
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
            itemsMenu.Hide()
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
            itemsMenu.Hide()
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
            itemsMenu.Hide()
            validTargets = getCross((x, y), gameBoard)
            pm(window, "Pick a target that is within range.")
            event = window.read()

            # if the target is within range
            if event[0] in validTargets:
                
                playsound("sounds/punch.mp3",block=False)
                # s1 is the victim's start row, compare to x
                s1 = event[0][0]

                # s2 is the victim's start column, compare to y
                s2 = event[0][1]
                if gameBoard[s1][s2][0].occupied == False:
                    pm(window, "There's no one to punch at that location!")
                    itemsMenu.Hide()
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
                            if gameBoard[s1 + 1][s2][0].tileType in [PublicStats.damagedFloor]:
                                # kill the piece
                                gameBoard[s1][s2][1] = 0
                                gameBoard[s1][s2][0].tileType = "default"
                                gameBoard[s1][s2][0].occupied = False
                                playsound("sounds/fall.mp3", block = False)
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
                            if gameBoard[s1 - 1][s2][0].tileType in [PublicStats.damagedFloor]:
                                # kill the piece
                                gameBoard[s1][s2][1] = 0
                                gameBoard[s1][s2][0].tileType = "default"
                                gameBoard[s1][s2][0].occupied = False
                                playsound("sounds/fall.mp3", block = False)
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
                            if gameBoard[s1][s2 + 1][0].tileType in [PublicStats.damagedFloor]:
                                # kill the piece
                                gameBoard[s1][s2][1] = 0
                                gameBoard[s1][s2][0].tileType = "default"
                                gameBoard[s1][s2][0].occupied = False
                                playsound("sounds/fall.mp3", block = False)
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
                            if gameBoard[s1][s2 - 1][0].tileType in [PublicStats.damagedFloor]:
                                # kill the piece
                                gameBoard[s1][s2][1] = 0
                                gameBoard[s1][s2][0].tileType = "default"
                                gameBoard[s1][s2][0].occupied = False
                                playsound("sounds/fall.mp3", block = False)
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

# wololo radial
        elif str.find(i, "wololo radial") >= 0:

            
            itemsMenu.Hide()
            highlightValidDistance(gameBoard, window, startLocation, actionType = "enemyHurtOnly", reachType = "radial")
            displayBoard(window, gameBoard)
            window.refresh()
            yesno = sg.popup_yes_no("Use?",keep_on_top=True)
            if yesno == "No":
                continue
            highlightValidDistance(gameBoard, window, startLocation, turnOff=True)
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
                        converted+=1
                        displayBoard(window, gameBoard)
                        sleep(.5)
                        gameBoard[ix][iy][1].ownedBy = player
                        displayBoard(window, gameBoard)
                        window.refresh()
                        sleep(.5)
                        gameBoard[ix][iy][1].ownedBy = enemy
                        displayBoard(window, gameBoard)
                        window.refresh()
                        sleep(.5)
                        gameBoard[ix][iy][1].ownedBy = player
                        displayBoard(window, gameBoard)
                        window.refresh()
                        
            gameBoard[x][y][1].storedItems.remove("wololo radial")

            if converted > 0:
                sg.popup(f"WOLOLO!  You've converted {converted} pieces to your side!", keep_on_top = True)
                pm(window, f"WOLOLO!  You've converted {converted} pieces to your side!")
                
            
            displayBoard(window, gameBoard)
            window.refresh()
            

# wololo row
        elif str.find(i, "wololo row") >= 0:

            
            itemsMenu.Hide()
            highlightValidDistance(gameBoard, window, startLocation, actionType = "enemyHurtOnly", reachType = "row")
            displayBoard(window, gameBoard)
            window.refresh()
            yesno = sg.popup_yes_no("Use?",keep_on_top=True)
            if yesno == "No":
                continue

            gameBoard[x][y][1].storedItems.remove("wololo row")
            highlightValidDistance(gameBoard, window, startLocation, turnOff=True)
            converted = 0
            # for each column inside the row
            for j in gameBoard[x]:
                    # if there is a piece
                    if j[0].occupied == True:

                        # if it's the enemy's piece
                        if j[1].ownedBy != playerTurn:
                            j[1].ownedBy = playerTurn
                            displayBoard(window, gameBoard)
                            window.refresh()
                            sleep(.5)
                            j[1].ownedBy = enemyTurn
                            displayBoard(window, gameBoard)
                            window.refresh()
                            sleep(.5)
                            j[1].ownedBy = playerTurn
                            displayBoard(window, gameBoard)
                            window.refresh()
                            sleep(.5)
                            converted += 1
                            
            if converted > 0:
                sg.popup(f"WOLOLO!  You've converted {converted} pieces to your side!", keep_on_top = True)
                pm(window, f"WOLOLO!  You've converted {converted} pieces to your side!")
                
            if converted == 0:
                sg.popup(f"Your incantation wasn't heart by any enemies.", keep_on_top = True)
                pm(window, f"Your incantation wasn't heart by any enemies.")
                
            displayBoard(window, gameBoard)
            window.refresh()       

# wololo column
        elif str.find(i, "wololo column") >= 0:

            
            itemsMenu.Hide()
            highlightValidDistance(gameBoard, window, startLocation, actionType = "enemyHurtOnly", reachType = "column")
            displayBoard(window, gameBoard)
            window.refresh()
            yesno = sg.popup_yes_no("Use?",keep_on_top=True)
            if yesno == "No":
                continue

            gameBoard[x][y][1].storedItems.remove("wololo column")
            highlightValidDistance(gameBoard, window, startLocation, turnOff=True)
            converted = 0
            # for each row inside the column
            for j in gameBoard:
                # if there is a piece
                if j[y][0].occupied == True:

                    # if it's the enemy's piece
                    if j[y][1].ownedBy != playerTurn:
                        j[y][1].ownedBy = playerTurn
                        displayBoard(window, gameBoard)
                        window.refresh()
                        sleep(.5)
                        j[y][1].ownedBy = enemyTurn
                        displayBoard(window, gameBoard)
                        window.refresh()
                        sleep(.5)
                        j[y][1].ownedBy = playerTurn
                        displayBoard(window, gameBoard)
                        window.refresh()
                        sleep(.5)
                        converted += 1
                            
            if converted > 0:
                sg.popup(f"WOLOLO!  You've converted {converted} pieces to your side!", keep_on_top = True)
                pm(window, f"WOLOLO!  You've converted {converted} pieces to your side!")
                
            if converted == 0:
                sg.popup(f"Your incantation wasn't heart by any enemies.", keep_on_top = True)
                pm(window, f"Your incantation wasn't heart by any enemies.")
            displayBoard(window, gameBoard)
            window.refresh()

# AI bomb
        elif str.find(i, "AI bomb") >= 0:
            itemsMenu.Hide()
            emptyList = emptySpots(gameBoard, True)
            if len(emptyList) == 0:
                sg.popup("There's no empty space for the AI bomb.  Aborting.", keep_on_top = True)
                continue
            else:
                bombLocation = random.choice(emptyList)
                x1 = bombLocation[0]
                y1 = bombLocation[1]
                gameBoard[x1][y1][0].tileType = "AI bomb"
                sg.popup("An AI bomb was airdropped onto the field. It'll walk around and may explode randomly by any player piece.", keep_on_top = True)
                gameBoard[x][y][1].storedItems.remove( "AI bomb")
                continue

            

# haphazard airstrike
        elif str.find(i, "haphazard airstrike") >= 0:

            gameBoard[x][y][1].storedItems.remove("haphazard airstrike")
            i = 5
            itemsMenu.Hide()
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
                        sg.popup("A piece was protected by a forcefield.", keep_on_top = True)
                        continue
                    elif gameBoard[x][y][1].forceFieldTurn == PublicStats.turnCount:
                        backupTile = gameBoard[x][y][0].tileType
                        gameBoard[x][y][0].tileType = "exploding"
                        displayBoard(window, gameBoard)
                        window.refresh()
                        sleep(1)
                        gameBoard[x][y][0].tileType = backupTile
                        sg.popup("A piece was protected by a forcefield.", keep_on_top = True)
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
            itemsMenu.Hide()
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
                        itemsMenu.Hide()
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
                        sg.popup("A piece was protected by a forcefield.", keep_on_top = True)
                        continue
                    elif gameBoard[x][y][1].forceFieldTurn == PublicStats.turnCount:
                        backupTile = gameBoard[x][y][0].tileType
                        gameBoard[x][y][0].tileType = "exploding"
                        displayBoard(window, gameBoard)
                        window.refresh()
                        sleep(1)
                        gameBoard[x][y][0].tileType = backupTile
                        gameBoard[x][y][1].activeBuffs.remove("Energy Forcefield")
                        sg.popup("A piece was protected by a forcefield.", keep_on_top = True)
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
            itemsMenu.Hide()
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
            return
        
        if event[0] == "CANCEL":
            itemsMenu.close()
            return
