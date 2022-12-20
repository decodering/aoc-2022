# Advent of Code 2022

*A repository solving code challenges in Eric Wastl's **[2022 Advent of Code](https://adventofcode.com/)**.*

**Content outline:**

- [AOC 2022 outline](#aoc-2022-outline)
- [How to run this repository](#how-to-run-this-repository)

## AOC 2022 outline

- Elves need 50 stars to feed reindeers by 12/05
- Each day there will be 2 puzzles, second one being unlocked after finishing first
- Each puzzle 1 half-star

## How to run this repository

A [makefile is attached](https://calmcode.io/makefiles/the-problem.html) for the simple running of the challenges. An example of how to run one of the makefile commands:

```bash
make day6
```

Sometimes some of these challenges have an alternative run for sample inputs, i.e. a kind of test to see if the expected answer is printed. This command is suffixed (perhaps not v accurately) with `-test`.

```bash
make day6-test
```

That's it! Finally:

```
         |
        -+-
         A
        /=\               /\  /\    ___  _ __  _ __ __    __
      i/ O \i            /  \/  \  / _ \| '__|| '__|\ \  / /
      /=====\           / /\  /\ \|  __/| |   | |    \ \/ /
      /  i  \           \ \ \/ / / \___/|_|   |_|     \  /
    i/ O * O \i                                       / /
    /=========\        __  __                        /_/    _
    /  *   *  \        \ \/ /        /\  /\    __ _  ____  | |
  i/ O   i   O \i       \  /   __   /  \/  \  / _` |/ ___\ |_|
  /=============\       /  \  |__| / /\  /\ \| (_| |\___ \  _
  /  O   i   O  \      /_/\_\      \ \ \/ / / \__,_|\____/ |_|
i/ *   O   O   * \i
/=================\
       |___|

```
