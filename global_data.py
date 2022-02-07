# dimensions of the playing field
columns = 10
rows = 10

if columns < 3:
    columns = 3
if rows < 3:
    rows = 3

# items settings
set_items_option_list = ["pure_random", "balanced", "insanity", "none"]
chosen_items_option = 1
items_probability_type = set_items_option_list[chosen_items_option]

# whose turn it is
current_player_turn = "player_1"

move_restriction = False
current_turn_piece_location = [0,0]


# how many turns have elapsed?
turn_count = 1

# this determines the number of item orbs that show up
orb_cycle_list = [3, 3, 0, 1, 2, 1, 1, 0, 1, 0, 0]

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
damaged_floor = (
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
def get_orb_generation_count():
    item_cycle = turn_count % 11
    return orb_cycle_list[item_cycle]
    
