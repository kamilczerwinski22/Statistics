# A script for comparing theoretical and experimental values of player A's chance of bankruptcy depending on
# the probability of winning in single game
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
    :param p: Probability of winning by player A in single game turn
    :param q: Probability of winning by player B in single game turn
    :param a_capital: Capital of player A
    :param b_capital: Capital of player B
    :return: Probability to win game by player A
    """
    # initial variables
    population: list = ['A', 'B']
    weights: list = [p, q]
    a_loses: int = 0

    # main function logic
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


def generate_theory_list(a_capital: int, b_capital: int) -> list:
    """
    Function for generating list with theoretical win probability values at each probability.
    :param a_capital: Capital of player A
    :param b_capital: Capital of player B
    :return: List of theoretical win probability values
    """
    # initial variables
    lst: list = []

    # main function logic
    for x in range(0, 11):
        p = x / 10.0
        q = round(1 - p, 1)
        try:
            lst.append(theory_probability(p=p, q=q, a_capital=a_capital, b_capital=b_capital))
        except ZeroDivisionError:
            lst.append(1.0)
    return lst


def generate_experimental_list(iterations: int, a_capital: int, b_capital: int) -> list:
    """
    Function for generating list with experimental win probability values at each probability.
    :param iterations: Number of games played
    :param a_capital: Capital of player A
    :param b_capital: Capital of player B
    :return: List of experimental values
    """
    # initial variables
    lst: list = []

    # main function logic
    for x in range(0, 11):
        p = x / 10.0
        q = round(1 - p, 1)
        print(f"Current p = {p}, q = {q}")
        try:
            lst.append(experimental_probability(iterations=iterations,
                                                a_capital=a_capital,
                                                b_capital=b_capital,
                                                p=p,
                                                q=q))
        except ZeroDivisionError:
            lst.append(1.0)
    return lst


def show_graph(iterations: int, a_capital: int, b_capital: int) -> None:
    """
    Function for generating scatter/plot chart with experimental and theoretical values for player A winning
    probability.
    :param iterations: Number of games played
    :param a_capital: Capital of player A
    :param b_capital: Capital of player B
    :return: None
    """
    # initial variables and generating data
    theory_list: list = generate_theory_list(a_capital=a_capital,
                                             b_capital=b_capital)
    print(f'Theoretical list done')
    experimental_list: list = generate_experimental_list(iterations=iterations,
                                                         a_capital=a_capital,
                                                         b_capital=b_capital)
    print(f'Experimental list done')
    p_values: list = [x / 10.0 if x != 0 else 0 for x in range(0, 11)]

    # draw graph
    y_pos = range(len(experimental_list))
    plt.plot(theory_list, color='red', label=f'Theoretical values', marker='o', markerfacecolor='green',
             markeredgecolor='black')
    plt.xticks(y_pos, p_values)
    plt.grid(axis='y')
    plt.yticks([i / 10 for i in range(0, 11)], [f'{i}%' for i in range(0, 101, 10)])
    plt.ylabel("Chance of player A going bankrupt")
    plt.xlabel("P values")
    plt.title("Player A's bankrupt chance chart", loc='left')
    plt.text(6.7, 1.1, f'A capital = {a_capital}, B capital = {b_capital},\n Iterations = {iterations}')
    plt.legend()
    plt.savefig('example1.png')
    plt.show()


if __name__ == '__main__':
    show_graph(10000, 50, 50)
