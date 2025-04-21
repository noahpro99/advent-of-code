file_name = "input.txt"
x = open(file_name).read().splitlines()
X, Y = len(x[0]), len(x)
start_cur = [(i, r.find("^")) for i, r in enumerate(x) if r.find("^") > 0][0]
new_d = {
    (-1, 0): (0, 1),
    (0, 1): (1, 0),
    (1, 0): (0, -1),
    (0, -1): (-1, 0),
}

visited_p1 = set()
cur = start_cur
dir = (-1, 0)
while 0 <= cur[0] and cur[0] < Y and 0 <= cur[1] and cur[1] < X:
    visited_p1.add(cur)
    try:
        if x[cur[0] + dir[0]][cur[1] + dir[1]] == "#":
            dir = new_d[dir]
    except:
        pass
    cur = (cur[0] + dir[0], cur[1] + dir[1])


new_d = {
    (-1, 0): (0, 1),
    (0, 1): (1, 0),
    (1, 0): (0, -1),
    (0, -1): (-1, 0),
}


def loops(map):
    visited = set()
    cur = start_cur
    dir = (-1, 0)
    visited.add((cur, dir))
    while True:
        ahead_c = (cur[0] + dir[0], cur[1] + dir[1])
        if ahead_c[0] < 0 or ahead_c[0] >= Y or ahead_c[1] < 0 or ahead_c[1] >= X:
            return False
        if map[ahead_c[0]][ahead_c[1]] == "#":
            dir = new_d[dir]
        else:
            cur = (cur[0] + dir[0], cur[1] + dir[1])
        if (cur, dir) in visited:
            return True
        visited.add((cur, dir))


p2 = 0
for i in range(X):
    for j in range(Y):
        if x[i][j] != "." or (i, j) not in visited_p1:
            continue
        new_map = [[c for c in r] for r in x]
        new_map[i][j] = "#"
        if loops(new_map):
            p2 += 1

print(len(visited_p1))
print(p2)
