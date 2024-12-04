from typing import List, Tuple

def get_data(data_path: str) -> List[str]:
    data = []
    with open (data_path, "r") as input_file:
        for line in input_file:
            data.append(line)
    return data


# This can find the search_word in non linear paths.
# I thought this is where part 2 was going.
# We dont want that, but it's fun.
def search_squiggle(data: List[str], search_word: str, current_position: Tuple[int, int],
           search_letter_index: int) -> int:
    if data[current_position[0]][current_position[1]] != search_word[search_letter_index]:
        # search failed
        return 0
    else:
        # current letter matches, end or recurse
        if search_letter_index == (len(search_word) - 1):
            # found the last letter, so full word was found.
            return 1
        else:
            # need to look for the next letter
            num_found = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    new_row = current_position[0] + i
                    new_col = current_position[0] + j
                    if (0 <= new_row < len(data)) and (0 <= new_col < len(data[new_row])):
                        new_position = (new_row, new_col)
                        num_found += search(data, search_word, new_position, search_letter_index + 1)
            return num_found

def search(data: List[str], search_word: str) -> int:
    num_matches = 0
    for row_num in range(len(data)):
        for col_num in range(len(data[row_num])):
            # check strings in all 8 directions from current position.
            for row_direction in [-1, 0, 1]:
                for col_direction in [-1, 0, 1]:
                    search_passed = True
                    for search_index in range(len(search_word)):
                        new_row = row_num + (search_index * row_direction)
                        new_col = col_num + (search_index * col_direction)
                        # check if the new_row and new_col are valid
                        if (new_row < 0
                            or new_row >= len(data)
                            or new_col < 0
                            or new_col >= len(data[new_row])
                            or data[new_row][new_col] != search_word[search_index]
                        ):
                            # new position out of bounds or data didnt match search word
                            search_passed = False
                            break
                    if search_passed:
                        num_matches += 1
    return num_matches

def x_search(data: List[str]) -> int:
    num_matches = 0
    # no need to check edges since we are looking for an x.
    # also makes it so I dont have to do bounds checking :)
    for row_num in range(1, len(data) - 1):
        for col_num in range(1, len(data[row_num]) - 1):
            if data[row_num][col_num] == "A":
                # check if it makes x-mas
                left, right = col_num - 1, col_num + 1
                up, down =  row_num - 1, row_num + 1
                if (((data[up][left] == "M" and data[down][right] == "S") or
                     (data[up][left] == "S" and data[down][right] == "M")) and
                    ((data[up][right] == "M" and data[down][left] == "S") or
                     (data[up][right] == "S" and data[down][left] == "M"))):
                    # it made an x and spelled "MAS"
                    num_matches += 1
    return num_matches

def part_1(data: List[str]) -> None:
    word_matches = search(data, "XMAS")
    print("Part 1 matches:", word_matches)

def part_2(data: List[str]) -> None:
    x_matches = x_search(data,)
    print("Part 2 matches:", x_matches)

data = get_data("inputs/input4.txt")
part_1(data)
part_2(data)
