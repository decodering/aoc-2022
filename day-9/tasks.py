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


def get_elements_visible_in_grid(grid: np.array) -> List[Tuple[int, int]]:
    num_rows, num_cols = grid.shape
    visible_points = []
    visible_points.extend(
        list(zip([0] * num_cols, list(range(num_cols))))
    )  # Top row visible
    visible_points.extend(
        list(zip([num_rows - 1] * num_cols, list(range(num_cols))))
    )  # Bot row visible
    visible_points.extend(
        list(zip(list(range(1, (num_rows - 1))), [0] * (num_rows - 2)))
    )  # first col visible
    visible_points.extend(
        list(zip(list(range(1, (num_rows - 1))), [num_cols - 1] * (num_rows - 2)))
    )  # last col visible

    # Process inner points
    for i in range(1, (num_rows - 1)):
        for j in range(1, (num_cols - 1)):
            top_slice = grid[:i, j]
            bot_slice = grid[(i + 1) :, j]
            left_slice = grid[i, :j]
            right_slice = grid[i, (j + 1) :]
            height = grid[i, j]

            for visibility_line in [top_slice, bot_slice, left_slice, right_slice]:
                visibility = [True if el < height else False for el in visibility_line]
                if all(visibility):
                    visible_points.append((i, j))
                    break

    return visible_points


def get_scenic_scores(grid: np.array) -> np.array:
    num_rows, num_cols = grid.shape
    scenic_scores = np.zeros(((num_rows - 2), (num_cols - 2)), int)

    # Process scores of inner points
    for i in range(1, (num_rows - 1)):
        for j in range(1, (num_cols - 1)):
            height = grid[i, j]
            top_slice = np.flip(
                grid[:i, j]
            )  # Flip so it goes from point to edge direction
            bot_slice = grid[(i + 1) :, j]
            left_slice = np.flip(
                grid[i, :j]
            )  # Flip so it goes from point to edge direction
            right_slice = grid[i, (j + 1) :]

            total_score = 1
            for a_slice in [top_slice, bot_slice, left_slice, right_slice]:
                score = 0
                for neighbouring_height in a_slice:
                    score += 1
                    if neighbouring_height >= height:
                        break
                total_score *= score
            scenic_scores[i - 1, j - 1] = total_score
    return scenic_scores


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
        time_1_millisecs = timer.stop(reset=True) / (10**6)

        scenic_score_array = get_scenic_scores(grid=gridspace)
        time_2_millisecs = timer.stop(reset=True) / (10**6)

        total_time_millisecs = timer.timers[timer_name] * (10**3)

    # Print out results
    print(
        dedent(
            f"""
    Task 1 ({time_1_millisecs:.2f}ms elapsed):
    Num visible: {len(visible_coords)}

    Task 2 ({time_2_millisecs:.2f}ms elapsed):
    {scenic_score_array}
    Max score: {np.amax(scenic_score_array)}

    Total time taken: {total_time_millisecs:.2f}ms
    """
        )
    )


if __name__ == "__main__":
    main()
