from typing import List, Tuple, Dict

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

def traverse_lab_map(lab_map: List[List[str]],
                    guard_position: Tuple[int, int] = None,
                    current_direction_index: int = 0,
                    pathing: Dict[Tuple[int, int], List[int]] = None) -> bool:
    # first find the current position of the guard
    original_map = False
    if guard_position is None:
        original_map = True
        for row_index, row in enumerate(lab_map):
            if "^" in row:
                column_index = row.index("^")
                guard_position = (row_index, column_index)
                break
    if pathing is None:
        pathing = {}

    inserted_obstacle_locations = []

    # use a list of tuples track and update the direction
    #                up    right   down    left
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    next_guard_position = get_next_position(guard_position, directions[current_direction_index])

    # keep a dictionary of visited locations and the direction of travel at that tile
    possible_obstacle_count = 0

    pathing.setdefault(guard_position, []).append(current_direction_index)
    # if the next position is not valid, the guard has exited the lab. Quit pathing
    while is_position_valid(lab_map, next_guard_position):
        if lab_map[next_guard_position[0]][next_guard_position[1]] == "#":
            # if the next position is an obstacle, turn and dont update position
            current_direction_index += 1
            if current_direction_index >= len(directions):
                current_direction_index = 0

            # check for looping
            if guard_position in pathing and current_direction_index in pathing[guard_position]:
                return True
            pathing.setdefault(guard_position, []).append(current_direction_index)
        else:
            # check if inserting an obstacle in front of the guard will cause a loop
            if original_map and True:
                # only the original map is allowed to check for new obstacles to induce a loop
                if lab_map[next_guard_position[0]][next_guard_position[1]] == ".":
                    if next_guard_position not in pathing:
                        lab_map[next_guard_position[0]][next_guard_position[1]] = "#"
                        # create a deep copy of pathing to send over to the new instance
                        pathing_copy = {tile : list(pathing[tile]) for tile in pathing}
                        if traverse_lab_map(lab_map,
                                            guard_position=guard_position,
                                            current_direction_index=current_direction_index,
                                            pathing=pathing_copy):
                            if next_guard_position not in inserted_obstacle_locations:
                                possible_obstacle_count += 1
                                inserted_obstacle_locations.append(next_guard_position)
                        # replace the original lab_map
                        lab_map[next_guard_position[0]][next_guard_position[1]] = "."

            # no obstacle. Update the position and mark the tile as traversed
            guard_position = next_guard_position
            pathing.setdefault(guard_position, []).append(current_direction_index)

        next_guard_position = get_next_position(guard_position, directions[current_direction_index])

    if original_map:
        print("Part 1 -- unique tiles visited:", len(pathing))
        print("Part 2 -- possible obstacle locations", possible_obstacle_count)

    return False

lab_map = get_data("inputs/input6.txt")
traverse_lab_map(lab_map)
