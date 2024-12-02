"""Day 2 of Advent of Code 2024"""
import math
from utils.abstract_day import Day

class DayCode(Day):
    """
    Solutions to Day 2 of AOC, which you can find here: https://adventofcode.com/2024/day/2
    """
    @classmethod
    def parse_input(cls, in_str: str) -> list[list[int]]:
        """
        Parse the input for this problem

        Args:
            in_str: The raw input string

        Returns:
            A list of reports, where each report is a list of integers
        """
        out_list = []
        for line in in_str.splitlines():
            report = []
            for digit in line.split(" "):
                report.append(int(digit))
            out_list.append(report)
        return out_list

    @classmethod
    def part_1(cls, in_str: str) -> str:
        """
        The input data is a collection of lines ("Reports") of integers ("Levels")
        coming from a reactor. A report is deemed safe if the levels meet both of the
        following criteria:
        1. The levels all increase OR all decrease
        2. Every two adjacent levels differ by at least one and at most three.
        The goal of the task is to return the number of safe reports in the set

        My approach here is to simply check each report digit by digit. To check a report,
        we first compare the first to digits to get the direction of movement, either
        ascending (+1) or descending (-1). For each pair (including the first one), we then
        take the difference between the two and multiply it by the direction, giving us the
        distance traveled in the correct direction (up for ascending, down for descending).
        If this distance is between 1 and 3, then all criteria are met. If not, we can break
        out of the loop early to save a few iterations.

        Args:
            in_str: The input string from AoC

        Returns:
            The count of safe reports in the input
        """
        reports = cls.parse_input(in_str)
        count = 0
        for report in reports:
            is_safe = True
            travel_direction = 0
            # Assumption: Each report has at least 1 level
            prev_digit = report[0]
            for digit in report[1:]:
                diff = digit - prev_digit
                prev_digit = digit
                if travel_direction == 0:
                    travel_direction = math.copysign(1, diff)

                # Distance toward the correct direction,
                # i.e if the difference is +3 and we should be ascending, that's +3 correct dist.
                # If it's +3 and we should be descending, it's -3.
                correct_dist = diff * travel_direction
                if correct_dist > 3 or correct_dist < 1:
                    is_safe = False
                    break
            if is_safe:
                count += 1
        return count

    @classmethod
    def part_2(cls, in_str: str) -> str:
        return ""
