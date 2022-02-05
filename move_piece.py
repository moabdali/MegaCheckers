import global_data
import board

gb          =   board.gb
columns     =   global_data.columns
rows        =   global_data.rows

def valid_move(start_location, end_location):

    #validate range
    if (    start_location[0] >= rows or end_location[1] >= rows or
            start_location[1] >= columns or end_location[1] >= columns or
            start_location[0] < 0 or end_location[0] < 0 or
            start_location[1] < 0 or end_location[1] < 0):
        print("SELECTED LOCATION IS OUTSIDE THE PLAYING FIELD")
        return False
    
    #find the tile that corresponds to the coordinates; must be done after
    #validating the range
    start_tile, end_tile = get_start_end_coords(start_location, end_location)

    #check if there's a piece; use both checks just in case
    if not start_tile.piece or not start_tile.occupied:
        print("NO PIECE HERE")
        if start_tile.piece or start_tile.occupied:
            print("""Additionally, an error occurred where piece status and
occupied status do not match.  Piece, occupied: """,
                  start_tile.piece, start_tile.occupied);
        return False
    
    #check if it's your piece
    if not start_tile.piece.owned_by == global_data.current_player_turn:
        print("NOT YOUR PIECE")
        return False

    #check if player is double clicking the same piece to open item menu
    if start_tile is end_tile:
        print("OPENING ITEM MENU")
        ##################################
        # DEBUG                          #
        # PUT IN ITEM FUNCTION           #
        ##################################

        #return False because you didn't actually move;
        #want to continue doing the make a move loop
        
        return False
    
    #check if ending location is your own piece
    if end_tile.piece and end_tile.piece.owned_by == global_data.current_player_turn:
        ###################################
        #  DEBUG                          #
        #  PUT IN A CHECK FOR CANNIBALISM #
        ###################################
        print("You can't kill your own piece!")
        return False
        
    if end_tile.piece and end_tile.piece.owned_by != global_data.current_player_turn:
        ################################
        #  DEBUG                       #
        #  TRY TO KILL ENEMY FUNCTION  #
        ################################
        print("Killed an enemy!")
        return True
        

    #if trying to jump up to a higher tile
    if (end_tile.tile_height - start_tile.tile_height >= 2 and
        "grappling_hook" not in start_tile.piece.active_buffs):
        print("Tile is way too high")
        return False
        
    return True

def move_piece(start_location, end_location):
    #gb = game_board
    if (valid_move(start_location, end_location)):
        start_tile, end_tile = get_start_end_coords(start_location, end_location)
        start_tile.occupied = False
        temp_piece = start_tile.piece
        start_tile.piece = None
        end_tile.piece = temp_piece
        end_tile.piece.x_location = end_location[0]
        end_tile.piece.y_location = end_location[1]
        end_tile.occupied = True
        print(end_tile.print_info())
    else:
        return False

def get_start_end_coords(start_location, end_location):
    return gb[start_location[0]][start_location[1]] , gb[end_location[0]][end_location[1]]
