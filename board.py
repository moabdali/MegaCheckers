################################################################################
# Changelog:
# Date............Author.......Change
# 2022-Feb-05.....moabdali.....Initial Version
# 2022-Feb-16.....moabdali.....added some "current turn piece" logic to keep
#                               track of the current turn piece even after
#                               shuffling; and also to try to recover from
#                               a bad current turn check (none or many pieces)
################################################################################

import random

import display
import global_data
import piece
import tile

columns = global_data.columns
rows = global_data.rows
tile = tile.Tile
piece = piece.Piece

# the game_board
game_board = [[tile(r, c) for c in range(columns)] for r in range(rows)]


# print information on each tile
def print_all_tile_info(detailed_info=False):
    for row in game_board:
        for each_tile in row:
            each_tile.print_info(detailed_info)


# set up the board by putting pieces on opposite ends            
def initialize_start():
    # player1
    for row in range(0, 2):
        for column in range(0, columns):
            cur_tile = game_board[row][column] = (tile(row, column))
            cur_piece = cur_tile.piece = piece(start_location=(row, column))
            cur_tile.occupied = True
            cur_piece.owned_by = "player_1"
            cur_tile.tile_type = "default"
            
    # player2
    for row in range(rows-1, rows-3, -1):
        for column in range(0, columns):
            # create and initialize a new blank tile and assign its location
            cur_tile = game_board[row][column] = tile(row, column)
            # set the current piece to the tile we're working with
            cur_piece = cur_tile.piece = piece(start_location=(row, column))
            cur_tile.occupied = True
            cur_piece.owned_by = "player_2"
            cur_tile.tile_type = "default"

    #################################################################################
    #                                                                               #
    #       DEBUG BOARD MODIFIERS HERE                                              #
    #                                                                               #
    #################################################################################
    game_board[rows//2][columns//2].tile_height = 3
    game_board[0][0].tile_height = 2

    # destroy random spots for practice
    rand_row = random.randint(0, rows-1)
    rand_col = random.randint(0, columns-1)
    random_damage = random.choice(global_data.damaged_floor)
    game_board[rand_row][rand_col].tile_type = random_damage
    game_board[rand_row][rand_col].occupied = False
    game_board[1][0].piece.active_buffs.append("move_diagonal")
    game_board[8][1].piece.active_buffs.append("move_diagonal")
    #################################################################################
    #                                                                               #
    #       END DEBUG BOARD MODIFIER                                                #
    #                                                                               #
    #################################################################################
    
    return game_board


# display the table in text form
def print_ascii_table():
    display.print_ascii_board(game_board, rows, columns)
    

# make sure that location info for each tile is properly reported
def verify_location_data(expected=False):
    changes_occurred = False
    for row_index, row in enumerate(game_board):
        for col_index, each_tile in enumerate(row):
            # verify tile's location
            if (each_tile.start_location[0] != row_index or
                    each_tile.start_location[1] != col_index):
                changes_occurred = True
                if not expected:
                    print("MISMATCH OF REPORTED LOCATION AND ACTUAL LOCATION.  UPDATED.")
                each_tile.start_location[0] = row_index
                each_tile.start_location[1] = col_index
            # verify each piece's location, only if a piece is there
            if each_tile.piece:
                if not each_tile.occupied:
                    changes_occurred = True
                    if not expected:
                        print(f"""Piece exists at location {row_index},{col_index}, but is
reported unoccupied.  Updating status.""")
                    each_tile.occupied = True
                if (each_tile.piece.x_location != row_index or
                        each_tile.piece.y_location != col_index):
                    changes_occurred = True
                    if not expected:
                        print(f"""Piece's self reported location {each_tile.piece.x_location},
{each_tile.piece.y_location} doesn't match the true location {row_index},{col_index}.  Updating.""")
                    each_tile.piece.x_location = row_index
                    each_tile.piece.y_location = col_index
                if each_tile.occupied and not each_tile.piece:
                    print("Listed as occupied, but nothing there.  This is bad!")
                    each_tile.occupied = False
    if changes_occurred and expected:
        print("updated location info :)")


# find and list all fully empty tiles
def find_empty_tiles():
    empty_tiles = []
    for row_index, row in enumerate(game_board):
        for col_index, each_tile in enumerate(row):
            if not each_tile.occupied and each_tile.tile_type == "default":
                if (not each_tile.secret_agent and
                        not each_tile.item_orb):
                    empty_tiles.append(each_tile.start_location)
    return empty_tiles


# find the current turn piece (if any)
def find_current_turn_pieces():
    found_current_turn_pieces = []
    for row_index, row in enumerate(game_board):
        for col_index, each_tile in enumerate(row):
            cur_piece = each_tile.piece
            if cur_piece and cur_piece.current_turn_piece and cur_piece.owned_by == global_data.current_player_turn:
                found_current_turn_pieces.append([cur_piece.x_location, cur_piece.y_location])
    if len(found_current_turn_pieces) != 1:
        print("Error with current turn piece...")
        print("""Report this glitch.  In the meantime, be honest and tell us\
the row of the piece that moved, then the column.""")
        found_current_turn_pieces = []
        x = input("row ")
        y = input("column ")
        found_current_turn_pieces.append([x, y])
        
    if len(found_current_turn_pieces) == 1:
        global_data.current_turn_piece_location = found_current_turn_pieces[0]
    else:
        print("There is not exactly one location. This is bad.")
    # print("Current turn piece result: ", found_current_turn_pieces)
    # print("Globalcurrentpieceloc: ", global_data.current_turn_piece_location)
    return found_current_turn_pieces
