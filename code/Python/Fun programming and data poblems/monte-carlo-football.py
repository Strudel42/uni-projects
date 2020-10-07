import random
import numpy as np

TOTAL_GAMES = 100000


# Games are comprised of 7 matche

# Super helpful as it can break simulations down by number of losses and wins
class GameResult:
    wins = 0
    losses = 0

    def __init__(self, wins, losses):
        self.wins = wins
        self.losses = losses


# this function checks if your random number drawn from a uniform random distribution function is less that p_win (in
# this case p_win is 0.550)

def generate_result(p_win):
    i = random.uniform(0, 1)
    return i < p_win


# This basically counts how many wins or losses you get so while wins is <= 3 and losses <= 3 it will see if you won
# a game or not using a number between 0 and 1 as an input (win percentage) when it hits 4 wins or 4 losses then it
# will stop the loop and put it in the game result class as 4 wins 3 losses then it will start again if you include
# the function in a loop of total games that is to say that if you look at the foor loop at (line 45-47) it will play
# the game for 100000 simulations (in this case as TOTAL_GAMES is set to 100000)

def play_game(p_win_chance):
    wins = 0
    losses = 0
    while wins <= 3 and losses <= 3:
        if generate_result(p_win_chance):
            wins += 1
        else:
            losses += 1
    return GameResult(wins, losses)


# This function basically adds the wins and losses and counts that into a result ie if number_of_matches == 4 Then it
# will count all games that are 4 wins 0 losses or 4 losses 0 wins so for 5 as an input it will count all games with
# 4 wins and 1 loss and vice versa Note it that obviously it work within 4,5,6 or 7 but anything less than 4 and
# greater than 7 will not work
def games_concluded_in_matches(number_of_mathces):
    result = 0

    for GameResult in game_results:
        if GameResult.wins + GameResult.losses == number_of_mathces:
            result += 1
    return result


game_results = [None] * TOTAL_GAMES
for i in range(TOTAL_GAMES):
    game_results[i] = play_game(0.550)

number_w = 0  # Number of wins
number_l = 0  # Number of losses
for game_result in game_results:  # for loop which counts the number of wins and number of losses in the GameResults
    # array using the GameResult class.
    if game_result.wins >= 4:
        number_w += 1
    else:
        number_l += 1

probability_of_win = number_w / (number_w + number_l)
for i in range(4, 8):
    print('Probability of the game concluding after', i, 'matches is:',
          (games_concluded_in_matches(i) / TOTAL_GAMES) * 100, '%')

print('\n')

print(generate_result(0.9))

print('Probability of winning the game is: ', (probability_of_win * 100), '%',
      '\n')  # Again the game is comprised of 7 matches meaning that the chance to win at least 4 out of 7 matches is
# higher than 55% for a single match
