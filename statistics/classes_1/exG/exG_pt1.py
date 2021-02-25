# A script for showing number of wins trajectory for player A.
# Part 1: winning trajectory depending on number of the game
# Author: Kamil Czerwiński, Jagiellonian University, CS 2020/2021

import matplotlib.pyplot as plt
import random


def play_game(a_capital: int, b_capital: int, p: float) -> bool:
    """
    Function for performing single game. Return player A value (True/False).
    :param a_capital: Capital of player A
    :param b_capital: Capital of player B
    :param p: Probability to win single round by player A
    :return: Return player A value (True/False)
    """
    # initial variables
    population: list = ['A', 'B']
    weights: list = [p, 1 - p]

    # main game
    while True:
        if random.choices(population, weights)[0] == 'A':
            a_capital += 1
            b_capital -= 1
        else:
            a_capital -= 1
            b_capital += 1
        if a_capital == 0:
            return False
        if b_capital == 0:
            return True


def generate_color() -> tuple:
    """Helper function for generating random color.
     :return: Tuple (r, g, b) signifying color"""
    r: float = random.random()
    b: float = random.random()
    g: float = random.random()
    return r, g, b


def generate_game_grap(num_of_games: int, a_capital: int, b_capital: int) -> None:
    """
    Function for performing multiple games and generating adequate graph.
    :param num_of_games: Number of games to perform at each probability
    :param a_capital: Capital of player A
    :param b_capital: Capital of player B
    :return: None
    """
    # initial variables
    probabilities: list = [0.3, 0.5, 0.7]
    results_data: list = []

    # main program logic
    for probability in probabilities:
        current_game_results = [(0, 0)]
        current_game_wins = 0
        for game in range(1, num_of_games + 1):
            result = play_game(a_capital=a_capital, b_capital=b_capital, p=probability)
            if result:
                current_game_wins += 1
            current_game_results.append((game, current_game_wins))
        results_data.append(current_game_results)

    # draw graph
    fig, ax = plt.subplots()
    for idx, vals in enumerate(zip(results_data, probabilities), 2):
        plot, prob = vals
        color = generate_color()
        x_values = [pair[0] for pair in plot]
        y_values = [pair[1] for pair in plot]
        ax.step(x_values, y_values, color=color, zorder=idx, label=f'p={prob}')
    ax.grid(zorder=1)
    ticks_range = range(num_of_games + 1)
    plt.xticks(ticks_range)
    plt.yticks(ticks_range)
    plt.ylabel(f"Number of wins")
    plt.xlabel(f"Current game number")
    plt.title(f"Player A's winning trajectory for different probabilities\n"
              f"with initial capital A={a_capital}, B={b_capital}", loc='left')
    plt.legend()
    # fig.savefig("example1_pt1.png")
    plt.show()


if __name__ == '__main__':
    generate_game_grap(10, 50, 50)
