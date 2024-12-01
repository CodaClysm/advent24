from typing import List, Tuple

def get_data(data_path: str) -> Tuple[List[int], List[int]]:
    left_data = []
    right_data = []
    with open (data_path, "r") as input_file:
        for line in input_file:
            line = line.strip()
            left, right = line.split("   ")
            left_data.append(int(left))
            right_data.append(int(right))

    left_data.sort()
    right_data.sort()
    return left_data, right_data


def part_1(left_data: List[int], right_data: List[int]) -> int:
    total_distance = 0
    for index in range(len(left_data)):
        total_distance += abs(left_data[index] - right_data[index])
    return total_distance

def part_2(left_data: List[int], right_data: List[int]) -> int:
    similarity_score = 0
    for left_id in left_data:
        similarity_score += left_id * right_data.count(left_id)
    return similarity_score


left_data, right_data = get_data("inputs/input1.txt")

distance = part_1(left_data, right_data)
print("Total distance between ids:", distance)

similarity = part_2(left_data, right_data)
print("Similarity score: ", similarity)