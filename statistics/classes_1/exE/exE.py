# A script for showing maximal game length for player A's winning in single turn probabilities.
# Author: Kamil Czerwiński, Jagiellonian University, CS 2020/2021

import matplotlib.pyplot as plt
import random


def play_game(a_capital: int, b_capital: int, p: float) -> int:
    """
    Function for performing a single game.
    :param a_capital: Capital of player A
    :param b_capital: Capital of player B
    :param p: Probability to win single round (turn) by player A
    :return: Number of turns in the played game
    """
    # initial variables
    population: list = ['A', 'B']
    weights: list = [p, 1 - p]
    game_turn: int = 0

    # main game
    while True:
        if random.choices(population, weights)[0] == 'A':
            a_capital += 1
            b_capital -= 1
        else:
            a_capital -= 1
            b_capital += 1
        game_turn += 1
        if a_capital == 0 or b_capital == 0:
            break
    return game_turn


def generate_game_grap(games_number_per_probability: int, a_capital: int, b_capital: int) -> None:
    """
    Function for performing multiple games and generating adequate graph.
    :param games_number_per_probability: Number of games to perform at each probability
    :param a_capital: Capital of player A
    :param b_capital: Capital of player B
    :return: None
    """
    # initial variables
    probability_for_turns: list = []
    most_turns: list = []

    # main program logic
    for current_prob in range(0, 101, 10):
        a_win_probability = current_prob / 100
        print(f"Current p: {a_win_probability}")
        current_highest = 0
        for game in range(games_number_per_probability):
            game_length = play_game(a_capital=a_capital, b_capital=b_capital, p=a_win_probability)
            if game_length > current_highest:
                current_highest = game_length
        probability_for_turns.append(a_win_probability)
        most_turns.append(current_highest)

    # draw graph
    fig, ax = plt.subplots()
    ax.locator_params(axis='y', nbins=22)
    x_pos = [x for x in range(len(probability_for_turns))]
    bars = ax.bar(x_pos, most_turns, color='green', edgecolor='black', zorder=2)
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() * 0.5, 1.01 * height, '{}'.format(height), ha='center', va='bottom',
                fontproperties='serif', fontsize=9)
    plt.xticks(x_pos, probability_for_turns)
    ax.grid(axis='y', zorder=1)
    plt.ylabel(f"Lmax")
    plt.xlabel(f"p(A)")
    plt.title(f"Distribution of the maximum game length at {games_number_per_probability} games")
    fig.savefig("example1.png")
    plt.show()


if __name__ == '__main__':
    generate_game_grap(games_number_per_probability=1000,
                       a_capital=50,
                       b_capital=50)
