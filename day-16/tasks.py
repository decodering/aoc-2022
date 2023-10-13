"""
Sliding window algorithm to determine 'visibility'.

Euclidean grid space.
"""
from os.path import join, splitext
from pathlib import Path
from sys import argv
from textwrap import dedent

import numpy as np
import numpy.typing as npt

from src.timer import Timer
from src.utils import read_text_file

## PSEUDO
# The earlier hitting the thing, the better
# At a depth of X (i.e. 5) --> Find the best move (i.e. for the first Y)
# At a depth of


def get_tunnel_connections_dict(lines: list) -> dict:
    ## STATE data objects
    # VALVE_CONNECTIONS
    # VALVE_PRESSURE_STATE
    #
    # CURRENT_POSITION
    # CURRENT_SCORE
    # TIME_LEFT --> Do it as a list, e.g. ['BB','CC','OPEN',...]

    for line in lines:
        valve = line.split(" ")[1]
        flow_rate = line.split(" ")[4].split("=")[-1].rstrip(";")
        if "lead to valves" in line:
            valve_connections = (
                line.split("lead to valves")[-1].replace(" ", "").split(",")
            )
        elif "leads to valve" in line:
            valve_connections = (
                line.split("leads to valve")[-1].replace(" ", "").split(",")
            )
        else:
            raise ValueError
        print(f"{valve}: {flow_rate} -- {valve_connections}")


def main():
    timer_name = "day16-timer"
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
        get_tunnel_connections_dict(lines)
        time_1_millisecs = timer.stop(reset=True) / (10**6)
        total_time_millisecs = timer.timers[timer_name] * (10**3)

    # Print out results
    print(
        dedent(
            f"""
    Task 1 ({time_1_millisecs:.2f}ms elapsed):
    anser....
    
    Total time taken: {total_time_millisecs:.2f}ms
    """
        )
    )


if __name__ == "__main__":
    main()
