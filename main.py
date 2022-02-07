################################################################################
# Changelog:
# Date............Author.......Change
# 2022-Feb-04.....moabdali.....Initial Version
# 2022-Feb-05.....moabdali.....Added item pickups, item orb generation
# 2022-Feb-06.....moabdali.....Added some calls to between_turns functions
# 2022-Feb-07.....moabdali.....Cleaned up comments/debugs, added a function for
#                              grouping together the functions/actions that
#                              occur between turns
###############################################################################

import  global_data
from    tile import tile
from    piece import piece
import  board
import  move_piece
import  PySimpleGUI as sg
import  random
import  items
import  between_turns

# for ease of reading, I scrunched together the functions that run between each turn
#   note that the order of functions is pretty important in some cases.  Some notable
#   cases are: check_if_piece_fell should run before any floor repairs are done.
#   while not as important, generation of item orbs should be done AFTER the floors
#   get reparations done, as this improves the randomness of where they show up (more
#   space).  Setting the current turn to false should be done after checking to see
#   that pieces are killed; no point in doing extra writes if they're going to die.
#   Likewise, reset moves only after we know the piece isn't going to die.  Count pieces
#   obviously must be done last, as it checks counts for game win conditions
def list_of_functions_between_turns():
    global_data.turn_count += 1
    global_data.move_restriction = False
    between_turns.switch_turns()
    move_piece.check_if_piece_fell()
    between_turns.repair_floor(game_board)
    board.verify_location_data()
    items.generate_item_orbs()
    between_turns.set_current_turn_piece_to_false(game_board)
    between_turns.reset_moves_left(game_board)
    between_turns.count_pieces(game_board)

# semi global variables for main for easier reading    
columns     =   global_data.columns
rows        =   global_data.rows
game_board  =   board.initialize_start()

    ############################################################################
    #                                                                          #
    #       DEBUG MOVE TEST HERE                                               #
    #                                                                          #
    ############################################################################
# modify starting pieces
game_board[0][0].piece.active_buffs.append("move again")
game_board[0][0].piece.move_distance_max = 3
# game_board[rows-1][columns - 1].piece.active_buffs.append("move again")
# end modify starting pieces

# turn_end is used to see if the 'between turn' functions should be run; the while
#   loop runs each time the player is expected to move; there are times when the
#   player gets to move more than once, but we don't want 'in between turns'
#   functions to run if that's the case; only when the turn actually ends
turn_end = True

# main game loop here
while True:
    # the stuff that happens between turns such as switching whose turn it is
    # or resetting the number of moves a piece with 'move again' can make
    if turn_end == True:
        list_of_functions_between_turns()
    # denote that the turn hasn't ended    
    turn_end = False
    
    board.print_ascii_table()
    print(global_data.current_player_turn,"'s turn.")
    print("Turn # ", global_data.turn_count)
    
    #check to make sure any wayward item orbs are picked up on a given player's
    #turn.  This normally wouldn't occur, but a shuffler item may cause this to
    #occur.  Game logic dictates that picking up orbs can only be done on your
    #turn, but cannot make you waste a turn on their own.
    move_piece.check_item_pickups()
    
    # if this is the first time a piece has moved this turn
    if global_data.move_restriction == False:
        start_location = []
        try:
            start_location.append( int(input("start row >>")) )
            # debugger code for getting info
            if start_location[0] == 99:
                board.print_all_tile_info(True);
                continue
            start_location.append( int(input("start col >>")) )
        except ValueError:
            print("Not an integer.")
            continue
    # else, if a piece has moved already and is eligible for another move
    else:
        start_location = global_data.current_turn_piece_location
        print("Start location for already-moved piece is", start_location)

    # if you were unable to move the piece (because you picked a bad start location)
    if not move_piece.select_piece(start_location):
        continue

    try:
        # reset here because we don't want to keep appending
        end_location = []
        end_location.append( int(input("end row >>")) )
        # debugger code for getting info
        if end_location[0] == 99:
            board.print_all_tile_info(True);
            continue
        end_location.append( int(input("end col >>")) )
    except ValueError:
        print("Not an integer.")
        continue
    # if you were unable to move, mostly because of a bad end_location,
    # restart the input entry to the very beginning.  Note that if you
    # get here when you're under the effects of a "move again" style item,
    # your start location automatically gets forced as that of the last
    # known piece that triggered the move again.
    if not move_piece.move_piece( start_location , end_location ):
        continue

    #check for moving again
    ###########
    # DEBUG: need to do something with current turn piece
    ###########
    
    move_restriction, want_to_move_again = move_piece.move_again(end_location)
    # if player confirms they wish to activate the effects of a move again,
    # then allow them to
    if want_to_move_again:
        continue     

    # the player has ended their turn
    turn_end = True
    #perform item pickups after moving
    move_piece.check_item_pickups()
    
    #pause_me = input("Continue?")
    #if pause_me == " ":
    #    board.print_all_tile_info(True);
        
    #################################################################################
    #                                                                               #
    #       DEBUG END MOVE TEST HERE                                                #
    #                                                                               #
    #################################################################################



