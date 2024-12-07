from typing import List, Tuple
import time

def get_data(data_path: str) -> List[List[str]]:
    lab_map = []
    with open (data_path, "r") as input_file:
        for line in input_file:
            line = line.strip()
            lab_map.append([tile for tile in line])
    return lab_map

def get_next_position(current_position: Tuple[int, int],
                       direction: Tuple[int, int]) -> Tuple[int, int]:
    return (current_position[0] + direction[0], current_position[1] + direction[1])


def is_position_valid(lab_map: List[List[str]], position: Tuple[int, int]) -> bool:
    return (0 <= position[0] < len(lab_map)) and (0 <= position[1] < len(lab_map[position[0]]))

def traverse_lab_map(lab_map: List[List[str]]) -> bool:
    # first find the current position of the guard
    guard_position = None
    for row_index, row in enumerate(lab_map):
        if "^" in row:
            column_index = row.index("^")
            guard_position = (row_index, column_index)
            break
    # Mark the starting position as traversed
    try:
        lab_map[guard_position[0]][guard_position[1]] = "X"
    except:
        print(lab_map)
        exit(1)
    # use a list of tuples track and update the direction
    #                up    right   down    left
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    current_direction_index = 0
    next_guard_position = get_next_position(guard_position, directions[current_direction_index])

    # keep track of the position you are in when you hit an obstacle and where the obstacle is
    # if you hit it multiple times from the same tile, you are looping.
    obstacles_hit = []

    while is_position_valid(lab_map, next_guard_position):
        if lab_map[next_guard_position[0]][next_guard_position[1]] == "#":
            # if the next position is an obstacle, turn and dont update position
            current_direction_index += 1
            if current_direction_index >= len(directions):
                current_direction_index = 0

            loop_detection_tuple = (guard_position, next_guard_position)
            if loop_detection_tuple in obstacles_hit:
                # return true if the guard is stuck in a loop.
                return True
            obstacles_hit.append(loop_detection_tuple)
        else:
            # no obstacle. Update the position and mark the tile as traversed
            guard_position = next_guard_position
            lab_map[guard_position[0]][guard_position[1]] = "X"

        next_guard_position = get_next_position(guard_position, directions[current_direction_index])

    # return false because the guard was able to traverse the lab without looping.
    return False


def part_1(lab_map: List[List[str]]) -> None:
    traverse_lab_map(lab_map)
    traversed_tiles = sum(row.count("X") for row in lab_map)
    print("Part 1 unique tiles visited:", traversed_tiles)

def part_2(lab_map: List[List[str]]) -> None:
    # try placing an obstacle at every position and check if it causes a loop
    num_obstacle_positions = 0
    for row_num, row in enumerate(lab_map):
        for col_num, col in enumerate(row):
            if col[0] == "#" or col[0] == "^":
                # dont try an obstacle where one already is.
                # Also dont try to place it at the guard's starting position
                continue
            # make a deep copy of the lab, and replace the current row/col with an obstacle
            lab_copy = list(lab_map)
            for i, row in enumerate(lab_copy):
                lab_copy[i] = list(row)

            lab_copy[row_num][col_num] = "#"
            if traverse_lab_map(lab_copy):
                num_obstacle_positions += 1

    print("Part 2 obstacle options:", num_obstacle_positions)

lab_map = get_data("inputs/input6.txt")
part_1(lab_map)

# get a new lab map for part 2.
lab_map = get_data("inputs/input6.txt")
start = time.time()
part_2(lab_map)
print("Part 2 took:", time.time() - start)

"""
Solutions:
5030
1928

Part 2 times:
    original: ~ 20 seconds
"""