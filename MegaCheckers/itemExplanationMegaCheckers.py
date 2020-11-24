# imported by useItemsMegaCheckers -> megaCheckers
# relies on: nothing



def longExplanation(window, itemName):
        if itemName == "auto win":
            explanation = "This amazing item is the most powerful and coveted in this game.  By using the auto win, you automatically win the game!*\n\n\nin 100 turns."
        elif itemName == "AI bomb":
            explanation = "Summon a bomb onto a random empty tile.  For each piece next to the bomb, there's a 20% chance that the bomb will expode, removing everything in a 3x3 square centered on itself.  The bomb randomly walks to a neighboing empty square between turns.  Jumping on it kills it."
        elif itemName == "bernie sanders":
            explanation = "Every piece on the field gets hit by a 100% tax rate. Bernie then uses the power of socialism and wealth redistribution to randomly reassign the items to any pieces on the field that can pick up items."
        elif itemName == "berzerk":
            explanation = "Your piece gains the berzerk buff, which is actually more like a mix of a buff and a debuff - a berzerk piece can eat both ally and enemy alike, and if it eats anyone, it gets to immediately move again.  If that move results in eating someone, it gets to go a third time.  Each time it eats someone, it gains a stack of meat.  At the beginning of each turn, the feral piece eats one of its stored meats.  If it has no meat to eat, it dies."
        elif itemName == "bowling ball":
            explanation = "Easily one of the most powerful powers in the game.  The piece using this item turns into a bowling ball, stripping it of all other buffs, debuffs and held items.  Instead of normal movement options, this piece will get a menu that allows it to head up//down//left//right.  It will angrily fling itself in the direction chosen until it crashes into a piece or a wall or falls into a damaged tile.  While it is rolling, it is immune to most forms of damage, including mines and lasers.  Crashing into an enemy causes the enemy to die, and for the bowling ball to stop.  Hitting an allied piece causes it to become stunned. Item orbs and trap orbs get destroyed without affecting a moving bowling ball.  Damaged and destroyed floors will instantly remove the bowling ball from the game, so watch out!  THE BOWLING BALL IS NOT IMMUNE WHILE NOT MOVING AND CAN BE EASILY DESTROYED BY ANY METHOD OF DESTRUCTION, INCLUDING BEING JUMPED!" 
        elif itemName in ("canyon column","canyon radial","canyon row"):
            explanation = "All affect tiles get lowered to -2 elevation.  Damaged/missing tiles remain damaged or destroyed, but will be lowered when they respawn like normal.  Pieces are not affected when they are lowered (aside for potentially being unable to climb back out).  Trip mines do not go off, as it is the tile moving, not the piece."
        elif itemName == "care package drop":
            explanation = "Call in a harmless airstrike on an opponent's piece. That tile and all surrounding pieces and empty tiles get an item orb dropped on them.  Try using this ability on solo enemy pieces that are surrounded by your pieces for best results.  Can also make a great disrespectful move to insult your enemy by saying you're so ahead that you'll give them extra powers."
        elif itemName == "charity":
            explanation = "Summon an extra piece for your opponent.  The piece will be a basic piece with no powers or anything (but can pick up items and use them as any other normal piece would). Since the piece belongs to your opponent, only they can use it.  It will count toward your enemy's Pieces Remaining score.  Use this power strategically to block in opponents, or to get easy access meat for your berzerk piece, for example."
        elif itemName == "dead man's trigger":
            explanation = "A mutually assured destruction piece - your piece straps a bomb to itself and holds a trigger.  As long as the trigger is held, nothing happens.  If this piece dies to an opponent jumping on it, the trigger falls out of its (hand?  Do pieces even have hands?  How do they hold items?) and causes the bomb to explode, killing the piece that jumped on it.  The bomb has no effect on pieces that kill it using other methods from afar."
        elif itemName == "dump items":
            explanation = "Gather up all your items into a dump orb.  Then throw the orb really hard onto any empty space.  Any piece can pick up that orb to gain all the items that were held.  Use this when you want to buff up another piece or if you know you're going to die."
        elif itemName == "elevate tile":
            explanation = "Use this to elevate your tile to any higher elevation.  Elevating a tile does not cause any damage to your piece and does not set off trip mines, as the piece itself isn't moving."
        elif itemName == "Energy Forcefield":
            explanation = "After arming your forcefield, a bubble forms around your piece, preparing it to protect you from most types of explosions or energy attacks.  If you get involved in such an attack, the forcefield will turn on at full power and protect you from the source of the attack and also any further energy attacks until the end of your turn, whereupon the battery runs out and leaves you vulnerable again."
        elif itemName == "floor restore":
            explanation = "Restore a missing or damaged floor tile to a default pristine condition.  Elevation changes are not considered damage, so it will be restored to whatever modified elevation the tile is set at."
        elif itemName == "grappling hook":
            explanation = "Ladders are so boring, and jetpacks are too energy intensive, so pieces opt to use ninjaesque grappling hooks to climb tiles.  The grappling hook is permanently reusable, so as long as a piece has one, it can keep climbing tiles regardless of their height for the rest of the game."
        elif itemName == "haphazard airstrike":
            explanation = "In desperation, you call on an allied nation that owes you a favor.  They are not very rich, but they send what they can - an old WW1 style bi plane where a pilot manually tosses out powerful bombs.  These bombs aren't very precise, so while they're powerful, they might also affect you.  Tosses five bombs.  Each bomb leaves a hole in the ground, instantly destroying whatever was on that tile."
        elif itemName == "haymaker":
            explanation = "Wind up a really strong punch, and let the piece next to you have it!  Wait... pieces don't even have hands... how do...  nevermind, let's not worry about that. The punch will not harm the piece (which can be friend or foe) directly, but will send them flying in the direction you punched them.  They will be affected by bombs or lasers or such in the way, but cannot pick up item orbs (nor trap orbs).  If they crash into a piece, both pieces will be stunned.  Pieces flung into a hole die instantly."
        elif itemName == "heir":
            explanation = "Per your royal birthright (or more accurately, because you found and activated an heir item), you can demand all allied pieces to bequeath you their items.  Enemy pieces don't believe in your claim of royalty, so they are unaffected."
        elif itemName in ("invert elevation all","invert elevation row","invert elevation column","invert elevation radial"):
            explanation = "All of the tiles on the board reach their opposite heights. -1 becomes +1, +1 becomes -1, +2 becomes -2, -2 becomes +2.  0/neutral elevation remains the same.  Destroyed or damaged floor tiles remain in the state that they are, but will respawn in the changed height."
        elif itemName == "jump proof":
            explanation = "Per OSHA standards, you don a hard hat.  The hard hat somehow makes you immune to damage from multi-ton pieces jumping on you, so enemies can't use their default attack on you anymore (berzerk pieces have to kill with a jump first, so even though they eat you, they can't kill you since they can't start with a jump kill).  Other modes of attack such as bombs or fire or knocking you into a hole still kill you."
        elif itemName == "jumpoline":
            explanation = "Spawns a jumpoline, which is what they used to call those devices consisting of a piece of taut, strong fabric stretched between a steel frame using many coiled springs, at least until your mom jumped on one, renaming it to Trampolines for some reason. If a piece belonging to either player jumps onto a jumpoline, they'll be tossed to another random empty square."
        elif itemName in ("laser column","laser row"):
            explanation = "Set a laser turret on an empty tile. The laser will keep firing a beam in the directions it's supposed to (row = left and right; column = up and down), melting any pieces it hits.  It does not affect other turrets, nor most non-piece tiles (it does kill mines) as they are too short to get hit.  A turret can be destroyed safely by jumping straight onto them."
        elif itemName == "magnet":
            explanation = "Use a strong magnet that seems to work on any material.  Light items such as mines and item orbs and trap orbs immediately surrounding you are sucked in to your tile.  Afterwards, the tile surrounding the inner tile will get sucked in - any item orbs or bombs there get pulled in to the inner tile, before your magnet stops working.  Pieces overlapping item orbs or trap orbs interact with them like normal."
        elif itemName == "move again":
            explanation = "Activate this item to get the move again shoes.  After this piece moves, you may choose to move it again.  If you accept, you can use items like normal (with only this piece), and then make one more move (only with this piece).  Each extra move again shoes will allow you an extra move."
        elif itemName == "move diagonal":
            explanation = "Using this piece allows you to also move diagonally now.  You can, of course, still move straight if you choose to do so."
        elif itemName in ("mutual treason column","mutual treason radial","mutual treason row"):
            explanation = "Both your and your opponent's pieces give riveting speeches to each other in the affected area, convincing all pieces to switch their allegiances (if there are no enemy pieces in range, your pieces discuss mutiny and leave you anyway)."
        elif itemName == "mystery box":
            explanation = "Place a mysterious ? next to you.  Any piece that touches it has a random effect applied to them.  There are quite s few effects that can occur.  Some of them include: getting your piece purified of negative effects, getting multiple item orbs, having your items stolen, getting blown up.  You will be told what effect happens when it does."
        elif itemName in ("napalm column", "napalm radial","napalm row"):
            explanation = "Fire off flames and fuel at enemy pieces in range. The pieces burn very hot and leave holes in the ground.  Allied pieces and tiles not occupied by enemies are unaffected."
        elif itemName == "orb eater":
            explanation = "Spawn an orb eater (which is totally not just a mouse) in an empty spot.  These will walk around randomly and eat item orbs and trap orbs that are adjacent to them.  Legends say that they should not be allowed to eat too many orbs lest terrible things happen... but they're just legends... right?"
        elif itemName == "place mine":
            explanation = "Place an explosive on an adjacent empty tile.  Anyone stepping on this tile will explode.  The bomb is not concealed whatsoever."
        elif itemName in ("purify column","purify radial","purify row"):
            explanation = "All allied pieces in range get all negative effects removed from them.  Who needs a doctor when you can just use this item to cure anything?"
        elif itemName == "purity tile":
            explanation = "Place a bubbly tile down that cleans off any negative effects from any pieces that step into it.  This tile can also rescue trip-mined pieces as it removes the bomb before it can blow up."
        elif itemName == "recall":
            explanation = "This piece leaves a recall mark on its current tile and gains a recall mark as well.  A snapshot in time is taken of the piece.  In ten turns, the tile will be returned to its snapshot, and the piece will be brought back in time to its original location and condition.  This is true even if the piece is killed.  Since the piece is brought back in time, any new changes to the piece since the snapshot are removed.  Note that even if you have a recall piece queued for a future turn, if you run out of pieces, you still lose, as you would have zero pieces on the field at that moment."
        elif itemName == "reproduce":
            explanation = "The piece that uses this gives birth in an adjacent empty tile to a brand new baby piece.  How?  Life... uh.... finds a way."
        elif itemName == "round earth theory":
            explanation = "The scientists said it was crazy to believe in the theory that the playing field is not actually flat. Pieces who are woke enough to believe in the round earth theory will walk off the edge of the playing field and reappear on the opposite side.  Even with this evidence, other pieces will still refuse to believe in the theory, calling you a conspiracy nut, unless they also pick up a round earth theory item.  What a bunch of unintelligent fools."
        elif itemName == "secretAgent":
            explanation = "Using this item gets you in contact with the secret agent that was hiding in an empty tile next to your piece.  This agent will snatch all of your opponent's item orbs if they stand on his tile.  If you visit the agent, he will give you whatever he has stolen."
        elif itemName == "seismic activity":
            explanation = "A random magnitude earthquake occurs.  The playing field will have its tiles raised and lowered a random amount.  The number of tiles affected, and the severity to which they're lowered or raised (between -2 and +2) are determined by the severity of the earthquake.  Pieces are not harmed in anyway, regardless of the power of the earthquake."
        elif itemName in ("shuffle all","shuffle column","shuffle radial","shuffle row"):
            explanation = "All affected tiles get shuffled around randomly.  Trip mines do not go off as the pieces themselves aren't moving.  Tile modifications (such as recall marks or purity tiles) go with them to whichever location they are moved to.  Laser beams are not actually on the tile, so they do not move, although the turrets do get moved if they're on an effect tile."
        elif itemName == "shuffle item orbs":
            explanation = "All item orbs on the field get shuffled around randomly.  Trap orbs are also moved around as the item is also fooled by their appearance."
        elif itemName == "sink tile":
            explanation = "Use this to depress your tile to any lower elevation.  Lowering a tile does not cause any damage to your piece, and does not set off trip mines, as the piece itself isn't moving."
        elif itemName == "smart bombs":
            explanation = "You call in a favor owed to you by a rich allied nation.  They send in a high quality bomber that hits three targets.  The pilot doesn't particularly care for his job, though, so while he will guarantee you won't get hit, he won't guarantee you that he's going to hit an enemy.  Bombed tiles are destroyed completely."
        elif itemName == "snake tunneling":
            explanation = "A robotic snake burrows under the field and moves in an adjacent direction, 10 times.  Any tile it burrows to gets knocked up to full elevation, killing any enemies on the tile.  The snake doesn't have a set location it wants to get to, so it randomly chooses to go up/down/left/right on any given move, making backtracking possible.  The snake leaves after the 10th move."
        elif itemName == "spooky hand":
            explanation = "After using this item, a disturbingly creepy hand decides to take residence underneath the playing field for the rest of the game.  After a 10-15 turn wait, the hand will emerge suddenly and snatch an occupied tile, along with its helpless victim (the hand doesn't care who it 'belongs to' and will attack any piece it wants).  It'll remain underground for another 10-15 turns doing whatever it is that spooky hands do, before repeating the cycle until the game ends."
        elif itemName in ("steal items column","steal items radial","steal items row"):
            explanation = "Steal item orbs that are held by any enemies in the affected range.  Note: this does not steal active powers; you need Steal Powers for that."
        elif itemName in ("steal powers column","steal powers radial","steal powers row"):
            explanation = "Steal most beneficial powers from enemies in the affected range.  It won't let you steal some special powers such as bowling ball or berzerk. Note: this doesn't let you steal held item orbs; you need Steal Items for that."
        elif itemName == "sticky time bomb":
            explanation = "Attach a really strong time bomb to any piece within your range (also includes your allies or even yourself).  In five turns, the sticky bomb will explode, destroying the tile that has the piece, and all surrounding tiles."
        elif itemName in ("study column","study radial","study row"):
            explanation = "Become a skilled student and study your allies and learn what they know.  You can gain virtually any power they have (without them losing their powers).  You cannot learn from your opponents, nor can you learn some powers such as Bowling Ball or Berzerk."
        elif itemName in ("suicide bomb column","suicide bomb radial","suicide bomb row"):
            explanation = "Become a suicide bomber and indiscriminately kill all pieces (friend and foe) within range."
        elif itemName in ("teach column","teach radial","teach row"):
            explanation = "Become a master tutor and teach all the skills you know (buffs that are active) to all your allies that are in range that are capable of learning powers.  This does not teach them unactivated item orbs."
        elif itemName == "trap orb":
            explanation = "Place a trap orb on an empty tile that is next to your piece. It is indistinguishable from a real item orb.  If your opponent picks up a trap orb, they will explode.  The trap orb cannot be identified by enemies and any attempts to examine it makes it appear like a regular item orb.  Your pieces will ignore trap orbs that belong to you (and you can examine the space on your turn to confirm that it's a trap)."
        elif itemName in ("trip mine column", "trip mine radial","trip mine row"):
            explanation = "All affected enemies in range get a motion detector mine attached to them. If they move away from the tile, they blow up.  Items that shuffle tiles around will not set off the bomb, neither will teleporting, as the mine doesn't sense motion.  Using items also won't set off the bombs.  If a piece jump kills you, it will safely destroy the bomb before it can go off, so it is safe to attack a trip mined piece."
        elif itemName == "trump":
            explanation = "This piece makes an empty promise to create a wall, and to its own surprise, actually follows up on that promise.  You can choose between a vertical or horizontal wall; all tiles within range are raised to the maximmum height of +2."
        elif itemName == "vampiricism":
            explanation = "Become a vampire!  Any pieces killed will have their life essence drained, allowing you to steal (most) powers from them.  You cannot absorb Bowling Ball or Berzerker powers.  Luckily, your breed of vampire is not affected in any way by sunlight.  On the downside, you can't revive victims as love slaves (they remain dead, sorry)."
        elif itemName == "vile radial":
            explanation = "All affected in-range enemies are hit by a vile poison that removes all existing buffs from them."
        elif itemName == "warp":
            explanation = "The piece is randomly warped to an empty location. The location chosen is completely pseudorandom, so if you end up in a terrible space, that's your fault for having bad luck.  Complaints about the game being rigged will be duly ignored.  Since the piece isn't actually moving, trip mines will not go off."
        elif itemName in ("wololo column","wololo radial","wololo row"):
            explanation = "Chant the powerful wololo incantation of the legendary and ancient Ayoh Eetoo religion's monks, convincing affected enemies to join your team (while somehow also changing their colors to your colors)"
        elif itemName == "worm hole":
            explanation = "Set a worm hole location on an adjacent empty spot.  Your pieces can jump to the worm hole from anywhere on the field as long as there isn't an ally hogging it.  If an enemy piece is on your wormhole, you can teleport a piece there to jumpkill it.  Alternatively, you can kill your own piece with a berzerker piece.  Pieces cannot use an enemy's worm hole to teleport to.  Trip mines will go off as the piece has to move to get to the worm hole."
        else:
            explanation = "There was no information found for this piece... Please notify support and let them know what item caused this message to appear."
        return explanation
    


def itemExplanation(i):
        if i == "auto win":
            explanation = "CONGRATULATIONS! THIS IS THE MOST POWERFUL ITEM IN THE GAME!  AS SOON AS YOU ACTIVATE THIS, YOU WILL WIN\nin 100 turns."
        elif i == "AI bomb":
            explanation = "Drop in a walking bomb that has a chance of exploding if it is next to any piece."
        elif i == "bowling ball":
            explanation = "Lose all buffs, debuffs and items, but become an angry, powerful bowling ball."
        elif i == "bernie sanders":
            explanation = "Taxes all pieces on the field and gathers up all of your unactivated items and all of your opponent's unactivated items.  Shuffles the items around and randomly redistributes the wealth \namong all pieces that are capable of receiving items.  DO YOU FEEL THE BURN?  If so... that might be a napalm row...  uh oh."
        elif i == "berzerk":
            explanation = "RIP AND TEAR!  KILL ENEMY. EAT ENEMY! MOVE AGAIN!  EAT! THREE TIMES! STORE MEAT. DIE IF GO HUNGRY!"
        elif i in ("canyon row","canyon column","canyon radial"):
            explanation = "Lower tiles in the affected range."
        elif i == "care package drop":
            explanation = "A plane drops off some item orbs near the selected opponent"
        elif i == "charity":
            explanation = "Gift your opponent a brand new piece.  How charitable!"
        elif i == "dead man's trigger":
            explanation = "Strap a bomb to yourself and activate the trigger.  If you die, you release the trigger, and the enemy that jumped on you dies as well."
        elif i == "dump items":
            explanation = "Jettison all your items to any empty place on the field.  Anyone can pick it up."
        elif i == "elevate tile":
            explanation = "Spontaneously cause the tile that you're standing on to rise up to a chosen height.  Let the other pieces know you are above them, in more ways than one."
        elif i == "Energy Forcefield":
            explanation = "A forcefield that will protect you from an explosion or energy attack; the shield remains active for one turn, shielding you from further explosions."
        elif i == "floor restore":
            explanation = "Repair all damaged/missing floor tiles and replace them with pristine ones."
        elif i == "grappling hook":
            explanation = "Use a grappling hook to climb the tallest of tiles with barely any effort.  Be a ninja!  Or Batman.  Or nerd with a hook-on-a-rope.  Whatever."
        elif i == "haphazard airstrike":
            explanation = "Call in an airstrike from an underfunded army.  The plane doesn't have targeting systems installed, so it will carpet bomb the field at random."
        elif i == "haymaker":
            explanation = "Unleash a strong punch that sends a piece flying."
        elif i == "heir":
            explanation = "You're going to have a great heir day, luck is in the heir!  For all of your allied pieces are going to give you their items."
        elif i in ("invert elevation all","invert elevation column","invert elevation radial","invert elevation row"):
            explanation = "Change the elevations to their opposite but equal level.  -2 sunken tiles become +2 elevated.  -1 becomes +1.  0 remains neutral. And so on."
        elif i == "jump proof":
            explanation = "Your piece dons a dapper hard hat, naturally making you immune to being jumped on.  It does not provide any other forms of protection."
        elif i == "jumpoline":
            explanation = "Spawns a jumpoline, which is what they used to call those devices consisting of a piece of taut, strong fabric stretched between a steel frame using many \ncoiled springs, at least until your mom jumped on one.  If a piece belonging to either player jumps onto a jumpoline, they'll be tossed to another random empty square."
        elif i in ("laser column","laser row"):
            explanation = "Place a laser turret that shoots out long range beams that burn any piece it hits."
        elif i == "magnet":
            explanation = "Uses Science (tm) to create a powerful magnet that pulls in nearby lightweight objects, then proceeds to pull in slightly farther items if there is room to pull them in."
        elif i == "move again":
            explanation = "Activate this to gain the move again shoes, which allow this piece to permanently move twice in one turn. This effect stacks if it uses multiple move agains."
        elif i == "move diagonal":
            explanation = "Activate this piece to gain a cool diagonal arrows logo, which allow this piece to permanently move diagonal (while still having access to normal movement)"
        elif i == "secretAgent":
            explanation = "Activate this to reveal a secret agent in a neighboring square.  This creepy guy will steal items from your opponents if they visit his square, and will give those items to you if you visit him."
        elif i in ("mutual treason column", "mutual treason row", "mutual treason radial"):
            explanation = "You and your opponent both utilize some excellent propoganda... any affected pieces permanently switch their allegiances."
        elif i == "mystery box":
            explanation = "Summon a mystery box.  Each time someone steps onto it, a random effect occurs to them (can be good or bad)."
        elif i in ("napalm radial", "napalm column", "napalm row"):
            explanation = "Fire off a stream of fire and sticky substances at your opponents.  Any opponent hit by it will burn to a crisp and leave a hole in the ground.  Allies are unaffected thanks to your sweet aiming skills."
        elif i == "orb eater":
            explanation = "Summon a hungry orb eater (totally not a mouse) on any empty spot in the field.  It will move around in between turns and eat up any item orbs it finds. Legend has \nit that you shouldn't let an orb eater eat too many..."
        elif i == "shuffle all":
            explanation = "Shuffle everything on the board.  Insanity!"
        elif i == "place mine":
            explanation = "Place a mine down on an adjacent square.  Any player stepping on it goes boom."
        elif i in ("purify radial", "purify column", "purify row"):
            explanation = "Clear out all negative effects from all of your allies within range.  Who needs a medical degree when you have this?!"
        elif i == "purity tile":
            explanation = "Step into this tile to remove all negative effects from your piece.  Rinse, lather, repeat. (I mean, you can if you want, but you'd just be wasting your time if you're already purified, y'know?)"
        elif i == "recall":
            explanation = "at the earlier time no matter what.  Activate this and your tile will be marked with a recall logo, which in 10 turns will whisk you back to the exact snapshot you were at the earlier time no matter what.\n Activate this and your tile will be marked with a recall logo, which in 10 turns will whisk you back to the exact snapshot you were"
        elif i == "reproduce":
            explanation = "Use this to create a baby piece within range.  It will be a brand new simple piece.  How do non-sentient pieces have babies?  Life... uh... finds a way."
        elif i == "seismic activity":
            explanation = "Induce an earthquake.  A random magnitude earthquake will occur: the higher the magnitude, the more drastically the field will be altered.  Random elevations and depressions will occur throughout the field.  Surprisingly, no pieces will be harmed."
        elif i == "round earth theory":
            explanation = "The scientists called us insane, but thanks to the power of pseudoscience, you prove the earth is totally round, so if you can totally wrap around the playing field.  \nThat is, if you wanted to, you can move from the right edge of the map straight to the left edge.  Or from the top straight to the bottom.  Pac man style."
        elif i in ("shuffle column", "shuffle radial", "shuffle row","shuffle all"):
            explanation = "All tiles in the affected area get shuffled around randomly."
        elif i == "shuffle item orbs":
            explanation = "All item orbs (and trap orbs) get removed from the field and then are randomly redistributed on empty spots of the field."
        elif i == "sink tile":
            explanation = "Use sheer will to lower the tile to a chosen elevation."
        elif i == "smart bombs":
            explanation = "A well funded military sends in a precision bomber to shoot bombs on the field and will make sure to avoid hitting your pieces."
        elif i == "snake tunneling":
            explanation = "A robotic snake starts digging around from the summoning point.  It burrows around and pushes the ground up (to an elevation of 2), killing enemies but sparing your pieces."
        elif i == "spooky hand":
            explanation = "A scary hand that will periodically grab a random piece from the field, permanently removing it from play.  \nAfter claiming a victim, it takes its time doing whatever it is that spooky hands do, before looking for a new victim."
        elif i in ("steal items column","steal items radial","steal items row"):
            explanation = "Steal all unactivated items from all enemies in range.  POSSESSION IS 9/10 OF THE LAW, YO!"
        elif i in ("steal powers column","steal powers radial","steal powers row"):
            explanation = "Steal (almost) all active buffs from all enemies in range.  Finders keepers! (exceptions exist for some buffs, such as bowling ball)"
        elif i == "sticky time bomb":
            explanation = "Attach a bomb to any in-range piece (including your own).  After five turns, it explodes, killing all surrounding pieces."
        elif i in ("study column", "study row", "study radial"):
            explanation = "Copy any activated buffs from your in-range allies (aside for special cases such as recall and bowling ball)"
        elif i in ("suicide bomb column", "suicide bomb row", "suicide bomb radial"):
            explanation = "Kills every piece within range - yours and your enemy's.  Terrorism is not cool, but I guess it's ok if non-sentient pieces do it to each other."
        elif i in ("teach column", "teach radial", "teach row"):
            explanation = "Become a master tutor and teach your in-range allies whatever buffs you have."
        elif i == "trap orb":
            explanation = "Put a bomb disguised as an item orb that will explode on your enemy if they touch it.  The trap orb looks exactly like a normal item orb, \nso there's no way to tell it apart.  However, your pieces will be aware that it's a trap and will be unaffected by them (stepping on them leaves the trap as-is so that your opponent still has a shot at getting tricked by it"
        elif i in ("trip mine radial", "trip mine row", "trip mine column"):
            explanation = "Set up a bomb on all in-range enemies that can detect when the piece moves.  Upon moving, the piece will trigger the bomb, causing it to explode upon finishing its action.  \nA piece that has a trip mine set up on it can still use most items (including teleporting items) safely without setting the bomb off. However, items that are linked to moving will still set it off."
        elif i == ("trump"):
            explanation = "We're gonna build a great wall, a wall greater than what the enemy team ever built, and we're gonna make them pay for it!  The wall will be built by taking all of the affected tiles and raising them to max height.  The wall can either be built as a row or a column."
        elif i in ("vile radial", "vile column", "vile row"):
            explanation = "Apply the 'vile' debuff to all enemies within range. This nasty effect stops affected pieces from being able to apply buffs to themselves.  \nThey can still pick up any items normally, and use items that don't apply positive effects to themselves."
        elif i == "warp" :
            explanation = "Your piece is randomly whisked away to an empty spot in the field. Where you end up is completely random, so don't bother whining about \n'boo hoo how come I always end up in the worst position possible everytime I use this item', because that's your fault for being unlucky."
        elif i in ("wololo radial", "wololo column", "wololo row"):
            explanation = "Your piece uses the ancient incantation of the ancient Ayoh Eetoo religion, which convinces all in-range pieces that hear the word of truth to join your \nside.  It somehow changes their color to match your team's color, too.  Weird how that works."
        elif i == "worm hole":
            explanation = "Set up a worm hole at an adjacent tile.  As long as your pieces are not on the warp tile, you can use your move to teleport to that worm hole from anywhere."
        elif i == "vampiricism":
            explanation = "Pounce and feed on a piece's essence, gaining its power.  Sorry, the piece doesn't come back from the dead as your lover, nor do you get to sparkle in the sun.  Well, you do, because you're made of metal, but whatever."
        
        else:
            explanation = f"no explanation supplied for {i}... yet"

        return explanation

