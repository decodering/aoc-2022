from os.path import join
from pathlib import Path
import numpy as np

parent_dir = Path(__file__).parent.resolve()
input_fname = "input.txt"

with open(join(parent_dir, input_fname)) as file:
    lines = file.read().splitlines()

input_struct = []
for ind, line in enumerate(lines):
    if line == "":
        starting_line_num = ind + 1
        break
    input_struct.append(line)
move_instructs = lines[starting_line_num:]

input_struct_data = {
    "col1": [],
    "col2": [],
    "col3": [],
    "col4": [],
    "col5": [],
    "col6": [],
    "col7": [],
    "col8": [],
    "col9": [],
}
for line_num, line in enumerate(input_struct[:-1], 1):
    for i in range(9):
        crate_letter = line[(i * 4) : ((i + 1) * 4)].strip()
        if crate_letter != "":
            input_struct_data[f"col{i+1}"].insert(0, crate_letter[1])

print(f"Printing input struct")
for k in input_struct_data.keys():
    print(input_struct_data[k])

for instruct in move_instructs:
    _, move_amt, _, source_col, _, dest_col = instruct.split(" ")
    move_amt = int(move_amt)

    crates_to_move_reversed = list(
        reversed(input_struct_data[f"col{source_col}"][-move_amt:])
    )

    input_struct_data[f"col{dest_col}"].extend(crates_to_move_reversed)
    input_struct_data[f"col{source_col}"] = input_struct_data[f"col{source_col}"][
        :-move_amt
    ]

print(f"\n\n================\nPrinting FINAL input struct\n\n")
for k in input_struct_data.keys():
    print(input_struct_data[k])
