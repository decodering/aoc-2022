"""
xxx
"""

from collections import deque
from dataclasses import dataclass
from os.path import join
from pathlib import Path
from sys import argv
from textwrap import dedent
from typing import Tuple, Optional

from src.timer import Timer
from src.utils import read_text_file


@dataclass
class ElvenDir:
    name: str
    child_dirs: list = None
    parent_dir: str = None
    files: list = None
    depth_from_root: int = None
    dir_size: int = None


def build_parsed_instructions(instructions_list: list) -> deque:
    parsed_instructions = deque(iterable=[])
    # Get a list of instructions in the above format
    for instruction in instructions_list:
        is_command = True if instruction[0] == "$" else False
        if is_command:
            split_string = instruction.split(" ")[1:]  # Ignore first part '$'
            assert 1 <= len(split_string) <= 2
            is_cd_command = True if len(split_string) == 2 else False
            # CASE: cd 'dir' command
            if is_cd_command:
                _, cd_target_folder = split_string
                if cd_target_folder != "/":
                    assert "/" not in cd_target_folder
                parsed_instructions.append({"cd": cd_target_folder})
            # CASE: ls command
            else:
                parsed_instructions.append({"ls": []})
        # CASE: ls command outputs
        else:
            assert list(parsed_instructions[-1].keys()) == ["ls"]
            parsed_instructions[-1]["ls"].append(instruction)
    return parsed_instructions


def parse_files_list(objects_list: list) -> Tuple[list, list, int]:
    child_dirs = []
    files_list = []
    dir_size = 0
    for f in objects_list:
        part_1, part_2 = f.split(" ")
        is_dir = True if part_1 == "dir" else False
        if is_dir:
            child_dirs.append(part_2)
        else:
            files_list.append(part_2)
            dir_size += int(part_1)
    return child_dirs, files_list, dir_size


def get_directory_sizes_from_input(instructions_list: list) -> dict:
    """
    Returns dict {'/asd/asd':1232,...}

    First get a set of instructions:
    [
        {'cd': 'asd'},
        {'ls': [...]},
    ]
    """

    parsed_instructions = deque(
        build_parsed_instructions(instructions_list=instructions_list)
    )

    pwd = "/"
    depth = 0
    dir_dict = dict()

    # Parse instructions
    is_cd_cmd = True
    for instruction_dict in parsed_instructions:
        instruction_dict = list(instruction_dict.items())
        assert len(instruction_dict) == 1
        command, values = instruction_dict[0]

        is_cd_cmd = True if command == "cd" else False
        if is_cd_cmd:
            assert isinstance(values, str)
            if values == "..":
                pwd = "/".join(pwd.split("/")[:-1])
                pwd = "/" if not pwd else pwd
                depth -= 1
            else:
                pwd = join(pwd, values) if values != "/" else pwd
                depth += 1 if values != "/" else 0
        else:
            assert isinstance(values, list)
            parent_dir, dir_name = pwd.split("/")[-2:] if pwd != "/" else (None, "/")
            parent_dir = "/" if parent_dir == "" else parent_dir
            child_dirs, files_list, dir_size = parse_files_list(objects_list=values)

            assert pwd not in dir_dict.keys()
            dir_dict[pwd] = ElvenDir(
                name=dir_name,
                parent_dir=parent_dir,
                child_dirs=child_dirs,
                files=files_list,
                depth_from_root=depth,
                dir_size=dir_size,
            )

    # Recursively go through each child dir and make sure the dir_sizes match up
    dir_object = dir_dict["/"]
    child_dirs = dir_object.child_dirs

    def get_dir_size(dir_dict: dict, e: ElvenDir, pwd: str = "/"):
        dir_size = e.dir_size
        child_dirs = [join(pwd, d) for d in e.child_dirs]

        for d_path in child_dirs:
            dir_object = dir_dict[d_path]
            fsize = get_dir_size(dir_dict=dir_dict, e=dir_object, pwd=d_path)
            dir_size += fsize

        return dir_size

    dir_size_dict = dict()
    for d_path in dir_dict.keys():
        dir_size_dict[d_path] = get_dir_size(
            dir_dict=dir_dict, e=dir_dict[d_path], pwd=d_path
        )

    return dir_dict, dir_size_dict


def get_directory_to_delete(
    dir_size_dict: dict,
    disk_space: int,
    min_space_needed: int,
) -> Optional[Tuple[str, str]]:
    used_space = dir_size_dict["/"]
    free_space = disk_space - used_space
    if free_space < min_space_needed:
        space_to_be_cleared = min_space_needed - free_space
        sorted_dir_sizes = sorted(dir_size_dict.items(), key=lambda x: x[-1])
        for d_path, size in sorted_dir_sizes:
            if size >= space_to_be_cleared:
                return d_path, used_space
    else:
        return None


def main():
    DEBUG = False
    DISK_SPACE = 70000000
    SPACE_NEEDED = 30000000
    timer_name = "day7-timer"
    test_mode = True if len(argv) > 1 else False
    parent_dir = Path(__file__).parent.resolve()
    input_fname = "input.txt" if not test_mode else "sample.txt"

    lines = read_text_file(join(parent_dir, input_fname))

    with Timer(name=timer_name, return_ns=True, ns_mode=True) as timer:
        dir_dict, dir_size_dict = get_directory_sizes_from_input(
            instructions_list=lines
        )
        time_1_microsecs = timer.stop(reset=True) / 1000
        dir_to_delete, used_space = get_directory_to_delete(
            dir_size_dict=dir_size_dict,
            disk_space=DISK_SPACE,
            min_space_needed=SPACE_NEEDED,
        )
        time_2_microsecs = timer.stop(reset=True) / 1000
        total_time_microsecs = timer.timers[timer_name] * (10**6)

    # Print out results
    dirs_under_100000 = {}
    for ind, (k, v) in enumerate(dir_dict.items(), 1):
        if DEBUG:
            print(k, v)
            if ind == len(dir_dict.items()):
                print("")
    for k, v in dir_size_dict.items():
        if DEBUG:
            print(k, v)
        if v < 100000:
            dirs_under_100000[k] = v

    print(
        dedent(
            f"""
    Task 1 ({time_1_microsecs:.1f}us elapsed):
    Num dirs under 10000 - {len(dirs_under_100000.keys())} dirs
    Total size of these dirs - {sum(dirs_under_100000.values())} bytes

    Task 2 ({time_2_microsecs:.1f}us elapsed):
    Dir to delete - {dir_to_delete} ({dir_size_dict[dir_to_delete]} bytes large)
    Used space - {used_space}/70,000,000 bytes ({70000000-used_space} bytes free)

    Total time taken: {total_time_microsecs:.1f}us
    """
        )
    )


if __name__ == "__main__":
    main()
