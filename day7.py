from typing import List, Tuple, Dict

def get_data(data_path: str) -> Tuple[List[int], List[List[int]]]:
    results = []
    inputs = []
    with open (data_path, "r") as input_file:
        for line in input_file:
            line = line.strip()
            result, inputs_str = line.split(": ")
            results.append(int(result))
            inputs.append([int(x) for x in inputs_str.split(" ")])
    return results, inputs

def recursive_solve(result: int, inputs: List[int], current_val: int, allow_concat: bool) -> bool:
    # base case:
    if current_val > result:
        # early exit. No operators allow value to decrease
        return False

    if len(inputs) == 0:
        # no more branches. If the current_val is the desired result, return true.
        return current_val == result
    else:
        # test multiplying or dividing by the next value
        input_values = list(inputs)
        next_val = input_values[0]
        del input_values[0]
        if allow_concat:
            return (recursive_solve(result, input_values, current_val + next_val, allow_concat) or
                    recursive_solve(result, input_values, current_val * next_val, allow_concat) or
                    recursive_solve(result, input_values, int(str(current_val) + str(next_val)), allow_concat))
        else:
            return (recursive_solve(result, input_values, current_val + next_val, allow_concat) or
                    recursive_solve(result, input_values, current_val * next_val, allow_concat))


def is_result_possible(result: int, inputs: List[int], allow_concat: bool) -> bool:
    input_values = list(inputs)
    starting_val = input_values[0]
    del input_values[0]
    return recursive_solve(result, input_values, starting_val, allow_concat)

def part_1(results: List[int], inputs: List[List[int]]) -> None:
    result_sum = 0
    for result, input_values in zip(results, inputs):
        if is_result_possible(result, input_values, False):
            result_sum += result
    print("Part 1 sum:", result_sum)

def part_2(results: List[int], inputs: List[List[int]]) -> None:
    result_sum = 0
    for result, input_values in zip(results, inputs):
        if is_result_possible(result, input_values, True):
            result_sum += result
    print("Part 2 sum:", result_sum)

results, inputs = get_data("inputs/input7.txt")
part_1(results, inputs)
part_2(results, inputs)
