def blink(stone, depth):
    if depth == 75:
        return 1
    if (stone, depth) in cache:
        return cache[(stone, depth)]
    if stone == 0:
        cache[(stone, depth)] = blink(1, depth + 1)
        return cache[(stone, depth)]
    if len(str(stone)) % 2 == 0:
        left_digits = int(str(stone)[: len(str(stone)) // 2])
        right_digits = int(str(stone)[len(str(stone)) // 2 :])
        cache[(stone, depth)] = blink(left_digits, depth + 1) + blink(
            right_digits, depth + 1
        )
        return cache[(stone, depth)]
    else:
        cache[(stone, depth)] = blink(stone * 2024, depth + 1)
        return cache[(stone, depth)]


f = open("input.txt").read().splitlines()
cache = {}
stones = [int(x) for x in f[0].split()]
final_stones = [blink(stone, 0) for stone in stones]
print(final_stones)

# 186203
# 221291560078593
