from typing import List, Tuple, Dict
import time
from sympy import Matrix, Integer

def get_data(data_path: str) -> List[Matrix]:
    data = []
    with open (data_path, "r") as input_file:
        button_a = []
        button_b = []
        prize = []
        for line in input_file:
            line = line.strip()
            if "Button A" in line:
                button_a = [int("".join([character for character in split if character.isnumeric()])) for split in line.split(",")]
            elif "Button B" in line:
                button_b = [int("".join([character for character in split if character.isnumeric()])) for split in line.split(",")]
            elif "Prize" in line:
                prize = [int("".join([character for character in split if character.isnumeric()])) for split in line.split(",")]
                # assemble a matrix with the given values.
                m = Matrix([[button_a[0], button_b[0], prize[0]],
                            [button_a[1], button_b[1], prize[1]]])
                data.append(m)
                # reset values
                button_a = []
                button_b = []
                prize = []
    return data

def part_1(data: List[Matrix]) -> None:
    tokens = 0
    for m in data:
        m_rref = m.rref()
        a_presses = m_rref[0][2]
        b_presses = m_rref[0][5]
        if isinstance(a_presses, Integer) and isinstance(b_presses, Integer):
            tokens += 3 * a_presses
            tokens += b_presses
    print("Part 1 --", tokens)
    return

def part_2(data: List[Matrix]) -> None:
    tokens = 0
    for m in data:
        m[2] = m[2] + 10000000000000
        m[5] = m[5] + 10000000000000
        m_rref = m.rref()
        a_presses = m_rref[0][2]
        b_presses = m_rref[0][5]
        if isinstance(a_presses, Integer) and isinstance(b_presses, Integer):
            tokens += 3 * a_presses
            tokens += b_presses
    print("Part 2 --", tokens)
    return

data = get_data("inputs/input13.txt")
start = time.time()
part_1(data)
part_2(data)
print("finished in", time.time() - start, "seconds")
