################################################################################
# items - the items and what they do
# CHANGELOG:
#   DATE            AUTHOR      CHANGES
#   2022-Feb-05     moabdali    initial creation
#   2022-Feb-06     moabdali    added weighted probabilities for items
#
################################################################################

import copy
import random

import board
import global_data

# the odds of items showing up depending on what option was chosen in global_data
no_odds = 0
rare_odds = 1
low_odds = 5
normal_odds = 10
common_odds = 15


items = [
    "AI bomb",  # walking bomb
    "auto win",  # win in 50 turns
    "bernie sanders",  # redistribute inactive items
    "berzerk",  # if you kill a piece, go again. But die if you haven't eaten lately
    "bowling ball",  # out of control bowling ball
    "canyon column",  # create a trench
    "canyon radial",
    "canyon row",
    "care package drop",  # drop item orbs near an opponent
    "charity",  # 10 Give an opponent a piece
    "dead man's trigger",  # if your piece is jumped on, the enemy dies, too
    "dump items",  # dump your items anywhere on the field
    "elevate tile",  # raise a tile
    "Energy Forcefield",  # create a defensive shield on your piece
    "floor restore",  # restore all tiles
    "grappling hook",  # hook your way up a tall tile
    "haphazard airstrike",  # indiscriminately bomb the playing field
    "haymaker",  # punch a piece away
    "heir",  # forcefully take all of your allied pieces' powers
    "invert elevation all",  # 20 lower tall tiles, raise low tiles
    "invert elevation column",
    "invert elevation radial",
    "invert elevation row",
    "jump proof",  # piece cannot be jumped on
    "jumpoline",  # jump onto this tile in order to be bounced elsewhere
    "laser column",  # create a laser that burns all units in range
    "laser row",
    "magnet",  # "suck in" all nearby pieces
    "move again",  # get an extra move with this piece
    "move diagonal",  # 30 move diagonally
    "mutual treason column",  # swap ownership of all pieces in range
    "mutual treason radial",
    "mutual treason row",
    "mystery box",  # a mystery effect occurs
    "napalm column",  # burn all enemy pieces in range, the floor melts away
    "napalm radial",
    "napalm row",
    "orb eater",  # summon a mouse that eats orbs
    "place mine",  # drop a mine
    "purify column",  # 40 remove all negative effects from your pieces in range
    "purify radial",
    "purify row",
    "purity tile",  # create a reusable tile that heals any piece that steps on it
    "recall",  # return a piece to the condition it was in at the time of use, in 10 turns
    "reproduce",  # create a brand new piece next to the current piece
    "round earth theory",  # ignore boundaries of the playing field - loop around
    "secretAgent",  # steals your enemy's items and gives them to you
    "seismic activity",  # earthquake that randomly changes the elevation of the tiles
    "shuffle all",  # move tiles around randomly
    "shuffle column",  # 50
    "shuffle item orbs",  # move item orbs around randomly
    "shuffle radial",
    "shuffle row",
    "sink tile",  # lower the tile
    "smart bombs",  # shoot the playing field with no threat of damage to your pieces
    "snake tunneling",  # a snake randomly moves nearby tiles up randomly; killing enemies
    "spooky hand",  # a scary hand that will stay resident under the field and kidnap enemies
    "steal items column",  # steal items from the enemy
    "steal items radial",
    "steal items row",  # 60
    "steal powers column",  # steal activated powers from the enemies
    "steal powers radial",
    "steal powers row",
    "sticky time bomb",  # attach a time bomb to any piece, it will blow up in a few turns
    "study column",  # copy powers from your allies
    "study radial",
    "study row",
    "suicide bomb column",  # kill yourself and your enemies
    "suicide bomb radial",
    "suicide bomb row",  # 70
    "teach column",  # copy powers TO your allies
    "teach radial",
    "teach row",
    "trap orb",  # set a trap that blows up your enemy if they step on it.  Looks like an item orb
    "trip mine column",  # set a mine on your enemies.  If they move, they die.
    "trip mine radial",
    "trip mine row",
    "trump",  # build a wall (raise the tiles)
    "vampiricism",  # steal powers from your enemy
    "vile radial",  # 80 enemy can't activate items
    "warp",  # teleport randomly
    "wololo column",  # steal enemy pieces
    "wololo radial",
    "wololo row",
    "worm hole",  # set a  worm hole; any of YOUR pieces can jump straight to it as long as it's not occupied
]

if global_data.items_probability_type == "balanced":
    weights = (
        normal_odds,    # AI bomb
        low_odds,       # auto win
        low_odds,       # bernie sanders
        normal_odds,    # berzerk
        low_odds,       # bowling ball
        normal_odds,    # canyon column
        low_odds,       # canyon radial
        low_odds,       # canyon row
        low_odds,       # care package drop
        low_odds,       # charity #10

        common_odds,    # dead man's trigger
        low_odds,       # dump items
        low_odds,       # elevate tile
        low_odds,       # energy forcefield
        rare_odds,      # floor restore
        normal_odds,    # grappling hook
        normal_odds,    # haphazard airstrike
        normal_odds,    # haymaker
        rare_odds,      # heir
        rare_odds,      # invert elevation all #20

        rare_odds,      # invert elevation column
        rare_odds,      # invert elevation radial
        rare_odds,      # invert elevation row
        normal_odds,    # jump proof
        normal_odds,    # jumpoline
        low_odds,       # laser column
        low_odds,       # laser row
        common_odds,    # magnet
        common_odds,    # move again
        common_odds,    # move diagonal #30

        normal_odds,    # mutual treason column
        low_odds,       # mutual treason radial
        low_odds,       # mutual treason row
        normal_odds,    # mystery box
        low_odds,       # napalm column
        low_odds,       # napalm radial
        low_odds,       # napalm row
        normal_odds,    # orb eater
        common_odds,    # place mine
        normal_odds,    # purify column #40

        normal_odds,    # purify radial
        normal_odds,    # purify row
        low_odds,       # purity tile
        low_odds,       # recall
        low_odds,       # reproduce
        normal_odds,    # round earth theory
        normal_odds,    # secretAgent
        low_odds,       # seismic activity
        rare_odds,      # shuffle all
        low_odds,       # shuffle column  #50

        common_odds,    # shuffle item orbs
        common_odds,    # shuffle radial
        common_odds,    # shuffle row
        low_odds,       # sink tile
        normal_odds,    # smart bombs
        normal_odds,    # snake tunneling
        normal_odds,    # spooky hand
        common_odds,    # steal items column
        low_odds,       # steal items radial
        rare_odds,      # steal items row

        low_odds,       # steal powers column
        rare_odds,      # steal powers radial
        rare_odds,      # steal powers row
        common_odds,    # sticky time bomb
        rare_odds,      # study column
        rare_odds,      # study radial
        rare_odds,      # study row
        low_odds,       # suicide bomb column
        low_odds,       # suicide bomb radial
        low_odds,       # suicide bomb row#70

        rare_odds,      # teach column
        rare_odds,      # teach radial
        rare_odds,      # teach row
        common_odds,    # trap orb
        common_odds,    # trip mine column
        rare_odds,      # trip mine radial
        rare_odds,      # trip mine row
        low_odds,       # trump
        common_odds,    # vampiricism
        common_odds,    # vile radial#80

        common_odds,    # warp
        low_odds,       # wololo column
        rare_odds,      # wololo radial
        rare_odds,      # wololo row
        common_odds,    # worm hole #85
        )
    # create a modified weighted items list
    items = random.choices(items, weights, k=1000)
    
    
# generate orbs between turns (if possible)
def generate_item_orbs():
    empty_squares = board.find_empty_tiles()
    num_orbs_to_spawn = global_data.get_orb_generation_count()
    while (num_orbs_to_spawn > 0 and
           len(empty_squares) > 0):
        tl = random.choice(empty_squares)
        board.game_board[tl[0]][tl[1]].tile_type = "item_orb"
        empty_squares.remove(tl)
        num_orbs_to_spawn -= 1


# get a random item
def get_item():
    return "shuffle row"
    # return random.choice(items)


# show all the items a piece holds
def show_items(piece):
    for item in piece.stored_items:
        print(item + " ", end="")
    print("")


# allows user to cancel using an item
def cancel_item():
    yorno = input("Do you wish to use item?  y/n")
    # true = cancel
    if yorno in ("Y", "y", "Yes", "YES"):
        return True
    # false = don't cancel
    return False


# attempt to use an item
def use_item(piece):
    
    # check if disabled (prevented from using items)
    if "paralyzed" in piece.active_debuffs:
        print("Piece is paralyzed.  This piece cannot use items.")
        return False
    
    # check what item is to be used
    item_chosen = input("Which item do you wish to use?")
    
    # check if have
    if item_chosen not in piece.stored_items:
        print("You don't possess that item.")
        return False

    # display range

    # check where player is sure they want to use it
    
    if cancel_item():
        return False
    
    # attempt to use item
    if item_logic(item_chosen, piece):
        print("Used item here")
        return True
    else:
        print("item not used or implemented properly?")
        return False


def remove_item(item_chosen, piece):
    try:
        piece.stored_items.remove(item_chosen)
        return True
    except:
        return False


################################################################################
#       ITEM LOGIC
################################################################################
def item_logic(item=None, piece=None):
    
    player_turn = global_data.current_player_turn
    if player_turn == "player_1":
        enemy_turn = "player_2"
    elif player_turn == "player_2":
        enemy_turn = "player_1"
    else:
        print("An error occurred with player turn assignment")
        return
    if not item:
        print("No item selected")
        return
    x = piece.x_location
    y = piece.y_location
    
    
# shuffle column
    if item == "shuffle column":
        # itemsMenu.Hide()
        g = board.game_board
        # if g[x][y][1].grey == True:
        #    g[x][y][1].currentTurnPiece = True
        #    g[x][y][1].grey = False
        
        cg = []
        locations = []
        if remove_item(item, piece):
            print("Deleted one copy of item.")
        else:
            print("Item not in list.  This is a really bad error.")
        # for rows called i, in gameboard
        x = 0

        # laserCheck(window, gameBoard, resetOnly = True)
        for row in g:
            # copy the column's tiles to cg    
            cg.append(copy.deepcopy(row[y]))
            locations.append((x, y))
            row[y].tile_type = "default"
            row[y].occupied = False
            # displayBoard(window, g)
            # window.refresh()
            # sleep(0.1)
            x += 1

        # shuffle locations to look cooler?
        random.shuffle(locations)
        # shuffle locations to look cooler?

        # displayBoard(window, gameBoard)
        # window.refresh()

        # locations contains the coordinates of what we're pasting to
        while len(locations) > 0:
            # for more shuffling, pick a random location
            rand_coord = random.choice(locations)
            # grab a backed up tile
            rand_tile_info = random.choice(cg)
            # paste to the random output location
            g[rand_coord[0]][rand_coord[1]] = rand_tile_info
            # remove that location from the output list
            locations.remove(rand_coord)
            # remove that location from the input list
            cg.remove(rand_tile_info)
            # laserChecks
            # g[randCoord[0]][randCoord[1]][0].horiLaser = False
            # displayBoard(window, g)
            # window.refresh()
            # sleep(0.1)
        # laserCheck(window, gameBoard)
        # displayBoard(window, g)
        board.verify_location_data(expected=True)
        return True
    
# shuffle row
    elif item == "shuffle row":
        # itemsMenu.Hide()
        g = board.game_board
        # if g[x][y][1].grey == True:
        #    g[x][y][1].currentTurnPiece = True
        #    g[x][y][1].grey = False
        # cg = copied gameboard
        cg = [] 
        locations = []
        # deplete item
        if remove_item(item, piece):
            print("Deleted one copy of item.")
        else:
            print("Item not in list.  This is a really bad error.")
        # laserCheck(window, gameBoard, resetOnly = True)
        
        # for pieces in the row
        for i_index, i in enumerate(g[piece.x_location]):
            # copy the row's tiles to cg    
            cg.append(copy.deepcopy(i))
            locations.append((piece.x_location, i_index))
            print("Backed up a piece")
            # g[x][i_index][0].tileType = "default"
            # g[x][i_index][0].occupied = False
            # displayBoard(window, g)
            # window.refresh()
            # sleep(0.1)

        # shuffle locations to look cooler?
        random.shuffle(locations)
        # shuffle locations to look cooler?

        # displayBoard(window, gameBoard)
        # window.refresh()

        while len(locations) > 0:
            rand_coord = random.choice(locations)
            rand_tile_info = random.choice(cg)
            g[rand_coord[0]][rand_coord[1]] = rand_tile_info
            locations.remove(rand_coord)
            cg.remove(rand_tile_info)
            # laserChecks
            # g[randCoord[0]][randCoord[1]][0].horiLaser = False
            # displayBoard(window, g)
            # window.refresh()
            # sleep(0.1)
        # updating move data since everything will be out of whack
        board.verify_location_data(expected=True)
        # laserCheck(window, gameBoard)
        # displayBoard(window, g)
        return True
