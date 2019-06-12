import random
import os
SCORE_TO_WIN = 100

class PlayGame:
    """Plays the dice game Pig with two players"""
    def __init__(self):
        # clear to start the game
        os.system("clear")
        # player one is always the user
        self.player_one = Player(self)
        # player two could be human or not
        self.player_two = self.get_opponent()
        # initialize the scoreboard with two players
        self.scoreboard = Scoreboard(self.player_one, self.player_two)
        # start with player one in the first game
        self.player_ones_turn = True
    
    def get_opponent(self):
        """populates the second player with either a human or computer player"""
        number_of_players = None
        while True:
            number_of_players = input("How many players? 1 or 2? ")
            try:
                if int(number_of_players) == 2:
                    return Player(self)
                elif int(number_of_players) == 1:
                    return ComputerPlayer(self)
                else:
                    print("Players more than 2 not supported.")
            except:
                print("Invalid entry, try again.")
    
    def play_game(self):
        # reset the scores at the start of the game
        # AREA FOR IMPROVEMENT would probably be better as a method of player
        self.player_one.score = 0
        self.player_two.score = 0

        # play the game while it's not over
        game_over = False
        while not game_over:
            self.scoreboard.display()
            if self.player_ones_turn:
                print(self.player_one.name)
                game_over = self.player_one.take_turn()
            else:
                print(self.player_two.name)
                game_over = self.player_two.take_turn()
            # this logic should make the loser go first next game
            # also this "toggles" whose turn it is
            self.player_ones_turn = not self.player_ones_turn
        self.play_again_query()

    def play_again_query(self):
        response = input("Do you want to play again? ")
        try:
            # play the game again, retaining the player, game, and scoreboard objects
            if response[0].lower() == "y":
                self.play_game()
        except:
            pass
            
class Scoreboard:
    """Tracks scores for the current turn, game, and multiple games"""
    def __init__(self, player_one, player_two):
        self.player_one = player_one
        self.player_two = player_two
        self.turn_score = 0
    
    def display(self):
        os.system("clear")
        print(f"""
            {self.player_one.name}: {self.player_one.score}       {self.player_two.name}: {self.player_two.score}
        
            {self.win_percentage()}

            Turn Score: {self.turn_score}
        """)

    def win_percentage(self):
        # if player one is winning the series
        if self.player_one.wins > self.player_two.wins:
            winning_player = self.player_one.name
            # round the win percentage to 3 decimal places and multiply by 100
            winning_player_percent = round(self.player_one.wins/(self.player_one.wins+self.player_two.wins),3)
        # same for player two
        elif self.player_one.wins < self.player_two.wins:
            winning_player = self.player_two.name
            winning_player_percent = round(self.player_two.wins/(self.player_one.wins+self.player_two.wins),3)
        else:
        # change format if the series is tied
            return "Series is tied"
        return f"{winning_player} win %: {100*winning_player_percent}"


class Player:
    """Makes a player class"""
    def __init__(self, game):
        self.score = 0
        self.name = self.get_name()
        self.game = game
        self.wins = 0

    def get_name(self):
        """gets a name for the player"""
        while True:
            name = input("New player, what's your name? ")
            if len(name) < 10:
                return name
            else:
                print("Only names up to 10 characters are supported")

    def take_turn(self):
        """method for human player taking a turn, reurns True if the
        player won on their turn, False if not"""
        the_die = Die()
        turn_over = False
        # initialize the current score in scoreboard for a new turn
        self.game.scoreboard.turn_score = 0

        while not turn_over:
            roll = the_die.roll()
            if roll == 1:
                # update the scoreboard and display again so that current score
                # is 0 on a bust
                self.game.scoreboard.turn_score = 0
                self.game.scoreboard.display()
                print(f"{self.name}, you BUSTED!")
                input("Press Enter to Continue")
                turn_over = True
            else:
                # roll, update, and then refresh
                self.game.scoreboard.turn_score += roll
                self.game.scoreboard.display()
                print(f"{self.name}, you rolled a {roll}")
                # any input, including enter, will roll besides something
                # that starts with an "h" or "H"
                choice = input("What do you want to do? (Roll/Hold) ")
                try:
                    if choice[0].lower() == "h":
                        self.score += self.game.scoreboard.turn_score
                        turn_over = True
                except:
                    pass
        # the player says that they won if they did
        # AREA FOR IMPROVEMENT: this should be a method in game or player
        if self.score >= SCORE_TO_WIN:
            print(f"{self.name} wins!")
            self.wins += 1
            return True
        return False

class ComputerPlayer:
    """makes a computer player with random personalities, mimics most
    of the Player class"""
    def __init__(self, game, personality="scared"):
        self.game = game
        # personality object helps with move strategy
        self.personality = Personality()
        self.name = self.personality.name
        self.score = 0
        self.wins = 0

    def take_turn(self):
        the_die = Die()
        turn_over = False
        self.game.scoreboard.turn_score = 0
        while not turn_over:
            roll = the_die.roll()
            if roll == 1:
                self.game.scoreboard.turn_score = 0
                self.game.scoreboard.display()
                print(f"{self.name} BUSTED!")
                # this stalls the computer player until the player knows what happened
                input("Press Enter to Continue")
                turn_over = True
            else:
                self.game.scoreboard.turn_score += roll
                self.game.scoreboard.display()
                print(f"{self.name} rolled a {roll}")
                # to make the move, the computer player needs to know both total scores and the
                # current score
                # AREA FOR IMPROVEMENT: this is a mess and feels like it could be shortened
                choice = self.personality.get_move(self.score, self.game.player_one.score, self.game.scoreboard.turn_score)
                # AREA FOR IMPROVEMENT: this is repeated code
                try:
                    if choice[0].lower() == "h":
                        self.score += self.game.scoreboard.turn_score
                        turn_over = True
                except:
                    pass
        # AREA FOR IMPROVEMENT: this is repeated code, probably could be even better if
        # ComputerPlayer inherited Player
        if self.score >= SCORE_TO_WIN:
            print(f"{self.name} wins!")
            self.wins += 1
            return True
        return False

class Personality:
    """a personality class designed to make moves in Pig"""
    def __init__(self, name=None):
        potential_names = ["Scared","Chaser","Smart"]
        if name in potential_names:
            self.name = name
        else:
            index = random.randint(0,(len(potential_names)-1))
            self.name = potential_names[index]

    def get_move(self, my_score, opp_score, curr_score):
        """this is a filter for selecting the correct personality method for get_move"""
        # AREA FOR IMPROVEMENT: this would be more efficient as a dictionary of functions
        if self.name == "Scared":
            return self.get_scared_move(my_score, opp_score, curr_score)
        if self.name == "Chaser":
            return self.get_chaser_move(my_score, opp_score, curr_score)
        if self.name == "Smart":
            return self.get_smart_move(my_score, opp_score, curr_score)
    
    def get_scared_move(self, my_score, opp_score, curr_score):
        
        if curr_score + my_score >= SCORE_TO_WIN:
            move = "hold"
        elif curr_score >= 15:
            move = "hold"
        else:
            move = "roll"
        print(f"{self.name} will {move}.")
        input("Press Enter to Continue.")
        return move

    def get_chaser_move(self, my_score, opp_score, curr_score):
        
        if curr_score + my_score >= SCORE_TO_WIN:
            move = "hold"
        elif curr_score + my_score < opp_score:
            move = "roll"
        elif curr_score >= 25:
            move = "hold"
        else:
            move = "roll"
        print(f"{self.name} will {move}.")
        input("Press Enter to Continue.")
        return move

    def get_smart_move(self, my_score, opp_score, curr_score):
        
        if curr_score + my_score >= SCORE_TO_WIN:
            move = "hold"
        elif curr_score >= 20:
            move = "hold"
        else:
            move = "roll"
        print(f"{self.name} will {move}.")
        input("Press Enter to Continue.")
        return move

class Die:
    """makes 1 die and can roll it"""
    def __init__(self, sides=6):
        self.sides = sides

    def roll(self):
        return random.randint(1, self.sides)

game = PlayGame()
game.play_game()