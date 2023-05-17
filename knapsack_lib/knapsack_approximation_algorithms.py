import numpy as np
import knapsack_plotter as kplot
import pandas as pd
import math


def greedy_unbounded(items, capacity):
    """

    :param capacity:
    :param items:
    :return: solution to unbounded knapsack problem.
    This is a 2-factor approximation algorithm for the knapsack problem that runs in linear time.
    """
    solution = np.zeros(len(items))

    item_ratios = np.array([items[i][1] / items[i][0] for i in range(len(items))])
    # argsorting negative item_ratios to reverse order.
    index_of_sorted = np.argsort(-item_ratios)
    sorted_items = items[index_of_sorted]

    capacity_left = capacity

    for i in range(len(sorted_items)):
        amount_of_current = capacity_left // sorted_items[i][0]
        solution[index_of_sorted[i]] += amount_of_current
        capacity_left -= amount_of_current * sorted_items[i][0]

    return solution


def greedy_01(items, capacity):
    solution = np.zeros(len(items))

    item_ratios = np.array([items[i][1] / items[i][0] for i in range(len(items))])
    # argsorting negative item_ratios to reverse order.
    index_of_sorted = np.argsort(-item_ratios)
    sorted_items = items[index_of_sorted]

    capacity_left = capacity

    for i in range(len(sorted_items)):
        if sorted_items[i][0] > capacity:
            continue

        if sorted_items[i][0] > capacity_left:
            current_value = np.sum(items[:, 1][solution == 1])
            return solution if current_value > sorted_items[i][1] else np.eye(1, len(items), i)[0, :]
        else:
            solution[index_of_sorted[i]] += 1
            capacity_left -= sorted_items[i][0]

    return solution


if __name__ == '__main__':
    test_items = np.array([[2, 3], [3, 5], [10, 9]])
    sol = greedy_01(test_items, 10)
    print(sol)

    kplot.bar_solutions(test_items, sol, total=True)
