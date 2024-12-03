from typing import List

def read_data(data_path: str) -> List[List[int]]:
    reports = []
    with open (data_path, "r") as input_file:
        for report in input_file:
            report = report.strip()
            reports.append([int(level) for level in report.split(" ")])
    return reports

def is_safe(report: List[int]) -> bool:
    # returns whether or not the report is safe
    # Rules:
    #   1) safe if all levels are decreasing or increasing
    #   2) any two levels must not vary by an amount other than 1, 2, or 3.
    prev_level = None
    is_increasing = None
    for level in report:
        if prev_level is None:
            # cant fail on the first value
            prev_level = level
            continue
        if is_increasing is None:
            # determine if the values are increasing or decreasing
            if prev_level < level:
                is_increasing = True
            elif prev_level > level:
                is_increasing = False
            else:
                # values are the same. This violates rule 2. Not safe
                return False

        if (is_increasing and prev_level >= level) or (not is_increasing and prev_level <= level):
            # rule 1 violation
            return False

        difference = abs(prev_level - level)
        if difference < 1 or difference > 3:
            # rule 2 violation
            return False
        prev_level = level
    return True

def part_1(reports: List[List[int]]) -> int:
    # returns the number of safe levels
    num_safe = 0
    for report in reports:
        if is_safe(report):
            num_safe += 1
    return num_safe

def part_2(reports: List[List[int]]) -> int:
    # returns the number of safe levels
    num_safe = 0
    for report in reports:
        if is_safe(report):
            num_safe += 1
        else:
            # Safety module triggered.
            # Test if removing a level makes it safe
            for i in range(len(report)):
                new_report = list(report)
                del new_report[i]
                if is_safe(new_report):
                    num_safe += 1
                    break
    return num_safe

reports = read_data("inputs/input2.txt")
print("Number of safe levels:", part_1(reports))
print("Number of safe levels with safety module:", part_2(reports))