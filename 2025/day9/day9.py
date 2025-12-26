# %%
import matplotlib.pyplot as plt

biggest_coords = (0, 0), (0, 0)

f = [tuple(map(int, x.split(","))) for x in open("input.txt").read().splitlines()]
xmean, ymean = (
    sum(x for (x, _) in f) / len(f),
    (sum(y for (_, y) in f) / len(f)) - 1e2,
)

biggest = 0
for x, y in f:
    for x2, y2 in f:
        if (x, y) == (x2, y2):
            continue
        xlo, xhi = sorted((x, x2))
        ylo, yhi = sorted((y, y2))
        if any(xlo < x3 < xhi and ylo < y3 < yhi for (x3, y3) in f):
            continue
        if xlo < xmean < xhi and ylo < ymean < yhi:
            continue
        area = (abs(x - x2) + 1) * (abs(y - y2) + 1)
        if area > biggest:
            biggest = area
            biggest_coords = (x, y), (x2, y2)


print(biggest)
# 4618517036 high
# 1353351168 low
# %%
# plot the polygon

xys = f + [f[0]]
xs = [x for (x, _) in xys]
ys = [y for (_, y) in xys]
plt.plot(xs, ys)
plt.plot(
    [
        biggest_coords[0][0],
        biggest_coords[1][0],
        biggest_coords[1][0],
        biggest_coords[0][0],
        biggest_coords[0][0],
    ],
    [
        biggest_coords[0][1],
        biggest_coords[0][1],
        biggest_coords[1][1],
        biggest_coords[1][1],
        biggest_coords[0][1],
    ],
)
# mean
plt.plot([xmean], [ymean], "ro", markersize=2)
plt.show()
# %%
