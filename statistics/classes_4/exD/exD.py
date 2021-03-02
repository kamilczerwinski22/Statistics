# Script that calculates population by state policy. Initial values are:
# - probability of boy being born,
# - probability of girl being born,
# - starting population,
# - percentage of fertility of the couples formed
# A simulation of two policies (one child, one son) of population control for 10 generations is created. Script
# generates graphs of the number of people depending on the generation number.
# Author: Kamil Czerwiński, Jagiellonian University, CS 2020/2021

import random
import matplotlib.pyplot as plt
from math import floor


# one child policy
def calculate_population_one_child(num_of_people: int, men_factor: float, fertility: float):
    """
    Function calculating number of people at each of the 10 iterations (generations) and generating adequate bar
    graph for one child politics (every couple has one child, regardless of gender).
    :param num_of_people: Number of people in first generation
    :param men_factor: Initial percentage of males in the population/probability of boy being born
    :param fertility: Percentage of fertility of the couples formed
    :return:
    """
    # initial variables
    population_list: list = [num_of_people]
    generations_list: list = [0]
    num_of_man: int = floor(num_of_people * men_factor)
    num_of_woman: int = num_of_people - num_of_man
    num_of_pairs: int = min(num_of_man, num_of_woman)
    kid_probability: list = [men_factor, 1 - men_factor]  # boy, girl

    # main loop with 10 iterations
    for iteration in range(1, 11):
        current_num_of_man = 0
        current_num_of_woman = 0
        # each population reduction
        for _ in range(floor(num_of_pairs * fertility)):
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

    print("One child policy")
    print(f"Generations number: {generations_list}")
    print(f"Population: {population_list}")

    # draw graph
    fig, ax = plt.subplots()
    ax.grid(zorder=1, axis='y')
    # ax.locator_params(axis='y', nbins=20)
    bars = ax.bar(generations_list, population_list, width=0.8, color='#0086C1', edgecolor='black', zorder=2)
    ax.ticklabel_format(style='plain')
    plt.yticks([num for num in range(0, num_of_people + 1, num_of_people // 10)])
    plt.xticks(generations_list)
    # print values above bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() * 0.5, 1.01 * height, '{}'.format(height), ha='center', va='bottom',
                fontproperties='serif', fontsize=8)
    plt.ylabel(f"Population size")
    plt.xlabel(f"Generations")
    plt.title(f"Population control - one child policy", loc='left')
    fig.savefig(f"example1.png")
    plt.show()


# One son policy
def calculate_population_one_son(num_of_people: int, men_factor: float, fertility: float):
    """
    Function calculating number of people at each of the 10 iterations (generations) and generating adequate bar
    graph for one child politics (every couple has has children until a boy is born).
    :param num_of_people: Number of people in first generation
    :param men_factor: Initial percentage of males in the population/probability of boy being born
    :param fertility: Percentage of fertility of the couples formed
    :return:
    """
    # initial variables
    population_list: list = [num_of_people]
    generations_list: list = [0]
    num_of_man: int = floor(num_of_people * men_factor)
    num_of_woman: int = num_of_people - num_of_man
    num_of_pairs: int = min(num_of_man, num_of_woman)
    kid_probability: list = [men_factor, 1 - men_factor]  # boy, girl

    # main loop with 10 iterations
    for iteration in range(1, 11):
        current_num_of_man = 0
        current_num_of_woman = 0
        # each population reduction
        for _ in range(floor(num_of_pairs * fertility)):
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

    print("One son policy")
    print(f"Generations number: {generations_list}")
    print(f"Population: {population_list}")

    # draw graph
    fig, ax = plt.subplots()
    ax.grid(zorder=1, axis='y')
    # ax.locator_params(axis='y', nbins=20)
    bars = ax.bar(generations_list, population_list, width=0.8, color='#0086C1', edgecolor='black', zorder=2)
    ax.ticklabel_format(style='plain')
    plt.yticks([num for num in range(0, num_of_people + 1, num_of_people//10)])
    plt.xticks(generations_list)
    # print values above bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() * 0.5, 1.01 * height, '{}'.format(height), ha='center', va='bottom',
                fontproperties='serif', fontsize=8)
    plt.ylabel(f"Population size")
    plt.xlabel(f"Generations")
    plt.title(f"Population control - one son policy", loc='left')
    fig.savefig(f"example2.png")
    plt.show()


if __name__ == '__main__':
    # initial variables
    initial_population = 10 ** 6
    main_men_factor = 0.51
    main_fertility = 0.92
    # calling functions
    calculate_population_one_child(initial_population, main_men_factor, main_fertility)
    calculate_population_one_son(initial_population, main_men_factor, main_fertility)
