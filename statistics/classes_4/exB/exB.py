# Script with a simulation of a given number of dice rolls (or until one of the players goes bankrupt). To win
# player's roll have to be higher than his opponent's (Player's dice roll > opponent's dice roll). Winning gives one
# coin to the player, losing takes one away.
# The script generates experimental and theoretical graphs of the dependence of capital on the number of games.
# The experimental average win per game is also compared to the theoretical value.
# Author: Kamil Czerwiński, Jagiellonian University, CS 2020/2021

import random
import matplotlib.pyplot as plt


def calculate_experimental(player_capital: int, num_of_games: int) -> tuple:
    """
    Function for calculating experimental capital after number of games.
    :param num_of_games: Number of dice rolls
    :param player_capital: Players starting capital
    :return: Tuple (capital, iterations) containing capital list, iterations number list, average winnings per game
    """
    # list with starting values
    capital_value_list = [player_capital]
    iterations_number_list = [0]

    # main game
    for iteration in range(1, num_of_games + 1):
        croupier_roll = random.randint(1, 6)
        player_roll = random.randint(1, 6)
        if player_roll < croupier_roll:
            player_capital += 1
        else:
            player_capital -= 1
        # if player gone bankrupt, break
        if player_capital <= 0:
            print("Player gone bankrupt!")
            capital_value_list.append(player_capital)
            iterations_number_list.append(iteration)
            break
        # add values to the list every 10 iterations
        if iteration % 10 == 0:
            capital_value_list.append(player_capital)
            iterations_number_list.append(iteration)

    win_per_game = round((capital_value_list[-1] - capital_value_list[0]) / iterations_number_list[-1], 3)
    print(f"Experimental value of winning in single game: {win_per_game}")

    return capital_value_list, iterations_number_list, win_per_game


def calculate_theoretical(player_capital: int) -> tuple:
    """
    Function for calculating theoretical capital. Player's theoretical winnings per game are -1/6.
    :param player_capital: Players starting capital
    :return: Tuple (capital, iterations) containing capital list, iterations number list and theoretical average
    winnings per game. For convenient reasons capital and iterations lists are normalized (only min and max value in
    lists)
    """
    capital_list: list = [player_capital, 0]
    iterations_list: list = [0, player_capital * 6]  # [starting turn, turn at which player's capital will hit 0]. *6
    # because of -1/6 winnings per game value
    game_winnings = round(-1/6, 3)
    print(f"Experimental value of winning in single game: {game_winnings}")
    return capital_list, iterations_list, game_winnings


def roll_the_dices(player_capital: int) -> None:
    """
    Function for generating data and drawing graphs.
    :param player_capital: Player's starting capital
    :return: None
    """
    # call functions
    experimental_list_capital, experimental_list_iterations, experimental_game_winnings = calculate_experimental(
        player_capital=player_capital, num_of_games=10**5)
    theory_list_capital, theory_list_iterations, theory_game_winnings = calculate_theoretical(
        player_capital=player_capital)

    # draw graph
    fig, ax = plt.subplots()
    ax.plot(experimental_list_iterations, experimental_list_capital, color='red', label=f'Experimental values')
    ax.plot(theory_list_iterations, theory_list_capital, color='blue', label=f'Theoretical values')
    ax.text(0.0, 0.0, f"Experimental average winnings per game: {experimental_game_winnings}\n"
                       f"Theoretical average winnings per game: {theory_game_winnings}")
    ax.grid()
    ax.legend()
    plt.ylabel(f"Player's capital")
    plt.xlabel(f"Number of dice rolls")
    plt.title(f"Capital dependence on the number of games\nStarting capital {player_capital}", loc='left')
    fig.savefig(f"example2.png")
    plt.show()


if __name__ == '__main__':
    roll_the_dices(5000)
