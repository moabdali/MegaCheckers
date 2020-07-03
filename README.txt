MegaCheckers:

A game where you take turns moving pieces to kill all of your enemy's pieces.  To do this, your pieces jump onto the enemy piece to crush them.  In order to aid you with this goal, every few turns a random number of mystery items will appear on empty spaces.  You pick up an item and on any subsequent turn,  you can use the item (depending on what the item is) to destroy enemy pieces, to set up traps, to alter the playing field (raise/lower, destroy, magnetize, make one way, push pieces, etc), to power up your piece, and so on.  Eventually networking will be enabled.  

v.0.9.17 added trap orbs item (puts down a mine that looks like a normal orb, but doesn't affect you if you placed it), and fixed a glitch in move again that gave you unlimited turns (missing a return statement when a player says no to moving again, ironically). However, the item orb disappears when you step on your own, so that logic needs to be updated or the item changed to do something else if you pick it up.

v.0.9.16 Corrected some death check errors that occur due to piece dying early and not properly setting the space as "not occupied".  Added "always on top" to all popups to avoid errors where the popup disappears.

v.0.9.15 Added a mine item.  Added a death check related to traps (to make it easier to program new traps without a ton of checks being needed each time); can be used to replace existing code if I feel like it

v.0.9.14 Added better move again icons (and implemented them).

v.0.9.13.1 Hotfix:  was missing a continue command in the previous code.  Whenever a piece was killed, instead of continuing, it would "return", ending the player's turn.  It should be working properly from now on.  

v.0.9.13 Mostly complete with "move again".  There appears to be a glitch occurring with stacking move again powerups - if you keep moving around normally, there are no issues.  But it seems that you lose turns if you click on a wrong piece between moves or if you pick up an item.  More testing will  need to be done, but uploading this build, along with a temporary limit of one "move again buff" so that my code is backed up for the former, and so that I don't spend too much time on a situation that will likely rarely occur anyway (for the latter).

v.0.9.12 Added move diagonal.  

v.0.9.11 Finished all directions of the haymaker.  Still need to do laser/mine checks.  Will probably do that after I actually program some mines and lasers.

v.0.9.10 Overhauled the graphics.  Uses 3d images made in Paint 3d along with dynamically generated pieces with regards to power ups and whatnot.  Also changed some errors in code flow (continues when finishing up each activity in displayBoard) and added a console output in case someone misses a message (also removed many sleep commands now that it's ok for them to miss a message; this helps the game feel more responsive). 

v.0.9.9 Added haymaker power up as well as fixed some logic errors with items not getting picked up if a piece was forced there (this was technically not a glitch because until now there wasn't a way to end up on an item tile without intentionally moving there; this is more of a new feature, if anything)

v.0.9.8 Added a "stunned" debuff concept.  Pieces that are stunned cannot move or attack until the player has had one turn (this means if you stun your own piece, you can't use it this turn, but you can the next. However, if you stun your opponent's piece, their piece won't be unstunned until you finish your current turn AND their turn ends)

v.0.9.7 Added trip mine radial, including updating the move function to account for a player moving.  Need testing to see if forcefields properly protect you.  Functionality intends that you can use one shield to protect against any number of simultaneous trip mine blasts. 

v.0.9.6 Added purify radial and abolish foe power radial.

v.0.9.5 Added napalm radial  Consider adding a cheat menu for easier debugging

v.0.9.4 Added napalm row

v.0.9.3 Added napalm column

v.0.9.2 Added a crossCheck function to make snake tunneling and similar cross checks easier.  Also, added snake tunneling.

v.0.9.1 Added smartBombs (better air strike).  Added better handling of when you click an empty space or an enemy (instead of waiting on you to click a second square after making a false selection, it immediately tells you that you made an invalid choice and starts over).  Consider changing it to where clicking on the same non-owned square twice gives you the information popup instead.

v.0.9: Added the jumpproof item.

v.0.8.9: Added functions to check for radial/column/row.  This will reduce errors and speed up implementation of new items.

v.0.8.8: Modified all popups to always stay on top.

v.0.8.7: Selected pieces appear grey now.  There's a player turn indicator. Reduced spacing between tiles.  

v.0.8.6:
	Added a button to exit the program safely.  TKinter has an error where it breaks if you hit the X button, so the exit button is disabled now.  I also reformatted the tutorial window to look a little neater.

v.0.8.5:
	Added a tutorial that explains the basics and teaches you how to select units, how to move units, how to use an item, and (eventually) how to inspect tiles and pieces.  Tutorial todo: make formatting prettier, catch errors based on clicking the options instead of a button (might just disable buttons to make it safer), and to add the "inspect" tutorial.  Eventually need something for raising/lowering tiles.

v.0.8.4:
	Starting a simple tutorial mode to teach new players.

v.0.8.3:
	Added Wololo - allows you to steal an enemy's piece.  Needs to have the range properly added in.  Also for far future:  need to make a tutorial.

v.0.8.2:
	Added a haphazard bombing run.  Added floor damage (and floor repair).  Added some explosions.  Next update should make it to where if a piece is exploded, an explosion shows up.

v.0.8.1:
	Renamed suicideRow to SuicideBomb Row (so that you know it kills everyone and that it's not just suiciding your pieces).  Added a suicide column.


v.0.8:
	Has an updated avatar serving function.  It'll automatically keep track of what your avatar should be so that you (I) don't have to manually reassign them for each scenario.  Also, the shield (forcefield) feature has been successfully implemented.  Avatars appear to properly update on every combination involving (or not involving) shields and holding items.

v.0.7:
	Has an examine option now.  You can check public stats about the pieces and gameboard.  Features checks that prevent the buttons from being enabled if it won't flow with the game's logic.  (For example, the button is disabled if you click "use item" before clicking a piece that can use an item).  To do: add the shield, test if the pieces revert to normal.  Test to see if buffs show up properly (shield).

v 0.6:
	Can keep track of empty spaces now. Orbs exist now. You can pick up items now.  The only item implemented is the "suicide row", but it's confirmed working.  The avatar attribute is now in effect.  Your piece's avatar changes color when it's holding an item.  (Haven't tested whether it disappears when it's used up since the only working item right now kills you anyway).  Corrected in error in keeping track of the location of pieces (forgot to change i,j to rows-i-1,j for the initialization procedure).  Added an item button that greys out when not valid.  Changed the visual size of the field to help fit on smaller monitors.  To do: add the option to view the stats of an orb (maybe via a context menu?), add more items (shield most likely).  Test to make sure pieces revert to normal when they don't have an item held anymore.

v 0.5.1:
	Spawn orbs now.  Spawns in legal locations.

v 0.5:
	Major logic changes.  No longer use a "player" class, as it seems pointless, at least at the moment.  Instead, the gameBoard list now contains two elements per location - a tile object slot to keep track of the tile (its conditions), and a piece object to keep track of the pieces (their items, location, and ownership).  This should result in easier coding going forward.  Beginning work on tracking empty spaces for item orb spawns.  

v 0.4:
	Put in even more information frames, including number of pieces left.  Messages show up more neatly now.  Considering a log output somewhere on the side or bottom. 

v 0.3:
	Put in a information frame on bottom, game properly calculates whether you can move to a location (diagonals have NOT been implemented yet - that will be added when that item is added to the game; same with "around the world" items that let you move pacman style from the right edge of the field to the left, for example).  Popups have been removed since all info appears on the bottom now. Still need todo the item generation.

v 0.2:
	Gameboard properly updates between turns.  Pieces can move around anywhere (teleporting). Pieces can kill.  Turns are properly tracked and a player can't move his piece twice (opposing players can't control their opponent's pieces).  To do: generate items and allow them to be picked up.  Note: this requires changing the board logic to go from "0" for a blank area to having a 1 for denoting that items exist.  Alternatively, may need to have a new class to represent spaces as eventually I'll want the floor to be raised and damaged and whatnot. 

v 0.1:
	Starting right out with a GUI.  Currently shows the field and properly generates the starting pieces and has a logical gameboard that gets displayed for debug purposes in the console.  The next commit should feature the ability to move the pieces around, followed by a commit for properly killing a piece, followed by generating items, then picking up items, then using items (with just a print message for now). 