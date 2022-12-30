"""
Sliding window algorithm to determine 'visibility'.

Euclidean grid space.
"""

from collections import deque
from os.path import join, splitext
from pathlib import Path
from sys import argv
from textwrap import dedent
from typing import Any, List, Optional, Tuple

import numpy as np
import numpy.typing as npt

from src.timer import Timer
from src.utils import read_text_file


def main():
    timer_name = "day10-timer"
    parent_dir_abspath = Path(__file__).parent.resolve()
    test_mode = True if len(argv) > 1 else False
    test_file = (
        (f"{argv[1]}.txt" if (not splitext(argv[1])[-1]) else argv[1])
        if test_mode
        else None
    )
    input_fname = "input.txt" if not test_mode else test_file

    lines = read_text_file(join(parent_dir_abspath, input_fname))

    with Timer(name=timer_name, return_ns=True, ns_mode=True) as timer:
        pass
        time_1_millisecs = timer.stop(reset=True) / (10**6)
        pass
        time_2_millisecs = timer.stop(reset=True) / (10**6)
        total_time_millisecs = timer.timers[timer_name] * (10**3)

    # Print out results
    print(lines)
    print(
        dedent(
            f"""
    Task 1 ({time_1_millisecs:.2f}ms elapsed):
    XX
    
    Task 2 ({time_2_millisecs:.2f}ms elapsed):
    XX
    
    Total time taken: {total_time_millisecs:.2f}ms
    """
        )
    )


if __name__ == "__main__":
    main()
