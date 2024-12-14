from typing import List, Tuple, Dict
import time

def get_data(data_path: str) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
    data = []
    with open (data_path, "r") as input_file:
        for line in input_file:
            line = line.strip()
            position_str, velocity_str = line.split(" ")
            px, py = [int("".join([character for character in split if character.isnumeric() or character == "-"])) for split in position_str.split(",")]
            vx, vy = [int("".join([character for character in split if character.isnumeric() or character == "-"])) for split in velocity_str.split(",")]
            position = (px, py)
            velocity = (vx, vy)
            data.append((position, velocity))
    return data

def propagate(position: Tuple[int, int], velocity: Tuple[int, int], prop_time: int) -> Tuple[int, int]:
    # propagate the given postition by the velocity for the given time.
    # return new position
    delta_p_x = velocity[0] * prop_time
    delta_p_y = velocity[1] * prop_time
    return (position[0] + delta_p_x, position[1] + delta_p_y)

def constrain(position: Tuple[int, int], width: int, height: int):
    # constrain a position between a height and width.
    # since the robots teleport, we can find the position by taking the mod of the non-teleported position
    return (position[0] % width, position[1] % height)

def print_positions(positions: List[Tuple[int, int]], width: int, height: int, write: bool, elapsed_time: int):
    # generate board
    board = [["."] * width for _ in range(height)]
    for x, y  in positions:
        if isinstance(board[y][x], int):
            board[y][x] = board[y][x] + 1
        else:
            board[y][x] = 1

    # print board
    board_string = "\n"
    for row in board:
        board_string += "\t" + "".join(str(x) for x in row) + "\n"
    print(board_string)

    if write:
        with open("tree.txt", "a") as tree_file:
            board_string = "\n\nElapsed time: " + str(elapsed_time) + "\n" + board_string
            tree_file.write(board_string)


def part_1(data: List[Tuple[Tuple[int, int], Tuple[int, int]]]) -> None:
    PROP_TIME = 100
    WIDTH = 101
    HEIGHT = 103
    #WIDTH = 11
    #HEIGHT = 7
    quadrant_totals = [0] * 4

    new_positions = []
    for position, velocity in data:
        print("robot original position", position)
        new_position = propagate(position, velocity, PROP_TIME)
        print("robot propped position", new_position)
        new_position = constrain(new_position, WIDTH, HEIGHT)
        new_positions.append(new_position)
        print("robot constrained position", new_position)
        print("")

        left = (WIDTH // 2) - 1
        right = (WIDTH // 2) + 1
        up = (HEIGHT // 2) - 1
        down = (HEIGHT // 2) + 1

        if new_position[0] <= left:
            if new_position[1] <= up:
                # quadrant 1
                print("Adding robot to quad 1")
                quadrant_totals[0] = quadrant_totals[0] + 1
            elif new_position[1] >= down:
                # quadrant 2
                print("Adding robot to quad 2")
                quadrant_totals[1] = quadrant_totals[1] + 1
        elif new_position[0] >= right:
            if new_position[1] <= up:
                # quadrant 3
                print("Adding robot to quad 3")
                quadrant_totals[2] = quadrant_totals[2] + 1
            elif new_position[1] >= down:
                # quadrant 4
                print("Adding robot to quad 4")
                quadrant_totals[3] = quadrant_totals[3] + 1

    print_positions(new_positions, WIDTH, HEIGHT, False, PROP_TIME)

    print("Robot quadrant totals:", quadrant_totals)
    safety_factor = 1
    for quad_total in quadrant_totals:
        safety_factor *= quad_total

    print("Part 1 --", safety_factor)
    return


def part_2(data: List[Tuple[Tuple[int, int], Tuple[int, int]]]) -> None:
    WIDTH = 101
    HEIGHT = 103
    #WIDTH = 11
    #HEIGHT = 7

    left = (WIDTH // 2) - 1
    right = (WIDTH // 2) + 1
    up = (HEIGHT // 2) - 1
    down = (HEIGHT // 2) + 1


    mutable_positions = [position for position, _ in data]

    for total_elapsed_time in range(1, 100000):
        quadrant_totals = [0] * 4
        for position_index, position in enumerate(mutable_positions):
            velocity = data[position_index][1]
            new_position = propagate(position, velocity, 1)
            new_position = constrain(new_position, WIDTH, HEIGHT)
            mutable_positions[position_index] = new_position

            if new_position[0] <= left:
                if new_position[1] <= up:
                    quadrant_totals[0] = quadrant_totals[0] + 1
                elif new_position[1] >= down:
                    quadrant_totals[1] = quadrant_totals[1] + 1
            elif new_position[0] >= right:
                if new_position[1] <= up:
                    quadrant_totals[2] = quadrant_totals[2] + 1
                elif new_position[1] >= down:
                    quadrant_totals[3] = quadrant_totals[3] + 1

        safety_factor = 1
        for quad_total in quadrant_totals:
            safety_factor *= quad_total

        if safety_factor < 100000000:
            # maybe this is a tree?
            print_positions(mutable_positions, WIDTH, HEIGHT, True, total_elapsed_time)

    return

data = get_data("inputs/input14.txt")
start = time.time()
part_1(data)
part_2(data)
print("finished in", time.time() - start, "seconds")