# %%
from itertools import count, product
from math import prod, sqrt

from tqdm import tqdm


def dist(a, b):
    return sqrt(sum([((a[i] - b[i]) ** 2) for i in range(len(a))]))


f = open("input.txt").read().splitlines()
boxes = [tuple(map(int, x.split(","))) for x in f]
dists = {dist(b1, b2): (b1, b2) for (b1, b2) in product(boxes, boxes) if b1 != b2}
cir2boxes = {i: [b] for (i, b) in enumerate(boxes)}
box2cir = {b: i for (i, b) in enumerate(boxes)}
p2 = None
num_circuits = len(cir2boxes)
for i in tqdm(count()):
    if len(dists) == 0:
        break
    shortest = dists.pop(min(dists.keys()))
    new_cir = box2cir[shortest[0]]
    change_cir = box2cir[shortest[1]]
    if new_cir == change_cir:
        continue
    num_circuits -= 1
    if num_circuits == 1:
        p2 = shortest[0][0] * shortest[1][0]
        break
    change_boxes = cir2boxes[change_cir]
    for box in change_boxes:
        box2cir[box] = new_cir
    cir2boxes[new_cir] = cir2boxes[new_cir] + change_boxes
    cir2boxes.pop(change_cir)
    if i == 1000:
        print(prod(sorted([len(v) for v in cir2boxes.values()])[-3:]))
print(p2)
