import global_data

class piece():
    
    def __init__(self, start_location = (0,0)):
        self.x_location =               start_location[0]
        self.y_location =               start_location[1]
        self.piece_type =               "default piece type"
        self.avatar =                   "default"
        self.move_distance_max =        1
        self.active_buffs =             []
        self.active_debuffs =           []
        self.stored_items =             []
        self.owned_by =                 "neutral"
        self.grey =                     False
        self.moves_left =               1
        self.current_turn_piece =       False
        self.standing_on_self_orb =     False
        self.recall_turn =              False
        self.force_field_turn =         0
        self.sticky_time_bomb =         True
        self.berzerker_meat_count =     False
        self.berzerker_attacks_left =   False
        self.death_mark =               None
        # helper variable for keeping track of whether the ball
        # is in motion and needs a rotating movement animation
        self.bowlMotion =               False
        self.bowlOrientation =          1

        # future implementation; pieces can upgrade their levels
        self.pieceLevel = 1
        self.pieceExp = 0
        
    def print_location(self):
        print(f"Location is {self.x_location}, {self.y_location}.")
        
    def print_items(self):
        print(f"Items include {self.stored_items}")
        
    def remove_all_buffs(self):
        self.active_buffs = []
        
    def remove_all_debuffs(self):
        self.active_debuffs = []
        
    def remove_an_item(self, item_chosen = None):
        if item_chosen:
            if item_chosen in self.stored_items:
                self.stored_items.remove(item_chosen)
                
    def print_detailed_info(self):
        # ownership
        print("This piece is owned by ", end = "")
        if ( self.owned_by == global_data.current_player_turn ):
            print("you.")
        else:
            print("your opponent.")

        if self.current_turn_piece:
            print("<<<<THIS PIECE MOVED THIS TURN.>>>>")
        
        if self.stored_items:
            print("Items held: ")
            for each_item in self.stored_items:
                print(each_item)
        else:
            print("No items held")
    
