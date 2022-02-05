# dimensions of the playing field
columns = 10
rows = 10

# whose turn it is
current_player_turn = "player_1"

# how many turns have elapsed?
turnCount = 1

# this determines the number of item orbs that show up
orbCycleList = [3, 0, 0, 1, 2, 1, 1, 0, 1, 0, 0]
# index for the item cycle
item_cycle = 0

# for the spooky hand item; if spooky hand is true, then
# the item is active; the turn counter determines when
# the hand will attack
spooky_hand = False
spooky_hand_turn_counter = 15

# determines where hotspots are located (teleports that your players
# can jump to
hotspot = []

# number of recalls that are available
recall_count = 0

# DEBUG: make better comments for this
playerAutoWin = 0
playerAutoWinTurn = False

# DEBUG: screen settings; keep normal for now
screenSize = "normal"

# do players want to see extended item explanations on pickup?
showItemExplanations = True

# state of the floor
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

# how many orbs do we want to generate this turn?
def getOrbCount(self):
    cycle = PublicStats.turnCount % 11
    return PublicStats.orbCycleList[cycle]
    
    

    

