# Script that calculates population by state policy. Initial values are:
# - probability of boy being born,
# - probability of girl being born,
# - starting population,
# - percentage of fertility of the couples formed
# A simulation of two policies (one child, one son) of population control for 10 generations is created. Situation
# similar to exD, but this time some of the couples break the law and have 6 children, regardless of policy.
# Script generates graphs of the number of people depending on the generation number.
# Author: Kamil Czerwiński, Jagiellonian University, CS 2020/2021

import random
import matplotlib.pyplot as plt
from math import floor


# one child policy with % of couples breaking the law
def calculate_population_one_child_breaking_law(num_of_people: int, men_factor: float,
                                                fertility: float, breaking_law_percentage: float) -> None:
    """
    Function calculating number of people at each of the 10 iterations (generations) and generating adequate bar
    graph for one child politics (every couple has one child, regardless of gender). Some couples are breaking the
    law and have 6 children, regardless of policy.
    :param num_of_people: Number of people in first generation
    :param men_factor: Initial percentage of males in the population/probability of boy being born
    :param fertility: Percentage of fertility of the couples formed
    :param breaking_law_percentage: Chance for a couple to break the law
    :return: None
    """
    # initial variables with starting values
    population_list: list = [num_of_people]
    generations_list: list = [0]
    num_of_man: int = floor(num_of_people * men_factor)
    num_of_woman: int = num_of_people - num_of_man
    num_of_pairs: int = min(num_of_man, num_of_woman)
    cheating_weights: list = [breaking_law_percentage, 1 - breaking_law_percentage]
    cheating_available_choices: list = [True, False]
    kid_probability: list = [men_factor, 1 - men_factor]  # boy, girl

    # main loop with 10 iterations
    for iteration in range(1, 11):
        current_num_of_man = 0
        current_num_of_woman = 0
        # each population reduction
        for _ in range(floor(num_of_pairs * fertility)):
            # if couple is breaking the law, they will have 6 children
            cheating = random.choices(cheating_available_choices, cheating_weights)[0]
            if cheating:
                for _ in range(6):
                    child_gender = random.choices(["male", "female"], kid_probability)[0]
                    if child_gender == "male":
                        current_num_of_man += 1
                    else:
                        current_num_of_woman += 1
            else:
                child_gender = random.choices(["male", "female"], kid_probability)[0]
                if child_gender == "male":
                    current_num_of_man += 1
                else:
                    current_num_of_woman += 1
        # updating variables
        num_of_man = current_num_of_man
        num_of_woman = current_num_of_woman
        num_of_pairs = min(current_num_of_woman, current_num_of_man)
        population_list.append(num_of_woman + num_of_man)
        generations_list.append(iteration)

    print(f"One child politics with {breaking_law_percentage:.0%} of couples breaking the law")
    print(f"Generations number: {generations_list}")
    print(f"Population: {population_list}")

    # draw graph
    fig, ax = plt.subplots()

    # generate bars
    bars = ax.bar(generations_list, population_list, width=0.8, color='#0086C1', edgecolor='black', zorder=2)

    # print values above bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() * 0.5, 1.01 * height, '{}'.format(height), ha='center', va='bottom',
                fontproperties='serif', fontsize=8)

    ax.ticklabel_format(style='plain')
    plt.yticks([num for num in range(0, num_of_people + 1, num_of_people // 10)])
    plt.xticks(generations_list)
    ax.grid(zorder=1, axis='y')

    plt.ylabel(f"Population size")
    plt.xlabel(f"Generations")
    plt.title(f"Population control - one child policy \n{breaking_law_percentage:.0%} of couples break the law",
              loc='left')
    fig.savefig(f"example1.png")
    plt.show()


# one son policy with % of couples breaking the law
def calculate_population_one_son_breaking_law(num_of_people: int, men_factor: float,
                                              fertility: float, breaking_law_percentage: float):
    """
    Function calculating number of people at each of the 10 iterations (generations) and generating adequate bar
    graph for one child politics (every couple has has children until a boy is born). Some couples are breaking the
    law and have 6 children, regardless of policy.
    :param num_of_people: Number of people in first generation
    :param men_factor: Initial percentage of males in the population/probability of boy being born
    :param fertility: Percentage of fertility of the couples formed
    :param breaking_law_percentage: Chance for a couple to break the law
    :return: None
    """
    # initial variables with starting values
    population_list: list = [num_of_people]
    generations_list: list = [0]
    num_of_man: int = floor(num_of_people * men_factor)
    num_of_woman: int = num_of_people - num_of_man
    num_of_pairs: int = min(num_of_man, num_of_woman)
    cheating_weights: list = [breaking_law_percentage, 1 - breaking_law_percentage]
    cheating_available_choices: list = [True, False]
    kid_probability: list = [men_factor, 1 - men_factor]  # boy, girl

    # main loop with 10 iterations
    for iteration in range(1, 11):
        current_num_of_man = 0
        current_num_of_woman = 0
        # each population reduction
        for _ in range(floor(num_of_pairs * fertility)):
            # if pair is cheating the system, they will have 6 children despite law regulations
            if random.choices(cheating_available_choices, cheating_weights)[0]:
                for _ in range(6):
                    child_gender = random.choices(["male", "female"], kid_probability)[0]
                    if child_gender == "male":
                        current_num_of_man += 1
                    else:
                        current_num_of_woman += 1
            else:
                while True:
                    child_gender = random.choices(["male", "female"], kid_probability)[0]
                    if child_gender == "male":
                        current_num_of_man += 1
                        break
                    else:
                        current_num_of_woman += 1
        # updating variables
        num_of_man = current_num_of_man
        num_of_woman = current_num_of_woman
        num_of_pairs = min(current_num_of_woman, current_num_of_man)
        population_list.append(num_of_woman + num_of_man)
        generations_list.append(iteration)

    print(f"One son politics with {breaking_law_percentage:.0%} of couples breaking the law")
    print(f"Generations number: {generations_list}")
    print(f"Population: {population_list}")

    # draw graph
    fig, ax = plt.subplots()

    # generate bars
    bars = ax.bar(generations_list, population_list, width=0.8, color='#0086C1', edgecolor='black', zorder=2)

    # print values above bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() * 0.5, 1.01 * height, '{}'.format(height), ha='center', va='bottom',
                fontproperties='serif', fontsize=8)

    ax.grid(zorder=1, axis='y')
    ax.ticklabel_format(style='plain')
    plt.yticks([num for num in range(0, num_of_people + 1, num_of_people // 10)])
    plt.xticks(generations_list)

    plt.ylabel(f"Population size")
    plt.xlabel(f"Generations")
    plt.title(f"Population control - one son policy \n{breaking_law_percentage:.0%} of couples break the law",
              loc='left')
    fig.savefig(f"example2.png")
    plt.show()


if __name__ == '__main__':
    # initial variables
    initial_population = 10 ** 6
    main_men_factor = 0.51
    main_fertility = 0.92
    main_breaking_law = 0.06
    # calling functions
    calculate_population_one_child_breaking_law(initial_population, main_men_factor, main_fertility, main_breaking_law)
    calculate_population_one_son_breaking_law(initial_population, main_men_factor, main_fertility, main_breaking_law)
