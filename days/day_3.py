"""Day 3 of Advent of Code 2024"""
import re
from utils.abstract_day import Day

class DayCode(Day):
    """
    Solutions to Day 3 of AOC, which you can find here: https://adventofcode.com/2024/day/3
    """

    @classmethod
    def part_1(cls, in_str: str) -> str:
        """
        The input is representative of the memory of a computer, which is corruputed.
        The goal of the corrupted program is to multiply some numbers, but many of
        the operations are not actually valid multiplication operations. A valid
        operation is written as "mul(X,Y)", where X and Y are 1-3 digit numbers.
        Operations which are similar to, but do not comform to this scheme are invalid.
        We need to sum the products of the multiplication operations. I also see
        some "do_not_mul()" and "then()" commands in the input, which may complicate
        part 2. These could also be part of some future day's task, as with the
        intcode computer from a previous year I solved. I'll be ignoring those (and recursive
        mul operations) for now, but I'll still keep them in mind.
        
        My solution is pretty simple, I just use a regex to find the operations, with
        a capturing group for each digit. Iterating over the string with this regex gives
        us the digits, which we just multiply and sum to get the answer.

        Args:
            in_str: The input string to process.

        Returns:
            The number of valid mul operations in the input.
        """
        # Match anything of the format "mul(X,Y)", where X and Y are 1-3 digit numbers.
        pattern = re.compile(r'mul\((\d{1,3}),(\d{1,3})\)')
        sum = 0
        for op in pattern.finditer(in_str):
            sum += int(op[1]) * int(op[2])
        return sum

    @classmethod
    def part_2(cls, in_str: str) -> str:
        """
        The twist today is easier than expected, it just asks us to check for
        "do()" and "don't()" operations. These respectively enable and disable the
        multiplication, so we just skip any mul() ops after a don't() until we find
        another do(). We start under the do() condition.

        For this one, I decided to get some regex practice in and solve it mostly
        with that. I created a second pattern to capture any text we should execute (
        i.e. enclosed by do() and don't()). This meant 

        Args:
            in_str: The input string from AoC

        Returns:
            The sum of the products, adhering to do() and don't() ops
        """
        # Match anything of the format "mul(X,Y)", where X and Y are 1-3 digit numbers.
        # Captures both digits as the two capture groups
        mul_pattern = re.compile(r'mul\((\d{1,3}),(\d{1,3})\)')
        # Match any text (including \n) enclosed by the following:
            # "do()" or the start of the string, greedy (the farthest left instance)
            # "don't()" or the end of the string, lazy (also the farthest left instance)
        # Captures the contained substring as the only capture group.
        do_pattern = re.compile(r"(?:(?:do\(\))|^)(.*?)(?:(?:don't\(\))|$)", re.S)
        sum = 0
        for code in do_pattern.finditer(in_str):
            for op in mul_pattern.finditer(code[1]):
                sum += int(op[1]) * int(op[2])
        return sum
