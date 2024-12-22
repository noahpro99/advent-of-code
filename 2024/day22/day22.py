from collections import defaultdict
from functools import lru_cache

f = open("input.txt", "r").read().splitlines()


@lru_cache(maxsize=None)
def secret_number(n):
    n ^= n * 64
    n %= 16777216
    n ^= n // 32
    n %= 16777216
    n ^= n * 2048
    n %= 16777216
    return n


p1 = []
counts = defaultdict(int)
for sn in f:
    snp1, snp2 = int(sn), int(sn)
    nums = []
    monkey_done = set()
    for i in range(2000):
        nums.append(snp2 % 10)
        snp2 = secret_number(snp2)
        snp1 = secret_number(snp1)
    p1.append(snp1)
    diffs = [x2 - x1 for x1, x2 in zip(nums, nums[1:])]
    for i in range(4, len(diffs)):
        diffs_key = tuple(diffs[i - 4 : i])
        if diffs_key not in monkey_done:
            counts[diffs_key] += nums[i]
            monkey_done.add(diffs_key)

print(sum(p1))
print(max(counts.values()))
