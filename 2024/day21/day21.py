# %%
import sys

sys.setrecursionlimit(int(1e6))

f = open("ex.txt").read().splitlines()
f
# %%

dir_pad = [
    [None, (-1, 0, 0), (0, 0, 1)],
    [(0, -1, 0), (1, 0, 0), (0, 1, 0)],
]

num_pad = [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], [None, "0", "A"]]


def pad_dists(pad):
    dists = {}
    for x in range(len(pad)):
        for y in range(len(pad[0])):
            if pad[x][y] is None:
                continue
            for x2 in range(len(pad)):
                for y2 in range(len(pad[0])):
                    if pad[x2][y2] is None:
                        continue
                    dists[pad[x][y] + pad[x2][y2]] = abs(x - x2) + abs(y - y2)
    return dists


np_dists = pad_dists(num_pad)
dp_dists = pad_dists(dir_pad)
dp_dists, np_dists
# %%


def neighbors(cur, code):
    neighbors = []
    r1x, r1y, r2x, r2y, r3x, r3y, ans = cur
    # robots 1 and 2 are on dir_pad and robot 3 is on num_pad
    for dx, dy, da, ds in [
        (0, 1, 0, ">"),
        (1, 0, 0, "v"),
        (0, -1, 0, "<"),
        (-1, 0, 0, "^"),
        (0, 0, 1, "A"),
    ]:
        if da == 1:
            b1x, b1y, b1a = dir_pad[r1x][r1y]
            if b1a == 1:
                b2x, b2y, b2a = dir_pad[r2x][r2y]
                if b2a == 1:
                    button3 = num_pad[r3x][r3y]
                    need_to_press = code[len(ans)]
                    print(button3, need_to_press)
                    if button3 != need_to_press:
                        continue
                    neighbors.append(
                        ((r1x, r1y, r2x, r2y, r3x, r3y, (*ans, button3)), ds)
                    )
                else:
                    r3x_new, r3y_new = r2x + b2x, r2y + b2y
                    if (
                        not (0 <= r3x_new < 4 and 0 <= r3y_new < 3)
                        or num_pad[r3x_new][r3y_new] is None
                    ):
                        continue
                    neighbors.append(((r1x, r1y, r2x, r2y, r3x_new, r3y_new, ans), ds))
            else:
                r2x_new, r2y_new = r2x + b1x, r2y + b1y
                if (
                    not (0 <= r2x_new < 2 and 0 <= r2y_new < 3)
                    or dir_pad[r2x_new][r2y_new] is None
                ):
                    continue
                neighbors.append(((r1x, r1y, r2x_new, r2y_new, r3x, r3y, ans), ds))
        else:
            r1x_new, r1y_new = r1x + dx, r1y + dy
            if (
                not (0 <= r1x_new < 2 and 0 <= r1y_new < 3)
                or dir_pad[r1x_new][r1y_new] is None
            ):
                continue
            neighbors.append(((r1x_new, r1y_new, r2x, r2y, r3x, r3y, ans), ds))
    return neighbors


p = False


def shortest_to(s, code):
    frontier = [(s, ())]
    visited = set()
    while frontier:
        cur, path = frontier.pop(0)
        if cur in visited:
            continue
        if cur == code:
            return path
        visited.add(cur)
        print(cur)

        if p:
            # print three grids to show where all the robots are
            print_dir_pad_1 = [[dir_pad[x][y] for y in range(3)] for x in range(2)]
            print_dir_pad_2 = [[dir_pad[x][y] for y in range(3)] for x in range(2)]
            print_num_pad = [[num_pad[x][y] for y in range(3)] for x in range(4)]
            r1x, r1y, r2x, r2y, r3x, r3y, ans = cur
            print_dir_pad_1[r1x][r1y] = "R1"
            print_dir_pad_2[r2x][r2y] = "R2"
            print_num_pad[r3x][r3y] = "R3"
            print("\n\n", path, visited)
            for row in print_dir_pad_1:
                print(row)
            for row in print_dir_pad_2:
                print(row)
            for row in print_num_pad:
                print(row)

        for n, ds in neighbors(cur, code):
            frontier.append((n, (*path, ds)))

    raise ValueError("No path found")


for code in f:
    # all start on A button
    path = shortest_to((0, 2, 0, 2, 3, 2, ""), code)
    print(code, "".join(path[1:]))

# %%
