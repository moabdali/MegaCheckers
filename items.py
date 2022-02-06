import random
import global_data
import board

items = ["item A", "item B", "item C", "item D"]

def generate_item_orbs():
    empty_squares = board.find_empty_tiles()
    num_orbs_to_spawn = global_data.get_orb_generation_count()
    while (num_orbs_to_spawn > 0 and
           len(empty_squares) > 0):
        tl = random.choice(empty_squares)
        board.game_board[tl[0]][tl[1]].tile_type = "item_orb"
        empty_squares.remove(tl)
        num_orbs_to_spawn -= 1

def get_item():
    return random.choice(items)

def show_items(piece):
    for items in piece.stored_items:
        print(items + " ", end = "")
    print("")

def cancel_item():
    yorno  = print("Do you wish to use item?  y/n")
    #true = cancel
    if yorno in ("Y","y","Yes","YES"):
        return True
    #false = don't cancel
    return False

def use_item(piece):
    
    #check if disabled (prevented from using items)
    if "paralyzed" in piece.active_debuffs:
        print("Piece is paralyzed.  This piece cannot use items.")
        return False
    
    #check what item is to be used
    item_chosen = input("Which item do you wish to use?")
    
    #check if have
    if item_chosen not in piece.stored_items:
        print("You don't possess that item.")
        return False

    
    #display range

    #check where player is sure they want to use it
    
    if cancel_item():
        return False
    
    #attempt to use item
    print("Used item here")
    
    #deplete item
    if remove_item(item_chosen, piece):
        print("Deleted one copy of item.")
        return True
    else:
        print("Item not in list.  This is a really bad error.")
        return False



def remove_item(item_chosen, piece):
    try:
        piece.stored_items.remove(item_chosen)
        return True
    except:
        return False
