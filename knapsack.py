import numpy as np
import functools
import time

arr = np.array([[5, 7],[7, 11], [11, 17]])
print(arr)
'''
A knapsack array is an np array of shape (n, 2).
arr[i][0] is the weight of the i'th item.
arr[i][1] is the value of the i'th item.
 
'''


def cache_decorator(func):
    cache = {}

    def wrapper(arr, w):
        wrapper.cache = cache
        if w in cache.keys():
            return cache[w]
        else:
            cache[w] = func(arr, w)
            return cache[w]

    return wrapper


def time_decorator(func):
    def wrapper(arr, w):
        s_time = time.time()
        ret_val = func(arr, w)
        e_time = time.time()
        print(f"The total time is {e_time - s_time}")
        return ret_val

    return wrapper


@cache_decorator
def knapsack_recursive(arr, w):
    cur_max = 0
    max_index = 0
    if w <= cur_max:
        return cur_max
    for i in range(len(arr)):
        if arr[i][0] <= w :
            new_val = arr[i][1] + knapsack_recursive(arr, w - arr[i][0])
            if cur_max < new_val:
                cur_max = new_val


    return cur_max



def knapsack_01_find_optimal_items(cache, arr, w):
    return_arr = [0 for i in range(len(arr))]
    cur_weight = w
    for i in range(len(arr) - 1, 0, -1):
        if cache[(cur_weight, i)] > cache[(cur_weight, i-1)]:
            return_arr[i] = 1
            cur_weight -= arr[i][0]
    if cur_weight >= arr[0][0]:
        return_arr[0] = 1
    return return_arr





def cache_decorator_01(func):
    cache = {}

    def wrapper(arr, w, index):
        wrapper.cache = cache
        if (w, index) in cache.keys():
            return cache[(w, index)]
        else:
            cache[(w, index)] = func(arr, w, index)
            return cache[(w, index)]

    return wrapper


@cache_decorator_01
def knapsack_01_recursive(arr, w, index):
    if w <= 0 or index < 0:
        return 0
    if w < arr[index][0]:
        return knapsack_01_recursive(arr, w, index - 1)
    return max(knapsack_01_recursive(arr, w, index - 1),
               arr[index][1] + knapsack_01_recursive(arr, w - arr[index][0], index - 1))

#
# s_time = time.time()
# print(knapsack_recursive(arr, 100))
# e_time = time.time()
# print(f"The total time is {e_time - s_time} seconds")


s_time = time.time()
print(knapsack_01_recursive(arr, 12, 2))
e_time = time.time()
print(f"The total time is {e_time - s_time} seconds")
print(knapsack_01_find_optimal_items(knapsack_01_recursive.cache, arr, 12))
