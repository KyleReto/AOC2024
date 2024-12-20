#!/usr/bin/env python3

"""Harness for all AOC days."""
import argparse
import importlib
import re
import sys
from traceback import format_exc
from os import listdir
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
parser.add_argument("-v", "--verbose",
                    help='print developer-facing exceptions to the command line (instead of '
                    'user-facing warnings)', action="store_true")
group = parser.add_mutually_exclusive_group()
group.add_argument("-s", "--sample_only",
                    help='run only the sample (excluding the full input)', action="store_true")
group.add_argument("-i", "--input-only",
                    help='run only the full input (excluding the sample)', action="store_true")
args = parser.parse_args()

# Find the associated module by name and run it.
day_module = importlib.import_module("days.day_" + str(args.day))
day_code: abstract_day = day_module.DayCode
input_url = f"https://adventofcode.com/2024/day/{args.day}/input"

if not args.input_only:
    try:
        with open("sample.txt", "r", encoding="utf-8") as f:
            test_str = f.read()
        try:
            print(f"Day {args.day} Part 1 Sample Output: {day_code.part_1(test_str)}")
            print(f"Day {args.day} Part 2 Sample Output: {day_code.part_2(test_str)}")
        # Exceptions here will always be due to user error, and the type is unpredictable
        except Exception as e: # pylint: disable=broad-exception-caught
            if not args.verbose:
                sys.exit("An unexpected exception occurred when attempting to run "
                            f"the solution for day {args.day}. Make sure your input.txt file "
                        f"is the one for day {args.day}, which you can find here: {input_url}."
                        "\nIf you meant to run a different day, use the --day flag."
                        "\nIf you want to print the exception instead of this message, use "
                        "the --verbose flag\n")
            else:
                sys.exit(format_exc())
    except FileNotFoundError:
        WARNING = ("No sample.txt file was found, skipping sample runs...\n"
            "If you'd like to run the smaller input samples provided by AoC separately from the "
            "main problem input, create a file called `sample.txt` and place it in the AOC2024 "
            "directory, then paste the sample input into that file.\n"
            "If you don't want to run the smaller input samples, use the --input-only flag "
            "to silence this warning.\n")
        if args.sample_only:
            sys.exit(WARNING)
        print(WARNING)


if not args.sample_only:
    try:
        with open("input.txt", "r", encoding="utf-8") as f:
            in_str = f.read()
    except FileNotFoundError:
        sys.exit("No input.txt file was found, so the solution could not be run.\n"
            "If you'd like to run this solution, please create a file "
            "with your desired input text called `input.txt` and place it in the "
            "AOC2024 directory.\n")
    try:
        print(f"Day {args.day} Part 1 Full Output: {day_code.part_1(in_str)}")
        print(f"Day {args.day} Part 2 Full Output: {day_code.part_2(in_str)}")

    # Exceptions here will always be due to user error, and the type is unpredictable
    except Exception as e: # pylint: disable=broad-exception-caught
        if not args.verbose:
            sys.exit("An unexpected exception occurred when attempting to run "
                    f"the solution for day {args.day}. Make sure your input.txt file "
                f"is the one for day {args.day}, which you can find here: {input_url}."
                "\nIf you meant to run a different day, use the --day flag."
                "\nIf you want to print the exception instead of this message, use "
                "the --verbose flag\n")
        else:
            sys.exit(format_exc())
