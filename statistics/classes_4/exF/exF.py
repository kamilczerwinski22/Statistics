# Script simulating Blackjack game. Player draw card until he exceeds 21 points. Number of cards drawn is collected.
# Graph of the probability of exceeding 21 points with the number of cards drawn is created.
# Author: Kamil Czerwiński, Jagiellonian University, CS 2020/2021

import random
import matplotlib.pyplot as plt


def blackjack_game() -> int:
    """
    Function simulating a single Blackjack game. The game ends when a player exceeds 21 points.
    :return: Number of cards needed to bust the game
    """
    # initial variables
    cards: list = ['2'] * 4 + ['3'] * 4 + \
                  ['4'] * 4 + ['5'] * 4 + \
                  ['6'] * 4 + ['7'] * 4 + \
                  ['8'] * 4 + ['9'] * 4 + \
                  ['10'] * 4 + ['K'] * 4 + \
                  ['Q'] * 4 + ['J'] * 4 + \
                  ['A'] * 4  # list simulating deck of cards
    score: int = 0
    num_of_cards: int = 0

    # main loop
    while score <= 21:
        card = cards.pop(random.randrange(len(cards)))
        if card.isnumeric():  # 2-10
            score += int(card)
            num_of_cards += 1
        else:
            if card == 'A':  # Ace
                score += 1
                num_of_cards += 1
            else:  # K, Q, J
                score += 10
                num_of_cards += 1
    return num_of_cards


def games_handler(num_of_iterations: int) -> None:
    """
    Function handling multiple games simulation, gathering data and generating adequate graphs.
    :param num_of_iterations: Number of Blackjack games to simulate
    :return: None
    """
    # initial variables
    # create dictionary to store number of card pulls with some starting values
    probability_dict: dict = {
                                0: 0,
                                1: 0,
                                2: 0,
                            }
    num_of_card_pulls: list = []
    final_end_game_probability: list = []
    quantity_of_pulls: list = []

    # play designated number of games
    for game in range(num_of_iterations):
        result = blackjack_game()
        if result not in probability_dict:
            probability_dict[result] = 1
        else:
            probability_dict[result] += 1

    # create final list with probabilities
    prev_value = 0
    for key, value in sorted(probability_dict.items()):
        num_of_card_pulls.append(key)
        final_end_game_probability.append((value+prev_value)/num_of_iterations)
        quantity_of_pulls.append(value)
        prev_value += value

    print(f"Number of cards drawn: {num_of_card_pulls}")
    print(f"Number of pulls: {quantity_of_pulls}")
    print(f"Probability of exceeding 21 points: {final_end_game_probability}")

    # draw graph
    fig, ax = plt.subplots()
    ax.plot(num_of_card_pulls, final_end_game_probability, color='red',
            marker='o', markerfacecolor='blue', markeredgecolor='black')

    ax.grid()
    plt.xticks(num_of_card_pulls)
    plt.yticks([prob/100 for prob in range(0, 101, 5)], [f'{prob/100:.0%}' for prob in range(0, 101, 5)])

    plt.ylabel(f"Probability of exceeding 21 points")
    plt.xlabel(f"Number of cards drawn")
    plt.title(f"Graph of probability of exceedance 21 points \nto the number of cards drawn", loc='left')
    fig.savefig(f"example1.png")
    plt.show()


if __name__ == '__main__':
    games_handler(10 ** 4)
