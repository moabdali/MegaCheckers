import PySimpleGUI as sg
import copy
import math
import random
from time import sleep



class PublicStats:
    
    turnCount = 1
    cycle = 0
    orbCycleList = [5,10,0,0,3,1,0,2,1]
    def getOrbCount(self):
        
        cycle = PublicStats.turnCount%9
        return PublicStats.orbCycleList[cycle]
                
class Piece:
    def __init__(self,row = None,column = None,playerTurn = None):
        #where the piece is currently residing
        self.location = (row,column)
        #what bonuses the player has
        self.activeBuffs = []
        #what maluses the player has
        self.activeDebuffs = []
        #what the player is holding (need a max; 5?)
        self.storedItems = []
        #what it looks like
        #self. avatar = f".//player{playerTurn}default.png"
        self. avatar = "default"
        self.ownedBy = playerTurn
        self.distanceMax = 1
        self.grey = False

    def determineAvatar(self):

        #if you have a shield
        if "Energy Forcefield" in self.activeBuffs:
            #and holding an item
            if len(self.storedItems)>0:
                #shield + item
                self.avatar = "shIt"
            else:
                #just shield
                self.avatar = "sh"
        #if you don't have a shield
        else:
            # if you have items
            if len(self.storedItems )>0:
                #items only
                self.avatar = f"player{self.ownedBy}stored"
            else:
                #nothing at all
                self. avatar = "default"

    
    
class Tile:
    def __init__(self, occupied = False):
        self.tileHeight = 0
        self.tileType = "default"
        self.occupied = occupied
    def describeSelf(self):
        
        if self.tileType == "default":
            sg.popup(f"This is a regular tile with an elevation of {self.tileHeight}",keep_on_top=True)
            return
        elif self.tileType == "itemOrb":
            sg.popup(f"This is an item orb tile with an elevation of {self.tileHeight}",keep_on_top=True)
            return
        elif self.tileType == "destroyed":
            sg.popup(f"This tile has been destroyed!  But don't worry, it'll come back in 5 turns.",keep_on_top=True)
            return
        elif self.tileType == "damaged4":
            sg.popup(f"This tile is being repaired.  It'll be ready for business in 4 turns.",keep_on_top=True)
            return
        elif self.tileType == "damaged3":
            sg.popup(f"This tile is being repaired.  It'll be up and at 'em in 3 turns.",keep_on_top=True)
            return
        elif self.tileType == "damaged2":
            sg.popup(f"This tile is being repaired.  It'll be repaired in 2 turns.",keep_on_top=True)
            return
        elif self.tileType == "damaged":
            sg.popup(f"This tile is almost ready!  It'll be ready on the next turn!",keep_on_top=True)
            return
        elif self.tileType == "boobyTrap":
            sg.popup(f"There's an obvious booby trap on this tile.  Don't move here without protection! It has an elevation of {self.tileHeight}",keep_on_top=True)
            return

def getColumn(location, gameBoard, grow = False):
    validLocations = []
    if grow == False:
        for i in range(len( gameBoard ) ):
            validLocations.append( i,location[1])
    return validLocations

def getRow(location, gameBoard):
    validLocations = []
    if grow == False:
        for i in range(len( gameBoard[0] ) ):
            validLocations.append( location[0],i)
    return validLocations

def getRadial(location, gameBoard, grow = False):
    validLocations = []
    rows = len(gameBoard)
    columns = len(gameBoard[0])
    
    if grow == False:
        #check if you can go one row up
        if location[0]-1 != -1:
            #check if you can also go left after going up (only false if you're in the top left corner)
            if location[1]-1 != -1:
                validLocations.append( (location[0]-1,location[1]-1) )
            #one row up (guaranteed already)
            validLocations.append( (location[0]-1,location[1]+0) )
            #check if you can also go right after going up (only false if you're in the top right corner)
            if location[1]+1 != columns:
                validLocations.append( (location[0]-1,location[1]+1) )
        #check if you can go left
        if location[1]-1 != -1:
            validLocations.append( (location[0],location[1]-1) )
        #you are guaranteed to append yourself
        validLocations.append( (location[0],location[1]) )
        #check if you can go right
        if location[1]+1 != columns:
            validLocations.append( (location[0],location[1]+1) )
        #check if you can go down
        if location[0]+1 != rows:
            #check bottom left
            if location[1]-1 != -1:
                validLocations.append( (location[0]+1,location[1]-1) )
            #bottom guaranteed
            validLocations.append( (location[0]+1,location[1]) )
            #check bottom right
            if location[1]+1 != columns:
                validLocations.append( (location[0]+1,location[1]+1) )
    return validLocations

       
def initializeField(columns,rows,window,gameBoard):
    
    for i in range(2):
        for j in range(columns): 
            #window[i,j].update(image_filename="player1default.png")
            gameBoard[i][j][0]=Tile(occupied=True)
            
            piece = Piece(playerTurn = 1)
            gameBoard[i][j][1]=piece
            gameBoard[i][j][1].location = (i,j)
            gameBoard[i][j][0].tileType = "player1default"
            gameBoard[i][j][1].avatar = "default"
            
            
    for i in range(2):
        for j in range(columns):
            #window[rows-i-1,j].update(image_filename="player2default.png")
            gameBoard[rows-i-1][j][0]=Tile(occupied=True)
            piece = Piece(playerTurn = 2)
            
            gameBoard[rows-i-1][j][1]=piece
            gameBoard[rows-i-1][j][1].location = (rows-i-1,j)
            gameBoard[rows-i-1][j][0].tileType = "player2default"
            gameBoard[rows-i-1][j][1].avatar = "default"
    



def countPieces(gameBoard,window):
    player1count = 0
    player2count = 0
    
    for i in gameBoard:
        for j in i:
            
            if j[1] != 0:
                
                if j[1].ownedBy == 1:
                    
                    player1count+=1
                elif j[1].ownedBy == 2:
                    player2count+=1
                    
    
    window['player1piececount'].update(f"Player 1 controls: {player1count}\n")
    window['player2piececount'].update(f"Player 2 controls: {player2count}\n")
    window.refresh()

def gamePlay(playerTurn, window, gameBoard):
    
        countPieces(gameBoard,window)
        createOrbs(window,gameBoard)
        displayBoard(window,gameBoard)
        movePiece(playerTurn, window,gameBoard)
        PublicStats.turnCount += 1
        repairFloor(window,gameBoard)
        
        
        


def getDistance(a,b,c,d):
    verticalDistance = abs(c-a)
    horizontalDistance = abs(d-b)
    distance = verticalDistance + horizontalDistance
    return distance

def createOrbs(window,gameBoard):
    emptySpots = 0
    for i in gameBoard:
        for j in i:
                if j[0].tileType == "default":
                    emptySpots+=1
    publicStats = PublicStats()
    orbsToPlace = publicStats.getOrbCount()

    if orbsToPlace > emptySpots:
        orbsToPlace = emptySpots

    while orbsToPlace > 0:
        i = random.randint(0,len(gameBoard)-1)
        j = random.randint(0,len(gameBoard[0])-1)
        
        
            
        if gameBoard[i][j][0].tileType == "default":
            orbsToPlace -= 1
            
            gameBoard[i][j][0].tileType = "itemOrb"
    
    

        
def displayBoard(window,gameBoard):
    
    for i in range(len(gameBoard)):

        for j in range(len(gameBoard[0])):

            if gameBoard[i][j][0].tileType == "exploding":
                window[i,j].update(image_filename="exploding.png")
                
            if gameBoard[i][j][0].tileType == "damaged4":
                window[i,j].update(image_filename="damaged4.png")
                
            if gameBoard[i][j][0].tileType == "damaged3":
                window[i,j].update(image_filename="damaged3.png")

            if gameBoard[i][j][0].tileType == "damaged2":
                window[i,j].update(image_filename="damaged2.png")

            if gameBoard[i][j][0].tileType == "damaged":
                window[i,j].update(image_filename="damaged.png")
    
            
            if gameBoard[i][j][0].occupied == False:
                
                if gameBoard[i][j][0].tileType == "default":
                    window[i,j].update(image_filename="blank.png")
                        
                    
                elif gameBoard[i][j][0].tileType == "itemOrb":
                    window[i,j].update(image_filename="itemOrb.png")

                elif gameBoard[i][j][0].tileType == "destroyed":
                    window[i,j].update(image_filename="destroyed.png")
            else:
                if gameBoard[i][j][0].occupied:
                    gameBoard[i][j][1].determineAvatar()
                    
                    if gameBoard[i][j][1].avatar=="default":
                        
                        window[i,j].update(image_filename=f"player{gameBoard[i][j][1].ownedBy}default.png")
                        if gameBoard[i][j][1].grey == True:
                            window[i,j].update(image_filename=f"Gplayer{gameBoard[i][j][1].ownedBy}default.png")
                    elif gameBoard[i][j][1].avatar==f"player{gameBoard[i][j][1].ownedBy}stored":
                        window[i,j].update(image_filename=f"player{gameBoard[i][j][1].ownedBy}stored.png")
                        if gameBoard[i][j][1].grey == True:
                            window[i,j].update(image_filename=f"Gplayer{gameBoard[i][j][1].ownedBy}stored.png")
                    elif gameBoard[i][j][1].avatar==f"shIt":
                        window[i,j].update(image_filename=f"Gp{gameBoard[i][j][1].ownedBy}shIt.png")
                        if gameBoard[i][j][1].grey == True:
                            window[i,j].update(image_filename=f"Gp{gameBoard[i][j][1].ownedBy}shIt.png")
                    elif gameBoard[i][j][1].avatar==f"sh":
                        window[i,j].update(image_filename=f"p{gameBoard[i][j][1].ownedBy}sh.png")
                        if gameBoard[i][j][1].grey == True:
                            window[i,j].update(image_filename=f"p{gameBoard[i][j][1].ownedBy}sh.png")
                    
                

                    
def pickUpItemOrb(gameBoard,x,y):
    #items = ["suicideBomb Row","Energy Forcefield","suicideBomb Column","Haphazard Airstrike","suicideBomb Radial","jumpProof"]
    items = ["suicideBomb Row","Energy Forcefield","suicideBomb Column","Haphazard Airstrike","suicideBomb Radial","jumpProof"]
    

    
    randItem = random.choice(items)
    gameBoard[x][y][1].storedItems.append(randItem)
    playerOwned = gameBoard[x][y][1].ownedBy
    gameBoard[x][y][1].avatar = f"player{playerOwned}stored"
    




def useItems(gameBoard,x,y,window):
    layout = []
    for i in gameBoard[x][y][1].storedItems:
        layout+= [ [sg.Button(i)] ]
    layout+= [ [sg.Button("CANCEL")] ]
    itemsMenu = sg.Window("Items Menu", layout,disable_close=True )

    while True:
            event = itemsMenu.read()
            i = event[0]

            if i == None:
                break
            
            #suicidebomb row
            if str.find(i,"suicideBomb Row")>=0:
                gameBoard[x][y][1].storedItems.remove("suicideBomb Row")
                #for each item inside the specific gameBoard row
                for j in gameBoard[x]:
                    if isinstance(j[1],Piece):
                        if "Energy Forcefield" in j[1].activeBuffs:
                            
                            j[1].activeBuffs.remove("Energy Forcefield")
                            
                        else:   
                            #set the tile to be empty
                            j[0].occupied = False
                            j[1] = 0
                            j[0].tileType = "default"


            #suicidebomb column
            elif str.find(i,"suicideBomb Column")>=0:
                gameBoard[x][y][1].storedItems.remove("suicideBomb Column")
                #for each item inside the specific gameBoard row
                for j in gameBoard:
                    if isinstance(j[y][1],Piece):
                        if "Energy Forcefield" in j[y][1].activeBuffs:
                            
                            j[y][1].activeBuffs.remove("Energy Forcefield")
                            
                        else:   
                            #set the tile to be empty
                            j[y][0].occupied = False
                            j[y][1] = 0
                            j[y][0].tileType = "default"
                            
            #suicidebomb radial
            elif str.find(i,"suicideBomb Radial") >=0:
                gameBoard[x][y][1].storedItems.remove("suicideBomb Radial")
                validTargets = getRadial((x,y),gameBoard)
                
                
                for i in validTargets:
                    x = i[0]
                    y = i[1]
                    
                    if isinstance(gameBoard[x][y][1],Piece):
                        if "Energy Forcefield" in gameBoard[x][y][1].activeBuffs:
                            
                            gameBoard[x][y][1].activeBuffs.remove("Energy Forcefield")
                            
                        else:   
                            #set the tile to be empty
                            gameBoard[x][y][0].occupied = False
                            gameBoard[x][y][1] = 0
                            gameBoard[x][y][0].tileType = "default"
                            
            #energy forcefield
            elif str.find(i,"Energy Forcefield")>=0:
                gameBoard[x][y][1].storedItems.remove("Energy Forcefield")
                gameBoard[x][y][1].activeBuffs.append("Energy Forcefield")
                displayBoard(window, gameBoard)

            #jump proof
            elif str.find(i,"jumpProof")>=0:
                gameBoard[x][y][1].storedItems.remove("jumpProof")
                gameBoard[x][y][1].activeBuffs.append("jumpProof")
                displayBoard(window, gameBoard)
                
                
            #wololo
            elif str.find(i,"Wololo (convert to your side)") >=0:
                    itemsMenu.close()
                    
                    window["information"].update("Choose an enemy to recruit")
                    
                    event = window.read()
                    player = gameBoard[x][y][1].ownedBy
                    if player == 1:
                        enemy = 2
                    elif player == 2:
                        enemy = 1
                    if gameBoard[event[0][0]][event[0][1]][1] == 0:
                        window["information"].update("Choose an enemy, not a vacant tile...")
                        sleep(1)
                        continue
                    elif gameBoard[event[0][0]][event[0][1]][1].ownedBy == enemy:
                        gameBoard[event[0][0]][event[0][1]][1].ownedBy = player
                        gameBoard[x][y][1].storedItems.remove("Wololo (convert to your side)")
                    else:
                        window["information"].update("Wololo only works on enemies.")
                        sleep(1)
                    displayBoard(window, gameBoard)
                    window.refresh()
                    

            elif str.find(i,"Haphazard Airstrike") >=0:
                
                gameBoard[x][y][1].storedItems.remove("Haphazard Airstrike")
                i = 5
                itemsMenu.close()
                while (i > 0):
                    i-=1
                    
                    x = random.randint(0,len(gameBoard)-1)
                    y = random.randint(0,len(gameBoard[0])-1)
                    
                    #if someone is on the spot
                    if gameBoard[x][y][0].occupied == True:
                        #if someone has a forcefield there, don't kill them
                        if "Energy Forcefield" in gameBoard[x][y][1].activeBuffs:
                            
                           
                            backupTile = gameBoard[x][y][0].tileType
                            gameBoard[x][y][0].tileType = "exploding"
                            displayBoard(window,gameBoard)
                            window.refresh()
                            sleep(1)
                            gameBoard[x][y][0].tileType = backupTile
                            gameBoard[x][y][1].activeBuffs.remove("Energy Forcefield")
                            continue
                        else:
                            gameBoard[x][y][0].occupied = False
                            gameBoard[x][y][1] = 0
                            gameBoard[x][y][0].tileType = "exploding"
                            displayBoard(window,gameBoard)
                            window.refresh()
                            sleep(1)
                            gameBoard[x][y][0].tileType = "destroyed"
                            continue
                            
                    else:
                        
                        
                        gameBoard[x][y][0].occupied = False
                        gameBoard[x][y][1] = 0
                        gameBoard[x][y][0].tileType = "exploding"
                        displayBoard(window,gameBoard)
                        window.refresh()
                        sleep(1)
                        gameBoard[x][y][0].tileType = "destroyed"


                



                
            if itemsMenu:    
                itemsMenu.close()
            return
            if event[0] == "CANCEL":
                itemsMenu.close()
                return
        
def repairFloor (window, gameBoard):
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
    
        




def movePiece(playerTurn, window, gameBoard):
    while True:
        displayBoard(window, gameBoard)
        window["exit"].update(disabled = False)
        usedItem = False
        #sg.popup_timed(f" It's player {playerTurn}'s turn.",font = "Cambria, 20",auto_close_duration=1)
        window["itemButton"].update(disabled = True)
        window["examineItem"].update(disabled = False)
        window.refresh()
        sleep(1.25)
        window['playerTurn'].update(f"{playerTurn}")
        window['information'].update(f"Pick a piece to move.")
        event = window.read()
        window["exit"].update(disabled = False)
        if "exit" in event:
            a = sg.popup_yes_no("Seriously, you want to exit this awesome game?",keep_on_top=True)
            if a == "Yes":
                sg.popup("Wow, your loss.",keep_on_top=True)
                window.close()
                raise SystemExit
            else:
                continue
        window["exit"].update(disabled = True)


        if "examineItem" in event:
            window["examineItem"].update(disabled = True)
            window['information'].update(f"What do you want to examine?",text_color = "red")
            event = window.read()

            
            #if no pieces exist here:
            if gameBoard[event[0][0]][event[0][1]][0].occupied == False:
                gameBoard[event[0][0]][event[0][1]][0].describeSelf()

            #if there is a piece:
            else:
                if playerTurn == gameBoard[event[0][0]][event[0][1]][1].ownedBy:
                    owner = "you"
                else:
                    owner = "your opponent"
                buffslist =""
                debuffslist = ""
                for i in gameBoard[event[0][0]][event[0][1]][1].activeBuffs:
                    buffslist += i + "\n"
                for i in gameBoard[event[0][0]][event[0][1]][1].activeDebuffs:
                    debuffslist += i + "\n"
                if buffslist == "":
                    buffslist = "NONE"
                if debuffslist == "":
                    debuffslist = "NONE"
                sg.popup(f"The piece here belongs to {owner}.\nIt currently holds {len(gameBoard[event[0][0]][event[0][1]][1].storedItems)} inactive items.\nIt has the following buffs:\n{buffslist}\nIt has the current debuffs:\n{debuffslist}",keep_on_top=True)
            window["examineItem"].update(disabled = False)
            continue


            
        window["itemButton"].update(disabled = False)
        window["examineItem"].update(disabled = True)
                
        
        startLocation = event[0]
        
        

        
        window['information'].update(f"Selection made, pick destination.")

        if gameBoard[startLocation[0]][startLocation[1]][1] != 0:
            gameBoard[startLocation[0]][startLocation[1]][1].grey = True



        displayBoard(window,gameBoard)
        event = window.read()
        
        window["examineItem"].update(disabled = True)
        endLocation = event[0]

        

        
        
        if ("itemButton" in event and gameBoard[ startLocation[0] ] [ startLocation[1] ] [0].occupied == True) or (startLocation == endLocation and gameBoard[ startLocation[0] ] [ startLocation[1] ] [0].occupied == True):
            
            
            if len(gameBoard[ startLocation[0] ] [ startLocation[1] ] [1].storedItems) > 0 and (gameBoard[ startLocation[0] ] [ startLocation[1] ] [1].ownedBy == playerTurn):
                
                useItems(gameBoard,startLocation[0],startLocation[1],window)
                
                
                if gameBoard[startLocation[0]][startLocation[1]][0].occupied == True:
                    gameBoard[startLocation[0]][startLocation[1]][1].grey = False
                countPieces(gameBoard,window)
                displayBoard(window,gameBoard)
                continue
            
            elif gameBoard[ startLocation[0] ] [ startLocation[1] ] [1].ownedBy != playerTurn:
                gameBoard[ startLocation[0] ] [ startLocation[1] ] [1].grey = False
                sg.popup("That's not your piece.",keep_on_top=True)
                continue

            elif len(gameBoard[ startLocation[0] ] [ startLocation[1] ] [1].storedItems )< 1:
                gameBoard[ startLocation[0] ] [ startLocation[1] ] [1].grey = False
                sg.popup("No items on this piece.",keep_on_top=True)
                continue
            
            else:
                sg.popup("An error occured in item lookups",keep_on_top=True)
        

        
        if (gameBoard[ startLocation[0] ] [ startLocation[1] ] [0].occupied == False ):
            window['information'].update(f"Nothing exists on the initial square!")
            window.refresh
            continue

        if gameBoard[startLocation[0]][startLocation[1]][1] != 0:
            gameBoard[startLocation[0]][startLocation[1]][1].grey = False
        displayBoard(window,gameBoard)    
            
        
        #if the spot you're moving from contains a piece
        if( gameBoard[ startLocation[0] ] [ startLocation[1] ] [0] .occupied):
            #if the piece is yours
            if (gameBoard[ startLocation[0] ] [ startLocation[1] ][1].ownedBy == playerTurn):


                #if it's too far
                if getDistance(startLocation[0],startLocation[1],endLocation[0],endLocation[1]) >  gameBoard[ startLocation[0] ] [ startLocation[1] ][1].distanceMax:
                    window['information'].update(f"That location is too far for you to move to!")
                    window.refresh
                    
                    continue

                #
                #if it's close enough:
                #

                #if the landing spot is an item Orb:
                if gameBoard[ endLocation[0] ] [ endLocation[1] ][0].tileType == "itemOrb":
                    
                    pickUpItemOrb(gameBoard,startLocation[0],startLocation[1])



                if gameBoard[ endLocation[0] ] [ endLocation[1] ][0].tileType in ["destroyed","damaged4","damaged3","damaged2","damaged"]:
                    window['information'].update(f"Can't move here!")
                    continue
                #if the landing spot is empty
                if gameBoard[ endLocation[0] ] [ endLocation[1] ][0].occupied == False:
                   

                    #copy the actual object over from the old address to the new one
                    gameBoard[endLocation[0]][endLocation[1]][1] = gameBoard[startLocation[0]][startLocation[1]][1]
                    
                    #set the original location as being empty; delete the class; set a default tile
                    gameBoard[ startLocation[0] ] [ startLocation[1] ][0].occupied = False
                    gameBoard[ startLocation[0] ] [ startLocation[1] ][1] = 0
                    gameBoard[startLocation[0]][startLocation[1]][0].tileType = "default"

                    #set the new location as occupied; set the tile as the type of the tile that moved (needs to be updated in future revisions)
                    gameBoard[ endLocation[0] ] [ endLocation[1] ][0].occupied = True
                    gameBoard[ endLocation[0] ] [ endLocation[1] ][1].location = (endLocation[0],endLocation[1])
                    gameBoard[ endLocation[0]][endLocation[1]][0].tileType = f"player{playerTurn}default"
                    
                    window['information'].update(f"Moved successfully!")
                    window.refresh
                    
                    return 1

                
                #killing own piece (illegal)
                elif gameBoard[ endLocation[0] ] [ endLocation[1] ][1].ownedBy == playerTurn:
                    window['information'].update(f"You can't jumpkill your own piece.")
                    window.refresh
                    continue

                
                    
                #kill enemy piece; elif enemy owns the ending location
                elif gameBoard[ endLocation[0] ] [ endLocation[1] ][1].ownedBy != playerTurn:
                    #test to see if the piece can be jumped
                    if "jumpProof" in gameBoard[ endLocation[0] ] [ endLocation[1] ][1].activeBuffs:
                        window['information'].update(f"This opponent is jump proof!")
                        window.refresh()
                        sleep(1)
                        continue
                        
                    #set the internal location of the piece to where you want to end up
                    gameBoard[ startLocation[0] ] [ startLocation[1] ][1].location = (endLocation[0],endLocation[1])
                    #move the piece object
                    gameBoard[ endLocation[0] ] [ endLocation[1] ][1] = gameBoard[ startLocation[0] ] [ startLocation[1]][1]
                    #delete the original piece
                    gameBoard[ startLocation[0] ] [ startLocation[1]][1]=0
                    #set the original location as empty
                    gameBoard[ startLocation[0] ] [ startLocation[1] ] [0].occupied = False

                    #set the new location as full
                    gameBoard[ endLocation[0] ] [ endLocation[1] ] [0].occupied = True
                    #set the original tile as default look
                    gameBoard[startLocation[0]][startLocation[1]][0].tileType = "default"
                    
                    
                    window['information'].update(f"Jumpkilled an enemy piece!")
                    sleep(1)
                    return 2
                    


            else:
                window['information'].update(f"That's not your piece!")
                window.refresh
                continue
                
        else:
            window['information'].update(f"Nothing here to move!")
            window.refresh
            continue
            
        
    
def begin():

    #variables 
    columns = 10
    rows = 10
    gameBoard = []
    
    
    #window
    frame_main = [  #pad was 10,10
                    [sg.Button(image_filename = ".\\blank.png",key=(i,j),size = (20,20), tooltip = "tooltip", pad = (2,2))for j in range (columns)]for i in range(0,rows)
    ]
    
    
    frame_layoutTurn = [ [sg.Image("up.png", key = "turn",visible = True)]]
    
    
    frame_layout = [
        [sg.T(f"Player:",font = "Cambria 30",pad = (4,4)), sg.T(f"",key='playerTurn',font = "Cambria 30",pad = (4,4))],
        [sg.T(f" "*100,key = 'information',size = (37,2),font="Cambria 30")]
        ]
    frame_layout2 = [

        [sg.T(f"Player 1 Controls: xx", key = 'player1piececount',font = "Cambria 20", text_color="blue")],
        [sg.T(f"Player 2 Controls: xx",key = 'player2piececount',font = "Cambria 20",text_color="red")]
        
        ]
    layout = [
        [sg.T("MegaCheckers",font="Cambria 50"),sg.Button("USE ITEMS",key="itemButton",image_filename = "backpack.png"),sg.Button("Look",button_color=("Blue","White"),tooltip = "Examine",font = "Cambria 20", key="examineItem",image_filename="examine.png"),sg.Button("Exit",key="exit")]
        ]
    layout += [
                        [   sg.Frame("Player Turn", frame_layoutTurn),
                            sg.Frame("Playing Field", frame_main),
                        sg.Frame('Remaining pieces:', frame_layout2,font='Calibri 20', title_color='blue')]]
        
      
    layout += [
        [sg.Frame('Information:', frame_layout,font='Calibri 20', title_color='blue')],
        ]
    
    window = sg.Window("MegaCheckers",layout,no_titlebar = True,disable_close = True, grab_anywhere = True, location = (0,0)).finalize()

    #window.maximize()
    
    
    
    #gameBoard for logic
    gameBoard = []
    line = []
    for i in range(columns):
        line.append([Tile(),0])
        gameBoard.append(0)
    
    
    for j in range(rows):
        gameBoard[j] = copy.deepcopy(line)


    initializeField(columns,rows,window,gameBoard)
    
    
    playerTurn = 1
    while True:
    
        
        gamePlay(playerTurn, window, gameBoard)
        if playerTurn == 1:
            window["turn"].update(filename = "down.png")
            playerTurn = 2
        else:
            window["turn"].update(filename = "up.png")
            playerTurn = 1



def tutorial():


    #variables 
    columns = 10
    rows = 10
    gameBoard = []
    
    frame_1 = [
        
            [sg.Button("Object of the game",key="object")],
            [sg.Button("How to select a piece",key="select")],
            [sg.Button("How to move",key="move")],
            [sg.Button("Items",key="items")],
            [sg.Button("Getting info on pieces",key="info")],
            [sg.Button("EXIT",key = "EXIT")]

        ]
    frame_2 = [
        [sg.Button(image_filename = ".\\blank.png",key=(i,j),size = (20,20), tooltip = "tooltip", pad = (10,10))for j in range (columns)]for i in range(0,rows)
        ]
    frame_3 = [

        [sg.T(" "*100, key = "tutorialInfo", font = "Cambria 20",size= (50,5))]

        ]
    frame_4 = [

        [sg.T(" "* 100,key = "information", font = "Cambria 20",size = (50,5) ) ]

        ]
    
    layout = [
                [sg.T("MegaCheckers", font = "Cambria 50",key = "title"), sg.Button("use item",image_filename = "./backpack.png",visible = False)],
                
                
        ]
    layout+= [
        
        [sg.Frame("Main screen",frame_1,key= "options",visible = True), sg.Frame("Game Play", frame_2, key = "gamePlay",visible=True)]
         ]
    layout += [
        [sg.Frame( "Tutorial Info",frame_3), sg.Frame("Information", frame_4)]
        ]




    #gameBoard for logic
    gameBoard = []
    line = []
    for i in range(columns):
        line.append([Tile(),0])
        gameBoard.append(0)
    
    
    for j in range(rows):
        gameBoard[j] = copy.deepcopy(line)


    

    window = sg.Window("MegaCheckers",layout,location = (0,0)).finalize()

    initializeField(columns,rows,window,gameBoard)
            
    
    window["options"].update(visible = True)

    while True:
        event = window.read()
        if event[0] == "EXIT":
            #QUIT
            window.close()
            raise SystemExit
        if event[0] == "object":
            window["gamePlay"].update(visible = True)
            myText = """OBJECT: The object of the game is to destroy all of your opponent's pieces or make it impossible for them to take a turn.  Your main method to do this will be by jumping on enemy pieces to kill them (don't worry, the pieces aren't sentient, so no one is getting hurt).  You will also be able to employ items that you find on the field to either protect yourself from your enemies or to blow them up someway or another."""
            window["tutorialInfo"].update(myText)

            
        elif event[0] == "select":
            window["gamePlay"].update(visible = True)
            while True:
                myText = """SELECTING A PIECE: to select your piece, simply left click on it.  Try it now!  Left click a blue piece."""
                window["tutorialInfo"].update(myText)
                displayBoard(window,gameBoard)
                

                
                event = window.read()

                if event[0] in ["object","select","move","items","info","cancel"]:
                    sg.popup("Restarting tutorial",keep_on_top=True)
                    window.close()
                    tutorial()
                if event[0] == "EXIT":
                    sg.popup("Exiting to main screen.",keep_on_top=True)
                    window.close()
                    main()

                
                x = int(event[0][0])
                y = int(event[0][1])
                if gameBoard[event[0][0]][event[0][1]][1]!=0 and gameBoard[x][y][1].ownedBy == 1:
                    myText = "Great job!  You've selected a piece.  Move onto a different topic."
                    window["tutorialInfo"].update(myText)
                    break
                else:
                    myText = "Sorry, that's not right.  Left click on a blue piece."
                    window["tutorialInfo"].update(myText,text_color="red")
                    window.refresh()
                    sleep(1)
                    window["tutorialInfo"].update(myText,text_color="white")
                    
                    
        elif event[0] == "move":
                window["gamePlay"].update(visible = True)
                outOfRangeTutorialIncomplete = True
                while True:
                    
                    while True:
                        notValidSelection = True
                        myText = """MOVING: normally you can move once per turn, and can only move one piece per turn.  Unless they have specific items, pieces can only move one space forward/back/sideways.  Let's try moving a piece now!  Start by selecting a blue piece on the second row from the top."""
                        window["tutorialInfo"].update(myText)
                        displayBoard(window,gameBoard)
                        while notValidSelection:
                            event = window.read()
                            
                            if event[0][0] == 1:
                                validSelection = False
                                myText = "Good work!  Now we can continue on to the next step."
                                rowOrig = event[0][0]
                                colOrig = event[0][1]
                                window["tutorialInfo"].update(myText)
                                window.refresh()
                                sleep(1.5)
                                break
                            else:
                                myText = "That's not correct.  You'll have to select a blue piece on the second row before we can continue."
                                window["tutorialInfo"].update(myText,text_color="red")
                                window.refresh()
                                sleep(1)
                                window["tutorialInfo"].update(myText,text_color="white")
                                
                        
                        window['information'].update(f"Piece selected!  Choose a destination tile within range.")
                        window.refresh
                        if outOfRangeTutorialIncomplete == True:
                            myText = """Now that we have clicked on one of your pieces, we can move it.  Notice that the information window lets you know that your piece was selected.  It's asking you to choose a location within range.  HOWEVER - try clicking on any empty space EXCEPT the one that's right in front of your selected piece."""
                        else:
                            myText = """Now that you know what it looks like when you try to move to an invalid space, let's do a valid space.  Choose the spot right in front of your selected piece."""
                            
                        window["tutorialInfo"].update(myText)
                        window.refresh()
                        event = window.read()
                        
                        if (event[0][0] < 2) or (event[0][0]) > (rows-2) and outOfRangeTutorialIncomplete == True:
                            myText = """That's not right.  For this tutorial, we need you to click on an empty space.  You clicked on a space that's occupied.  No worries, let's start over."""
                            window["tutorialInfo"].update(myText,text_color = "red")
                            sleep(2)
                            window["tutorialInfo"].update(myText,text_color = "white")
                            break
                        if (event[0][0] == rowOrig+1) and (event[0][1] == colOrig) and outOfRangeTutorialIncomplete == True :
                            myText = """You're getting ahead of yourself.  Normally this would be the right move, but trust me...  Just do what the tutorial says and pick any empty spot except for this one."""
                            window["tutorialInfo"].update(myText,text_color = "red")
                            window["information"].update("")
                            window.refresh()
                            sleep(4)
                            window["tutorialInfo"].update(myText,text_color = "white")
                            continue
                        if outOfRangeTutorialIncomplete == False and event[0][0] == rowOrig+1 and event[0][1] == colOrig:
                            myText = "Good job!  You've successfully moved a piece!  If you move onto a enemy in this way, you kill it!  Click on the items tutorial next!"
                            
                           
                            window["tutorialInfo"].update(myText,text_color = "white")
                            playerBackup = gameBoard[rowOrig][colOrig][1]
                            gameBoard[rowOrig][colOrig][1] = 0
                            gameBoard[event[0][0]][event[0][1]][1] = playerBackup


                            

                            
                            gameBoard[rowOrig][colOrig][0].occupied = False
                            gameBoard[rowOrig][colOrig][0].tileType = "default"
                            gameBoard[rowOrig+1][colOrig][0].occupied = True
                            displayBoard(window,gameBoard)
                            window.refresh()
                            window.read()
                            window.close()
                            tutorial()
                        else:
                            if outOfRangeTutorialIncomplete == True:
                                window['information'].update(f"That location is too far for you to move to!")
                                myText = "Good work!  Notice the error message in the information box.  During normal gameplay, you can keep an eye out on it to see what you can do.  Alright, now that you know what happens if you try to move out of range, let's try doing an actual move.  Choose a blue piece and then move it one square forward."""
                                window["tutorialInfo"].update(myText,text_color = "white")
                                window.refresh()
                                sleep(4)
                                window["information"].update("")
                                outOfRangeTutorialIncomplete = False
                                window.refresh
                                sleep(2)
                                break
                            else:
                                myText = """That's not a valid choice.  Let's try again."""
                                window["tutorialInfo"].update(myText,text_color = "white")
                                window.refresh()
                                sleep(1)
                            
                                
        elif event[0] == "items":
            myText = "This part of the tutorial assumes you've mastered selecting your pieces and moving around.  If you're still not familiar with that, please practice that some more before doing this next part.  Please grab the power tile in the middle: do this by selecting your blue tile that's next to it."
            window["gamePlay"].update(visible = True)
            window["tutorialInfo"].update(myText)
            gameBoard[2][4][0].tileType = "itemOrb"
            displayBoard(window,gameBoard)

            #click the thingy
            while True:
                event = window.read()
                if event[0] != (1,4):
                    myText = "You have to select the piece that's right next to the item orb tile"
                    window["tutorialInfo"].update(myText)
                    window.refresh()
                    continue
                else:
                    
                    while True:
                        myText = "Now that you've selected your piece, we need to click on the item orb to have your piece grab it."
                        window["tutorialInfo"].update(myText)
                        event = window.read()
                        if event[0] != (2,4):
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
                            gameBoard[rowOrig+1][colOrig][0].occupied = True
                            gameBoard[rowOrig+1][colOrig][1].storedItems.append("Energy Forcefield")
                            gameBoard[rowOrig+1][colOrig][1].determineAvatar()
                            
                            displayBoard(window,gameBoard)
                            window.refresh()
                            
                            sleep(1)
                            while True:
                                myText = "Alright, click on the powered up piece"
                                
                                event = window.read()
                                window["tutorialInfo"].update(myText)
                                if event[0] != (2,4):
                                    sg.popup("Click on the piece that you just moved",keep_on_top=True)
                                    continue
                                else:
                                    window["use item"].update(visible = True)
                                    myText = "There are two ways to use an item.  You can either click on the selected piece again, or you can click on the Use Item icon near the top.  Do either one."
                                
                                    event = window.read()
                                    window["tutorialInfo"].update(myText)

                                    if event[0]  == "use item" or event[0] == (2,4):
                                        myText = "There are two ways to use an item.  You can either click on the selected piece again, or you can click on the Use Item icon near the top.  Do either one."
                                        explodeLayout = [ [sg.Button("Cheater's Instawin Item of Instant Winning")] ]
                                        x = sg.Window("Items",explodeLayout)
                                        
                                        event = x.read()
                                        window["tutorialInfo"].update(myText)

                                        if event[0] == "Cheater's Instawin Item of Instant Winning":
                                            x.close()
                                            myText = "Congrats, you cheater.  This weapon (which only exists in this tutorial mode) will instantly destroy any enemy pieces on the field.  You now know pretty much everything you need to know to win.  Go out there and start playing with a friend."
                                            
                                            
                                            window["tutorialInfo"].update(myText)
                                            window.refresh()
                                            sleep(1)
                                            
                                            for i in range(2):
                                                for j in range(columns):
                                                    window[rows-i-1,j].update(image_filename="exploding.png")
                                            window.refresh()
                                            sleep(1)
                                            
                                            for i in range(2):
                                                for j in range(columns):
                                                    window[rows-i-1,j].update(image_filename="destroyed.png")
                                            window.refresh()
                                            sleep(1)

                                            
                                            for i in range(2):
                                                for j in range(columns):
                                                    window[rows-i-1,j].update(image_filename="exploding.png")
                                            window.refresh()
                                            sleep(1)
                                            
                                            for i in range(2):
                                                for j in range(columns):
                                                    window[rows-i-1,j].update(image_filename="blank.png")
                                            window.refresh()
                                            sleep(5)
                                        sg.popup("Restarting the tutorial",keep_on_top=True)
                                        tutorial()
                                            

                                        

                                    else:
                                        sg.popup("Nope, try again",keep_on_top=True)
                                        continue
                                
                                    
                            
                        
                        
                    
                            
                        
                            

                            
        else:
            myText = "Invalid choice.  Try clicking something on the menu."
            window["tutorialInfo"].update(myText)
            
                
                
            


    
    
def main():

    introLayout = [[sg.Text("MegaCheckers",font = "Cambria 100")]]
    frame_1 = [
        [sg.Button("Begin game",key="begin")],
        [sg.Button("How to play",key="tutorial")]
        ]
    introLayout+= [[sg.Frame("Choose an option",frame_1,key="options")]]
    introWindow = sg.Window("MegaCheckers",introLayout)
    event = introWindow.read()
    if event[0] == "tutorial":
        introWindow.close()
        tutorial()
    if event[0] == "begin":
        introWindow.close()
        begin()


    
    
    

    
main()
