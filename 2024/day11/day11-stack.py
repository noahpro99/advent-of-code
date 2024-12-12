from collections import defaultdict


def blink(stone, depth_left):
    stack = [(stone, depth_left, ())]
    while stack:
        cur_stone, cur_depth_left, parents = stack.pop()
        if (cur_stone, cur_depth_left) in cache:
            for parent_stone, parent_depth_left in parents:
                cache[(parent_stone, parent_depth_left)] += cache[
                    (cur_stone, cur_depth_left)
                ]
            continue
        if cur_depth_left == 0:
            for parent_stone, parent_depth_left in parents:
                cache[(parent_stone, parent_depth_left)] += 1
            continue
        if cur_stone == 0:
            stack.append(
                (1, cur_depth_left - 1, (*parents, (cur_stone, cur_depth_left)))
            )
        elif len(str(cur_stone)) % 2 == 0:
            left_digits = int(str(cur_stone)[: len(str(cur_stone)) // 2])
            right_digits = int(str(cur_stone)[len(str(cur_stone)) // 2 :])
            stack.append(
                (
                    left_digits,
                    cur_depth_left - 1,
                    (*parents, (cur_stone, cur_depth_left)),
                )
            )
            stack.append(
                (
                    right_digits,
                    cur_depth_left - 1,
                    (*parents, (cur_stone, cur_depth_left)),
                )
            )
        else:
            stack.append(
                (
                    cur_stone * 2024,
                    cur_depth_left - 1,
                    (*parents, (cur_stone, cur_depth_left)),
                )
            )

    return cache[(stone, depth_left)]


f = open("input.txt").read().splitlines()
cache = defaultdict(int)
stones = [int(x) for x in f[0].split()]
final_stones = [blink(stone, 75) for stone in stones]
print(sum(final_stones))
