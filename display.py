# display
# 2022-Feb-08 moabdali  module for printing ascii version of game board
#                       improved display by making bigger "blocks"; opens
#                       possibility for more information
# 2022-Feb-11 moabdali  Small change to show on print_ascii_board which pieces
#                       items or buffs active
# 2022-Feb-17 moabdali  Secret agent display logic

import global_data


def print_ascii_board(game_board, rows, columns):
    for row in range(0, rows):
        line_1 = ""
        line_2 = ""
        line_3 = ""

        line_1 += "   "
        for col in range(0, columns):
            line_1 += " __"
            line_1 += "\u0332" + str(col)
            line_1 += "__ "
        line_1 += "\n"
        line_1 += f"   "
        line_2 += f" {row} "
        line_3 += f"   "
        for column in range(0, columns):
            cur_tile = game_board[row][column]
            cur_piece = cur_tile.piece

            # if there is a piece on the tile, display the piece
            if cur_tile.occupied:
                if cur_piece.owned_by == "player_1":
                    # denotes has an item
                    if len(cur_piece.stored_items) > 0:
                        line_1 += "|PLY"
                        if len(cur_piece.active_buffs) > 0:
                            line_1 += "^1|"
                        else:
                            line_1 += "_1|"
                    # denotes has a buff
                    else:
                        line_1 += "|ply"
                        if len(cur_piece.active_buffs) > 0:
                            line_1 += "^1|"
                        else:
                            line_1 += "_1|"

                elif cur_piece.owned_by == "player_2":
                    # denotes has an item
                    if len(cur_piece.stored_items) > 0:
                        line_1 += "|PLY"
                        if len(cur_piece.active_buffs) > 0:
                            line_1 += "^2|"
                        else:
                            line_1 += "_2|"
                    # denotes has a buff
                    else:
                        line_1 += "|ply"
                        if len(cur_piece.active_buffs) > 0:
                            line_1 += "^2|"
                        else:
                            line_1 += "_2|"

                elif cur_piece.owned_by == "neutral":
                    line_1 += "|neut0|"

                else:
                    line_1 += "|E OCU|"
            # if not occupied, set the top row to unoccupied    
            else:
                line_1 += "|     |"

            # if unoccupied, just show the height
            if cur_tile.tile_type == "default":
                if cur_tile.tile_height == -3:
                    line_2 += "|-----|"
                elif cur_tile.tile_height == -2:
                    line_2 += "| --- |"
                elif cur_tile.tile_height == -1:
                    line_2 += "|  -  |"
                elif cur_tile.tile_height == 0:
                    line_2 += "|     |"
                elif cur_tile.tile_height == 1:
                    line_2 += "|  +  |"
                elif cur_tile.tile_height == 2:
                    line_2 += "| +++ |"
                elif cur_tile.tile_height == 3:
                    line_2 += "|+++++|"
                else:
                    line_2 += "|?????|"

            # Secret code here

            # damaged ground display
            elif cur_tile.tile_type == "destroyed":
                line_2 += "|XXXXX|"

            elif cur_tile.tile_type == "damaged8":
                line_2 += "|XX8XX|"

            elif cur_tile.tile_type == "damaged7":
                line_2 += "|XX7XX|"

            elif cur_tile.tile_type == "damaged6":
                line_2 += "|XX6XX|"

            elif cur_tile.tile_type == "damaged5":
                line_2 += "|XX5XX|"

            elif cur_tile.tile_type == "damaged4":
                line_2 += "|XX4XX|"

            elif cur_tile.tile_type == "damaged3":
                line_2 += "|XX3XX|"

            elif cur_tile.tile_type == "damaged2":
                line_2 += "|XX2XX|"

            elif cur_tile.tile_type == "damaged1":
                line_2 += "|XX1XX|"

            # if an item_orb
            if cur_tile.tile_type == "item_orb":
                line_3 += "|\u0332<\u0332<\u0332#\u0332>\u0332>|"
                line_2 += "|     |"
            elif cur_tile.tile_type == "secret agent":
                if not cur_tile.piece and cur_tile.secret_agent:
                    if cur_tile.secret_agent == global_data.current_player_turn:
                        line_3 += "|\u0332S\u0332P\u0332Y\u0332:\u0332)|"
                    else:
                        line_3 += "|\u0332S\u0332P\u0332Y\u0332:\u0332(|"
            # if not destroyed and not an item orb
            else:
                line_3 += "|_____|"

        print(line_1)
        print(line_2 + f" {row} ")
        print(line_3)
