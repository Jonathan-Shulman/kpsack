import math
import numpy as np


def binary_search_mitm(arr, low, high, x):
    # Check base case
    if high >= low:
        mid = math.ceil((high + low) / 2)

        # If element is present at the middle itself
        if arr[mid] == x or low == high:
            return mid

            # If element is smaller than mid, then the closes element with at most weight x must
        # be present in left subarray
        elif arr[mid] > x:
            return binary_search_mitm(arr, low, mid - 1, x)

        # Else the element with closes weight less than x can only be present in right subarray
        else:
            return binary_search_mitm(arr, mid, high, x)

    else:
        # failed search - shouldn't be possible with sensible input
        return -1


def merge_arrays(old_subsets, new_subsets, old_weights, new_weights):
    k = len(old_subsets)
    merged_weights = np.zeros(2 * k)
    merged_subsets = np.zeros(2 * k)
    old_index = 0
    new_index = 0
    for i in range(2 * k):
        if old_index >= k:
            merged_weights[i:] = new_weights[new_index:]
            merged_subsets[i:] = new_subsets[new_index:]
            break
        elif new_index >= k:
            merged_weights[i:] = old_weights[old_index:]
            merged_subsets[i:] = old_subsets[old_index:]
            break
        elif old_weights[old_index] <= new_weights[new_index]:
            merged_subsets[i] = old_subsets[old_index]
            merged_weights[i] = old_weights[old_index]
            old_index += 1
        else:
            merged_subsets[i] = new_subsets[new_index]
            merged_weights[i] = new_weights[new_index]
            new_index += 1
    return merged_subsets, merged_weights


def bin_array(num, length):
    """Convert a positive integer num into an m-bit bit vector with (the least significant digit in right)"""
    return np.array(list(np.binary_repr(np.uint64(num)).zfill(length))).astype(np.int8)


def number_to_subset_mask(num, length):
    """

    :param num: number we wish to convert to mask for a numpy array
    :param length: the length of the array. We must have 2 ^ length > num.
    :return: masking for the subset encoded by the number.
    """
    mask = np.full(length, False)
    bit_array = bin_array(num, length)
    for i in range(len(bit_array)):
        mask[i] = True if bit_array[len(bit_array) - 1 - i] == 1 else False
    return mask


def meet_in_the_middle_01(items, total_weight):
    """

    :param items: usual items array
    :param total_weight: total weight
    :return: solution in usual format
    Description:
    Meet in the middle algorithm for 0-1 knapsack.

    Conventions: len(items) = n, len(second) = k
    First, we divide items into two sub arrays, first and second. This division is arbitrary.
    We encode subsets of [n] by numbers i in the range 0 <= i < 2 ^ n, each number corresponding to the subset
    matching to it binary representation.

    We then use a sophisticated algorithm to sort the subsets of first in ascending order based on their total weight.
    This algorithm is special because it runs in O(2^k), i.e. LINEAR! in the amount of subsets.
    We store the result in two arrays:
    subsets_of_first: array of encodings of subsets (sorted).
    weights_subsets_of_first: array of the matching weights.

    Afterwards, we create the int array best_value_for_index. It satisfies:
    best_value_for_index[i] <= i, and best_value_for_index[i] is the index of the subset of weight <=
    weights_subsets_of_first[i] with maximal value.

    Values of these subsets are stored inside the dictionary values_for_best.


    Then, Iterating over second we find(binary search) for each subset the best matching subset in first such that
    their combined weight <= total_weight and return the resulting subset as an array.




    """
    n = len(items)
    first = items[:math.floor(n / 2)]
    k = len(first)
    second = items[math.floor(n / 2):]
    subsets_of_first = np.zeros(1)
    weights_subsets_of_first = np.zeros(1)
    # print(first)
    # print(second)
    for i in range(len(first)):
        # print(f"current weights: {weights_subsets_of_first.tolist()}")
        # print(
        #     f"new weights: {(weights_subsets_of_first + items[i][0]).tolist()}")
        # print(f"cur subsets: {subsets_of_first.tolist()}")
        # print(merge_arrays(subsets_of_first, subsets_of_first + (2 ** i),
        #                    weights_subsets_of_first,
        #                    weights_subsets_of_first + np.array(
        #                        [items[i][0] for j in
        #                         range(len(weights_subsets_of_first))])))
        subsets_of_first, weights_subsets_of_first = merge_arrays(subsets_of_first, subsets_of_first + (2 ** i),
                                                                  weights_subsets_of_first,
                                                                  weights_subsets_of_first + np.array(
                                                                      [items[i][0] for j in
                                                                       range(len(weights_subsets_of_first))]))
    # print(f"current weights: {weights_subsets_of_first}")
    #
    # print(f"cur subsets: {subsets_of_first}")
    best_subset_for_index = np.zeros(len(subsets_of_first))
    values_for_best = {0: 0}
    current_best_index = 0
    current_best_value = 0

    for i in range(len(subsets_of_first)):
        current_mask = number_to_subset_mask(subsets_of_first[i], k)
        current_value = np.sum(first[:, 1][current_mask])
        if current_value > current_best_value:
            current_best_index = i
            current_best_value = current_value
            best_subset_for_index[i] = current_best_index
            values_for_best[i] = current_best_value
        else:
            best_subset_for_index[i] = current_best_index
    # print(f"values for best {values_for_best}")
    # print(best_subset_for_index)
    # print(weights_subsets_of_first)
    # print(subsets_of_first)
    best_from_first = 0
    best_from_second = 0
    best_combined_value = 0

    for i in range(0, 2 ** (n - k), 1):
        current_mask = number_to_subset_mask(i, n - k)
        current_value = np.sum(second[:, 1][current_mask])
        current_weight = np.sum(second[:, 0][current_mask])
        index_of_matching_heaviest_subset = binary_search_mitm(weights_subsets_of_first, 0, (2 ** k) - 1,
                                                               total_weight - current_weight)
        index_of_best_match = best_subset_for_index[index_of_matching_heaviest_subset]
        value_of_best_match = values_for_best[index_of_best_match]
        if current_weight > total_weight:
            continue
        if value_of_best_match + current_value >= best_combined_value:
            # print(current_weight)
            # print(weights_subsets_of_first[index_of_matching_heaviest_subset])
            # print(index_of_matching_heaviest_subset)
            best_from_first = best_subset_for_index[index_of_matching_heaviest_subset]
            best_from_second = i
            best_combined_value = value_of_best_match + current_value

    # print(best_from_second)
    # print(best_from_first)
    # print(best_for_index)
    return np.flip(bin_array(subsets_of_first[np.int8(best_from_first)] + (2 ** k) * best_from_second, n))

