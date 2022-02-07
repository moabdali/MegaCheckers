import global_data
import tile
import piece
import random

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
    return game_board

# display the table in text form
def print_ascii_table():
    print("      0      1      2      3      4      5      6      7      8      9")
    for row in range(0,rows):
        print(f" {row} ", end = "")
        for column in range(0,columns):
            cur_tile = game_board[row][column]
            cur_piece = cur_tile.piece
 # if there is a piece on the tile, display the piece
            if cur_tile.occupied:
                if cur_piece.owned_by == "player_1":
                    if len(cur_piece.stored_items) > 0:
                        print("[PLY_1]",end="")
                    else:
                        print("[ply_1]",end="")
                    
                elif cur_piece.owned_by == "player_2":
                    if len(cur_piece.stored_items) > 0:
                        print("[PLY_2]",end="")
                    else:
                        print("[ply_2]",end="")
                    
                elif cur_piece.owned_by == "neutral":
                    print("[neut0]",end="")
                    
                else:
                    print("[error]",end="")
 # if the tile is not occupied, show modifiers (or default)
            else:
                #if completely empty, just show the height
                if cur_tile.tile_type == "default":
                    if cur_tile.tile_height == -3:
                        print("[-----]",end="")
                    elif cur_tile.tile_height == -2:
                        print("[ --- ]",end="")
                    elif cur_tile.tile_height == -1:
                        print("[  -  ]",end="")
                    elif cur_tile.tile_height == 0:
                        print("[     ]",end="")
                    elif cur_tile.tile_height == 1:
                        print("[  +  ]",end="")
                    elif cur_tile.tile_height == 2:
                        print("[ +++ ]",end="")
                    elif cur_tile.tile_height == 3:
                        print("[+++++]",end="")
                    else:
                        print("[?????]",end="")
                        
                #damaged ground display        
                if cur_tile.tile_type == "destroyed":
                    print("[XXXXX]",end="")
                elif cur_tile.tile_type == "damaged8":
                    print("[XX8XX]",end="")
                elif cur_tile.tile_type == "damaged7":
                    print("[XX7XX]",end="")
                elif cur_tile.tile_type == "damaged6":
                    print("[XX6XX]",end="")
                elif cur_tile.tile_type == "damaged5":
                    print("[XX5XX]",end="")
                elif cur_tile.tile_type == "damaged4":
                    print("[XX4XX]",end="")
                elif cur_tile.tile_type == "damaged3":
                    print("[XX3XX]",end="")
                elif cur_tile.tile_type == "damaged2":
                    print("[XX2XX]",end="")
                elif cur_tile.tile_type == "damaged1":
                    print("[XX1XX]",end="")
                    
                #if an item_orb
                elif cur_tile.tile_type == "item_orb":
                    print("[<<#>>]",end="")
        print("")
        print("      0      1      2      3      4      5      6      7      8      9")
#    print("      0      1      2      3      4      5      6      7      8      9")


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
