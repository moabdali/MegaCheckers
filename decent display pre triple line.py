# display
# 2022-Feb-08 moabdali  module for printing ascii version of game board
#                       improved display by making bigger "blocks"; opens
#                       possibility for more information

def print_ascii_board(game_board, rows, columns):
    print("      0      1      2      3      4      5      6      7      8      9")
        format_index = 0
    for row in range(0,rows):
        line_1 = ""
        line_2 = ""
        line_3 = ""
        
        print("    _____  _____  _____  _____  _____  _____  _____  _____  _____  _____")
        print("   |     ||     ||     ||     ||     ||     ||     ||     ||     ||     |")

        print(f" {row} ", end = "")
        for column in range(0,columns):
            cur_tile = game_board[row][column]
            cur_piece = cur_tile.piece
            
 # if there is a piece on the tile, display the piece
            if cur_tile.occupied:
                if cur_piece.owned_by == "player_1":
                    if len(cur_piece.stored_items) > 0:
                        print("|PLY_1|",end="")
                    else:
                        print("|ply_1|",end="")
                    
                elif cur_piece.owned_by == "player_2":
                    if len(cur_piece.stored_items) > 0:
                        print("|PLY_2|",end="")
                    else:
                        print("|ply_2|",end="")
                    
                elif cur_piece.owned_by == "neutral":
                    print("|neut0|",end="")
                    
                else:
                    print("|error|",end="")
 # if the tile is not occupied, show modifiers (or default)
            else:
                #if completely empty, just show the height
                if cur_tile.tile_type == "default":
                    if cur_tile.tile_height == -3:
                        print("|-----|",end="")
                    elif cur_tile.tile_height == -2:
                        print("| --- |",end="")
                    elif cur_tile.tile_height == -1:
                        print("|  -  |",end="")
                    elif cur_tile.tile_height == 0:
                        print("|     |",end="")
                    elif cur_tile.tile_height == 1:
                        print("|  +  |",end="")
                    elif cur_tile.tile_height == 2:
                        print("| +++ |",end="")
                    elif cur_tile.tile_height == 3:
                        print("|+++++|",end="")
                    else:
                        print("|?????|",end="")
                        
                #damaged ground display        
                if cur_tile.tile_type == "destroyed":
                    print("|XXXXX|",end="")
                elif cur_tile.tile_type == "damaged8":
                    print("|XX8XX|",end="")
                elif cur_tile.tile_type == "damaged7":
                    print("|XX7XX|",end="")
                elif cur_tile.tile_type == "damaged6":
                    print("|XX6XX|",end="")
                elif cur_tile.tile_type == "damaged5":
                    print("|XX5XX|",end="")
                elif cur_tile.tile_type == "damaged4":
                    print("|XX4XX|",end="")
                elif cur_tile.tile_type == "damaged3":
                    print("|XX3XX|",end="")
                elif cur_tile.tile_type == "damaged2":
                    print("|XX2XX|",end="")
                elif cur_tile.tile_type == "damaged1":
                    print("|XX1XX|",end="")
                    
                #if an item_orb
                elif cur_tile.tile_type == "item_orb":
                    print("|<<#>>|",end="")
        print("")
        
        if row != rows:
            print("   |_____||_____||_____||_____||_____||_____||_____||_____||_____||_____|")
            print("      0      1      2      3      4      5      6      7      8      9")

