# %%

import math

import numpy as np

f = open("input.txt").read().splitlines()
grid = [[char for char in row.split()] for r, row in enumerate(f)]
ops = grid[-1]
numbers = np.transpose(grid[:-1]).tolist()
p1 = 0
for nums, op in zip(numbers, ops):
    nums = list(map(int, nums))
    print(nums, op)
    if op == "+":
        p1 += sum(nums)
    else:
        p1 += math.prod(nums)

p1


# %%
