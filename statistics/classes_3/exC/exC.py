# Script showing the number of tasks in the system with their execution time when the system is clogging (tasks are
# arriving faster than the system can complete them).
# Version with a limitation of time in which tasks can appear in the system.
# Author: Kamil Czerwiński, Jagiellonian University, CS 2020/2021

import math
import random
import matplotlib.pyplot as plt


def calculate_poisson(lambda_a: float, lambda_s: float) -> tuple:
    """
    Function for calculating poisson values, where :'lambda a' is time needed for task to appear in the system,
    'lambda s' is time needed for system to execute the task.
    :param lambda_a: Average time of receipt of tasks into the system
    :param lambda_s: Average time of task execution by the system
    :return: Tuple (float, float) with poisson values for 'lambda a' and 'lambda s'
    """
    # initial variables
    random_u1 = random.random()
    random_u2 = random.random()

    # main function logic
    while random_u1 == 0 or random_u2 == 0:
        random_u1 = random.random()
        random_u2 = random.random()
    return -(math.log(random_u1, 10) / lambda_a), -(math.log(random_u2, 10) / lambda_s)


def calculate_time(lambda_a: float, lambda_s: float, max_time: int) -> None:
    """
    Function to simulate system operation with given values. Adequate graph is generated.
    :param max_time: Maximum time in which a task can enter the system
    :param lambda_a: Average time of receipt of tasks into the system
    :param lambda_s: Average time of task execution by the system
    :return: None
    """
    # initial variables
    scheduled_list: list = []  # list with the scheduled start time of the task with given index (task 0 - idx 0)
    ending_time_list: list = []  # list with the scheduled start time of the task with given index (task 0 - idx 0)
    queue_list_scheduled: list = []  # list with the position of the task with given index  in the queue when
    # entering the system (task 0 - idx 0)
    queue_list_after: list = []  # list with queue length when task with given index is leaving the system (task 0 -
    # idx 0)
    li_time_sum: int = 0  # sum of time needed to execute all tasks in the system
    counter: int = 0  # counter to keep track of queue positions

    # main program logic
    while li_time_sum <= max_time:
        # calculate current task arrival, execution time
        ti_current_in, tis_current = (round(x, 3) for x in calculate_poisson(lambda_a, lambda_s))
        li_time_sum += ti_current_in  # sum time needed to complete task

        # check current task queue position
        queue_pos_scheduled = sum(1 for element in ending_time_list if element > li_time_sum)
        queue_list_scheduled.append(queue_pos_scheduled)

        scheduled_list.append(li_time_sum)  # add task starting time
        if queue_pos_scheduled != 0:  # if task starts immediately
            ending_time_list.append(ending_time_list[counter - 1] + tis_current)
            print(f"I'm not first, my position in queue is: {queue_pos_scheduled}")
        else:  # if task is in queue
            ending_time_list.append(li_time_sum + tis_current)
            print("I'm first, so I'm starting immediately")

    # calculate queue length when task is leaving the system
    for counter, element in enumerate(ending_time_list):
        temp = sum(1 for num in scheduled_list if num < element) - 2 - counter
        queue_list_after.append(temp if temp > 0 else 0)
    counter += 1

    # draw graph
    # task arrival time dots
    plt.scatter(scheduled_list, queue_list_scheduled, color='red', zorder=3)
    # task execution time dots
    plt.scatter(ending_time_list, queue_list_after, color='blue', zorder=2)
    # number of task above each task arrival dot
    for scheduled_num in range(len(scheduled_list)):
        plt.text(scheduled_list[scheduled_num],
                 queue_list_scheduled[scheduled_num] + 0.05,
                 scheduled_num + 1,
                 color='000000',
                 horizontalalignment="center", zorder=4)
    plt.xticks(sorted(ending_time_list + scheduled_list), [])
    plt.yticks(range(0, max(queue_list_scheduled) + 1))
    plt.grid(axis='x', color='#d6d6d6')
    plt.title(f"Graph of the dependence of the number of tasks in the queue \nas time passes - system clogging ",
              loc='left')
    plt.ylabel(f"Number of tasks in the queue")
    plt.xlabel(f"Time")
    plt.savefig(f"example1.png")
    plt.show()


if __name__ == '__main__':
    calculate_time(lambda_a=1 / 15,
                   lambda_s=1 / 100,
                   max_time=50)
