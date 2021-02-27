# Do zrobienia jeszcze czas oczekiwania na wykonanie (chyba po prawej stronie). Wtedy te wykresy zaczną się pokrywać

import math
import random
import matplotlib.pyplot as plt


def calculate_poissone(lambda_a, lambda_s):
    random_u1 = random.random()
    random_u2 = random.random()
    while random_u1 == 0 or random_u2 == 0:
        random_u1 = random.random()
        random_u2 = random.random()
    return (-(math.log(random_u1, 10) / lambda_a), -(math.log(random_u2, 10) / lambda_s))


def calculate_time(lambda_a, lambda_s, max_time):
    scheduled_list = []
    ending_time_list = []
    queue_list_scheduled = []
    queue_list_after = []
    li_time_sum = 0
    queue_pos = 0
    counter = 0
    while li_time_sum <= max_time:
        ti_current_in, tis_current = (round(x, 3) for x in calculate_poissone(lambda_a, lambda_s))
        li_time_sum += ti_current_in
        print(f"li time sum = {li_time_sum}")

        queue_pos_scheduled = sum(1 for element in ending_time_list if element > li_time_sum)
        queue_list_scheduled.append(queue_pos_scheduled)

        print(f"queue pos: {queue_pos}")
        scheduled_list.append(li_time_sum)
        if queue_pos_scheduled != 0:
            ending_time_list.append(ending_time_list[counter - 1] + tis_current)
            print(f"łota siet, nie udało się, jestem {queue_pos_scheduled} w kolejce")
        else:
            ending_time_list.append(li_time_sum + tis_current)
            print("Przed czasem, startuje na kolejce 0")

    for counter, element in enumerate(ending_time_list):
        temp = sum(1 for num in scheduled_list if num < element) - 2 - counter
        queue_list_after.append(temp if temp > 0 else 0)

        print(f"moment przyjscia zadania {counter + 1} = {scheduled_list[counter]}")
        print(f"czas dzialania {counter + 1} = {tis_current}")
        print(f"moment zakoczenia {counter + 1} = {ending_time_list[counter]}")
        print('------------------------')
    counter += 1
    print(f"List schedule = {scheduled_list}")
    print(f"List ending time for task = {ending_time_list}")
    print(f"list of queue position at start = {queue_list_scheduled}")

    print(f"list of queue position at end = {queue_list_after}")

    # y_pos = range(max(scheduled_list))

    # red
    plt.scatter(scheduled_list, queue_list_scheduled, color='red')
    # blue
    plt.scatter(ending_time_list, queue_list_after, color='blue')

    # (lambda_a - lambda_s) * t
    plt.plot([0, max_time], [0, (lambda_a - lambda_s) * max_time], color='green', label=f'(lambda_a - lambda_s) * t')

    # # ((lambda_a - lambda_s) * t) / lambda_s
    # plt.plot([0, max_time], [0, ((lambda_a - lambda_s) * max_time) / lambda_s], color='cyan', label=f'((lambda_a - lambda_s) * t) / lambda_s')


    for scheduled_num in range(len(scheduled_list)):
        plt.text(scheduled_list[scheduled_num],
                 queue_list_scheduled[scheduled_num] + 0.05,
                 scheduled_num + 1,
                 color='000000',
                 horizontalalignment="center")
    plt.title('Wykres zależności ilości zad w kolejce w miarę upływającego czasu', loc='left')
    plt.ylabel('Ilość zadań w kolejce')
    plt.xlabel('Czas')
    plt.xticks(sorted(ending_time_list + scheduled_list), [])
    plt.yticks(range(0, max(queue_list_scheduled) + 1))
    plt.grid(axis='x', color='#d6d6d6')
    plt.legend(loc='upper right')
    plt.show()
    print(li_time_sum)

    return 'done'


print(calculate_time(1 / 15, 1 / 100, 1000))
