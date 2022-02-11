import global_data
import tile
import piece
import random
import display

columns =       global_data.columns
rows =          global_data.rows
tile =          tile.tile
piece =         piece.piece

# the gameboard
game_board = [[tile(r,c) for c in range(columns)] for r in range(rows)]

# print information on each tile
def print_all_tile_info(detailed_info = False):
    for row in game_board:
        for each_tile in row:
            each_tile.print_info(detailed_info)

# set up the board by putting pieces on opposite ends            
def initialize_start():
    #player1
    for row in range(0,2):
        for column in range(0,columns):
            cur_tile = game_board[row][column] = (tile(row, column))
            cur_piece = cur_tile.piece = piece( start_location = (row, column))
            cur_tile.occupied = True
            cur_piece.owned_by = "player_1"
            cur_tile.tile_type = "default"
            
    #player2
    for row in range(rows-1,rows-3,-1):
        for column in range(0,columns):
            #create and initialize a new blank tile and assign its location
            cur_tile = game_board[row][column] = tile(row, column)
            #set the current piece to the tile we're working with
            cur_piece = cur_tile.piece = piece( start_location = (row, column))
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

    #destroy random spots for practice
    rand_row = random.randint(0, rows-1)
    rand_col = random.randint(0, columns-1)
    random_damage = random.choice(global_data.damaged_floor)
    game_board[rand_row][rand_col].tile_type = random_damage
    game_board[rand_row][rand_col].occupied = False
    game_board[1][0].piece.active_buffs.append("move_diagonal")
    print("Appending move_diagonal")
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
def verify_location_data():
    for row_index, row in enumerate(game_board):
        for col_index, each_tile in enumerate(row):
            #verify tile's location
            if (each_tile.start_location[0] != row_index or
                each_tile.start_location[1] != col_index):
                print("MISMATCH OF REPORTED LOCATION AND ACTUAL LOCATION.  UPDATED.")
                each_tile.start_location[0] = row_index
                each_tile.start_location[1] = col_index
            #verify each piece's location, only if a piece is there
            if (each_tile.piece):
                if each_tile.occupied == False:
                    print(f"""Piece exists at location {row_index},{col_index}, but is
reported unoccupied.  Updating status.""")
                    each_tile.occupied = True
                if (each_tile.piece.x_location != row_index or
                    each_tile.piece.y_location != col_index):
                    print(f"""Piece's self reported location {each_tile.piece.x_location},
{each_tile.piece.y_location} doesn't match the true location {row_index},{col_index}.  Updating.""")
                    each_tile.piece.x_location = row_index
                    each_tile.piece.y_location = col_index
                    
#find and list all fully empty tiles
def find_empty_tiles():
    empty_tiles = []
    for row_index, row in enumerate(game_board):
        for col_index, each_tile in enumerate(row):
            if each_tile.occupied == False and each_tile.tile_type == "default":
                empty_tiles.append(each_tile.start_location)

    return empty_tiles


#find the current turn piece (if any)
def find_current_turn_pieces():
    found_current_turn_pieces = []
    for row_index, row in enumerate(game_board):
        for col_index, each_tile in enumerate(row):
            cur_piece = each_tile.piece
            if cur_piece and cur_piece.current_turn_piece and cur_piece.owned_by == global_data.current_player_turn:
                found_current_turn_pieces.append( (cur_piece.x_location, cur_piece.y_location))
    return found_current_turn_pieces
