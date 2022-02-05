import global_data
import board

game_board =    board.game_board
columns =       global_data.columns
rows =          global_data.rows

def getColumn(location, game_board, grow_range = False, include_self = True):
    validLocations = []
    if grow_range == False:
        for i in range(len(game_board)):
            validLocations.append( (i, location[1]) )
    print("column test", validLocations)
    return validLocations

def getRow(location, game_board,grow = False, include_self = True):
    validLocations = []
    if grow == False:
        for i in range(len(game_board[0])):
            validLocations.append( (location[0], i))
    print("row test", validLocations)
    return validLocations

def getRadial(location, game_board, grow = False, include_self = True):
    validLocations = []
    rows = len(game_board)
    columns = len(game_board[0])

    if grow == False:
        # check if you can go one row up
        if location[0] - 1 != -1:
            # check if you can also go left after going up (only false if you're in the top left corner)
            if location[1] - 1 != -1:
                validLocations.append((location[0] - 1, location[1] - 1))
            # one row up (guaranteed already)
            validLocations.append((location[0] - 1, location[1] + 0))
            # check if you can also go right after going up (only false if you're in the top right corner)
            if location[1] + 1 != columns:
                validLocations.append((location[0] - 1, location[1] + 1))
        # check if you can go left
        if location[1] - 1 != -1:
            validLocations.append((location[0], location[1] - 1))
        # you are guaranteed to append yourself
        validLocations.append((location[0], location[1]))
        # check if you can go right
        if location[1] + 1 != columns:
            validLocations.append((location[0], location[1] + 1))
        # check if you can go down
        if location[0] + 1 != rows:
            # check bottom left
            if location[1] - 1 != -1:
                validLocations.append((location[0] + 1, location[1] - 1))
            # bottom guaranteed
            validLocations.append((location[0] + 1, location[1]))
            # check bottom right
            if location[1] + 1 != columns:
                validLocations.append((location[0] + 1, location[1] + 1))
    print("radial", validLocations)
    return validLocations



getRadial( (9,9), game_board)
