from typing import List, Tuple, Dict, Set
import time

def get_data(data_path: str) -> List[str]:
    data = []
    with open (data_path, "r") as input_file:
        for line in input_file:
            line = line.strip()
            data.append(line)
    return data

def in_bounds(data: List[str], position: Tuple[int, int]) -> bool:
    return 0 <= position[0] < len(data) and 0 <= position[1] < len(data[position[0]])

def add_positions(p1: Tuple[int, int], p2: Tuple[int, int]) -> Tuple[int, int]:
    return (p1[0] + p2[0], p1[1] + p2[1])

def is_valid_position(data: List[str], position: Tuple[int, int], crop: str) -> bool:
    return in_bounds(data, position) and data[position[0]][position[1]] == crop

def get_bounds(data: List[str], position: Tuple[int, int], crop: str, perimeter: List[int],
               area: Set[Tuple[int, int]], corner_list: List[Set[Tuple[int, int]]]) -> bool:
    if position in area:
        # we have already been here and processed this tile. do nothing at all
        return True
    if not in_bounds(data, position) or data[position[0]][position[1]] != crop:
        # this position is a different crop, or it has already been visited
        perimeter[0] += 1
        return False
    else:
        # this position is part of the same crop field
        area.add(position)

        # direction vectors
        up_left_v, up_v, up_right_v = (-1, -1), (-1, 0), (-1, 1)
        left_v, right_v, = (0, -1), (0, 1)
        down_left_v, down_v, down_right_v = (1, -1), (1, 0), (1, 1)

        # wrt starting position
        up_left = add_positions(position, up_left_v)
        up = add_positions(position, up_v)
        up_right = add_positions(position, up_right_v)
        left = add_positions(position, left_v)
        right = add_positions(position, right_v)
        down_left = add_positions(position, down_left_v)
        down = add_positions(position, down_v)
        down_right = add_positions(position, down_right_v)

        up_valid = get_bounds(data, up, crop, perimeter, area, corner_list)
        right_valid = get_bounds(data, right, crop, perimeter, area, corner_list)
        down_valid = get_bounds(data, down, crop, perimeter, area, corner_list)
        left_valid = get_bounds(data, left, crop, perimeter, area, corner_list)

        # add corners.
        # if neither adjacent or both adjacent and not diagonal

        if (not (up_valid or right_valid)) or (up_valid and right_valid and (not is_valid_position(data, up_right, crop))):
            corner = set((position, up, up_right, right))
            corner_list.append(corner)

        if (not (right_valid or down_valid)) or (right_valid and down_valid and (not is_valid_position(data, down_right, crop))):
            corner = set((position, down, down_right, right))
            corner_list.append(corner)

        if (not (down_valid or left_valid)) or (down_valid and left_valid and (not is_valid_position(data, down_left, crop))):
            corner = set((position, down, down_left, left))
            corner_list.append(corner)

        if (not (left_valid or up_valid)) or (left_valid and up_valid and (not is_valid_position(data, up_left, crop))):
            corner = set((position, up, up_left, left))
            corner_list.append(corner)

        return True


def part_1_2(data: List[str]) -> None:
    checked_fields = set()
    cost = 0
    cost_2 = 0
    for row_num, row in enumerate(data):
        for col_num, col in enumerate(row):
            position = (row_num, col_num)
            if position in checked_fields:
                continue
            crop = data[row_num][col_num]
            perimeter = [0]
            area = set()
            corners = []
            get_bounds(data, position, crop, perimeter, area, corners)
            checked_fields.update(area)
            cost += len(area) * perimeter[0]
            cost_2 += len(area) * len(corners)

    print("Part 1 --", cost)
    print("Part 2 --", cost_2)
    return

data = get_data("inputs/sample.txt")
data = get_data("inputs/input12.txt")
start = time.time()
part_1_2(data)
print("finished in", time.time() - start, "seconds")



