PlayGame
#################
Responsibilities: handles the rules for the game
Collaborators: Scoreborard, Player, Dice

Scoreboard
#################
Responsibilities: handles the turn, game, and multi-game scoring
Collaborators: PlayGame, Player

Player
#################
Responsibilities: aware of turn, gets inputs, passes turn
Collaborators: PlayGame, Player, CompPlayer, Scoreboard, Dice

CompPlayer
#################
Responsibilities: aware of turn, makes decisions
Collaborators: PlayGame, Player, CompPlayer, Scoreboard, Dice

Dice
#################
Responsonsibilities: return a random number 1-6 for each die in the object
Collaborators: Player, PlayGame, Scoreboard