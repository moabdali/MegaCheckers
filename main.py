################################################################################
# Changelog:
# Date............Author.......Change
# 2022-Feb-04.....moabdali.....Initial Version
# 2022-Feb-05.....moabdali.....Added item pickups, item orb generation
# 2022-Feb-06.....moabdali.....Added some calls to between_turns functions
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


columns     =   global_data.columns
rows        =   global_data.rows

game_board  = board.initialize_start()

    ############################################################################
    #                                                                          #
    #       DEBUG MOVE TEST HERE                                               #
    #                                                                          #
    ############################################################################

#set all the pieces to have a false current turn; this is a catch all for in case
#I forgot to reset it elsewhere in the game
for row in game_board:
    for tile in row:
        if tile.occupied == True:
            tile.piece.current_turn_piece = False

#modify starting pieces
game_board[0][0].piece.active_buffs.append("move again")
game_board[0][0].piece.move_distance_max = 3
#game_board[rows-1][columns - 1].piece.active_buffs.append("move again")
#end modify starting pieces
move_piece.check_if_piece_fell()
board.verify_location_data()
between_turns.reset_moves_left(game_board)
print(game_board[0][0].piece.move_distance_max)
print("moves left externally set to " , game_board[0][0].piece.moves_left)
while True:
    board.print_ascii_table()
    print(global_data.current_player_turn,"'s turn.")
    print("Turn # ", global_data.turn_count)
    
    #check to make sure any wayward item orbs are picked up on a given player's
    #turn.  This normally wouldn't occur, but a shuffler item may cause this to
    #occur.  Game logic dictates that picking up orbs can only be done on your
    #turn, but cannot make you waste a turn on their own.
    move_piece.check_item_pickups()
    

    #if this is the first time a piece has moved this turn
    if global_data.move_restriction == False:
        start_location = []
        try:
            start_location.append( int(input("start row >>")) )
            if start_location[0] == 99:
                board.print_all_tile_info(True);
                continue
            start_location.append( int(input("start col >>")) )
        except ValueError:
            print("Not an integer.")
            continue

    #if a piece has moved already and is eligible for another move
    else:
        start_location = global_data.current_turn_piece_location
        print("Start location is", start_location)
        
    if not move_piece.select_piece(start_location):
        continue

    try:
        #reset here because we don't want to keep appending
        end_location = []
        end_location.append( int(input("end row >>")) )
        if end_location[0] == 99:
            board.print_all_tile_info(True);
            continue
        end_location.append( int(input("end col >>")) )
    except ValueError:
        print("Not an integer.")
        continue

    if not move_piece.move_piece( start_location , end_location ):
        continue

    #check for moving again
    ###########
    # DEBUG: need to do something with current turn piece
    ###########
    x = end_location[0]
    y = end_location[1]
    
    if game_board[x][y].piece:
        print("Test 1")
        #make sure that piece belongs to you
        if game_board[x][y].piece.owned_by == global_data.current_player_turn:
            print("Test 2")
            #does the piece have an item that may let it move again
            print("Test 3")
            if ("berzerker" in game_board[x][y].piece.active_buffs or
                "move again" in game_board[x][y].piece.active_buffs):
                #if they have more than 0 moves left
                print("Test 4")
                print(game_board[x][y].piece.moves_left)
                if (game_board[x][y].piece.moves_left > 0):
                    move_again_prompt = input("YOU CAN MAKE ANOTHER MOVE. Y/N")
                    if move_again_prompt in ('Y', 'y', "yes", "Yes"):
                        move_restriction = True
                        global_data.current_turn_piece_location[0] = game_board[x][y].piece.x_location
                        global_data.current_turn_piece_location[1] = game_board[x][y].piece.y_location
                        
                        continue
            
            
    
    #perform item pickups after moving
    move_piece.check_item_pickups()
    
    pause_me = input("Continue?")
    if pause_me == " ":
        board.print_all_tile_info(True);
        
    # mark piece as having moved as the current turn piece
    x = end_location[0]
    y = end_location[1]
    if game_board[x][y].piece:
        game_board[x][y].piece.current_turn_piece = True
        
    global_data.turn_count += 1
    
    items.generate_item_orbs()
    print(items.items)
    between_turns.repair_floor(game_board)
    between_turns.switch_turns()
    between_turns.count_pieces(game_board)
    between_turns.set_current_turn_piece_to_false(game_board)
    board.verify_location_data()
    move_piece.check_if_piece_fell()
    global_data.move_restriction = False
    between_turns.reset_moves_left(game_board)
    #################################################################################
    #                                                                               #
    #       DEBUG END MOVE TEST HERE                                                #
    #                                                                               #
    #################################################################################
    
