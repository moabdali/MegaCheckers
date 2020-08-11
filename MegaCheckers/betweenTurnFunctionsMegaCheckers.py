# imported by megaCheckers

import PySimpleGUI as sg
from playsound import playsound
import random
from useItemsMegaCheckers import *

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

        
def berzerkFunction(window, gameBoard, playerTurn):
    for i in gameBoard:
        for j in i:
            if j[0].occupied == True and j[1].ownedBy == playerTurn and "berzerk" in j[1].activeBuffs:
                j[1].berzerkMeatCount -= 1
                
                j[1].berzerkAttacksLeft = 3
                if j[1].berzerkMeatCount < 0:
                    
                    sg.popup("Your berzerk piece died of hunger.  Being berzerk is energy intensive!", keep_on_top = True)
                    pm(window, "Your berzerk piece died of hunger.  Being berzerk is energy intensive!")
                    playsound("sounds\destroy.wav",block=False)
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
