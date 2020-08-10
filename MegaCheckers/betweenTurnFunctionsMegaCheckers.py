# imported by megaCheckers

import PySimpleGUI as sg
from playsound import playsound


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
