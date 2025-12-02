# %%
f = [
    (int(x.split("-")[0]), int(x.split("-")[1]))
    for x in open("input.txt").read().split(",")
]

p1, p2 = 0, 0

for start, end in f:
    for x in range(start, end + 1):
        s = str(x)
        if len(s) % 2 == 0 and s[: len(s) // 2] == s[len(s) // 2 :]:
            p1 += x
        if s in (s + s)[1:-1]:
            p2 += x

print(p1, p2)
