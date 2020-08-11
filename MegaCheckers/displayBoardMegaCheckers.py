# imported by useItemsMegaCheckers --> megaCheckers


import PySimpleGUI as sg
import random
import string
from PIL import Image
from io import BytesIO
import base64
from playsound import playsound
from highlightsAndDistancesMegaCheckers import *


def damageCheck(window, gameBoard, tileCheck):
    x = tileCheck[0]
    y = tileCheck[1]
    g = gameBoard[x][y]
    if g[0].occupied == True:
        if g[1].forceFieldTurn == PublicStats.turnCount:
            return
        if "Energy Forcefield" in g[1].activeBuffs:
            g[1].activeBuffs.remove("Energy Forcefield")
            g[1].forceFieldTurn = PublicStats.turnCount
            displayBoard(window, gameBoard)
            window.refresh()
            return
    
    g[0].tileType = "exploding"
    displayBoard(window,gameBoard)
    window.refresh()
    g[0].occupied = False
    g[1] = 0
    g[0].tileType = "destroyed"
    displayBoard(window,gameBoard)
    window.refresh()
    return


#enemyOnly, both, alliesOnly
#death = forcefieldCheck(window, gameBoard, endLocation = ,danger =""
def forcefieldCheck(window, gameBoard, startLocation = 0, endLocation = 0, danger = "both"):
    g = endLocation
    #gs = gameBoard[startLocation[0]][startLocation[1]]
    #if g[0].horiLaser or g[0].vertLaser or g[0].crossLaser or g[0].tileType == "mine":
    #if g[0].horiLaser or g[0].vertLaser or g[0].crossLaser or g[0].tileType == "mine" or (g[0].occupied == True and g[1].ownedBy != playerTurn and "dead man's trigger" in g[0].activeBuffsList):
    playerTurn = 0
    enemyTurn = 0
    if PublicStats.turnCount%2 == 0:
        playerTurn = 2
        enemyTurn = 1
    elif PublicStats.turnCount%2!=0:
        playerTurn = 1
        enemyTurn = 2

    
    #only dangerous to the enemy

    #if there's a piece, and we're only hitting enemies, and the piece is an enemy:
    if g[0].occupied == True and (danger == "enemyOnly" or danger == "enemyHurtOnly")and g[1].ownedBy == enemyTurn:
        if g[1].forceFieldTurn == PublicStats.turnCount:
            #sg.popup("A forcefield is still active until the end of this turn.  It has saved you again.",keep_on_top=True)
            return False
        elif "Energy Forcefield" in g[1].activeBuffs:
            g[1].forceFieldTurn = PublicStats.turnCount
            g[1].activeBuffs.remove("Energy Forcefield")
            #sg.popup("The forcefield activated and will protect you from energy until the end of this turn",keep_on_top=True)
            return False
        else:
            #DEATH
            return True
        
    #dangerous to both

    #if there's a piece
    elif g[0].occupied == True and danger == "both":
        if g[1].forceFieldTurn == PublicStats.turnCount:
            #sg.popup("A forcefield is still active until the end of this turn.  It has saved you again.",keep_on_top=True)
            return False
        elif "Energy Forcefield" in g[1].activeBuffs:
            g[1].forceFieldTurn = PublicStats.turnCount
            g[1].activeBuffs.remove("Energy Forcefield")
            #sg.popup("The forcefield activated and will protect you from energy until the end of this turn",keep_on_top=True)
            return False
        else:
            #DEATH
            return True    

    #dangerous only to yourself
    elif g[0].occupied == True and g[1].ownedBy == playerTurn and (danger == "alliesOnly" or danger == "alliesHurtOnly"):
        if g[1].forceFieldTurn == PublicStats.turnCount:
            #sg.popup("A forcefield is still active until the end of this turn.  It has saved you again.",keep_on_top=True)
            return False
        elif "Energy Forcefield" in g[1].activeBuffs:
            g[1].forceFieldTurn = PublicStats.turnCount
            g[1].activeBuffs.remove("Energy Forcefield")
            #sg.popup("The forcefield activated and will protect you from energy until the end of this turn",keep_on_top=True)
            return False
        else:
            #DEATH
            return True
    else:
        return True

    
def laserCheck(window, gameBoard, resetOnly = False, laserSoundCheck = False):
    rows = len(gameBoard)
    columns = len(gameBoard[0])
    killedPiecesPlayer1 = 0
    killedPiecesPlayer2 = 0
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
                            

                            #enemyOnly, both, alliesOnly
                            
                            death = forcefieldCheck(window, gameBoard, endLocation = gameBoard[indexI][left] ,danger ="both")
                            #if you didn't die, then start looking in a different direction
                            if death == False:
                                break



                            #if it doesn't have a forcefield
                            else:
                                owner = gameBoard[indexI][left][1].ownedBy
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
                                sg.popup(f"The laser killed a piece owned by player {owner}.",keep_on_top=True)

                                if gameBoard[indexI][left][0].tileType == "horiLaserTripod":
                                    gameBoard[indexI][left][0].horiLaser = False
                                else:
                                    #laser sound
                                    #if laserSoundCheck == True:
                                    #    playsound("sounds/laser.mp3", block = False)
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
                                
                                #laser sound
                                #if laserSoundCheck == True:
                                #        playsound("sounds/laser.mp3", block = False)
                                gameBoard[indexI][left][0].horiLaser = True
                                if gameBoard[indexI][left][0].vertLaser == True:
                                    gameBoard[indexI][left][0].crossLaser = True


                    #RIGHT CHECK as long as we haven't gone past the right wall
                    while right < columns-1:
                        
                        right += 1
                       


                        #if there's a piece to the right
                        if gameBoard[indexI][right][0].occupied == True:


                            death = forcefieldCheck(window, gameBoard, endLocation = gameBoard[indexI][right] ,danger ="both")
                            #if you didn't die, then start looking in a different direction
                            if death == False:
                                break

                                

                            #if there isn't a forcefield on the piece
                            else:
                                owner = gameBoard[indexI][right][1].ownedBy
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
                                sg.popup(f"The laser killed a piece owned by player {owner}.",keep_on_top=True)
                                if gameBoard[indexI][right][0].tileType in ("horiLaserTripod","vertLaserTripod"):
                                    gameBoard[indexI][right][0].horiLaser = False
                                else:
                                    #laser sound
                                    #if laserSoundCheck == True:
                                    #    playsound("sounds/laser.mp3", block = False)
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
                                #laser sound
                                #if laserSoundCheck == True:
                                #        playsound("sounds/laser.mp3", block = False)
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
                            
                            death = forcefieldCheck(window, gameBoard, endLocation = gameBoard[up][indexJ] ,danger ="both")
                            #if you didn't die, then start looking in a different direction
                            if death == False:
                                break
                            
                            else:
                                owner = gameBoard[up][indexJ][1].ownedBy
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
                                sg.popup(f"The laser killed a piece owned by player {owner}.",keep_on_top=True)

                                
                                if gameBoard[up][indexJ][0].tileType in( "horiLaserTripod" , "vertLaserTripod"):
                                    gameBoard[up][indexJ][0].vertLaser = False
                                    gameBoard[up][indexJ][0].horiLaser = False
                                    gameBoard[up][indexJ][0].crossLaser = False
                                else:
                                    #laser sound
                                    #if laserSoundCheck == True:
                                    #    playsound("sounds/laser.mp3", block = False)
                                    gameBoard[up][indexJ][0].vertLaser = True
                                    
                                displayBoard(window, gameBoard)
                                window.refresh()
                        else:
                            
                            if gameBoard[up][indexJ][0].tileType in ("horiLaserTripod" , "vertLaserTripod"):
                                gameBoard[up][indexJ][0].vertLaser = False
                                gameBoard[up][indexJ][0].horiLaser = False
                                gameBoard[up][indexJ][0].crossLaser = False
                            else:
                                #laser sound
                                #if laserSoundCheck == True:
                                #        playsound("sounds/laser.mp3", block = False)
                                gameBoard[up][indexJ][0].vertLaser = True
                                if gameBoard[up][indexJ][0].horiLaser == True:
                                    gameBoard[up][indexJ][0].crossLaser = True
                    
                    while down < rows-1:
                        
                        down += 1
                       


                        #if there's a piece bottom
                        if gameBoard[down][indexJ][0].occupied == True:




                            death = forcefieldCheck(window, gameBoard, endLocation = gameBoard[down][indexJ] ,danger ="both")
                            #if you didn't die, then start looking in a different direction
                            if death == False:
                                break

                                
                            

                            #if there isn't a forcefield on the piece
                            else:
                                owner = gameBoard[down][indexJ][1].ownedBy
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
                                sg.popup(f"The laser killed a piece owned by player {owner}.",keep_on_top=True)
                                if gameBoard[down][indexJ][0].tileType in ( "horiLaserTripod" , "vertLaserTripod"):
                                    gameBoard[down][indexJ][0].vertLaser = False
                                    gameBoard[down][indexJ][0].horiLaser = False
                                    gameBoard[down][indexJ][0].crossLaser = False
                                else:
                                    #laser sound
                                    #if laserSoundCheck == True:
                                    #    playsound("sounds/laser.mp3", block = False)
                                    gameBoard[down][indexJ][0].vertLaser = True
                                displayBoard(window, gameBoard)
                                window.refresh()
                        #if there isn't a piece there
                        else:
                            if gameBoard[down][indexJ][0].tileType in ("horiLaserTripod" , "vertLaserTripod"):
                                gameBoard[down][indexJ][0].vertLaser = False
                            else:
                                #laser sound
                                #if laserSoundCheck == True:
                                #        playsound("sounds/laser.mp3", block = False)
                                gameBoard[down][indexJ][0].vertLaser = True
                                if gameBoard[up][indexJ][0].horiLaser == True:
                                    gameBoard[up][indexJ][0].crossLaser = True
                    left = indexJ
                    right = indexJ
                    up = indexI
                    down = indexI
                        
        return

    
def disableEverything(window, turnOn = False):
    if turnOn == False:
        window["exit"].update(disabled = True)
        #window["itemButton"].update(disabled=True)
        window["examineItem"].update(disabled=True)
        ###window["readItems"].update(disabled=True)
        window["cheetz"].update(disabled=True)
        window["Read Items"].update(disabled=True)
    else:
        window["exit"].update(disabled = False)
        #window["itemButton"].update(disabled=False)
        window["examineItem"].update(disabled=False)
        ###window["readItems"].update(disabled=False)
        window["cheetz"].update(disabled=False)
        window["Read Items"].update(disabled=False)
        
# print out messages to both the window and console
def pm(window, message):
    window["information"].update(message)
    print(message)
    
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
            if gameBoard[i][j][0].tileType == "AI bomb":
                cleanTile(gameBoard[i][j][0])
                avatarFunction(window, PublicPNGList[41], gameBoard, i, j)
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
                avatar.paste(wormHole2, (0, 0), wormHole2)
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
                        window[i, j].update(image_filename="images/recall.png")
                        
                    #if the mouse is here
                    if gameBoard[i][j][0].orbEater == True:
                        avatarFunction(window, PublicPNGList[10], gameBoard, i, j)
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
                    avatarFunction(window, PublicPNGList[3], gameBoard, i, j)
                    continue

                if gameBoard[i][j][0].tileType == "vertLaserTripod":
                    avatarFunction(window, PublicPNGList[9], gameBoard, i, j)
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
                        
                    if "grappling hook" in g.activeBuffs:
                        grapple = (PublicPNGList[40]).convert("RGBA")
                        avatar.paste(grapple, (0,0), grapple)
                        avatarFunction(window, avatar, gameBoard, i,j)
                        
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
                        
                    if g.forceFieldTurn == PublicStats.turnCount:
                        forcefieldBig = Image.open("images/forcefieldBig.png").convert("RGBA")
                        avatar.paste(forcefieldBig, (0, 0), forcefieldBig)

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

                    if g.berzerkMeatCount == 1:
                        meat1 = Image.open("images/meat1.png").convert("RGBA")
                        avatar.paste(meat1, (0, 0), meat1)
                    elif g.berzerkMeatCount == 2:
                        meat2 = Image.open("images/meat2.png").convert("RGBA")
                        avatar.paste(meat2, (0, 0), meat2)
                    elif g.berzerkMeatCount >= 3:
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


            


