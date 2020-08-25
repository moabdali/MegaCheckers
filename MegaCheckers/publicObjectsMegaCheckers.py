# imported by highlightsAndDistancesMegaCheckers -> displayBoardMegaCheckers -> useItemsMegaCheckers -> megaCheckers

#relies on: PIL for Image
from PIL import Image
import PySimpleGUI as sg

PublicPNGList = []


class PublicStats:
    turnCount = 1
    cycle = 0
    #orbCycleList = [5, 10, 0, 0, 3, 1, 0, 2, 1]
    orbCycleList = [3, 0, 0, 1, 2, 1, 1, 0, 1,0,0]
    spookyHand = False
    spookyHandTurnCount = 15
    hotSpot = []
    recallCount = 0
    playerAutoWin = 0
    playerAutoWinTurn = False
    screenSize = "normal"
    showItemExplanations = True
    def getOrbCount(self):
        cycle = PublicStats.turnCount % 11
        return PublicStats.orbCycleList[cycle]
    damagedFloor = ("damaged",
                    "destroyed",
                    "damaged1",
                    "damaged2",
                    "damaged3",
                    "damaged4",
                    "damaged5",
                    "damaged6",
                    "damaged7",
                    "damaged8")
    

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
        self.forceFieldTurn = 0
        self.stickyTimeBomb = False
        self.berzerkMeatCount = False
        self.berzerkAttacksLeft = False
        # helper variable for keeping track of whether the ball
        # is in motion and needs a rotating movement animation
        self.bowlMotion = False
        self.bowlOrientation = 1

        # future implementation; pieces can upgrade their levels
        self.pieceLevel = 1
        self.pieceExp = 0
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
        elif self.tileType == "mystery box":
            sg.popup(
                f"This is mystery box tile!  A random effect (can be bad or good) will occur when you step here.  It has an elevation of {self.tileHeight}",
                keep_on_top=True,
            )
            return f"This is mystery box tile!  A random effect (can be bad or good) will occur when you step here.  It has an elevation of {self.tileHeight}"



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
        "orb eater", #10
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
        "grapple icon", #40
        "AI bomb", #41
        ]):

        myImage = Image.open(f"images/{i}.png").convert("RGBA")
        PublicPNGList.append(myImage)

