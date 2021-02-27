# A script where starting from Markov chain node we draw the probability of passing from one node to another
# according to the given probability matrix (made from Markov chain). We do this many times. In the end we check how
# many times we visited each node.
# The pi values show a steady state drive.
# Script will show experimental results (theoretical results in script A).
# Author: Kamil Czerwiński, Jagiellonian University, CS 2020/2021

import matplotlib.pyplot as plt
import random


def calculations_handler(x_pos: int, iterations: int, leap: int) -> list:
    """
    Function for performing experimental calculations.
    :param x_pos: Starting node
    :param iterations: Number of node changes performed
    :param leap: Number of iterations after which current dictionary status will be saved to results list
    :return: List of list, where internal list represents dictionary status at each consecutive leap
    """
    # initial values
    status_dic: dict = {x: 0 for x in range(0, 3)}  # collecting information on the number of nodes visits
    results: list = []
    base_matrix: list = [[0.64, 0.32, 0.04],
                         [0.4, 0.5, 0.1],
                         [0.25, 0.5, 0.25]]  # base Markov matrix used for calculating - can be changed
    chances_states: list = [0, 1, 2]  # list used to keep track of current node and it's transition probabilities

    # main function logic
    for cur_iter in range(1, iterations + 1):
        current_chances = base_matrix[x_pos]
        x_pos = random.choices(chances_states, current_chances)[0]
        status_dic[x_pos] += 1
        if cur_iter % leap == 0:
            current_x_list = [x / cur_iter for x in status_dic.values()]
            results.append(current_x_list)
    return results


def show_graph(elements: list, num_of_iterations: int, leap: int) -> None:
    """
    Function for drawing graph adequate to received data.
    :param leap: Number of iterations after which dictionary status will be saved to results list
    :param elements: List of matrix elements where each internal list represents changes in single field of original
    matrix
    :param num_of_iterations: Number of iterations (node changes) to perform
    :return: None
    """
    # initial variables
    colors = (
        'red', 'green', 'cyan', 'red', 'green', 'cyan', 'red', 'green', 'cyan', 'black', 'black', 'black', 'black')

    # draw graph
    for idx, (results, color) in enumerate(zip(elements, colors)):
        y_pos = range(len(results))
        plt.plot(y_pos, results, color=color, label=f"x. = {idx}")
    plt.grid(zorder=0, axis='y')
    plt.xticks(range(0, round(num_of_iterations / leap) + 1, round(num_of_iterations / (leap * 10))),  # values to index
               range(0, num_of_iterations + 1, round(num_of_iterations // 10)))  # values to show
    plt.ylabel(f"Experimental pi values")
    plt.xlabel(f"Number of iterations: {num_of_iterations}, leap every: {leap}")
    plt.title(f"Markov matrix graph example experimental", loc='left')
    plt.legend(loc='upper right', fontsize='xx-small')
    plt.savefig(f"example1.png")
    plt.show()


def main() -> None:
    """
    Main program function.
    :return: None
    """
    iterations: int = 10000  # number of node jump/changes
    leap: int = 10  # dictionary with nodes visits amount will be saved each leap
    x_pos_start: int = 2  # starting node
    result = calculations_handler(x_pos_start, iterations, leap)
    res_transpose = list(zip(*result))  # transposed result where each internal list represents changes of one original
    # matrix field as the iteration progresses
    show_graph(res_transpose, iterations, leap)


if __name__ == '__main__':
    main()
