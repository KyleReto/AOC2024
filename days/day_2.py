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

    # Refactored after part 1
    @classmethod
    def check_report_safety(cls, report: list[int]) -> bool:
        """
        Check if a report is safe or not (without the Problem Dampener)

        Args:
            report: The report to check

        Returns:
            True if safe, False if not
        """
        travel_direction = 0
        # Assumption: Each report has at least 1 level
        prev_digit = report[0]
        for digit in report[1:]:
            diff = digit - prev_digit
            if travel_direction == 0:
                travel_direction = math.copysign(1, diff)

            # Distance toward the correct direction,
            # i.e if the difference is +3 and we should be ascending,
            # that's +3 correct dist.
            # If it's +3 and we should be descending, it's -3.
            correct_dist = diff * travel_direction
            if correct_dist > 3 or correct_dist < 1:
                return False
            prev_digit = digit
        return True

    @classmethod
    def part_2(cls, in_str: str) -> str:
        """
        The problem is the same as part 1, except that we can now use the Problem Dampener.
        This means that, if any one level could be removed and cause the report to be Safe,
        then that report should be considered Safe.

        For this part, my initial approach was to check the correct distance as before,
        and skip one digit if it didn't match. This would leave the prev_digit variable
        at whatever it was set to before, meaning it would accurately compare the digits as
        if the wrong digit was missing entirely. This was more efficient (O(n^2)) than the approach
        I ended up with, but it failed on edge cases like [1 3 2 3 5], since it would try to
        skip the 2 digit (the correct digit to skip is the first 3).
        I could have preservedthe efficiency by only checking for removed digits adjacent to
        a failure point, e.g. both 3 and 2 in the above example, I instead opted for a simple
        brute force approach where we precalculate all variations on the report missing any
        arbitrary digit, then check all variations one by one. Combined with moving the report
        safety check out to its own function, this is more intuitive and easy to maintain,
        at the cost of a ~2x speed penalty on this input, which is about 1ms.

        Args:
            in_str: The input string from AoC

        Returns:
            The number of safe reports in the set
        """
        reports = cls.parse_input(in_str)
        count = 0
        for report in reports:
            variations = [report]
            for idx, _ in enumerate(report):
                variation = report.copy()
                variation.pop(idx)
                variations.append(variation)

            for variation in variations:
                if cls.check_report_safety(variation):
                    count += 1
                    break
        return count
