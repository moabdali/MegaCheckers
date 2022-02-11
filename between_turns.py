################################################################################
# between_turns - collection of functions intended to run between each turn
# CHANGELOG:
#   DATE            AUTHOR      CHANGES
#   2022-Feb-05     moabdali    initial creation
#   2022-Feb-06     moabdali    added checks for damaged floor
#
################################################################################

import  PySimpleGUI as sg
import  random
#from    playsound import playsound
import  global_data
import  board

# playsound is an unreliable module; since sound isn't a necessity, we can
# try/catch it easily without any downside; a period  is used for debugging
##def playSoundExceptionCatcher(fileName, block = True):
##    try:
##        playsound(fileName, block)
##    except:
##        print("*")

################################################################################
# @brief repair_floor the tiles repair themselves a little each turn (1 step)
# @param[in,out] game_board the playing field; used to see current damage and
#                   update the damage level to the next lower step each time
################################################################################
def repair_floor(game_board):
    for row in game_board:
        for each_tile in row:
            if each_tile.tile_type == "destroyed":
                each_tile.tile_type = "damaged8"
            elif each_tile.tile_type == "damaged8":
                each_tile.tile_type = "damaged7"
            elif each_tile.tile_type == "damaged7":
                each_tile.tile_type = "damaged6"
            elif each_tile.tile_type == "damaged6":
                each_tile.tile_type = "damaged5"
            elif each_tile.tile_type == "damaged5":
                each_tile.tile_type = "damaged4"
            elif each_tile.tile_type == "damaged4":
                each_tile.tile_type = "damaged3"
            elif each_tile.tile_type == "damaged3":
                each_tile.tile_type = "damaged2"
            elif each_tile.tile_type == "damaged2":
                each_tile.tile_type = "damaged1"
            elif each_tile.tile_type == "damaged1":
                each_tile.tile_type = "default"
                each_tile.tile_height = 0
                
################################################################################
# @brief switch_turns change the current term to the opposite player's turn
################################################################################
def switch_turns():
    # stuff that happens between turns
    if global_data.current_player_turn == "player_1":
        global_data.current_player_turn = "player_2"
    else:
        global_data.current_player_turn = "player_1"


################################################################################
# @brief count_pieces how many pieces does each player have left? For display
#                       and for determining if the game is over
# @param[in] game_board we're counting the the number of pieces on the board
################################################################################
def count_pieces(game_board = None):
    player1count = 0
    player2count = 0
    for row in game_board:
        for each_tile in row:
            if each_tile.piece:
                if each_tile.piece.owned_by == "player_1":
                    player1count += 1
                elif each_tile.piece.owned_by == "player_2":
                    player2count += 1
    print("Player 1 pieces: ", player1count)
    print("Player 2 pieces: ", player2count)
    
    if player1count > 0 and player2count > 0:
        return
    # if control reaches here, then there is at least one loser
    
    # technically should only be "==0", but just to be safe we'll catch
    # negatives by using <= 0
    elif player1count <= 0 and player2count > 0:
        print("Player 2 wins.")
    elif player2count <= 0 and player1count > 0:
        print("Player 1 wins.")
    elif (player1count <= 0 and player2count <= 0):
        print("You both suck apparently - both players lost")
    input("Hit enter to exit.")
    raise SystemExit

################################################################################
# @brief set_current_turn_piece_to_false set all the pieces to have a false
#                                           current turn; this is a catch all
#                                           for a case where I might have
#                                           forgotten to reset it elsewhere in
#                                           the game
# @param[in,out] game_board checks for pieces and then sets them as not having
#                               made a move yet (this is a fail safe)
################################################################################
def set_current_turn_piece_to_false(game_board):
    for row in game_board:
        for each_tile in row:
            if each_tile.piece:
                each_tile.piece.current_turn_piece = False




def reset_moves_left(gb):
    for r_index, row in enumerate(gb):
        for tile_index, each_tile in enumerate(row):
            if each_tile.piece:
                if each_tile.piece.move_distance_max > 1:
                    #print("MOVE MAX IS",  gb[r_index][tile_index].piece.move_distance_max)
                    gb[r_index][tile_index].piece.moves_left = gb[r_index][tile_index].piece.move_distance_max
                    #print("moves left internally set to ",gb[r_index][tile_index].piece.moves_left)
