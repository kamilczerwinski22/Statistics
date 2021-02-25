# A script for comparing theoretical and experimental values of player A's chance of bankruptcy depending on
# the capital of player A and capital of player B
# Version 2 with A from 0 to 100 every 10 steps
# Author: Kamil Czerwiński, Jagiellonian University, CS 2020/2021

import random
import matplotlib.pyplot as plt


def theory_probability(p: float, q: float, a_capital: int, b_capital: int) -> float:
    """
    Function for calculating theoretical probability for specified p, q, player A capital, player B capital.
    :param p: Probability of winning by player A in single game turn
    :param q: Probability of winning by player B in single game turn
    :param a_capital: Capital of player A
    :param b_capital: Capital of player B
    :return: Probability to win by player A
    """
    # initial variables
    capital_sum: int = a_capital + b_capital

    # main function logic
    if p == 0.5 and q == 0.5:
        calculated_probability = 1 - (a_capital / capital_sum)
    else:
        calculated_probability = ((q / p) ** a_capital - (q / p) ** capital_sum) / (1 - (q / p) ** capital_sum)
    return calculated_probability


def experimental_probability(iterations: int, a_capital: int, b_capital: int, p: float, q: float) -> float:
    """
    Function for calculating experimental probability for specified p, q, player A capital, player B capital.
    :param iterations: Number of games
    :param p: Probability of winning by player A
    :param q: Probability of winning by player B
    :param a_capital: Capital of player A
    :param b_capital: Capital of player B
    :return: Probability to win by player A
    """
    # initial variables
    population: list = ['A', 'B']
    weights: list = [p, q]
    a_loses: int = 0

    # main script logic
    for _ in range(iterations):
        A_capital_game = a_capital
        B_capital_game = b_capital
        while A_capital_game != 0 and B_capital_game != 0:
            if random.choices(population, weights)[0] == 'A':
                A_capital_game += 1
                B_capital_game -= 1
            else:
                B_capital_game += 1
                A_capital_game -= 1
        if A_capital_game == 0:
            a_loses += 1
    return a_loses / iterations


def generate_theory_list(p: float, q: float) -> list:
    """
    Function for generating list with theoretical win probability values at each for given capital values.
    :param p: Probability of player A win in single game turn
    :param q: Probability of player B win in single game turn
    :return: List of theoretical win probability values
    """
    # initial variables
    lst: list = []

    # main function logic
    for x in range(0, 101, 10):
        a_capital = x
        b_capital = 100 - x
        lst.append(theory_probability(p=p, q=q, a_capital=a_capital, b_capital=b_capital))
    return lst


def generate_experimental_list(iterations: int, p: float, q: float) -> list:
    """
    Function for generating list with experimental win probability values at each for given capital values.
    :param iterations: Number of games played
    :param p: Probability of player A win in single game turn
    :param q: Probability of player B win in single game turn
    :return: List of experimental win probability values
    """
    # initial variables
    lst: list = []

    # main function logic
    for x in range(0, 101, 10):
        a_capital = x
        b_capital = 100 - x
        print(f"Current: A = {a_capital}, B = {b_capital}")
        lst.append(experimental_probability(iterations=iterations,
                                            a_capital=a_capital,
                                            b_capital=b_capital,
                                            p=p,
                                            q=q))
    return lst


def show_graph(iterations: int, p: float, q: float) -> None:
    """
    Function for generating scatter/plot chart with experimental and theoretical values for player A winning
    probability depending on player A and player B capitals.
    :param iterations: Number of games played
    :param p: Probability of player A win in single game turn
    :param q: Probability of player B win in single game turn
    :return: None
    """
    # initial variables and generating data
    theory_list = generate_theory_list(p=p,
                                       q=q)
    print(f"Theoretical list done")
    experimental_list: list = generate_experimental_list(iterations=iterations,
                                                         p=p,
                                                         q=q)
    print(f"Experimental list done")
    a_list: list = [x for x in range(0, 101, 10)]

    # draw graph
    y_pos = range(len(experimental_list))
    plt.scatter(y_pos, experimental_list, color='green', edgecolor='black', label=f'Experimental values', zorder=3)
    plt.plot(theory_list, color='red', label=f'Theoretical values', zorder=2)
    plt.grid(axis='y')
    plt.xticks(y_pos, a_list)
    plt.yticks([i / 10 for i in range(0, 11)], [f'{i}%' for i in range(0, 101, 10)])
    plt.ylabel("Chance of player A going bankrupt")
    plt.xlabel("Player A's capital")
    plt.title("Player A's bankrupt chance chart", loc='left')
    plt.text(7.7, 1.1, f'p = {p}, q = {q},\n Iterations = {iterations}')
    plt.legend()
    # plt.savefig('example3_ver2.png')
    plt.show()


if __name__ == '__main__':
    show_graph(iterations=5000,
               p=0.47,
               q=0.53)
