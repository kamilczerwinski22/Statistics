# Script simulating Blackjack game with two strategies - threshold strategy and basic strategy. Script generates graph
# comparing the probability of Player winning the game using different threshold values and basic strategy. To obtain
# comparable data independent of randomness of the game, simulation takes a large number of games and has the same
# random number generator seed for each strategy.
# Author: Kamil Czerwiński, Jagiellonian University, CS 2020/2021

import random
import matplotlib.pyplot as plt

# strategy dictionaries
soft_strategy: dict = {
    '8, 2': 'S', '8, 3': 'S', '8, 4': 'S', '8, 5': 'S', '8, 6': 'S',
    '8, 7': 'S', '8, 8': 'S', '8, 9': 'S', '8, 10': 'S', '8, 11': 'S',
    '7, 2': 'S', '7, 3': 'S', '7, 4': 'S', '7, 5': 'S', '7, 6': 'S',
    '7, 7': 'S', '7, 8': 'S', '7, 9': 'H', '7, 10': 'H', '7, 11': 'H',
    '6, 2': 'H', '6, 3': 'H', '6, 4': 'H', '6, 5': 'H', '6, 6': 'H',
    '6, 7': 'H', '6, 8': 'H', '6, 9': 'H', '6, 10': 'H', '6, 11': 'H',
}

hard_strategy: dict = {
    '17, 2': 'S', '17, 3': 'S', '17, 4': 'S', '17, 5': 'S', '17, 6': 'S',
    '17, 7': 'S', '17, 8': 'S', '17, 9': 'S', '17, 10': 'S', '17, 11': 'S',
    '16, 2': 'S', '16, 3': 'S', '16, 4': 'S', '16, 5': 'S', '16, 6': 'S',
    '16, 7': 'H', '16, 8': 'H', '16, 9': 'H', '16, 10': 'H', '16, 11': 'H',
    '12, 2': 'H', '12, 3': 'H', '12, 4': 'S', '12, 5': 'S', '12, 6': 'S',
    '12, 7': 'H', '12, 8': 'H', '12, 9': 'H', '12, 10': 'H', '12, 11': 'H',
    '11, 2': 'H', '11, 3': 'H', '11, 4': 'H', '11, 5': 'H', '11, 6': 'H',
    '11, 7': 'H', '11, 8': 'H', '11, 9': 'H', '11, 10': 'H', '11, 11': 'H',
}


def basic_strategy() -> bool:
    """
    Function simulating basic blackjack strategy in single game.
    :return: Player's win information (True/False)
    """
    # initial values
    # list simulating card deck
    cards: list = ['2'] * 4 + ['3'] * 4 + \
                  ['4'] * 4 + ['5'] * 4 + \
                  ['6'] * 4 + ['7'] * 4 + \
                  ['8'] * 4 + ['9'] * 4 + \
                  ['10'] * 4 + ['10'] * 4 + \
                  ['10'] * 4 + ['10'] * 4 + \
                  ['11'] * 4  # K Q J A
    croupier_cards: list = []
    player_cards: list = []
    player_score: int = 0
    stand: bool = False

    # main game
    # first pull - player and croupier take turns drawing cards
    player_cards.append(cards.pop(random.randrange(len(cards))))
    croupier_cards.append(cards.pop(random.randrange(len(cards))))
    player_cards.append(cards.pop(random.randrange(len(cards))))
    croupier_cards.append(cards.pop(random.randrange(len(cards))))
    croupier_show_card = croupier_cards[0]

    # player strategy
    while not stand:
        player_score = sum(int(x) for x in player_cards)

        # if player got Ace and went beyond 21 points use it as 1 point, else stay at using it as 11 points
        if '11' in player_cards and player_score > 21:
            player_cards.remove('11')
            player_cards.append('1')
            player_score = sum(int(x) for x in player_cards)

        # if player exceed 21 points he instantly loses
        if player_score > 21:
            return False

        # if player got Ace worth 11 points , play 'soft' strategy
        if '11' in player_cards:
            if player_score - 11 <= 6:  # hit
                current_strategy = soft_strategy[f'{6}, {croupier_show_card}']
            elif player_score - 11 >= 8:
                current_strategy = soft_strategy[f'{8}, {croupier_show_card}']
            else:
                current_strategy = soft_strategy[f'{player_score - 11}, {croupier_show_card}']

        # else play 'hard'
        else:
            if player_score >= 17:  # hit
                current_strategy = hard_strategy[f'17, {croupier_show_card}']
            elif player_score <= 11:
                current_strategy = hard_strategy[f'11, {croupier_show_card}']
            elif 16 >= player_score >= 13:
                current_strategy = hard_strategy[f'16, {croupier_show_card}']
            else:
                current_strategy = hard_strategy[f'{player_score}, {croupier_show_card}']

        # check current strategy
        if current_strategy == 'S':
            stand = True
        else:
            player_cards.append(cards.pop(random.randrange(len(cards))))

    # croupier strategy - draw cards until he has 17 or more points
    while True:
        croupier_score = sum(int(x) for x in croupier_cards)
        if croupier_score > 21 and player_score <= 21:
            return True
        if croupier_score >= 17:
            break
        croupier_cards.append(cards.pop(random.randrange(len(cards))))

    return player_score > croupier_score


def threshold_value_strategy(threshold: int) -> bool:
    """
    Function simulating threshold blackjack strategy in single game.
    :param threshold: Number of points a player has after reaching which he no longer draws cards (stand)
    :return: Player's win information (True/False)
    """
    cards = ['2'] * 4 + ['3'] * 4 + \
            ['4'] * 4 + ['5'] * 4 + \
            ['6'] * 4 + ['7'] * 4 + \
            ['8'] * 4 + ['9'] * 4 + \
            ['10'] * 4 + ['10'] * 4 + \
            ['10'] * 4 + ['10'] * 4 + \
            ['11'] * 4  # K Q J A

    croupier_cards = []
    player_cards = []
    player_score = 0
    stand = False

    # main game
    # first pull - player and croupier take turns drawing cards
    player_cards.append(cards.pop(random.randrange(len(cards))))
    croupier_cards.append(cards.pop(random.randrange(len(cards))))
    player_cards.append(cards.pop(random.randrange(len(cards))))
    croupier_cards.append(cards.pop(random.randrange(len(cards))))

    # player strategy
    while not stand:
        player_score = sum(int(x) for x in player_cards)

        # if player got Ace and went beyond 21 points use it as 1 point, else stay at using it as 11 points
        if '11' in player_cards and player_score > 21:
            player_cards.remove('11')
            player_cards.append('1')
            player_score = sum(int(x) for x in player_cards)

        # if player exceed 21 points he instantly loses
        if player_score > 21:
            return False

        if player_score >= threshold:
            break
        player_cards.append(cards.pop(random.randrange(len(cards))))

    # croupier strategy - draw cards until he has 17 or more points
    while True:
        croupier_score = sum(int(x) for x in croupier_cards)
        if croupier_score > 21 and player_score <= 21:
            return True
        if croupier_score >= 17:
            break
        croupier_cards.append(cards.pop(random.randrange(len(cards))))

    return player_score > croupier_score


def games_handler(num_of_games: int) -> None:
    """
    Functiong simulating threshold and basic Blackjack strategies for number of games. Adequate graphs are also
    generated. Simulation of each game in each strategy is implemented with the same random number generator seed (
    Every single game has different seed, but they are equal for every strategy e.g. Game one has seed=1 for each of
    threshold values and for basic strategy, game two has seed=2 for each of threshold values and for basic strategy
    etc.).
    :param num_of_games: Number of Blackjack games to perform each
    :return: None
    """
    # initial variables
    basic_strategy_score: int = 0
    threshold_values: list = [x for x in range(8, 21)]
    threshold_probabilities: list = []

    # basic strategy
    for seed in range(100, num_of_games + 100):
        random.seed(seed)
        if basic_strategy():
            basic_strategy_score += 1
    basic_strategy_win_ratio = basic_strategy_score / num_of_games
    basic_strategy_list = [basic_strategy_win_ratio] * len(threshold_values)
    print(f"Winning percentage for the basic strategy: {basic_strategy_win_ratio:.2%}")

    # threshold
    for i in range(8, 21):
        current_score = 0
        for seed in range(100, num_of_games + 100):
            random.seed(seed)
            if threshold_value_strategy(i):
                current_score += 1
        threshold_probabilities.append(current_score / num_of_games)
    print(f"Winning percentage for threshold strategies (value, probability): ")
    for value, probability in zip(threshold_values, threshold_probabilities):
        print(f"Threshold probability for {value} is {probability:.2%}")

    # draw graph
    fig, ax = plt.subplots()
    # threshold strategy plot
    ax.plot(threshold_values, threshold_probabilities, color='red', zorder=3, marker='o', markerfacecolor='blue',
            markeredgecolor='black', label='Threshold values')
    # basic strategy plot
    ax.plot(threshold_values, basic_strategy_list, color='magenta', zorder=2, label='Basic Strategy')

    ax.locator_params(axis='y', nbins=22)
    ax.grid(zorder=1)
    plt.xticks(threshold_values)

    plt.ylabel(f"Probability of winning")
    plt.xlabel(f"Threshold values")
    plt.title(f"Probability of winning relative to threshold value {num_of_games} games",
              loc='left')
    plt.legend()
    fig.savefig(f"example1.png")
    plt.show()


if __name__ == '__main__':
    games_handler(50000)
