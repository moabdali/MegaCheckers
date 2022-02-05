import  global_data
from    tile import tile
from    piece import piece
import  board
import  move_piece
import  PySimpleGUI as sg

game_board  =   board.game_board
columns     =   global_data.columns
rows        =   global_data.rows

game_board = board.initialize_start()
board.print_ascii_table()


    #################################################################################
    #                                                                               #
    #       DEBUG MOVE TEST HERE                                                    #
    #                                                                               #
    #################################################################################

start_location = (0,0)
end_location = (4,4)

move_piece.move_piece( start_location , end_location )

print("")
board.print_ascii_table()


start_location = (4,4)
end_location = (0,0)

move_piece.move_piece( start_location , end_location )
board.print_ascii_table()

print("")

#board.print_all_tile_info()

    #################################################################################
    #                                                                               #
    #       DEBUG END MOVE TEST HERE                                                #
    #                                                                               #
    #################################################################################
    
