# Script for calculating the average probability that a player wins in a single roll of the dice with a condition that
# his number must be greater than the opponent's (Player's dice roll > opponent's dice roll). Comparison of
# experimental probability value with expected theoretical value.
# Author: Kamil Czerwiński, Jagiellonian University, CS 2020/2021

import random


def roll_the_dices(num_of_iterations: int) -> None:
    """
    Function for simulating a set number of dice rolls. Results are automatically printed.
    :param num_of_iterations: Number of dice rolls to simulate
    :return: None
    """
    # initial variables
    player_wins: int = 0
    theoretical_win_chance: float = round(15/36, 4)

    # main loop
    for _ in range(num_of_iterations):
        croupier_roll = random.randint(1, 6)
        player_roll = random.randint(1, 6)
        if player_roll < croupier_roll:
            player_wins += 1

    experimental_win_chance = round(player_wins / num_of_iterations, 4)
    print(f"Results: \n"
          f"Theoretical probability of winning a single game: {theoretical_win_chance:.2%}\n"
          f"Experimental probability of winning a single game: {experimental_win_chance:.2%}")


if __name__ == '__main__':
    roll_the_dices(10**6)
