from itertools import product

f = open("input.txt").read()
pattern = lambda rows: [sum(1 for r in rows if r[i] == "#") for i in range(5)]
locks = [pattern(p.split("\n")) for p in f.split("\n\n") if p.split("\n")[0] == "#" * 5]
keys = [pattern(p.split("\n")) for p in f.split("\n\n") if p.split("\n")[0] == "." * 5]
total = sum(1 for k, l in product(keys, locks) if all(l + k <= 7 for l, k in zip(l, k)))
print(total)
