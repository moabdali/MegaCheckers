# 2022-Feb-19.....moabdali.....Trap orb work, clear tile function
################################################################################

import PySimpleGUI as sg


class Tile:
    def __init__(self, x=0, y=0):
        if x and y:
            self.start_location = [x, y]
        else:
            self.start_location = [0, 0]
        # is there a piece on this tile?
        self.occupied = False
        # initialize to assume there are no pieces
        self.piece = None
        # default means exactly that: a plain tile
        self.tile_type = "default"
        # how high (or sunk) is the tile?  For now it's intended that the tile can
        # be at most 3 units tall, and 3 units sunk
        self.tile_height = 0
        # tiles can be destroyed and will recover a bit every turn
        self.tile_damage = None
        # show lasers (from the laser item)
        self.hori_laser = False
        self.vert_laser = False
        self.cross_laser = False
        self.item_orb = None
        self.trap_orb = None
        # the orb_eater is a harmless mouse that eats item orbs
        # if True, the mouse exists here
        self.orb_eater = False
        # a worm hole allows a player that owns the worm_hole to jump to that tile,
        # provided that the title isn't occupied by the same player (nor a jump
        # proof enemy.  The _1 and _2 determines who owns it.)
        self.worm_hole_1 = False
        self.worm_hole_2 = False
        # how many turns are left before a recall occurs DEBUG: are you sure?
        self.recall_turn = False
        # is this spot going to recall?
        self.recall_backup = False
        # is this tile affected by a secret agent?  Gets replaced by the owner's
        # player_owner number
        self.secret_agent = False
        # what items has the secret_agent stolen?
        self.secret_agent_list = []
        # is this tile a purifier tile?
        self.purity_tile = False
        # what items have been dumped at this location (using an item dump)
        self.dump_list = []
        # should a snake tile be displayed here for tunnel snake?
        self.snake = False
        # what color should this tile be highlighted?
        self.highlight = False  # blue
        self.highlight_red = False  # red
        self.highlight_green = False  # green
        self.highlight_brown = False  # brown

    def clear_tile(self):
        self.item_orb = None
        self.trap_orb = None
        self.secret_agent = None

    def kill_piece_on_tile(self):
        self.occupied = False
        self.piece = None

    def print_info(self, detailed_info=False):
        print("Location: ", self.start_location)
        print("Tile type: ", self.tile_type)
        print("Tile height: ", self.tile_height)
        if self.piece:
            print("Has a piece (occupied)")
            if not self.occupied:
                print("!!!!! Has a piece, but flagged unoccupied !!!!")
        else:
            print("No piece here (unoccupied)")
            if self.occupied:
                print("!!!!  Unoccupied, but flagged as occupied !!!!")
        if detailed_info:
            if self.piece:
                self.piece.print_detailed_info()
        print("===============================================")

    def print_detailed_info(self):
        if self.tile_type == "default":
            sg.popup(
                # f"This is a regular tile with an elevation of {self.tile_height}",
                f"""This is a regular tile with an elevation of {self.tile_height}.
    Horizontal LaserBeam: {self.hori_laser}, Vertical LaserBeam: {self.vert_laser}, Cross LaserBeam: {self.cross_laser}
    Orb Eater on tile? {self.orb_eater}
    Player one's worm hole? {self.worm_hole_1}
    Player two's worm hole? {self.worm_hole_2}
    """,
                keep_on_top=True,
            )
            return f"This is a regular tile with an elevation of {self.tile_height}"
        elif self.tile_type == "itemOrb":
            sg.popup(
                f"This is an item orb tile with an elevation of {self.tile_height}",
                keep_on_top=True,
            )
            return f"This is an item orb tile with an elevation of {self.tile_height}"
        elif self.tile_type == "destroyed":
            sg.popup(
                f"This tile has been destroyed!  But don't worry, it'll come back in 5 turns.",
                keep_on_top=True,
            )
            return f"This tile has been destroyed!  But don't worry, it'll come back in 5 turns."
        elif self.tile_type == "damaged4":
            sg.popup(
                f"This tile is being repaired.  It'll be ready for business in 4 turns.",
                keep_on_top=True,
            )
            return (
                f"This tile is being repaired.  It'll be ready for business in 4 turns."
            )
        elif self.tile_type == "damaged3":
            sg.popup(
                f"This tile is being repaired.  It'll be up and at 'em in 3 turns.",
                keep_on_top=True,
            )
            return f"This tile is being repaired.  It'll be up and at 'em in 3 turns."
        elif self.tile_type == "damaged2":
            sg.popup(
                f"This tile is being repaired.  It'll be repaired in 2 turns.",
                keep_on_top=True,
            )
            return f"This tile is being repaired.  It'll be repaired in 2 turns."
        elif self.tile_type == "damaged1":
            sg.popup(
                f"This tile is almost ready!  It'll be ready on the next turn!",
                keep_on_top=True,
            )
            return f"This tile is almost ready!  It'll be ready on the next turn!"
        elif self.tile_type == "mine":
            sg.popup(
                f"There's an obvious booby trap on this tile.  Don't move here without protection! It has an "
                f"elevation of {self.tile_height}",
                keep_on_top=True,
            )
            return f"There's an obvious booby trap on this tile.  Don't move here without protection! It has an " \
                   f"elevation of {self.tile_height}"
        elif self.tile_type in ["trap_orb_0", "trap_orb_1", "trap_orb_2"]:
            # intentionally misleading!  We don't want to reveal what type it is
            sg.popup(
                f"This is an item orb tile with an elevation of {self.tile_height}",
                keep_on_top=True,
            )
            return f"This is an item orb tile with an elevation of {self.tile_height}"
        elif self.tile_type == "mystery box":
            sg.popup(
                f"This is mystery box tile!  A random effect (can be bad or good) will occur when you step here.  "
                f"It has an elevation of {self.tile_height}",
                keep_on_top=True,
            )
            return f"This is mystery box tile!  A random effect (can be bad or good) will occur when you step here.  " \
                   f"It has an elevation of {self.tile_height}"
