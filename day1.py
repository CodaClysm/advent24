from typing import List, Tuple

def get_data(data_path: str) -> Tuple[List[int], List[int]]:
    left_data = []
    right_data = []
    with open (data_path, "r") as input_file:
        for line in input_file:
            line = line.strip()
            left_id, right_id = line.split("   ")
            left_data.append(int(left_id))
            right_data.append(int(right_id))

    left_data.sort()
    right_data.sort()
    return left_data, right_data


def part_1(left_data: List[int], right_data: List[int]) -> int:
    total_distance = 0
    for index in range(len(left_data)):
        total_distance += abs(left_data[index] - right_data[index])
    return total_distance

def part_1_abbr(left_data: List[int], right_data: List[int]) -> int:
    return sum((abs(left_id - right_id) for left_id, right_id in zip(left_data, right_data)))

def part_2(left_data: List[int], right_data: List[int]) -> int:
    similarity_score = 0
    for left_id in left_data:
        similarity_score += left_id * right_data.count(left_id)
    return similarity_score

def part_2_abbr(left_data: List[int], right_data: List[int]) -> int:
    return sum((left_id * right_data.count(left_id) for left_id in left_data))

def part_2_optimized(left_data: List[int], right_data: List[int]) -> int:
    # Count occurances of each right_id in a dictionary so we only have to do one pass
    # of right_data.
    right_id_count = {}
    for right_id in right_data:
        right_id_count[right_id] = right_id_count.get(right_id, 0) + 1
    return sum((left_id * right_id_count.get(left_id, 0) for left_id in left_data))

left_data, right_data = get_data("inputs/input1.txt")

distance = part_1_abbr(left_data, right_data)
print("Total distance between ids:", distance)

similarity = part_2_optimized(left_data, right_data)
print("Similarity score: ", similarity)