MegaCheckers:

A game where you take turns moving pieces to kill all of your enemy's pieces.  To do this, your pieces jump onto the enemy piece to crush them.  In order to aid you with this goal, every few turns a random number of mystery items will appear on empty spaces.  You pick up an item and on any subsequent turn,  you can use the item (depending on what the item is) to destroy enemy pieces, to set up traps, to alter the playing field (raise/lower, destroy, magnetize, make one way, push pieces, etc), to power up your piece, and so on.  Eventually networking will be enabled.  

v 0.2:
	Gameboard properly updates between turns.  Pieces can move around anywhere (teleporting). Pieces can kill.  Turns are properly tracked and a player can't move his piece twice (opposing players can't control their opponent's pieces).  To do: generate items and allow them to be picked up.  Note: this requires changing the board logic to go from "0" for a blank area to having a 1 for denoting that items exist.  Alternatively, may need to have a new class to represent spaces as eventually I'll want the floor to be raised and damaged and whatnot. 

v 0.1:
	Starting right out with a GUI.  Currently shows the field and properly generates the starting pieces and has a logical gameboard that gets displayed for debug purposes in the console.  The next commit should feature the ability to move the pieces around, followed by a commit for properly killing a piece, followed by generating items, then picking up items, then using items (with just a print message for now). 