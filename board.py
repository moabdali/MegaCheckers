import global_data
import tile
import piece


columns =       global_data.columns
rows =          global_data.rows
tile =          tile.tile
piece =         piece.piece

# the gameboard
gb = game_board = [[tile(r,c) for c in range(columns)] for r in range(rows)]

def print_all_tile_info():
    for row in game_board:
        for columnrow in row:
            columnrow.print_info()
            
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
    game_board[4][4].tile_height = 3
    game_board[0][0].tile_height = 2
    
    return game_board

def print_ascii_table():
    for row in range(0,rows):
        for column in range(0,columns):
            cur_tile = game_board[row][column]
            cur_piece = cur_tile.piece
            if cur_tile.occupied:
                if cur_piece.owned_by == "player_1":
                    print("[ply_1]",end="")
                    
                elif cur_piece.owned_by == "player_2":
                    print("[ply_2]",end="")
                    
                elif cur_piece.owned_by == "neutral":
                    print("[neut0]",end="")
                    
                else:
                    print("[error]",end="")
            #if not occupied
            else:
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
        print("")
        print("")
            


