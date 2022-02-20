################################################################################
#   distances
#   DATE............NAME.........CHANGE
#   2022-Feb-09.....moabdali.....created initial file
#   2022-Feb-10.....moabdali.....added vertical and horizontal checking
#                                added textual representation of highlight map
#                                added distance limitation for normal
#                                      and move diagonal
#   2022-Feb-11.....moabdali.....began working on selective 'highlighting'
################################################################################
import board
import global_data

game_board = board.game_board


class RangeObject:
    """
    A class containing info that helps determine valid tile targets

    ...
    Attributes
    ----------
    location: set
        (row, column) coordinate of the originating tile
    include_self: bool
        whether the originating tile should be allowed as a target
    rows : int
        maximum rows
    columns: int
        maximum columns
    target_type: str
        which type of tiles should be highlighted (e.g. "enemies", "all")

    Methods
    -------
    reset_list()
        resets the target list to get rid of old data

    """

    def __init__(self,
                 location,
                 include_self,
                 rows,
                 columns,
                 target_type):
        """
        Constructs all relevant attributes; already explained above
        """
        self.location = location
        self.target_type = target_type
        self.include_self = include_self
        self.rows = rows
        self.columns = columns
        self.target_list = []

    def reset_list(self):
        """
        reset the target_list so that old data isn't mixed in
        """
        self.target_list = []


# print out the board, showing what the range of the unit is
def preview_range(range_object, start_piece):
    if start_piece.move_type == "radial":
        radial(range_object)
    elif start_piece.move_type == "cross":
        cross(range_object)
    else:
        range_object.reset_list()

    print_distances(range_object)


def self_check(range_object):
    """
    check to see if the self tile should be included; also runs a simple
    de-duplication check to avoid errors.  Runs the validate_tile helper
    function to see if the tile passes a type filter.
    """
    if range_object.include_self:
        if range_object.target_type in ("all", "self", "allies", "enemies"):
            if range_object.location not in range_object.target_list:
                validate_value = validate_tile(range_object, range_object.location)
                if validate_value:
                    range_object.target_list.append(validate_value)
    return False


def validate_tile(range_object, target_tile):
    """
    validates whether a given tile is able to pass through a specific filter.
    For example, if "enemies" is selected, only tiles containing enemies will
    be returned as valid.  If "empty" is selected, then only empty tiles will
    be returned.  If "all" is selected, then all tiles will be applicable (be
    very careful with this one)
    """
    x = target_tile[0]
    y = target_tile[1]
    # print("Target tile is", target_tile)
    if range_object.target_type == "all":
        # range_object.target_list.append(target_tile)
        # print("returning target tile: ", target_tile)
        return target_tile
    elif range_object.target_type == "allies":
        if game_board[x][y].piece:
            if game_board[x][y].piece.owned_by == global_data.current_player_turn:
                # range_object.target_list.append(target_tile)
                return target_tile
    elif range_object.target_type == "enemies":
        if game_board[x][y].piece:
            if game_board[x][y].piece.owned_by != global_data.current_player_turn:
                # range_object.target_list.append(target_tile)
                return target_tile
    elif range_object.target_type == "empty":
        if (not game_board[x][y].piece and
                game_board[x][y].tile_type == "default"):
            return target_tile
    else:
        input("There's an error with your target type.")


def up(range_object):
    test_location = (range_object.location[0] - 1,
                     range_object.location[1])
    if test_location[0] < 0:
        # print("Can't go up: ", test_location[0])
        pass
    else:
        # print("Testing up")
        if validate_tile(range_object, test_location):
            return test_location


def down(range_object):
    test_location = (range_object.location[0] + 1,
                     range_object.location[1])
    if test_location[0] >= range_object.rows:
        # print("Can't go down: ", test_location[0])
        pass
    else:
        # print("Testing down")
        if validate_tile(range_object, test_location):
            return test_location


def left(range_object):
    test_location = (range_object.location[0],
                     range_object.location[1] - 1)
    if test_location[1] < 0:
        # print("Can't go left: ", test_location[1])
        pass
    else:
        # print("Testing left", test_location)
        if validate_tile(range_object, test_location):
            # print("left passed!")
            return test_location


def right(range_object):
    test_location = (range_object.location[0],
                     range_object.location[1] + 1)
    if test_location[1] >= range_object.columns:
        # print("Can't go right: ", test_location[1])
        pass
    else:
        # print("Testing right", test_location)
        if validate_tile(range_object, test_location):
            # print("Right passed!")
            return test_location


def up_left(range_object):
    test_location = (range_object.location[0] - 1,
                     range_object.location[1] - 1)
    if test_location[0] < 0:
        # print("Can't go [up] left: ", test_location[0])
        return None

    if \
            test_location[1] < 0:
        # print("Can't go up [left]: ", test_location[1])
        return None

    else:
        # print("Testing up left", test_location)
        if validate_tile(range_object, test_location):
            # print("up left passed!")
            return test_location


def down_left(range_object):
    test_location = (range_object.location[0] + 1,
                     range_object.location[1] - 1)
    if test_location[0] >= range_object.rows:
        # print("Can't go [down] left: ", test_location[0])
        return None

    if test_location[1] < 0:
        # print("Can't go down [left]: ", test_location[1])
        return None

    else:
        # print("Testing down left", test_location)
        if validate_tile(range_object, test_location):
            # print("down left passed!")
            return test_location


def up_right(range_object):
    test_location = (range_object.location[0] - 1,
                     range_object.location[1] + 1)
    if test_location[0] < 0:
        # print("Can't go [up] right: ", test_location[0])
        return None

    if test_location[1] >= range_object.columns:
        # print("Can't go up [right]: ", test_location[1])
        return None

    else:
        # print("Testing up right", test_location)
        if validate_tile(range_object, test_location):
            # print("up right passed!")
            return test_location


def down_right(range_object):
    test_location = (range_object.location[0] + 1,
                     range_object.location[1] + 1)
    if test_location[0] >= range_object.rows:
        # print("Can't go [down] right: ", test_location[0])
        return None

    if test_location[1] >= range_object.columns:
        # print("Can't go down [right]: ", test_location[1])
        return None

    else:
        # print("Testing down right", test_location)
        if validate_tile(range_object, test_location):
            # print("down right passed!")
            return test_location


def cross(range_object):
    """
    Special function for finding a cross shaped set of tiles.
    Calls on up, left, down, right [and self if enabled] to get a plus shape
    """
    up_value = up(range_object)
    if up_value:
        range_object.target_list.append(up_value)

    down_value = down(range_object)
    if down_value:
        range_object.target_list.append(down_value)

    right_value = right(range_object)
    if right_value:
        range_object.target_list.append(right_value)

    left_value = left(range_object)
    if left_value:
        range_object.target_list.append(left_value)

    if range_object.include_self:
        self_value = self_check(range_object)
        # print("self_value in cross is: ", self_value)
        if self_value:
            range_object.target_list.append(self_value)


def diagonals(range_object):
    """
    Special function for getting an X shaped set of tiles touching the
    corners of the central tile.  The center will be included only if
    include_self within range_object is set to true; otherwise will be skipped.
    """
    up_left_values = up_left(range_object)
    # print("ULV: ",up_left_values)
    if up_left_values:
        range_object.target_list.append(up_left_values)

    down_left_values = down_left(range_object)
    # print("DLV: ",down_left_values)
    if down_left_values:
        range_object.target_list.append(down_left_values)

    up_right_values = up_right(range_object)
    # print("URV: ",up_right_values)
    if up_right_values:
        range_object.target_list.append(up_right_values)

    down_right_values = down_right(range_object)
    # print("DRV: ",down_right_values)
    if down_right_values:
        range_object.target_list.append(down_right_values)

    if range_object.include_self:
        self_value = self_check(range_object)
        # print("self_value in diagonal is: ", self_value)
        if self_value:
            range_object.target_list.append(self_value)


def radial(range_object):
    """
    a combination of diagonals and cross, gets all adjacent tiles that
    meet the filter requirement.  Makes a 3x3 square search if include_self
    is set to true (within the range_object).
    """
    diagonals(range_object)
    cross(range_object)
    if range_object.include_self:
        self_value = self_check(range_object)
        # print("self_value in radial is: ", self_value)
        if self_value:
            range_object.target_list.append(self_value)


def vertical(range_object):
    """
    Finds all valid tiles within the selected tile's column
    """
    for row in range(0, range_object.rows):
        if range_object.location[0] != row:
            # print("ro.location0 is ", range_object.location[0])
            test_location = (row,
                             range_object.location[1])
            # print("test_location is", test_location);
            if validate_tile(range_object, test_location):
                # print("vertical")
                range_object.target_list.append(test_location)

    if range_object.include_self:
        self_value = self_check(range_object)
        # print("self_value in vertical is: ", self_value)
        if self_value:
            range_object.target_list.append(self_value)


def horizontal(range_object):
    """
    Finds all valid tiles within the selected tile's row
    """
    for column in range(0, range_object.columns):
        if range_object.location[1] != column:
            # print("ro.location1 is ", range_object.location[1])
            test_location = (range_object.location[0],
                             column)
            # print("test_location is", test_location);
            if validate_tile(range_object, test_location):
                # print("horizontal")
                range_object.target_list.append(test_location)

    if range_object.include_self:
        self_value = self_check(range_object)
        # print("self_value in horizontal is: ", self_value)
        if self_value:
            range_object.target_list.append(self_value)


def print_distances(range_object, action_type=None):
    """
    show all locations that were put within the list
    (mostly for debugging really
    """
    try:
        x = range_object.location[0]
        y = range_object.location[1]
    except:
        print("***bad location data.  Aborting map display.***")
        return
    mover_perks = []
    # if a piece exists, find what buffs it has
    if game_board[x][y].piece:
        mover_perks = game_board[x][y].piece.active_buffs
    # print("Valid locations: ",range_object.target_list)
    row_index = 0
    print("     0   ||   1   ||  2    ||   3   ||   4   ||   5   ||   6   ||  7    ||   8   ||   9   |")
    for i in range(range_object.rows):
        print(row_index, end="")
        for j in range(range_object.columns):
            # if a piece is within range
            if (i, j) in range_object.target_list:
                if game_board[i][j].piece:
                    # if piece belongs to the player
                    if (game_board[i][j].piece.owned_by ==
                            global_data.current_player_turn):
                        if "cannibalism" in mover_perks:
                            print("[[ally ]]", end="")
                        else:
                            print("|*ally *|", end="")
                    else:
                        print("[[enemy]]", end="")

                # put in different tile types here#
                elif game_board[i][j].tile_type == "default":
                    # if the tile is within range of the player and unoccupied
                    if game_board[i][j].secret_agent:
                        if (game_board[i][j].secret_agent ==
                                global_data.current_player_turn):
                            print("[*spy:)*]", end="")
                        else:
                            print("[[spy:(]]", end="")

                    elif game_board[i][j].item_orb:
                        print("[[item ]]", end="")
                    elif game_board[i][j].trap_orb:
                        print("[[item*]]", end="")
                    else:
                        print("[[     ]]", end="")

                elif (game_board[i][j].tile_type in ("damaged1",
                                                     "damaged2",
                                                     "damaged3",
                                                     "damaged4",
                                                     "damaged5",
                                                     "damaged6",
                                                     "damaged7",
                                                     "damaged8",
                                                     "destroyed"
                                                     )):
                    print("[[dmged]]", end="")

                else:
                    print("[[error]]", end="")

            # if piece is not within range
            else:
                if (game_board[i][j].tile_type in ("damaged1",
                                                     "damaged2",
                                                     "damaged3",
                                                     "damaged4",
                                                     "damaged5",
                                                     "damaged6",
                                                     "damaged7",
                                                     "damaged8",
                                                     "destroyed"
                                                     )):
                    print("| dmged |", end="")
                elif game_board[i][j].piece:
                    if (game_board[i][j].piece.owned_by ==
                            global_data.current_player_turn):
                        # the action_type check is to prevent 0,0 from being highlighted
                        # when viewing the map (the default is to set 0,0 as the active piece
                        if (i, j) == (x, y) and action_type != "view":
                            print("|(ally) |", end="")
                        else:
                            print("| ally  |", end="")
                    else:
                        print("| enemy |", end="")
                # an unoccupied tile that is not within range of movement
                elif game_board[i][j].tile_type == "default":
                    # print( "|       |", end="")
                    if game_board[i][j].secret_agent:
                        if (game_board[i][j].secret_agent ==
                                global_data.current_player_turn):
                            print("| spy:) |", end="")
                        else:
                            print("| spy:( |", end="")
                    elif game_board[i][j].item_orb:
                        print("| item  |", end="")
                    elif game_board[i][j].trap_orb:
                        print("| item* |", end="")
                    else:
                        print("|       |", end="")
                else:
                    print("| error |", end="")
        print(row_index)
        row_index+=1
    print("     0   ||   1   ||  2    ||   3   ||   4   ||   5   ||   6   ||  7    ||   8   ||   9   |")


def highlight_tiles(range_object, action_type=None):
    try:
        x = range_object.location[0]
        y = range_object.location[1]
    except:
        print("An error occurred while highlighting")
        return

    if not action_type:
        return
    # blue all
    if action_type == "neutral":
        pass

    # red enemies, grey all else
    elif action_type == "hurt_enemies":
        pass

    # blue empty spaces
    elif action_type == "truly_empty":
        pass

    # allies green, all else grey
    elif action_type == "help_allies":
        pass

    # allies green, enemies red
    elif action_type == "help_allies_hurt_enemies":
        pass

    # enemies green, all else grey
    elif action_type == "help_enemies":
        pass

    # allies red, all else grey
    elif action_type == "hurt_allies":
        pass
