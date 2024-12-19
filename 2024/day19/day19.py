f = open("input.txt").read()
towels = f.split("\n\n")[0].split(", ")
patterns = f.split("\n\n")[1].split("\n")


def number_of_ways(p, towels, cache={}):
    if p in cache:
        return cache[p]
    if not p:
        return 1
    num_ways = 0
    for r in towels:
        if p.startswith(r):
            num_ways += number_of_ways(p[len(r) :], towels, cache)
    cache[p] = num_ways
    return num_ways


print(sum(1 for p in patterns if number_of_ways(p, towels) > 0))
print(sum(number_of_ways(p, towels) for p in patterns))
