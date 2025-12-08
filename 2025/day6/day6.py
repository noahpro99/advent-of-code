# %%
import math

import numpy as np

f = open("input.txt").read().splitlines()
grid = [[char for char in row.split()] for row in f]
ops = grid[-1]
numbers = np.transpose(grid[:-1]).tolist()
p1 = 0
for nums, op in zip(numbers, ops):
    nums = list(map(int, nums))
    if op == "+":
        p1 += sum(nums)
    else:
        p1 += math.prod(nums)

p2 = 0
grid = [[char for char in row] for row in f]
numbers = np.transpose(grid).tolist()
acc = 0
op = None
for col in numbers:
    if all(x == " " for x in col):
        p2 += acc
        acc = 0
        continue
    if col[-1] != " ":
        op = col[-1]
        if op == "*":
            acc = 1
    num = int("".join(col[:-1]))
    if op == "*":
        acc *= num
    if op == "+":
        acc += num
p2 += acc

print(p1, p2)
