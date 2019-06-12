import random
import os
SCORE_TO_WIN = 100

class PlayGame:
    """Plays the dice game Pig with two players"""
    def __init__(self):
        os.system("clear")
        self.player_one = Player(self)
        self.player_two = self.get_opponent()
        self.scoreboard = Scoreboard(self.player_one, self.player_two)
        self.play_game()
    
    def get_opponent(self):
        """populates the second player with either a human or computer player"""
        number_of_players = None
        while True:
            number_of_players = input("How many players? 1 or 2? ")
            try:
                if int(number_of_players) == 2:
                    return Player(self)
                elif int(number_of_players) == 1:
                    print("Computer opponent coming soon!")
                    return ComputerPlayer(self)
                else:
                    print("Players more than 2 not supported.")
            except:
                print("Invalid entry, try again.")
    
    def play_game(self):
        game_over = False
        first_players_turn = True
        while not game_over:
            self.scoreboard.display()
            if first_players_turn:
                print(self.player_one.name)
                game_over = self.player_one.take_turn()
            else:
                print(self.player_two.name)
                game_over = self.player_two.take_turn()
            first_players_turn = not first_players_turn
        self.play_again_query()

    def play_again_query(self):
        response = input("Do you want to play again? ")
        try:
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
        if self.player_one.wins > self.player_two.wins:
            winning_player = self.player_one.name
            winning_player_percent = round(self.player_one.wins/(self.player_one.wins+self.player_two.wins),1)
        elif self.player_one.wins < self.player_two.wins:
            winning_player = self.player_two.name
            winning_player_percent = round(self.player_two.wins/(self.player_one.wins+self.player_two.wins),1)
        else:
            return "Series is tied"
        return f"{winning_player} win %: {100*winning_player_percent}"


class Player:
    """Makes a player class"""
    def __init__(self, game):
        self.score = 0
        self.name = "default"
        self.game = game
        valid_input = False
        self.wins = 0
        while not valid_input:
            self.name = input("New player, what's your name? ")
            if len(self.name) < 10:
                valid_input = True
            else:
                print("Only names up to 10 characters are supported")

    def take_turn(self):
        the_die = Die()
        turn_over = False
        self.game.scoreboard.turn_score = 0
        while not turn_over:
            roll = the_die.roll()
            if roll == 1:
                self.game.scoreboard.turn_score = 0
                self.game.scoreboard.display()
                print(f"{self.name}, you BUSTED!")
                input("Press Enter to Continue")
                turn_over = True
            else:
                self.game.scoreboard.turn_score += roll
                self.game.scoreboard.display()
                print(f"{self.name}, you rolled a {roll}")
                choice = input("What do you want to do? (Roll/Hold) ")
                try:
                    if choice[0].lower() == "h":
                        self.score += self.game.scoreboard.turn_score
                        turn_over = True
                except:
                    pass

        if self.score >= SCORE_TO_WIN:
            print(f"{self.name} wins!")
            self.wins += 1
            return True
        return False

class ComputerPlayer:
    """makes a computer player with different selectable personalities"""
    def __init__(self, game, personality="scared"):
        self.game = game
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
                input("Press Enter to Continue")
                turn_over = True
            else:
                self.game.scoreboard.turn_score += roll
                self.game.scoreboard.display()
                print(f"{self.name} rolled a {roll}")
                choice = self.get_move()
                try:
                    if choice[0].lower() == "h":
                        self.score += self.game.scoreboard.turn_score
                        turn_over = True
                except:
                    pass

        if self.score >= SCORE_TO_WIN:
            print(f"{self.name} wins!")
            self.wins += 1
            return True
        return False

    def get_move(self):
        if self.game.scoreboard.turn_score + self.score >= SCORE_TO_WIN:
            move = "hold"
        elif self.game.scoreboard.turn_score < 15:
            move = "roll"
        else:
            move = "hold"
        print(f"They're going to {move}.")
        input("Press Enter to continue.")
        return move

class Personality:
    """a personality class designed to make moves in Pig"""
    def __init__(self, name=None):
        potential_names = ["Scared","Chaser","Smart"]
        if name in potential_names:
            self.name = name
        else:
            index = random.randint(0,(len(potential_names)-1))
            self.name = potential_names[index]

    # def get_move(my_score, opp_score, curr_score):
        
    

class Die:
    """makes 1 die and can roll it"""
    def __init__(self, sides=6):
        self.sides = sides

    def roll(self):
        return random.randint(1, self.sides)

game = PlayGame()
while True:
    game.play_game()