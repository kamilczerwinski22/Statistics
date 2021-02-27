# A script where we have N amount of users and N amount of states (same as exC but with different logging probability).
# Probabilities:
# Log in = 0.2
# Stay logged out = 0.8
# Log out = 1 - (0.008 * current state + 0.1)
# Stay logged in = 0.008 * current state + 0.1
# We simulate the trajectory - at each iteration each user have a change to be logged in or logged out (depending on
# users current state). We need to construct convergence graph.
# Values of Pi show the pursuit of a value to a stationary state.
# e.g.: At first we have state 0, because all users are logged out. After one iteration 5 users logged in - current
# state is 5, and so on. On the graph we show can show selected states.
# Author: Kamil Czerwiński, Jagiellonian University, CS 2020/2021

import random
import matplotlib.pyplot as plt


def change_state(users_list: list, iterations: int, x_to_track: int, leap: int) -> list:
    """
    Function for performing number of states changes for given user list.
    :param users_list: List of users for which we change states
    :param iterations: Number of state changes for each user
    :param x_to_track: Number of state to track
    :param leap: Number of iterations after which current dictionary status will be saved to results list
    :return: List of tracked state Pi values at each consecutive leap
    """
    # initial variables
    status_dic: dict = {x: 0 for x in range(len(users_list) + 1)}  # collecting number of occurrences of a given state
    chances_population: list = [0, 1]  # list for tracking if each user state: 0 - logged out, 1 - logged in
    chances_not_logged: list = [0.8, 0.2]  # probabilities to [stay logged out, log in] when user is not logged in
    results: list = []

    # main function logic
    for iteration in range(1, iterations + 1):
        current_x = sum(users_list)
        current_login_chance = 0.008 * current_x + 0.1
        current_logout_chance = 1 - current_login_chance
        chances_logged_weights = [current_logout_chance, current_login_chance]
        for idx, user in enumerate(users_list):
            if user == 0:
                users_list[idx] = random.choices(chances_population, chances_not_logged)[0]
            else:
                users_list[idx] = random.choices(chances_population, chances_logged_weights)[0]
        status_dic[sum(users_list)] += 1  # sum number of 1's in list - number of logged in users (current state)
        if iteration % leap == 0:
            results.append(status_dic[x_to_track] / iteration)
    return results


def show_graph(num_of_iterations: int, users: list, leap: int, xs_to_track: tuple) -> None:
    """
    Function for drawing graph adequate to received data.
    :param num_of_iterations: Number of each user login status possible changes
    :param users: List of users for which login status will be changed
    :param leap: Number of iterations after which dictionary status will be saved to results list
    :param xs_to_track: Number of states to track
    :return: None
    """
    # initial variables
    colors = ('red', 'black', 'green', 'blue', 'orange', 'olive', 'grey', 'brown', 'cyan', 'purple', 'pink')

    # draw graph
    for x, color in zip(xs_to_track, colors):
        results = change_state(users, num_of_iterations, x, leap)  # calculate Pi values for each state
        y_pos = range(len(results))
        plt.plot(y_pos, results, color=color, label=f"x = {x}")

    plt.grid(zorder=0, axis='y')
    plt.xticks(range(0, round(num_of_iterations / leap) + 1, round(num_of_iterations / (leap * 10))),  # values to index
               range(0, num_of_iterations + 1, round(num_of_iterations // 10)))  # values to show
    plt.ylabel(f"Experimental Pi values")
    plt.xlabel(f"Number of iterations: {num_of_iterations}, leap every: {leap}")
    plt.title(f"Markov matrix graph example experimental - {len(users)} users/states", loc='left')
    plt.legend(loc='upper right')
    plt.savefig(f"example1.png")
    plt.show()


def main() -> None:
    """
    Main function with all variables possible to change.
    :return: None
    """
    # initial variables
    users: list = [0 for _ in range(1, 101)]
    iterations: int = 10000
    leap: int = 10
    xs_to_track: tuple = (20, 25, 30, 35)

    # functions calling
    show_graph(num_of_iterations=iterations,
               users=users,
               leap=leap,
               xs_to_track=xs_to_track)


if __name__ == '__main__':
    main()
