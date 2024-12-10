from typing import List, Tuple, Dict
import time

class DiskBlock:
    def __init__(self, file_id:int, size:int):
        self.file_id = file_id
        self.size = size
    def copy(self):
        return DiskBlock(self.file_id, self.size)

def get_data(data_path: str) -> List[Tuple[int, int]]:
    disk_map_str = ""
    with open (data_path, "r") as input_file:
        for line in input_file:
            disk_map_str = line.strip()
            break

    i = 0
    disk_map = []
    while i < len(disk_map_str) - 1:
        pair = (int(disk_map_str[i]), int(disk_map_str[i+1]))
        disk_map.append(pair)
        i += 2
    if len(disk_map_str) % 2 != 0:
        # input length was odd. The last value was a file size, not empty size.
        disk_map.append((int(disk_map_str[-1]), 0))
    return disk_map

def compute_checksum(disk_data: List[int]):
    checksum = 0
    for index, val in enumerate(disk_data):
        if val is None:
            continue
        checksum += index * val
    return checksum


def part_1(disk_map: List[Tuple[int, int]]) -> None:
    disk_data = []
    # build the decompressed disk data.
    for file_id,  data_pair in enumerate(disk_map):
        file_size, free_size = data_pair
        for _ in range(file_size):
            disk_data.append(file_id)
        for _ in range(free_size):
            disk_data.append(None)

    # index front to back and back to front
    forward_index = 0
    back_index = len(disk_data) - 1

    # loop until all of the data in the back has been moved to the front
    while True:
        # get the next forward index that is empty
        while disk_data[forward_index] is not None:
            forward_index += 1
        # get the next back index that has data
        while disk_data[back_index] is None:
            back_index -= 1

        if (back_index < forward_index):
            break

        # we now have an empty spot in forward and data in back. Swap the data
        #print_disk(disk_data)
        #print("swapping", forward_index, "with", back_index)
        disk_data[forward_index] = disk_data[back_index]
        disk_data[back_index] = None
        #print_disk(disk_data)

    # all of the data is now sorted. Compute the checksum
    #print_disk(disk_data)
    print("Part 1 --", compute_checksum(disk_data))
    return

def print_blocks(disk_data: List[DiskBlock]):
    disk_str = ""
    for disk_block in disk_data:
        if disk_block.file_id is None:
            disk_str += "." * disk_block.size
        else:
            disk_str += str(disk_block.file_id) * disk_block.size
    print(disk_str)

def print_blocks_c(disk_data: List[DiskBlock]):
    disk_str = "\t"
    for block_index, disk_block in enumerate(disk_data):
        disk_str += str((block_index, disk_block.file_id, disk_block.size)) + "\n\t"
    print(disk_str)

def part_2(disk_map: List[Tuple[int, int]]) -> None:
    disk_data = []
    # build the decompressed disk data.
    for file_id,  data_pair in enumerate(disk_map):
        file_size, free_size = data_pair
        disk_data.append(DiskBlock(file_id, file_size))
        disk_data.append(DiskBlock(None, free_size))


    # index front to back and back to front
    back_index = len(disk_data) - 1

    # loop until all of the data in the back has been moved to the front
    while back_index >= 0:
        # get the next back_index that contains data
        while disk_data[back_index].file_id is None:
            back_index -= 1

        back_block = disk_data[back_index]
        # we now have the index of a disk block that we might want to move ahead
        # find the frontmost space that we can store this.
        swapped = False
        for front_index in range(back_index):
            front_block = disk_data[front_index]
            if front_block.file_id is None and front_block.size >= back_block.size:
                # we can swap the back block into this front block.
                # first insert the back block into front
                disk_data.insert(front_index, back_block.copy())

                # make the back block free space
                back_block.file_id = None

                # update the free space that we just used from the front
                front_block.size -= back_block.size
                break

        # decrement the back index regardless of if we swapped or not
        back_index -= 1

    # decompress the disk blocks
    decompressed_disk_data = []
    for block in disk_data:
        for _ in range(block.size):
            decompressed_disk_data.append(block.file_id)

    # all of the data is now sorted. Compute the checksum
    print("Part 2 --", compute_checksum(decompressed_disk_data))
    return

disk_map = get_data("inputs/sample.txt")
disk_map = get_data("inputs/input9.txt")
start = time.time()
part_1(disk_map)
part_2(disk_map)
print("finished in", time.time() - start, "seconds")