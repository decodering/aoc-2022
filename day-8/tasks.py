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


def main():
    timer_name = "day8-timer"
    test_mode = True if len(argv) > 1 else False
    parent_dir = Path(__file__).parent.resolve()
    input_fname = "input.txt" if not test_mode else "sample.txt"

    lines = read_text_file(join(parent_dir, input_fname))

    DEBUG = True

    with Timer(name=timer_name, return_ns=True, ns_mode=True) as timer:
        print(lines)
        time_1_microsecs = timer.stop(reset=True) / 1000
        total_time_microsecs = timer.timers[timer_name] * (10**6)

    # Print out results
    print(
        dedent(
            f"""
    Task 1 ({time_1_microsecs:.1f}us elapsed):
    XXX

    Total time taken: {total_time_microsecs:.1f}us
    """
        )
    )


if __name__ == "__main__":
    main()
