"""
Sliding window algorithm to determine 'visibility'
"""

from collections import deque
from dataclasses import dataclass
from os.path import join
from pathlib import Path
from sys import argv
from textwrap import dedent
from typing import Optional, Tuple, List

import numpy as np

from src.timer import Timer
from src.utils import read_text_file


def string_to_int_list(string: str) -> List[int]:
    return [int(char) for char in list(string)]


def get_elements_visible_in_grid(grid: np.array) -> List[Tuple]:
    
    outer_elements_visible = $$


def main():
    timer_name = "day8-timer"
    test_mode = True if len(argv) > 1 else False
    parent_dir = Path(__file__).parent.resolve()
    input_fname = "input.txt" if not test_mode else "sample.txt"

    lines = read_text_file(join(parent_dir, input_fname))
    gridspace = np.array([string_to_int_list(l) for l in lines], dtype=int)

    DEBUG = True

    with Timer(name=timer_name, return_ns=True, ns_mode=True) as timer:
        visible_coords = get_elements_visible_in_grid(grid=gridspace)
        time_1_millisecs = timer.stop(reset=True) / 1000000
        total_time_millisecs = timer.timers[timer_name] * (10**3)

    # Print out results
    print(gridspace)
    print(
        dedent(
            f"""
    Task 1 ({time_1_millisecs:.2f}ms elapsed):
    XXX

    Total time taken: {total_time_millisecs:.2f}ms
    """
        )
    )


if __name__ == "__main__":
    main()
