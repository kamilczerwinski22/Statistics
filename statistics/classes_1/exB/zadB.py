# A script for comparing theoretical and experimental values of player A's chance of bankruptcy depending on
# the probability of winning in single game
# Author: Kamil Czerwiński, Jagiellonian University, 2020/2021

import random
import matplotlib.pyplot as plt


def theory_probability(p: float, q: float, a_capital: int, b_capital: int) -> float:
    """
    Function for calculating theoretical probability for specified p, q, player A capital, player B capital.
    :param p: Probability of winning by player A
    :param q: Probability of winning by player B
    :param a_capital: Capital of player A
    :param b_capital: Capital of player B
    :return: Probability to win by player A
    """
    capital_sum: int = a_capital + b_capital
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
    population = ['A', 'B']
    weights = [p, q]
    A_loses = 0

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
            A_loses += 1
    return A_loses / iterations


def generate_theory_list(a_capital, b_capital) -> list:
    """
    Function for generating list with theoretical probability values.
    :param a_capital: Capital of player A
    :param b_capital: Capital of player B
    :return: List of theoretical values
    """
    lst = []
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
    Function for generating list with theoretical probability values.
    :param iterations: Number of games played
    :param a_capital: Capital of player A
    :param b_capital: Capital of player B
    :return: List of experimental values
    """
    lst = []
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
    theory_list = generate_theory_list(a_capital=a_capital, b_capital=b_capital)
    print(f'Theoretical list done')
    experimental_list = generate_experimental_list(iterations=iterations, a_capital=a_capital, b_capital=b_capital)
    print(f'Experimental list done')
    p_values = [x / 10.0 if x != 0 else 0 for x in range(0, 11)]

    # draw graph
    y_pos = range(len(experimental_list))
    plt.scatter(y_pos, experimental_list, color='green', edgecolor='black', label=f'Experimental values', zorder=3)
    plt.plot(theory_list, color='red', label=f'Theoretical values', zorder=2)
    plt.xticks(y_pos, p_values)
    plt.grid(axis='y')
    plt.yticks([i/10 for i in range(0, 11)], [f'{i}%' for i in range(0, 101, 10)])
    plt.ylabel('Chance of player A going bankrupt')
    plt.xlabel('P values')
    plt.title('Player A bankrupt chance chart', loc='left')
    plt.text(6.7, 1.1, f'A capital = {a_capital}, B capital = {b_capital},\n Iterations = {iterations}')
    plt.legend()
    plt.show()
    plt.savefig('example1.png')


if __name__ == '__main__':
    show_graph(1000, 50, 50)
