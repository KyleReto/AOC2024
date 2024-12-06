#!/usr/bin/env python3

"""Harness for all AOC days."""
import argparse
import importlib
import re
from os import listdir, path
from utils import abstract_day

parser = argparse.ArgumentParser(description='Run the AoC problem solutions.')

# This file is just a disposable test harness for my own use,
# so I didn't write it with cleanliness in mind.
max_day = 0
for filename in listdir("days"):
    match = re.search(r"day_(\d*)\.py", filename)
    if match is not None:
        matched_val = int(match.group(1))
        max_day = matched_val if matched_val > max_day else max_day

parser.add_argument("-d", "--day", help="The day of code to run", type=int,
                    choices=[i for i in range(1,max_day+1)], default=max_day)
parser.add_argument("-s", "--sample-only",
                    help='run only the sample (excluding the full input)', action="store_true")
args = parser.parse_args()

# Find the associated module by name and run it.
day_module = importlib.import_module("days.day_" + str(args.day))
day_code: abstract_day = day_module.DayCode
try:
    with open("sample.txt", "r", encoding="utf-8") as f:
        test_str = f.read()
    print("Part 1 Sample Output: ", day_code.part_1(test_str))
    print("Part 2 Sample Output: ", day_code.part_2(test_str))
except FileNotFoundError:
    print("No sample.txt file was found, skipping sample runs...\n"
          "If you'd like to run the smaller input samples provided by AoC separately from the main "
          "problem input, create a file called `sample.txt` and place it in the AOC2024 "
          "directory, then paste the sample input into that file.\n")

if not args.sample_only:
    try:
        with open("input.txt", "r", encoding="utf-8") as f:
            in_str = f.read()
    except FileNotFoundError:
        print("No input.txt file was found, defaulting to archived inputs...\n"
            "If you'd like to run this code on a custom input, please create a file "
            "with your desired input text called `input.txt` and place it in the "
            "AOC2024 directory.\n")
        with open(path.join("inputs",f"day_{args.day}.txt"), "r", encoding="utf-8") as f:
            in_str = f.read()
    print("Part 1 Full Output:   ", day_code.part_1(in_str))
    print("Part 2 Full Output:   ", day_code.part_2(in_str))
