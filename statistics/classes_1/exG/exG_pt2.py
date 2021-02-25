# A script for showing number of wins trajectory for player A.
# Part 1: Player A's capital depending on number of the game
# Author: Kamil Czerwiński, Jagiellonian University, CS 2020/2021

import matplotlib.pyplot as plt
import random


def play_game(a_capital: int, b_capital: int, p: float) -> list:
    """
    Function for performing single game.
    :param a_capital: Capital of player A
    :param b_capital: Capital of player B
    :param p: Probability to win single round by player A
    :return: List of (turn, capital) tuples containing player's A capital each turn.
    """
    # initial variables
    population: list = ['A', 'B']
    weights: list = [p, 1 - p]
    player_a_capital_turns: list = [(0, a_capital)]
    turn: int = 0

    # main game
    while True:
        if random.choices(population, weights)[0] == 'A':
            a_capital += 1
            b_capital -= 1
        else:
            a_capital -= 1
            b_capital += 1
        turn += 1
        player_a_capital_turns.append((turn, a_capital))
        if a_capital == 0:
            break
        if b_capital == 0:
            break
    return player_a_capital_turns


def generate_color() -> tuple:
    """Helper function for generating random color.
     :return: Tuple (r, g, b) signifying color"""
    r: float = random.random()
    b: float = random.random()
    g: float = random.random()
    return r, g, b


def generate_game_grap(a_capital: int, b_capital: int) -> None:
    """
    Function for performing multiple games and generating adequate graph.
    :param a_capital: Capital of player A
    :param b_capital: Capital of player B
    :return: None
    """
    # initial variables
    probabilities: list = [0.25, 0.5, 0.75]
    results_data: list = []

    # main program logic
    for probability in probabilities:
        result = play_game(a_capital=a_capital, b_capital=b_capital, p=probability)
        results_data.append(result)
    print(results_data)
    # draw graph
    fig, ax = plt.subplots()
    for current_plot_data, current_p in zip(results_data, probabilities):
        color = generate_color()
        x_values = [pair[0] for pair in current_plot_data]
        y_values = [pair[1] for pair in current_plot_data]
        ax.step(x_values, y_values, color=color, zorder=3, label=f'p={current_p}')
    ax.grid(zorder=1)
    ax.locator_params(axis='x', nbins=22)
    plt.yticks(range(0, a_capital + b_capital + 1, round((a_capital + b_capital) / 20)))
    plt.ylabel(f"Capital")
    plt.xlabel(f"Current game number")
    plt.title(f"Player A's capital for different probabilities\n"
              f"with initial capital A={a_capital}, B={b_capital}", loc='left')
    plt.legend()
    # fig.savefig("example1_pt2.png")
    plt.show()


if __name__ == '__main__':
    generate_game_grap(20, 20)
