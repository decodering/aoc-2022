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


def parse_instruction(instruction: str) -> Tuple[int, int]:
    direction, steps = [int(i) if i.isdigit() else i for i in instruction.split(" ")]
    move_row = steps if (direction == "D") else (-steps if (direction == "U") else 0)
    move_col = steps if (direction == "R") else (-steps if (direction == "L") else 0)
    return move_row, move_col


def is_in_acceptable_position(
    trailing_knot_pos: np.array, leading_knot_pos: np.array
) -> bool:
    """
    Tail position is centre position. Check if head_position is acceptable.
    """
    y, x = trailing_knot_pos
    is_acceptable_y = y - 1 <= leading_knot_pos[0] <= y + 1
    is_acceptable_x = x - 1 <= leading_knot_pos[1] <= x + 1
    return is_acceptable_x and is_acceptable_y


def move_trailing_knot_adjacent_to_leading(
    trailing_pos: np.array, leading_pos: np.array, checked: bool = False
) -> Optional[npt.NDArray[Any]]:
    if not checked and is_in_acceptable_position(
        trailing_knot_pos=trailing_pos, leading_knot_pos=leading_pos
    ):
        return
    head_y, head_x = leading_pos
    tail_y, tail_x = trailing_pos
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
        # Acceptable permutations: (1,2), (2,1), (1,1), (2,2)
        # NOTE: (1,1) should not be possible here with how this func is called in
        #       higher-lvl func and will not do anything
        assert (2 <= manhattan_distance <= 4) and (1 <= abs(x_distance) <= 2)
        if abs(x_distance) > abs(y_distance):
            move_matrix = np.array((y_distance, steps_shifted_in_x_axis))
        elif abs(x_distance) < abs(y_distance):
            move_matrix = np.array((steps_shifted_in_y_axis, x_distance))
        else:
            move_matrix = np.array((steps_shifted_in_y_axis, steps_shifted_in_x_axis))
    trailing_pos += move_matrix
    return trailing_pos


def get_coords_visited_and_gridspace_shape(
    raw_instructions: List[str],
    num_trailing_knots: int = 1,
    starting_pos: Tuple[int, int] = None,
) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
    starting_pos = (0, 0) if starting_pos is None else starting_pos
    assert num_trailing_knots >= 1

    knots_positions_dict = {0: np.array(starting_pos)}
    for i in range(1, num_trailing_knots + 1):
        knots_positions_dict[i] = np.array(starting_pos)
    visited_coords_last_knot = deque(iterable=[starting_pos])
    visited_coords_head = deque(iterable=[starting_pos])

    for instruct in raw_instructions:
        move_row, move_col = parse_instruction(instruction=instruct)
        is_lateral = True if (abs(move_col)) else False
        initial_head_pos = knots_positions_dict[0].copy()
        if is_lateral:
            neg_modifier = -1 if (move_col < 0) else 1
            iterator = range(1, (abs(move_col) + 1))
            step_increment = np.array((0, neg_modifier))
        else:
            neg_modifier = -1 if (move_row < 0) else 1
            iterator = range(1, (abs(move_row) + 1))
            step_increment = np.array((neg_modifier, 0))

        for _ in iterator:
            knots_positions_dict[0] += step_increment
            for i in range(1, num_trailing_knots + 1):
                leading_knot_pos = knots_positions_dict[(i - 1)]
                trailing_knot_pos = knots_positions_dict[i]
                if not is_in_acceptable_position(
                    trailing_knot_pos=trailing_knot_pos,
                    leading_knot_pos=leading_knot_pos,
                ):
                    updated_pos = move_trailing_knot_adjacent_to_leading(
                        trailing_pos=trailing_knot_pos.copy(),
                        leading_pos=leading_knot_pos.copy(),
                        checked=True,
                    )
                    knots_positions_dict[i] = updated_pos.copy()
                    if i == num_trailing_knots:
                        visited_coords_last_knot.append(tuple(updated_pos))
            visited_coords_head.append(tuple(knots_positions_dict[0]))

        move_matrix = np.array([move_row, move_col])
        assert np.array_equal(knots_positions_dict[0], (initial_head_pos + move_matrix))

    return visited_coords_last_knot, visited_coords_head


def main():
    timer_name = "day9-timer"
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
        (
            visited_coords_last_knot_1,
            visited_coords_head_1,
        ) = get_coords_visited_and_gridspace_shape(
            raw_instructions=lines, num_trailing_knots=1
        )
        time_1_millisecs = timer.stop(reset=True) / (10**6)
        (
            visited_coords_last_knot_9,
            visited_coords_head_9,
        ) = get_coords_visited_and_gridspace_shape(
            raw_instructions=lines, num_trailing_knots=9
        )
        time_2_millisecs = timer.stop(reset=True) / (10**6)
        total_time_millisecs = timer.timers[timer_name] * (10**3)

    # Print out results
    visited_grid_space_head, visited_grid_space_tail = {}, {}
    for ind, (visited_coords_head, visited_coords_last_knot) in enumerate(
        [
            (visited_coords_head_1, visited_coords_last_knot_1),
            (visited_coords_head_9, visited_coords_last_knot_9),
        ],
        1,
    ):
        head_y_list = [y for y, _ in visited_coords_head]
        head_x_list = [x for _, x in visited_coords_head]
        tail_y_list = [y for y, _ in visited_coords_last_knot]
        tail_x_list = [x for _, x in visited_coords_last_knot]
        visited_grid_space_head[f"task_{ind}"] = (
            len(np.unique(head_y_list)),
            len(np.unique(head_x_list)),
        )
        visited_grid_space_tail[f"task_{ind}"] = (
            len(np.unique(tail_y_list)),
            len(np.unique(tail_x_list)),
        )
    print(
        dedent(
            f"""
    Task 1 ({time_1_millisecs:.2f}ms elapsed):
    Number of unique visited coords by tail (2 knots): {len(set(visited_coords_last_knot_1))}
    Final gridspace shape (head, tail): {visited_grid_space_head['task_1']}, {visited_grid_space_tail['task_1']}

    Task 2 ({time_2_millisecs:.2f}ms elapsed):
    Number of unique visited coords by tail (10 knots): {len(set(visited_coords_last_knot_9))}
    Final gridspace shape (head, tail): {visited_grid_space_head['task_2']}, {visited_grid_space_tail['task_2']}

    Total time taken: {total_time_millisecs:.2f}ms
    """
        )
    )


if __name__ == "__main__":
    main()
