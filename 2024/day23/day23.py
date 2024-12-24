from collections import defaultdict

f = open("input.txt").read().splitlines()
conns_list = [x.split("-") for x in f]
conns = defaultdict(set)
for a, b in conns_list:
    conns[a].add(b)
    conns[b].add(a)


def p1(conns):
    threes_set = set()
    frontier = [(key, ()) for key in conns]
    while frontier:
        node, path = frontier.pop()
        if len(path) == 3:
            if node == path[0]:
                threes_set.add(tuple(sorted(path)))
            continue
        for neighbor in conns[node]:
            frontier.append((neighbor, (*path, node)))
    return len([x for x in threes_set if any([i for i in x if i[0] == "t"])])


def p2(conns):
    biggest_group = frozenset()
    frontier = [(key, frozenset([key])) for key in conns]
    visited = set()
    while frontier:
        node, group = frontier.pop()
        if any([group.issubset(x) for x in visited]):
            continue
        visited.add(group)
        if len(group) > len(biggest_group):
            biggest_group = group
        for neighbor in conns[node]:
            if all([x in conns[neighbor] for x in group]):
                frontier.append((neighbor, group | {neighbor}))
    return ",".join(sorted(biggest_group))


print(p1(conns))
print(p2(conns))
