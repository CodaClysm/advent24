import re

def get_data(data_path: str) -> str:
    data = ""
    with open (data_path, "r") as input_file:
        for line in input_file:
            data += line.strip()
    return data


def parse_memory(data: str, always_enable: bool) -> int:
    sum = 0

    # mul() regex
    regex = "(mul\\([0-9]+,[0-9]+\\))"
    # do() regex
    regex += "|" + "(do\\(\\))"
    # don't() regex
    regex += "|" + "(don't\\(\\))"

    commands = re.findall(regex, data)
    enabled = True
    # process commands in the order they were encountered.
    for command in commands:
        if command[0]:
            # command is a mul command
            factors = re.search("[0-9]+,[0-9]+", command[0])
            lhs, rhs = [int(factor) for factor in factors.group().split(",")]
            product = lhs * rhs
            if enabled or always_enable:
                sum += product
        elif command[1]:
            # command is a do command
            enabled = True
        elif command[2]:
            # command is a don't command
            enabled = False

    return sum

def part_1(data: str) -> int:
    print("Part 1 sum:", parse_memory(data, True))

def part_2(data: str) -> int:
    print("Part 2 sum:", parse_memory(data, False))


data = get_data("inputs/input3.txt")
part_1(data)
part_2(data)