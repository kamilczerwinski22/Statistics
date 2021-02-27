# A script where for a given probability matrix (made from a markov chain)
# multiply it by itself N times until a convergence criterion is found (each successive
# multiplication yields very small changes), e.g. |P^n - P^(n-1)| < 10^(-5).
# The pi values show a steady state drive.
# Script will show theoretical results (experimental results in script B).
# Author: Kamil Czerwiński, Jagiellonian University, CS 2020/2021


import matplotlib.pyplot as plt


def multiply_matrix_by_matrix(first_matrix: list, second_matrix: list) -> list:
    """
    Function for performing matrix multiplication from scratch (without math modules).
    Result is matrix full of 0's, with dimension created according to pattern:
    (M x A) * (A x N) = M x N; E.g. 3x2 * 2x4 = 3x4 (3 rows & 4 cols in result matrix).
    :param first_matrix: First matrix for multiply represented as double nested list
    :param second_matrix: Second matrix for multiply represented as double nested list
    :return: Result matrix represented as double nested list
    """
    # main function logic
    result = [[0 for _ in range(len(second_matrix[0]))] for _ in range(len(first_matrix))]
    for i in range(len(first_matrix)):  # iteration through rows of first matrix
        for j in range(len(second_matrix[0])):  # iteration through cols of second matrix
            for k in range(len(second_matrix)):  # iteration through rows of second matrix
                result[i][j] += first_matrix[i][k] * second_matrix[k][j]
    return result


def highest(matrix: list) -> float:
    """
    Function for finding highest number in matrix.
    :param matrix: Given matrix to search in
    :return: Highest number in given matrix
    """
    return max(item for sublist in matrix for item in sublist)


def calculation_handler(convergence_criterion: float) -> tuple:
    """
    Function for handling matrix by matrix multiplication and performing main calculations.
    :param convergence_criterion: Assumed convergence criterion after which calculations stop
    :return: Tuple containing (result, counter), where result is matrix multiplied counter times by itself
    """
    # initial variables
    result: list = []
    base_matrix: list = [[0.64, 0.32, 0.04],
                         [0.4, 0.5, 0.1],
                         [0.25, 0.5, 0.25]]  # base Markov matrix used for calculating - can be changed
    next_matrix: list = base_matrix
    counter: int = 1

    # main function logic
    while True:
        prev_matrix = next_matrix
        next_matrix = multiply_matrix_by_matrix(next_matrix, base_matrix)
        result.append([x for sublist in prev_matrix for x in sublist])
        if abs(highest(prev_matrix) - highest(next_matrix)) < convergence_criterion:
            result.append([x for sublist in next_matrix for x in sublist])
            return result, counter
        counter += 1


def show_graph(elements: list, max_iteration_number: int) -> None:
    """
    Function for drawing graph adequate to received data.
    :param elements: List of matrix elements where each internal list represents changes in single field of original
    matrix
    :param max_iteration_number: Number of the maximum iteration at which the convergence criterion was reached
    :return: None
    """
    # initial variables
    colors = (
        'red', 'green', 'cyan', 'red', 'green', 'cyan', 'red', 'green', 'cyan', 'black', 'black', 'black', 'black')

    # draw graph
    for results, color in zip(elements, colors):
        y_pos = range(len(results))
        plt.plot(y_pos, results, color=color, label=f"P.p. = {results[0]}")
    plt.grid(zorder=0)
    plt.ylabel(f"Theoretical pi values")
    plt.xlabel(f"Number of iterations. Max iteration until convergence criterion meet: {max_iteration_number}")
    plt.title(f"Markov matrix graph example theoretical", loc='left')
    plt.legend(loc='upper right', fontsize='xx-small')
    plt.savefig(f"example1.png")
    plt.show()


def main() -> None:
    """
    Main program function
    :return: None
    """
    result, max_iteration = calculation_handler(0.00001)
    res_transpose = list(zip(*result))  # transposed result where each internal list represents changes of one original
    # matrix field as the iteration progresses
    show_graph(res_transpose, max_iteration)


if __name__ == '__main__':
    main()
