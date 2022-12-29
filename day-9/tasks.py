"""
Sliding window algorithm to determine 'visibility'.

Euclidean grid space.
"""

from collections import deque
from os.path import join
from pathlib import Path
from sys import argv
from textwrap import dedent
from typing import Any, List, Optional, Tuple

import numpy as np
import numpy.typing as npt

from src.timer import Timer
from src.utils import read_text_file


def is_in_acceptable_position(tail_position: np.array, head_position: np.array) -> bool:
    """
    Tail position is centre position. Check if head_position is acceptable.
    """
    y, x = tail_position
    is_acceptable_y = y - 1 <= head_position[0] <= y + 1
    is_acceptable_x = x - 1 <= head_position[1] <= x + 1
    return is_acceptable_x and is_acceptable_y


def move_tail_adjacent_to_head(
    tail_position: np.array, head_position: np.array, checked: bool = False
) -> Optional[npt.NDArray[Any]]:
    if not checked and is_in_acceptable_position(
        tail_position=tail_position, head_position=head_position
    ):
        return
    head_y, head_x = head_position
    tail_y, tail_x = tail_position
    y_distance = head_y - tail_y
    x_distance = head_x - tail_x

    manhattan_distance = abs(x_distance) + abs(y_distance)
    is_unidirectional = (x_distance == 0) or (y_distance == 0)

    neg_modifier_y = -1 if (y_distance < 0) else 1
    neg_modifier_x = -1 if (x_distance < 0) else 1
    steps_shifted_in_x_axis = neg_modifier_x * (abs(x_distance) - 1)
    steps_shifted_in_y_axis = neg_modifier_y * (abs(y_distance) - 1)
    if is_unidirectional:
        assert manhattan_distance == 2
        if abs(x_distance):
            move_matrix = np.array((0, steps_shifted_in_x_axis))
        else:
            move_matrix = np.array((steps_shifted_in_y_axis, 0))
    else:
        print(y_distance, x_distance)
        assert (manhattan_distance in [2, 3]) and (abs(x_distance) in [1, 2])
        if abs(x_distance) > abs(y_distance):
            move_matrix = np.array((y_distance, steps_shifted_in_x_axis))
        else:
            move_matrix = np.array((steps_shifted_in_y_axis, x_distance))
    tail_position += move_matrix
    return tail_position


def get_coords_visited_and_gridspace_shape(
    raw_instructions: List[str],
) -> Tuple[List[Tuple[int, int]], Tuple[int, int]]:
    current_head_pos = np.array((0, 0))
    current_tail_pos = np.array((0, 0))
    visited_coords = deque(iterable=[(0, 0)])
    neg_x, pos_x, neg_y, pos_y = 0, 0, 0, 0
    for instruct in raw_instructions:
        direction, steps = [int(i) if i.isdigit() else i for i in instruct.split(" ")]
        move_col = (
            steps if (direction == "R") else (-steps if (direction == "L") else 0)
        )
        move_row = (
            steps if (direction == "D") else (-steps if (direction == "U") else 0)
        )

        is_lateral = True if (abs(move_col)) else False
        local_head_pos = current_head_pos.copy()
        if is_lateral:
            neg_modifier = -1 if (move_col < 0) else 1
            iterator = range(1, (abs(move_col) + 1))
            step_increment = np.array((0, neg_modifier))
        else:
            neg_modifier = -1 if (move_row < 0) else 1
            iterator = range(1, (abs(move_row) + 1))
            step_increment = np.array((neg_modifier, 0))

        print(instruct)
        for _ in iterator:
            local_head_pos += step_increment
            if not is_in_acceptable_position(
                tail_position=current_tail_pos, head_position=local_head_pos
            ):
                updated_tail_pos = move_tail_adjacent_to_head(
                    tail_position=current_tail_pos.copy(),
                    head_position=local_head_pos.copy(),
                    checked=True,
                )
                current_tail_pos = updated_tail_pos.copy()
                visited_coords.append(tuple(current_tail_pos))
            if local_head_pos[1] < 0:
                neg_x = min(neg_x, local_head_pos[1])
            else:
                pos_x = min(pos_x, local_head_pos[1])
            if local_head_pos[0] < 0:
                neg_y = min(neg_y, local_head_pos[0])
            else:
                pos_y = min(pos_y, local_head_pos[0])
            print(current_tail_pos, local_head_pos)

        move_matrix = np.array([move_row, move_col])
        print("yoyo", move_matrix, current_head_pos)
        current_head_pos += move_matrix

    final_gridspace_shape = np.array(((pos_y - neg_y), (pos_x - neg_x)))
    return visited_coords, final_gridspace_shape


def main():
    timer_name = "day9-timer"
    test_mode = True if len(argv) > 1 else False
    parent_dir = Path(__file__).parent.resolve()
    input_fname = "input.txt" if not test_mode else "sample.txt"

    DEBUG = True
    lines = read_text_file(join(parent_dir, input_fname))

    with Timer(name=timer_name, return_ns=True, ns_mode=True) as timer:
        visited_coords, gridspace_shape = get_coords_visited_and_gridspace_shape(
            raw_instructions=lines
        )
        time_1_millisecs = timer.stop(reset=True) / (10**6)

        total_time_millisecs = timer.timers[timer_name] * (10**3)

    # Print out results
    print(
        dedent(
            f"""
    Task 1 ({time_1_millisecs:.2f}ms elapsed):
    Number of unique visited coords: {len(set(visited_coords))}
    Final gridspace shape: {gridspace_shape}

    Total time taken: {total_time_millisecs:.2f}ms
    """
        )
    )


if __name__ == "__main__":
    main()
