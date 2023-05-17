import math
import numpy as np


def knapsack_recursive_unbounded(items, total_weight, cache_unbounded):
    """

    :param items:
    :param total_weight:
    :param cache_unbounded:
    :return: value of the best choice of items.
    """
    if total_weight in cache_unbounded.keys():
        return cache_unbounded[total_weight]

    max_profit = 0
    if total_weight <= 0:
        return 0
    for i in range(len(items)):
        if items[i][0] <= total_weight:
            current_profit = items[i][1] + knapsack_recursive_unbounded(items, total_weight - items[i][0],
                                                                        cache_unbounded)
            if current_profit > max_profit:
                max_profit = current_profit
    cache_unbounded[total_weight] = max_profit
    return max_profit


def knapsack_recursive_unbounded_setup_cache(items, total_weight, cache_unbounded_items):
    """

    :param items:
    :param total_weight:
    :param cache_unbounded_items:

    :return: value of the best choice of items.
    Additionally, cache_unbounded_items[total_weight][0] will be the maximal profit.
    Note that cache_unbounded_items[w] for w less than the weight of all items will be [0, 0].

    Using cache: cache_unbounded_items.
    """

    if total_weight in cache_unbounded_items.keys():
        return cache_unbounded_items[total_weight][0]

    max_profit = 0
    max_profit_index = 0
    if total_weight <= 0:
        return 0
    for i in range(len(items)):
        if items[i][0] <= total_weight:
            current_profit = items[i][1] + knapsack_recursive_unbounded_setup_cache(items, total_weight - items[i][0],
                                                                                    cache_unbounded_items)
            if current_profit > max_profit:
                max_profit = current_profit
                max_profit_index = i
    cache_unbounded_items[total_weight] = np.array([max_profit, max_profit_index])
    return max_profit


def knapsack_recursive_unbounded_get_items(items, total_weight, cache_unbounded_items, item_quantities):
    """

    :param items:
    :param total_weight:
    :param cache_unbounded_items:
    :param item_quantities:
    :return: item_quantities[i] will be the amount of items of type=i picked in the best solution.

    """

    if total_weight <= 0 or cache_unbounded_items[total_weight][0] <= 0:
        return
    item_quantities[cache_unbounded_items[total_weight][1]] += 1
    knapsack_recursive_unbounded_get_items(items, total_weight - items[cache_unbounded_items[total_weight][1]][0],
                                           cache_unbounded_items, item_quantities)
    return


def memoization_unbounded(items, total_weight):
    cache_unbounded_items = {}
    sol_arr_unbounded = np.zeros(len(items))
    knapsack_recursive_unbounded_setup_cache(items, total_weight, cache_unbounded_items)
    knapsack_recursive_unbounded_get_items(items, total_weight, cache_unbounded_items, sol_arr_unbounded)
    return sol_arr_unbounded


def knapsack_recursive_01(items, total_weight, index, cache_01):
    """

    :param items:
    :param total_weight:
    :param index:
    :param cache_01:
    :return:
    """
    if total_weight <= 0 or index < 0:
        return 0

    elif (total_weight, index) in cache_01.keys():
        return cache_01[(total_weight, index)]

    if total_weight < items[index][0]:
        cache_01[(total_weight, index)] = knapsack_recursive_01(items, total_weight, index - 1, cache_01)
        return cache_01[(total_weight, index)]

    cache_01[(total_weight, index)] = max(knapsack_recursive_01(items, total_weight, index - 1, cache_01),
                                          items[index][1] + knapsack_recursive_01(items, total_weight - items[index][0],
                                                                                  index - 1,
                                                                                  cache_01))
    return cache_01[(total_weight, index)]


def knapsack_recursive_01_get_items(items, total_weight, index, cache_01_items, item_quantities):
    """

    :param items:
    :param total_weight:
    :param cache_unbounded_items:
    :param item_quantities:
    :return: item_quantities[i] will be the amount of items of type=i picked in the best solution.

    """
    if index < 0:
        return
    if total_weight <= 0 or cache_01_items[(total_weight, index)][0] <= 0:
        return
    if cache_01_items[(total_weight, index)][1]:
        item_quantities[index] += 1
        knapsack_recursive_01_get_items(items, total_weight - items[index][0], index - 1, cache_01_items,
                                        item_quantities)
        return
    else:
        knapsack_recursive_01_get_items(items, total_weight, index - 1, cache_01_items,
                                        item_quantities)
    return


def knapsack_recursive_01_setup_cache(items, total_weight, index, cache_01_items):
    """

    :param items:
    :param total_weight:
    :param index:
    :param cache_01_items:
    :return: value of the best choice of items.
    Additionally, cache_unbounded_items[(total_weight, len - 1)][0] will be the maximal profit.
    Note that cache_unbounded_items[(w, index)] for w less than the weight of all items will be [0, 0].

    cache structure will be:
    cache_01_items(w, index) = [maximal profit with weight <= w and items of indices <= index, flag for including current]

    """
    if total_weight <= 0 or index < 0:
        return 0

    elif (total_weight, index) in cache_01_items.keys():
        return cache_01_items[(total_weight, index)][0]

    if total_weight < items[index][0]:
        cache_01_items[(total_weight, index)] = np.array(
            [knapsack_recursive_01_setup_cache(items, total_weight, index - 1, cache_01_items), 0])
        return cache_01_items[(total_weight, index)][0]
    profit_with_current = items[index][1] + knapsack_recursive_01_setup_cache(items, total_weight - items[index][0],
                                                                              index - 1,
                                                                              cache_01_items)
    profit_without_current = knapsack_recursive_01_setup_cache(items, total_weight, index - 1, cache_01_items)
    if profit_with_current >= profit_without_current:
        cache_01_items[(total_weight, index)] = np.array([profit_with_current, 1])
    else:
        cache_01_items[(total_weight, index)] = np.array([profit_without_current, 0])
    return cache_01_items[(total_weight, index)][0]


def knapsack_01_dp_optimized_space(items, total_weight):
    """

    :param items:
    :param total_weight:
    :return: value of the best choice of items.
    Optimized algorithm in terms of space complexity, O(W) instead of O(n * W).
    """

    dp = np.zeros(total_weight + 1)
    for i in range(len(items)):
        # by inverting the order of iteration over the range, we can achieve a similar "unbounded" algorithm.
        for w in range(total_weight, 0, -1):
            if items[i][0] <= w:
                dp[w] = max(dp[w], dp[w - items[i][0]] + items[i][1])
    return dp[total_weight]


def memoization_01(items, total_weight):
    """
    This algorithm is a concatenation of knapsack_recursive_01_get_items with knapsack_recursive_01_setup_cache.
    :param items:
    :param total_weight:
    :return:
    """
    cache_01_items = {}
    sol_arr_01 = np.zeros(len(items))
    knapsack_recursive_01_setup_cache(items, total_weight, len(items) - 1, cache_01_items)
    knapsack_recursive_01_get_items(items, total_weight, len(items) - 1, cache_01_items, sol_arr_01)
    return sol_arr_01
