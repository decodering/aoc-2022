"""
Should make a more efficient sliding window algo that doesn't do it per char, but per 4 chars
"""

from os.path import join
from pathlib import Path
from sys import argv
from time import time
from typing import Optional, Tuple
from textwrap import dedent

from src.utils import read_text_file
from src.timer import Timer


def detect_marker(
    stream_input: str,
    marker_len: int = 4,
) -> Optional[Tuple[int, list]]:
    for i in range(len(stream_input) - marker_len):
        curr_window = stream_input[i : i + marker_len]
        # print(i, curr_window, len(np.unique(curr_window)))
        if len(set(curr_window)) == marker_len:
            return (i + marker_len), curr_window
    print("WARNING: No marker detected! Returning None...")
    return None


def main():
    timer_name = "timer"
    test_mode = True if len(argv) > 1 else False

    parent_dir = Path(__file__).parent.resolve()
    input_fname = "input.txt" if not test_mode else "sample1.txt"

    lines = read_text_file(join(parent_dir, input_fname))
    stream = lines[0]
    assert len(lines) == 1

    print(f"Processing a stream of enconded input, {len(stream)} chars long...")

    with Timer(name=timer_name, return_ns=True, ns_mode=True) as timer:
        marker_loc1, curr_window1 = detect_marker(stream_input=stream, marker_len=4)
        time_1_microsecs = timer.stop(reset=True) / 1000
        marker_loc2, curr_window2 = detect_marker(stream_input=stream, marker_len=14)
        time_2_microsecs = timer.stop(reset=True) / 1000
        total_time_microsecs = timer.timers[timer_name] * (10**6)

    print(
        dedent(
            f"""
    Task 1: {marker_loc1} Num of characters needed process until start of marker ('{curr_window1}'). {(time_1_microsecs):.3f}us taken.
    Task 2: {marker_loc2} Num of characters needed process until start of message ('{curr_window2}'). {(time_2_microsecs):.3f}us taken.
    Total time: {total_time_microsecs:.3f}us taken
    """
        )
    )


if __name__ == "__main__":
    main()
