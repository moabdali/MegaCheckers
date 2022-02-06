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
from    playsound import playsound
import  global_data

# playsound is an unreliable module; since sound isn't a necessity, we can
# try/catch it easily without any downside; a period  is used for debugging
def playSoundExceptionCatcher(fileName, block = True):
    try:
        playsound(fileName, block)
    except:
        print("*")

#the floor repairs itself a little each turn
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

#swap turns
def switch_turns(game_board = None):
    # stuff that happens between turns
    if global_data.current_player_turn == "player_1":
        global_data.current_player_turn = "player_2"
    else:
        global_data.current_player_turn = "player_1"



# how many pieces does each player have left?
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
    if player1count == 0:
        print("Player 2 wins.")
        input("Hit enter to exit.")
        raise SystemExit
    if player2count == 0:
        print("Player 1 wins.")
        input("Hit enter to exit.")
        raise SystemExit


def set_current_turn_piece_to_false(game_board):
    #set all the pieces to have a false current turn; this is a catch all for in
    #case I forgot to reset it elsewhere in the game
    
    for row in game_board:
        for each_tile in row:
            if each_tile.piece:
                each_tile.piece.current_turn_piece = False
