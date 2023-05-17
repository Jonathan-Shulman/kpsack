import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def bar_solution(items, solution):
    fig, ax = plt.subplots(figsize=(10, 5))
    x_axis = np.arange(len(items))
    ax.bar(x_axis - 0.1, solution, width=0.2, color='blue', label=f"solution")

    plt.xlabel('Items: (Weight, Value)')
    plt.ylabel('Quantities')
    plt.title("Knapsack distribution of item quantities")
    plt.xticks(x_axis, [f"({item[0]}, {item[1]})" for item in items])
    plt.show()


def bar_solutions(items, *args, total=False):
    fig, ax = plt.subplots(figsize=(10, 5))
    x_axis = 0.8 * len(args) * np.arange(len(items))
    colors_list = ['b', 'r', 'y', 'g'] * len(args)
    for count, solution in enumerate(args):
        solution_weight = np.int32(np.sum(np.array([items[j][1] * args[count][j] for j in range(len(items))])))
        if total:
            ax.bar(x_axis - 0.4 * ((1 - len(args)) / 2 + count), args[count], width=0.4, color=colors_list[count],
                   label=f"solution {count + 1}: value {solution_weight}")
        else:
            ax.bar(x_axis - 0.4 * ((1 - len(args)) / 2 + count), args[count], width=0.4, color=colors_list[count],
                   label=f"solution {count + 1}")

    plt.xlabel('Items: (Weight, Value)')
    plt.ylabel('Quantities')
    plt.title("Knapsack distribution of item quantities")
    plt.xticks(x_axis, [f"({item[0]}, {item[1]})" for item in items])
    ax.legend()
    plt.show()

