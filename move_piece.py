################################################################################
# Changelog:
# Date............Author.......Change
# 2022-Feb-05.....moabdali.....Initial Version
# 2022-Feb-06.....moabdali.....Check item pickups, added cannibalism check,
#                               added death checks for jumping onto damaged tiles
# 2022-Feb-17.....moabdali.....Secret Agent implemented
# 2022-Feb-18.....moabdali.....Trap orb work
################################################################################

import board
import global_data
import items
import python_distances

game_board = board.game_board
columns = global_data.columns
rows = global_data.rows
# piece_teleported_this_turn = False
# piece_moved_this_turn = False


###############################################################################
# @brief: select_piece verifies the user is selecting one of their own pieces #
# @param[in] start_location a set in the form (r,c) that determines the index #
#               of the game_board that the user is attempting to access.      #
# @return: True/False   True: player has selected their own piece             #
#                       False: player has not selected their own piece        #
###############################################################################
def select_piece(start_location):
    
    # validate that coordinates are within the playing field
    if (start_location[0] >= rows or start_location[1] >= columns or
            start_location[0] < 0 or start_location[1] < 0):
        print("SELECTED LOCATION IS OUTSIDE THE PLAYING FIELD")
        return False
    
    # find the tile that corresponds to the coordinates; must be done after
    # validating the range
    start_tile = game_board[start_location[0]][start_location[1]]

    # verify there's a piece there; use both checks just in case
    #################################################################
    #   DEBUG                                                       #
    #   Consider making this trigger the tile info feature if no    #
    #   visible pieces here                                         #
    #################################################################
    if not start_tile.piece or not start_tile.occupied:
        print("NO PIECE HERE")
        input("")
        if start_tile.piece or start_tile.occupied:
            print("""Additionally, an error occurred where piece status and
occupied status do not match.  Piece, occupied: """,
                  start_tile.piece, start_tile.occupied)
        return False
    
    # verify it's your piece
    #################################################################
    #   DEBUG                                                       #
    #   Consider making this trigger the enemy info feature if your #
    #   enemy resides here                                          #
    #################################################################
    if not start_tile.piece.owned_by == global_data.current_player_turn:
        print("NOT YOUR PIECE")
        input("")
        return False

    print("Accepted start location.")
    ########################################################################
    # distance check (be sure to look for exceptions such as warp, diagonal,
    # and round earth theory
    ########################################################################
    start_tile.piece.process_move_type()
    
    range_object = python_distances.RangeObject(
                            start_location,
                            False,
                            rows,
                            columns,
                            "all"
                            )
    python_distances.preview_range(range_object, start_tile.piece)
    
    start_tile.piece.print_detailed_info()
    return True


################################################################################
# @brief: valid_move after validating that your piece exists at the start      #
#           location, this function validates that you can legally move to     #
#           the chosen location (or activates the item menu if you double      #
#           click the piece                                                    #
# @param[in] start_location a set in the form (r,c) of the current player's    #
#               piece showing the index of said piece in game_board.  Verified #
# @param[in] end_location a set in the form (r,c) showing the index of where   #
#               the player wishes to move the selected piece to (or opens the  #
#               item menu if the start location and end location match)        #
# @return   True/False  True: player has successfully moved their piece        #
#                       False: player has not been able to move their piece    #
################################################################################
def valid_move(start_location, end_location):
    # validate that coordinates are within the playing field
    if (start_location[0] >= rows or end_location[1] >= rows or
            start_location[1] >= columns or end_location[1] >= columns or
            start_location[0] < 0 or end_location[0] < 0 or
            start_location[1] < 0 or end_location[1] < 0):
        print("SELECTED LOCATION IS OUTSIDE THE PLAYING FIELD")
        return False
    
    # find the tile that corresponds to the coordinates; must be done after
    # validating the range
    start_tile, end_tile = get_start_end_coords(start_location, end_location)
    start_location = (start_location[0], start_location[1])
    end_location = (end_location[0], end_location[1])
    # check if player is double clicking the same piece to open item menu
    if start_tile is end_tile:
        # does piece actually have any items?
        if len(start_tile.piece.stored_items) < 1:
            print("This piece has no items.")
            return False
        
        print("OPENING ITEM MENU")
        ##################################
        # DEBUG                          #
        # PUT IN ITEM FUNCTION           #
        ##################################
        items.show_items(start_tile.piece)
        if items.use_item(start_tile.piece):
            print("Used item")
        else:
            print("Didn't use item")
        # return False because you didn't actually move;
        # we want to continue doing the make a move loop
        return False
    
    # distance check (be sure to look for exceptions such as warp, diagonal, and
    # round earth theory
    start_tile.piece.process_move_type()
    if start_tile.piece.move_type == "radial":
        print("Move diagonal available")
        range_object = python_distances.RangeObject(
            start_location,
            False,
            rows,
            columns,
            "all"
            )
        python_distances.radial(range_object)
        python_distances.print_distances(range_object)
        if end_location not in range_object.target_list:
            print("Too far, not in radial!")
            return False

    # else if round earth theory
    if start_tile.piece.move_type == "round earth theory":
        print("round earth theory")

    if start_tile.piece.move_type == "round earth theory move diagonal":
        print("round earth theory plus move diagonal")
        
    # no modifications
    elif start_tile.piece.move_type == "cross":
        range_object = python_distances.RangeObject(
            start_location,
            False,
            rows,
            columns,
            "all"
            )
        python_distances.cross(range_object)
        python_distances.print_distances(range_object)
        if end_location not in range_object.target_list:
            print("started here: ", start_location)
            print("trying to get here: ", end_location)
            print("targetlist:", range_object.target_list)
            print("Too far! (not in cross range)")
            return False
    
    # if the landing tile is damaged
    if end_tile.tile_type in global_data.damaged_floor:
        # mark the piece's STARTING point because it hasn't moved yet
        start_tile.piece.death_mark = "piece_fell"
        # make sure piece can't move after it dies (this is to preempt a situation
        # where you may have extra moves left due to items)
        start_tile.piece.move_again = 0
        return True
    
    # if you're trying to jump up to a much higher tile
    if (end_tile.tile_height - start_tile.tile_height >= 2 and
            "grappling_hook" not in start_tile.piece.active_buffs):
        print("Tile is way too high")
        return False
    
    # check if ending location is your own piece
    if (end_tile.piece and
            end_tile.piece.owned_by == global_data.current_player_turn and
            "cannibalism" not in start_tile.piece.active_buffs):
        print("You can't kill your own piece!")
        return False

    # check if you can cannibalize your own piece
    if (end_tile.piece and
            end_tile.piece.owned_by == global_data.current_player_turn and
            "cannibalism" in start_tile.piece.active_buffs):
        print("You cannibalized your own piece!  You monster!")
        if end_tile.piece.stored_items:
            if "burdened" in start_tile.piece.active_debuffs:
                print("""Your killed ally had items, but you were unable to take\
them as you are burdened.""")
                return True
            for each_scavenged_item in end_tile.piece.stored_items:
                print("You scavenged a ", each_scavenged_item)
                start_tile.piece.stored_items.append(each_scavenged_item)
        return True
        
    if end_tile.piece and end_tile.piece.owned_by != global_data.current_player_turn:
        ##################################
        #  DEBUG                         #
        #  "TRY TO KILL ENEMY" FUNCTION  #
        ##################################
        print("Killed an enemy!")
        return True

    if end_tile.item_orb:
        print("You picked up an item.")
        return True
    
    return True


###############################################################################
# @brief move_piece after getting a helper function to verify the move is     #
#           legal, moves the piece to the location requested, then updates    #
#           relevant properties of the tile and piece to show that the move   #
#           has successfully occurred.                                        #
# @param[in] start_location a set in the form (r,c) of the player's piece.    #
#               The piece has been verified as belonging to the player.       # 
# @param[in] end_location a set in the form (r,c) of where the player would   #
#               like to move their piece.  This location has not been yet     #
#               been verified, but will be using the valid_move helper.       #
# @return True/False    True: player successfully moved their piece           #
#                       False: player was not allowed to move piece           #
###############################################################################

def move_piece(start_location, end_location):
    print("Attempted start and end locations: ", start_location, end_location)
    if valid_move(start_location, end_location):
        start_tile, end_tile = get_start_end_coords(start_location, end_location)
        start_tile.occupied = False
        temp_piece = start_tile.piece
        
        # in case the piece fell into a damaged tile
        if start_tile.piece.death_mark == "piece_fell":
            print("Your piece jumped into the void!  Suicide is never the answer.")
            start_tile.piece = None
        
        # if the piece is still alive and moved successfully
        elif not start_tile.piece.death_mark:
            start_tile.piece = None
            end_tile.piece = temp_piece
            end_tile.piece.x_location = end_location[0]
            end_tile.piece.y_location = end_location[1]
            end_tile.occupied = True
            end_tile.piece.moves_left -= 1
            global_data.move_restriction = True
            global_data.current_turn_piece_location = end_location
            end_tile.piece.current_turn_piece = True
            # debug: correct placement?
            secret_agent_check()
            print("current turn info: ", end_tile.piece.current_turn_piece)
            return True
        # if the piece is marked for death for unknown reasons (catchall)
        else:
            start_tile.piece = None
            print("The piece died prematurely!")
            
        # True = "a move was made"
        global_data.move_restriction = True
        if end_tile.piece:
            end_tile.piece.current_turn_piece = True
        print("[unique branch [suicide] ] Move was made.")
        return True
    
    # if not valid_move/you used an item/canceled movement
    else:
        print("You did not move.")
        # false = "no move made; try again"
        return False


# check to see if pieces are standing on an item orb 
def check_item_pickups():
    for row in game_board:
        for each_tile in row:
            if (each_tile.item_orb and
                    each_tile.piece and
                    each_tile.piece.owned_by == global_data.current_player_turn and
                    "burdened" not in each_tile.piece.active_debuffs):
                
                each_tile.item_orb = False
                received_item = items.get_item()
                each_tile.piece.stored_items.append(received_item)
                print(global_data.current_player_turn+f"""'s piece picked up an
item! ({received_item})""")
            # trap orb check for allied piece
            elif (each_tile.trap_orb and
                        each_tile.piece and
                        each_tile.piece.owned_by == each_tile.trap_orb):
                    print(global_data.current_player_turn + f"""'s piece is precariously standing on an allied trap\
 orb.  Good thing you didn't try to pick it up!""")
            # trap orb for unallied pieces
            elif (each_tile.trap_orb and
                    each_tile.piece and
                    each_tile.piece.owned_by != each_tile.trap_orb):
                # forcefield check
                if each_tile.piece.owned_by == global_data.current_player_turn:
                    print(f"Your piece blew up by {each_tile.trap_orb}'s trap orb.")
                else:
                    print(f"Your opponent's piece was blown up by {each_tile.trap_orb}'s trap orb")
                each_tile.kill_piece_on_tile()
                each_tile.clear_tile()
                #board.verify_location_data()
# check for secret agent
def secret_agent_check():
    for row in game_board:
        for each_tile in row:
            if (each_tile.secret_agent and
                    each_tile.piece and
                    each_tile.piece.owned_by == each_tile.secret_agent):

                if len(each_tile.secret_agent_list) > 0:
                    if "burdened" not in each_tile.piece.active_debuffs:
                        print("The secret agents hands you: ")
                        for stolen_item in each_tile.secret_agent_list:
                            print(stolen_item)
                            each_tile.piece.stored_items.append(stolen_item)
                        each_tile.secret_agent_list = []
                        print("The agent vanishes as his contract is complete.")
                        each_tile.secret_agent = None
                        return
                    if "burdened" in each_tile.piece.active_debuffs:
                        print("""The secret agent would have given you some\
items, but you are burdened.  Bring another piece here for a nice payout.""")
                        return

                elif len(each_tile.secret_agent_list) == 0:
                    print("The agent has nothing of use for you at this time.")
                    return
            if (each_tile.secret_agent and
                    each_tile.piece and
                    each_tile.piece.owned_by != each_tile.secret_agent):
                if each_tile.piece.stored_items:
                    print("The secret agent stole all your items!")
                    for stolen_item in each_tile.piece.stored_items:
                        each_tile.secret_agent_list.append(stolen_item)
                        print(stolen_item)
                    each_tile.piece.stored_items = []
                    return
                else:
                    print("""The enemy secret agent stands near you menacingly...\
But doesn't do anything since you don't have any items for him to steal""")
                    return


# check for fall death at beginning of turn
def check_if_piece_fell():
    for row_index, row in enumerate(game_board):
        for col_index, each_tile in enumerate(row):
            if each_tile.tile_type in global_data.damaged_floor:
                if game_board[row_index][col_index].piece:
                    print(game_board[row_index][col_index].piece.owned_by+f"""\
's piece at ({row_index},{col_index}) fell through a damaged tile into the void.\
 RIP.""")
                    game_board[row_index][col_index].piece = None
                    game_board[row_index][col_index].occupied = False


# move_again
def move_again(end_location):
    x = end_location[0]
    y = end_location[1]
    
    if game_board[x][y].piece:
        # make sure that piece belongs to you
        if game_board[x][y].piece.owned_by == global_data.current_player_turn:
            # does the piece have an item that may let it move again
            if ("berzerker" in game_board[x][y].piece.active_buffs or
                    "move again" in game_board[x][y].piece.active_buffs):
                # if they have more than 0 moves left
                print(game_board[x][y].piece.moves_left)
                if game_board[x][y].piece.moves_left > 0:
                    move_again_prompt = input("YOU CAN MAKE ANOTHER MOVE. Y/N")
                    if move_again_prompt in ('Y', 'y', "yes", "Yes"):
                        move_restriction = True
                        global_data.current_turn_piece_location[0] = game_board[x][y].piece.x_location
                        global_data.current_turn_piece_location[1] = game_board[x][y].piece.y_location
                        return move_restriction, True
    return False, False


# get corresponding tiles from the starting and ending coordinates
def get_start_end_coords(start_location, end_location):
    return game_board[start_location[0]][start_location[1]], game_board[end_location[0]][end_location[1]]
