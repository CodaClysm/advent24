from typing import List, Tuple, Dict
import time
from multiprocessing import Pool

def get_data(data_path: str) -> List[int]:
    data = []
    with open (data_path, "r") as input_file:
        for line in input_file:
            line = line.strip()
            data = [int(x) for x in line.split(" ")]
            return data

def blink(original_stones: List[int], num_blinks) -> List[int]:
    stones = list(original_stones)
    for _ in range(num_blinks):
        stone_index = 0
        new_stones = []
        for stone_index, stone_val in enumerate(stones):
            stone_str = str(stone_val)
            if stone_val == 0:
                stones[stone_index] = 1
            elif len(stone_str) % 2 == 0:
                split_index = len(stone_str) // 2
                left_stone = int(stone_str[:split_index])
                right_stone = int(stone_str[split_index:])
                new_stones.append(right_stone)
                stones[stone_index] = left_stone
            else:
                stones[stone_index] = stones[stone_index] * 2024
        stones.extend(new_stones)
    return stones

def part_1(stones: List[int]) -> None:
    new_stones = blink(stones, 25)
    print("Part 1 --", len(new_stones))
    return

def thread_it(inputs):
    stone, map_25_count, map_25_list = inputs
    total_stones = 0
    if stone not in map_25_count:
        blink_list = blink([stone], 25)
        map_25_count[stone] = len(blink_list)
        map_25_list[stone] = blink_list

    for stone_2 in map_25_list[stone]:
        if stone_2 not in map_25_count:
            blink_list = blink([stone_2], 25)
            map_25_count[stone_2] = len(blink_list)
            map_25_list[stone_2] = blink_list

        total_stones += map_25_count[stone_2]
    return total_stones

def part_2(stones: List[int]) -> None:
    stones_25 = blink(stones, 25)
    map_25_count = {}
    map_25_list = {}
    total_stones = 0

    for stone in stones_25:
        if stone not in map_25_count:
            blink_list = blink([stone], 25)
            map_25_count[stone] = len(blink_list)
            map_25_list[stone] = blink_list

    with Pool(30) as p:
        total_stones = sum(p.map(thread_it, [(stone, map_25_count, map_25_list) for stone in stones_25]))

    print("Part 2 --", total_stones)
    return

data = get_data("inputs/input11.txt")
start = time.time()
part_1(data)
part_2(data)
print("finished in", time.time() - start, "seconds")