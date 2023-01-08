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


def get_signal_strength(
    instructions: List[str], starting_register_value: int = 1
) -> Tuple[dict, int]:
    clock_tick_count, signal_strength = 0, 0
    register_value = starting_register_value
    main_tick_intervals = deque([60, 100, 140, 180, 220])
    tick_interval = 20
    full_score_dict = {clock_tick_count: register_value}
    score_dict = {}
    for instruct in instructions:
        is_noop = instruct == "noop"
        clock_increment = 2 if not is_noop else 1
        clock_tick_count += clock_increment
        if (tick_interval is not None) and (clock_tick_count >= tick_interval):
            score_dict[tick_interval] = register_value
            signal_strength += register_value * tick_interval
            tick_interval = (
                main_tick_intervals.popleft() if main_tick_intervals else None
            )
        full_score_dict[clock_tick_count] = register_value
        if not is_noop:
            _, signal_increment = instruct.split(" ")
            register_value += int(signal_increment)

    return score_dict, signal_strength


def get_crt_image(
    instructions: List[str], starting_register_value: int = 1
) -> List[str]:
    clock_tick_count = 0
    sprite_LR_buffer = 1
    register_x_value = starting_register_value
    for instruction in instructions:
        is_noop = instruction == "noop"
        if is_noop:
            pass
        else:
            pass
        clock_increment = 2 if not is_noop else 1
        clock_tick_count += clock_increment
        sprite_positions = [
            register_x_value - sprite_LR_buffer,
            register_x_value,
            register_x_value + sprite_LR_buffer,
        ]


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
        score_dict, signal_strength = get_signal_strength(instructions=lines)
        time_1_millisecs = timer.stop(reset=True) / (10**6)
        crt_image = get_crt_image(instructions=lines)
        time_2_millisecs = timer.stop(reset=True) / (10**6)
        total_time_millisecs = timer.timers[timer_name] * (10**3)

    # Print out results
    print(
        dedent(
            f"""
    Task 1 ({time_1_millisecs:.2f}ms elapsed):
    Score dict: {score_dict}
    Cumulative signal strength: {signal_strength}
    
    Task 2 ({time_2_millisecs:.2f}ms elapsed):
    CRT image: {crt_image}
    
    Total time taken: {total_time_millisecs:.2f}ms
    """
        )
    )


if __name__ == "__main__":
    main()
