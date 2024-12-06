from typing import List, Tuple, Dict

def get_data(data_path: str) -> Tuple[Dict[int, List[int]], List[List[int]]]:
    rules = {}
    updates = []

    with open (data_path, "r") as input_file:
        for line in input_file:
            if "|" in line:
                rule = line.split("|")
                prev_page = int(rule[0])
                if prev_page not in rules:
                    rules[prev_page] = []
                rules[prev_page].append(int(rule[1]))
            elif "," in line:
                updates.append([int(page) for page in line.split(",")])

    return rules, updates

def is_update_valid(rules: Dict[int, List[int]], update: List[int]) -> bool:
    previous_pages = []
    for current_page in update:
        if current_page in rules and any(following_page in previous_pages for following_page in rules[current_page]):
            return False
        previous_pages.append(current_page)
    return True

def fix_update(rules: Dict[int, List[int]], update: List[int]) -> List[int]:
    # build a master list for all rules
    while not is_update_valid(rules, update):
        # find the conflict and swap the positions of the conflicting pages
        previous_pages = []
        for current_index, current_page in enumerate(update):
            if current_page in rules:
                for following_page in rules[current_page]:
                    if following_page in previous_pages:
                        # these pages conflict. Swap positions
                        conflict_index = update.index(following_page)
                        temp = update[conflict_index]
                        update[conflict_index] = update[current_index]
                        update[current_index] = temp
            previous_pages.append(current_page)
    return update

def part_1(rules: Dict[int, List[int]], updates: List[List[int]]) -> None:
    midpoint_sum = sum(update[len(update)//2] for update in updates if is_update_valid(rules, update))
    print("Part 1 sum:", midpoint_sum)

def part_2(rules: Dict[int, List[int]], updates: List[List[int]]) -> None:
    midpoint_sum = 0
    for update in updates:
        if not is_update_valid(rules, update):
            fixed_update = fix_update(rules, update)
            midpoint_sum += fixed_update[len(fixed_update)//2]
    print("Part 2 sum:", midpoint_sum)

rules, updates = get_data("inputs/input5.txt")
part_1(rules, updates)
part_2(rules, updates)
