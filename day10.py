from typing import List, Tuple, Dict, Set
import time

def get_data(data_path: str) -> List[str]:
    topo_map = []
    with open (data_path, "r") as input_file:
        for line in input_file:
            line = line.strip()
            topo_map.append(line)
    return topo_map

def search_squiggle(data: List[str], search_word: str, current_position: Tuple[int, int],
           search_letter_index: int, peaks_reached: Set[Tuple[int, int]]) -> int:
    if data[current_position[0]][current_position[1]] != search_word[search_letter_index]:
        # search failed
        return 0
    else:
        # current letter matches, end or recurse
        if search_letter_index == (len(search_word) - 1):
            # found the last letter, so full word was found.
            if peaks_reached is not None:
                if current_position not in peaks_reached:
                    peaks_reached.add(current_position)
                    # return 1 because a new peak was reached
                    return 1
                # return 0 because this peak has already been reached
                return 0
            # this will happen if we are not tracking peaks that we already reached.
            # return 1 because a new peak was reached.
            return 1
        else:
            # need to look for the next letter
            num_found = 0
            for i, j in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                new_row = current_position[0] + i
                new_col = current_position[1] + j
                if (0 <= new_row < len(data)) and (0 <= new_col < len(data[new_row])):
                    new_position = (new_row, new_col)
                    num_found += search_squiggle(data, search_word, new_position, search_letter_index + 1, peaks_reached)
            return num_found

def part_1(topo_map: List[str]) -> None:
    total_score = 0
    for row_num, row in enumerate(topo_map):
        for col_num, col_val in enumerate(row):
            total_score += search_squiggle(topo_map, "0123456789", (row_num, col_num), 0, set())
    print("Part 1 --", total_score)
    return

def part_2(topo_map: List[str]) -> None:
    total_score = 0
    for row_num, row in enumerate(topo_map):
        for col_num, col_val in enumerate(row):
            total_score += search_squiggle(topo_map, "0123456789", (row_num, col_num), 0, None)
    print("Part 2 --", total_score)
    return

topo_map = get_data("inputs/sample.txt")
topo_map = get_data("inputs/input10.txt")
start = time.time()
part_1(topo_map)
part_2(topo_map)
print("finished in", time.time() - start, "seconds")