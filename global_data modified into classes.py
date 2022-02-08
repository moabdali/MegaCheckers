class global_data():
    def __init__(self):
        # dimensions of the playing field
        self.columns = 10
        self.rows = 10
    
        if self.columns < 3:
            self.columns = 3
        if self.rows < 3:
            self.rows = 3

        # items settings
        self.set_items_option_list = ["pure_random", "balanced", "insanity", "none"]
        self.chosen_items_option = 1
        self.items_probability_type = set_items_option_list[chosen_items_option]

        # whose turn it is; set to player_2 to allow initial swaps to occur
        self.current_player_turn = "player_2"

        self.move_restriction = False
        self.current_turn_piece_location = [0,0]


        # how many turns have elapsed?
        self.turn_count = 0

        # this determines the number of item orbs that show up
        self.orb_cycle_list = [3, 3, 0, 1, 2, 1, 1, 0, 1, 0, 0]

        # for the spooky hand item; if spooky hand is true, then
        # the item is active; the turn counter determines when
        # the hand will attack
        self.spooky_hand = False
        self.spooky_hand_turn_counter = 15

        # determines where hotspots are located (teleports that your players
        # can jump to
        self.hotspot = []

        # number of recalls that are available
        self.recall_count = 0

        # DEBUG: make better comments for this
        self.playerAutoWin = 0
        self.playerAutoWinTurn = False

        # DEBUG: screen settings; keep normal for now
        self.screenSize = "normal"

        # do players want to see extended item explanations on pickup?
        self.showItemExplanations = True

        # state of the floor
        self.damaged_floor = (
                    "destroyed",
                    "damaged1",
                    "damaged2",
                    "damaged3",
                    "damaged4",
                    "damaged5",
                    "damaged6",
                    "damaged7",
                    "damaged8")

        # how many orbs do we want to generate this turn?
        def get_orb_generation_count():
            self.item_cycle = turn_count % 11
            return self.orb_cycle_list[item_cycle]
        

