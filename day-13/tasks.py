from ast import literal_eval
from os.path import join, splitext
from pathlib import Path
from sys import argv
from typing import List, Tuple, Union
import numpy as np
from src.utils import read_text_file


def get_idx_of_right_orders(lines: List[str]) -> List[int]:
    def _parse_value_pair(value_pair: Tuple[List, List]) -> bool:
        left, right = value_pair
        while right:
            if not left:
                return True
            left_val = left.pop(0)
            right_val = right.pop(0)
            print("values", left_val, right_val)

            list_types = [
                1 if type(left_val) == list else 0,
                1 if type(right_val) == list else 0,
            ]
            num_list_types = sum(list_types)

            if num_list_types != 0:
                left_val = left_val if type(left_val) is list else [left_val]
                right_val = right_val if type(right_val) is list else [right_val]

                if _parse_value_pair(value_pair=(left_val, right_val)):
                    return True
            else:
                if right_val > left_val:
                    return True
                elif right_val < left_val:
                    return False
        return False

    value_pairs = []
    print("raw", lines)
    for i in range(np.ceil(len(lines) / 3).astype(int)):
        idx_start = 3 * i
        idx_end = 3 * (i + 1)

        pairs_of_values = tuple(
            [literal_eval(list_str) for list_str in lines[idx_start : idx_end - 1]]
        )
        value_pairs.append(pairs_of_values)

    idx_of_right_orders = []
    print("value_pairs", value_pairs)
    for ind, (left, right) in enumerate(value_pairs, start=1):
        # Edge case where 2 lists are same
        if left == right:
            raise ValueError(f"Value pairs are the same!! - {left,right}")

        print(f"Starting ind {ind}")
        if _parse_value_pair(value_pair=(left, right)):
            idx_of_right_orders.append(ind)
    return idx_of_right_orders


if __name__ == "__main__":
    parent_dir_abspath = Path(__file__).parent.resolve()
    test_mode = True if len(argv) > 1 else False
    test_file = (
        (f"{argv[1]}.txt" if (not splitext(argv[1])[-1]) else argv[1])
        if test_mode
        else None
    )
    input_fname = "input.txt" if not test_mode else test_file

    lines = read_text_file(join(parent_dir_abspath, input_fname))
    task1_answer = get_idx_of_right_orders(lines=lines[: 3 * 50])
    print(task1_answer)
    print(sum(task1_answer))

    # assert task1_answer == set([1, 2, 4, 6])
