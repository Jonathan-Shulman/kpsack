import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import memoization_algorithms as ma
import meet_in_the_middle as mitm
import knapsack_plotter as kplot

if __name__ == '__main__':
    
    for i in range(5):
        random_len = 17
        random_weights = np.random.randint(60, size=random_len) + 5
        random_costs = np.random.randint(60, size=random_len) + 5
        random_items = np.vstack((random_weights, random_costs)).reshape(random_len, 2)
        meet_sol = mitm.meet_in_the_middle_01(random_items, 100)
        memo_sol = ma.memoization_01(random_items, 100)
        kplot.bar_solutions(random_items, memo_sol, meet_sol)
