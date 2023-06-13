from ast import literal_eval
from os.path import join, splitext
from pathlib import Path
from sys import argv
from textwrap import dedent
from typing import List, Tuple, Union

import numpy as np
from dc2_python_utils.python_utils_general.utils_log_formatting import print_dict

from src.utils import read_text_file

DEBUG = False


def get_idx_of_right_orders(
    lines: List[str],
    debug: bool = False,
) -> List[int]:
    def _print(*args, **kwargs) -> None:
        if debug:
            print(*args, **kwargs)

    def _parse_value_pair(
        value_pair: Tuple[List, List],
        root: bool = True,
    ) -> bool:
        left, right = value_pair
        while right:
            if not left:
                return True
            left_val = left.pop(0)
            right_val = right.pop(0)
            _print(f"values: '{left_val}' || '{right_val}'")

            list_types = [
                1 if type(left_val) == list else 0,
                1 if type(right_val) == list else 0,
            ]
            num_list_types = sum(list_types)

            if num_list_types != 0:
                left_val = left_val if type(left_val) is list else [left_val]
                right_val = right_val if type(right_val) is list else [right_val]

                val = _parse_value_pair(
                    value_pair=(left_val, right_val),
                    root=False,
                )
                if val is not None:
                    return val
            else:
                if right_val > left_val:
                    return True
                elif right_val < left_val:
                    return False

        # Returns false if left is not empty!
        return False if (root or left) else None

    value_pairs = []
    for i in range(np.ceil(len(lines) / 3).astype(int)):
        idx_start = 3 * i
        idx_end = 3 * (i + 1)

        pairs_of_values = tuple(
            [literal_eval(list_str) for list_str in lines[idx_start : idx_end - 1]]
        )
        value_pairs.append(pairs_of_values)

    idx_of_right_orders = []
    _print("value_pairs", value_pairs)
    for ind, (left, right) in enumerate(value_pairs, start=1):
        # Edge case where 2 lists are same
        if left == right:
            raise ValueError(f"Value pairs are the same!! - {left,right}")

        _print(f"Starting ind {ind}")
        if _parse_value_pair(value_pair=(left, right)):
            idx_of_right_orders.append(ind)
    return idx_of_right_orders


def task2():
    pass


if __name__ == "__main__":
    parent_dir_abspath = Path(__file__).parent.resolve()
    test_mode = True if len(argv) > 1 else False
    test_file = (
        (f"{argv[1]}.txt" if (not splitext(argv[1])[-1]) else argv[1])
        if test_mode
        else None
    )

    prompt_answer_dict_1 = (
        {test_file: None}
        if test_file
        else {
            "test1.txt": None,
            "sample1.txt": None,
            "input1.txt": None,
        }
    )

    for input_fname in prompt_answer_dict_1.keys():
        lines = read_text_file(join(parent_dir_abspath, input_fname))
        idx_of_right_orders = get_idx_of_right_orders(lines=lines, debug=DEBUG)
        prompt_answer_dict_1[input_fname] = (
            sum(idx_of_right_orders),
            idx_of_right_orders,
        )
        # Test case
        if not test_file and "test" in input_fname:
            assert set(prompt_answer_dict_1[input_fname][-1]) == set([1, 2, 4, 6])
        print(input_fname)
        print(prompt_answer_dict_1[input_fname])
