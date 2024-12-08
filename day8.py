from typing import List, Tuple, Dict

def get_data(data_path: str) -> List[str]:
    antenna_map = []
    with open (data_path, "r") as input_file:
        for line in input_file:
            line = line.strip()
            antenna_map.append(line)
    return antenna_map

def get_antenna_positions(antenna_map: List[str]) -> Dict[str, Tuple[int, int]]:
    antenna_positions = {}
    for row_num, row in enumerate(antenna_map):
        for col_num, letter in enumerate(antenna_map[row_num]):
            if letter != ".":
                position = (row_num, col_num)
                antenna_positions.setdefault(letter, []).append(position)
    return antenna_positions

def is_position_valid(antenna_map: List[str], position: Tuple[int, int]):
    # returns if the position is in bounds for hte given antenna map
    return ((0 <= position[0] < len(antenna_map))
            and (0 <= position[1] < len(antenna_map[position[0]])))

def get_positon_diff_vector(position_a: Tuple[int, int],
                            position_b: Tuple[int, int]) -> Tuple[int, int]:
    return (position_b[0] - position_a[0], position_b[1] - position_a[1])

def add_vector_to_position(position: Tuple[int, int],
                           vector: Tuple[int, int]) -> Tuple[int, int]:
    return (position[0] + vector[0], position[1] + vector[1])

def multiply_vector(vector: Tuple[int, int], factor: int) -> Tuple[int, int]:
    return (vector[0] * factor, vector[1] * factor)

def inverse_vector(vector: Tuple[int, int]) -> Tuple[int, int]:
    return multiply_vector(vector, -1)

def part_1(antenna_map: List[str], antenna_positions: Dict[str, Tuple[int, int]]) -> None:
    unique_nulls = set()
    for letter, position_list in antenna_positions.items():
        # check all combinations of antenna positions
        for i in range(len(position_list)):
            for j in range(i + 1, len(position_list)):
                position_a = position_list[i]
                position_b = position_list[j]
                a_b_vector = get_positon_diff_vector(position_a, position_b)
                b_a_vector = inverse_vector(a_b_vector)
                # add a_b_vector to b to get doubled distance
                null_a = add_vector_to_position(position_b, a_b_vector)
                if is_position_valid(antenna_map, null_a):
                    # this null is valid. Add it.
                    unique_nulls.add(null_a)
                # add b_a_vector to a to get doubled distance
                null_b = add_vector_to_position(position_a, b_a_vector)
                if is_position_valid(antenna_map, null_b):
                    # this null is valid. Add it.
                    unique_nulls.add(null_b)

    print("Part 1 -- number of unique nulls:", len(unique_nulls))
    return

def part_2(antenna_map: List[str], antenna_positions: Dict[str, Tuple[int, int]]) -> None:
    unique_nulls = set()
    for letter, position_list in antenna_positions.items():
        # check all combinations of antenna positions
        for i in range(len(position_list)):
            for j in range(i + 1, len(position_list)):
                position_a = position_list[i]
                position_b = position_list[j]
                a_b_vector = get_positon_diff_vector(position_a, position_b)
                b_a_vector = inverse_vector(a_b_vector)

                # add a_b_vector to b to get doubled distance
                null_a = add_vector_to_position(position_b, a_b_vector)
                while is_position_valid(antenna_map, null_a):
                    # this null is valid. Add it.
                    unique_nulls.add(null_a)
                    null_a = add_vector_to_position(null_a, a_b_vector)

                # add b_a_vector to a to get doubled distance
                null_b = add_vector_to_position(position_a, b_a_vector)
                while is_position_valid(antenna_map, null_b):
                    # this null is valid. Add it.
                    unique_nulls.add(null_b)
                    null_b = add_vector_to_position(null_b, b_a_vector)

        # add antennas if more than 1 of this frequency
        if len(position_list) > 1:
            unique_nulls.update(position_list)

    print("Part 2 -- number of unique nulls:", len(unique_nulls))
    return

antenna_map = get_data("inputs/input8.txt")
antenna_positions = get_antenna_positions(antenna_map)
part_1(antenna_map, antenna_positions)
part_2(antenna_map, antenna_positions)