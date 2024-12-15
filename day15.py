from typing import List, Tuple, Dict
from utils.positionUtils import add_positions
import time

DIRECTION_VECTORS = {"^" : (-1, 0),
                     ">" : (0, 1),
                     "v" : (1, 0),
                     "<" : (0, -1)}

# based on the movement direction, a list of vectors for [left, right] diagonal vector relative to movement direction.
UP_LEFT_VECTOR = (-1, -1)
UP_RIGHT_VECTOR = (-1, 1)
DOWN_LEFT_VECTOR = (1, -1)
DOWN_RIGHT_VECTOR = (1, 1)

def get_data(data_path: str) -> Tuple[Dict[Tuple[int, int], str], List[str]]:
    warehouse = {}
    movements = []

    with open (data_path, "r") as input_file:
        is_map_data = True
        for row_index, line in enumerate(input_file):
            line = line.strip()

            if len(line) == 0:
                # switch to movement data
                is_map_data = False
                continue

            for column_index, character in enumerate(line):
                if is_map_data:
                    # parse map data
                    position = (row_index, column_index)
                    warehouse[position] = character
                else:
                    # read movement data
                    movements.append(character)
    return (warehouse, movements)

def get_robot_position(warehouse: Dict[Tuple[int, int], str]):
    for position, value in warehouse.items():
        if value == "@":
            return position
    return None


def move_robot(warehouse: Dict[Tuple[int, int], str], movement: str, robot_position: Tuple[int, int]):
    next_position = add_positions(robot_position, DIRECTION_VECTORS[movement])

    box_encountered = False
    # search in the direction of movement until you find a wall or empty space
    while warehouse[next_position] == "O":
        box_encountered = True
        next_position = add_positions(next_position, DIRECTION_VECTORS[movement])

    if warehouse[next_position] == "#":
        # if a wall is in the first available position, we cant move anything.
        return robot_position
    if warehouse[next_position] == ".":
        if box_encountered:
            # if the next space is empty and a box was encountered, put a box there
            warehouse[next_position] = "O"
            # now move the robot 1 tile forward from its starting position
            warehouse[robot_position] = "."
            new_robot_position = add_positions(robot_position, DIRECTION_VECTORS[movement])
            warehouse[new_robot_position] = "@"
            return new_robot_position
        else:
            # if the next space is empty and no box was encountered, move the robot there
            warehouse[robot_position] = "."
            new_robot_position = add_positions(robot_position, DIRECTION_VECTORS[movement])
            warehouse[new_robot_position] = "@"
            return new_robot_position


def print_warehouse(warehouse: Dict[Tuple[int, int], str]) -> None:
    warehouse_str = ""
    prev_row = 0
    for position, value in warehouse.items():
        if position[0] != prev_row:
            warehouse_str += "\n"
            prev_row = position[0]
        warehouse_str += value
    print(warehouse_str, "\n")
    return


def part_1(warehouse: Dict[Tuple[int, int], str], movements: List[str]) -> None:
    robot_positon = get_robot_position(warehouse)

    print("Starting state")
    print_warehouse(warehouse)

    # now that we have the starting position, we can start to process each of the movements
    for movement in movements:
        robot_positon = move_robot(warehouse, movement, robot_positon)
        print("move", movement)
        print_warehouse(warehouse)

    # we have now moved the robot through all of its valid motions
    # calculate the GPS value
    gps_sum = 0
    for position, value in warehouse.items():
        if value == "O":
            gps_sum += (100 * position[0]) + position[1]

    print("Part 1 --", gps_sum)
    return

def gen_part2_warehouse(warehouse: Dict[Tuple[int, int], str]) -> Dict[Tuple[int, int], str]:
    new_warehouse = {}
    for position, value in warehouse.items():
        new_left = (position[0], position[1] * 2)
        new_right = (position[0], (position[1] * 2) + 1)
        if value == "#":
            new_warehouse[new_left] = "#"
            new_warehouse[new_right] = "#"
        elif value == ".":
            new_warehouse[new_left] = "."
            new_warehouse[new_right] = "."
        elif value == "@":
            new_warehouse[new_left] = "@"
            new_warehouse[new_right] = "."
        elif value == "O":
            new_warehouse[new_left] = "["
            new_warehouse[new_right] = "]"
    return new_warehouse

def can_move(warehouse: Dict[Tuple[int, int], str], movement: str, current_position: Tuple[int, int]) -> bool:
    next_position = add_positions(current_position, DIRECTION_VECTORS[movement])
    # determine if the robot can move in the "movement" direction without pushing a box into a wall
    if warehouse[next_position] == ".":
        # next position is free, we can move there.
        return True
    elif warehouse[next_position] == "#":
        # next position is a wall, cant move there.
        return False
    else:
        # either a "[" or "]"
        if movement == "<" or movement == ">":
            # if moving left or right, they cant collide, so we dont need to branch
            return can_move(warehouse, movement, next_position)
        else:
            # If moving up or down, we need to check forward-left or forward-right depending on what part of the box we are pushing.
            # we will always will be moving forward.
            can_go_forward = can_move(warehouse, movement, add_positions(current_position, DIRECTION_VECTORS[movement]))
            if warehouse[next_position] == "[":
                # next position is the left side of a box.
                if movement == "v":
                    return can_go_forward and can_move(warehouse, movement, add_positions(current_position, DOWN_RIGHT_VECTOR))
                else:
                    return can_go_forward and can_move(warehouse, movement, add_positions(current_position, UP_RIGHT_VECTOR))
            elif warehouse[next_position] == "]":
                if movement == "^":
                    return can_go_forward and can_move(warehouse, movement, add_positions(current_position, UP_LEFT_VECTOR))
                else:
                    return can_go_forward and can_move(warehouse, movement, add_positions(current_position, DOWN_LEFT_VECTOR))

def push_boxes(warehouse: Dict[Tuple[int, int], str], movement: str, current_position: Tuple[int, int]) -> None:
    next_position = add_positions(current_position, DIRECTION_VECTORS[movement])
    # determine if the robot can move in the "movement" direction without pushing a box into a wall
    if warehouse[next_position] == ".":
        # next position is free, we can move there.
        warehouse[next_position] = warehouse[current_position]
        warehouse[current_position] = "."
        return
    elif warehouse[next_position] == "#":
        # next position is a wall, cant move there... this shouldnt happen because we already checked for it
        print("ERROR: tried to move to an invalid location")
        return
    else:
        # either a "[" or "]"
        if movement == "<" or movement == ">":
            # if moving left or right, they cant collide, so we dont need to branch
            lateral_position = next_position
            push_boxes(warehouse, movement, lateral_position)
            warehouse[lateral_position] = warehouse[current_position]
            warehouse[current_position] = "."

        else:
            # If moving up or down, we need to check forward-left or forward-right depending on what part of the box we are pushing.
            # we will always will be moving forward.
            forward_position = next_position
            diagonal_position = None
            if warehouse[next_position] == "[":
                # next position is the left side of a box.
                if movement == "v":
                    diagonal_position = add_positions(current_position, DOWN_RIGHT_VECTOR)
                    push_boxes(warehouse, movement, diagonal_position)
                else:
                    diagonal_position = add_positions(current_position, UP_RIGHT_VECTOR)
                    push_boxes(warehouse, movement, diagonal_position)
            elif warehouse[next_position] == "]":
                if movement == "^":
                    diagonal_position = add_positions(current_position, UP_LEFT_VECTOR)
                    push_boxes(warehouse, movement, diagonal_position)
                else:
                    diagonal_position = add_positions(current_position, DOWN_LEFT_VECTOR)
                    push_boxes(warehouse, movement, diagonal_position)

            push_boxes(warehouse, movement, forward_position)
            warehouse[forward_position] = warehouse[current_position]
            warehouse[current_position] = "."
            warehouse[diagonal_position] = warehouse[current_position]
            warehouse[current_position] = "."




def move_robot_2(warehouse: Dict[Tuple[int, int], str], movement: str, robot_position: Tuple[int, int]):
    if can_move(warehouse, movement, robot_position):
        push_boxes(warehouse, movement, robot_position)
        return add_positions(robot_position, DIRECTION_VECTORS[movement])
    else:
        # unable to move the robot. return its current position and dont move any boxes
        return robot_position

def part_2(warehouse: Dict[Tuple[int, int], str], movements: List[str]) -> None:
    warehouse = gen_part2_warehouse(warehouse)
    robot_positon = get_robot_position(warehouse)
    print("Starting state")
    print_warehouse(warehouse)

    # now that we have the starting position, we can start to process each of the movements
    for movement in movements:
        print("move", movement)
        robot_positon = move_robot_2(warehouse, movement, robot_positon)
        print_warehouse(warehouse)

    # we have now moved the robot through all of its valid motions
    # calculate the GPS value
    gps_sum = 0
    for position, value in warehouse.items():
        if value == "[":
            gps_sum += (100 * position[0]) + position[1]

    print("Part 2 --", gps_sum)
    return

warehouse, movements = get_data("inputs/input15.txt")
start = time.time()
part_1(dict(warehouse), movements)
part_2(warehouse, movements)
print("finished in", time.time() - start, "seconds")