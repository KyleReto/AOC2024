"""Day 7 of Advent of Code 2024"""
import re
from operator import mul, add, concat
from typing import Callable
from utils.abstract_day import Day

class DayCode(Day):
    """
    Solutions to Day 7 of AOC, which you can find here: https://adventofcode.com/2024/day/7
    """

    @classmethod
    def parse_input(cls, in_str: str) -> list[tuple[int, list[int]]]:
        """
        Parse the input into a more usable form

        Args:
            in_str: The input string, of the format x: y z ...

        Returns:
            A list of the format [x, [y, z, ...]]
        """
        parsed = []
        number_regexp = re.compile(r"\d+")
        for line in in_str.splitlines():
            numbers = number_regexp.findall(line)
            parsed.append((int(numbers[0]), [int(num) for num in numbers[1:]]))
        return parsed

    @classmethod
    def check_equation(cls, equation: tuple[int, list[int]],
                       operators: list[Callable[[int, int], int]]
                       ) -> list[list[Callable[[int, int], int]]]:
        """
        Check if any sequence of operators can solve a given equation

        Args:
            equation: The equation object, (x, [y, z, ...]), 
            where x is the desired result and [y, z, ...] is the list of operands
            operators: The valid operators to try between each operand.

        Returns:
            True if a solution exists, false otherwise
        """
        equations = [equation]
        while equations:
            result, operands = equations.pop()
            if len(operands) == 1:
                if operands[0] == result:
                    return True
                continue
            for operator in operators:
                left_eval = operator(operands[0], operands[1])
                simplified_equation = [left_eval] + operands[2:]
                equations.append((result, simplified_equation))
        return False

    @classmethod
    def part_1(cls, in_str: str) -> str:
        """
        Today's problem involves a collection of equations, written as "x: y z ...",
        where X is the result and y, z, etc. are operands. The trick is that we don't know
        which operators to place between each operand. To solve the day, we need to find the
        sum of all equations which have at least one solution. For part 1, we have only two
        possible operands: add (+) and multiply (*). I suspect that part 2 will add more, based
        on the text of the problem. For this problem, all operators move left to right, ignoring
        typical PEMDAS rules.

        My solution was to write a function that checks a given equation, taking any number of
        operators (defined as any binary function between integers). This function interprets
        the problem as a sort of tree traversal, where each number is a node forming x branches,
        where x is the number of different operators. We maintain a list of equations, and at each
        iteration, we process one equation from that list, splitting it into two sub-equations,
        each one shorter than the previous step. If an equation only has one remaining operand, we
        check if it's the result; if it is, we return True; if not, we remove it from the list
        instead of splitting it. I could also include optimizations to prune the tree earlier,
        such as not evaluating nodes which are already greater than the result, or by doing addition
        before multiplication and skipping the multiplication if the addition was too big. However,
        the function as written works on any binary operation on integers, and these optimizations
        would prevent it from working on some set of those operations, so I elected not to add them.

        Args:
            in_str: The input string, of the format x: y z ...

        Returns:
            The sum of all the X values from the valid equations
        """
        equations = cls.parse_input(in_str)
        total = 0
        for equation in equations:
            if cls.check_equation(equation, [mul, add]):
                total += equation[0]
        return total

    @classmethod
    def concat_integers(cls, a: int, b: int) -> int:
        """
        Concatenate two integers, e.g. concat(1, 2) = 12.

        Args:
            a: The first integer
            b: The second integer

        Returns:
            The two integers, concatenated
        """
        return int(f"{a}{b}")

    @classmethod
    def part_2(cls, in_str: str) -> str:
        """
        Part 2 adds another operator, concatenation ("||"). My previous solution covers this case.

        Solving this part just meant writing a one-line concatenation function and passing it in.
        I've gotta say, it feels pretty great to have my previous code just handle this case. It is
        a bit slower than I'd like, though. I tried implementing the optimizations
        I mentioned in part 1, plus using math to do the conatenation instead of casting to a
        string, but neither made the solution run meaningfully faster, so I left it as-is. I added
        a quick and dirty progress bar, as I did in part 6, to show users a progress estimate.

        Args:
            in_str: The input string, of the format x: y z ...

        Returns:
            The sum of all the X values from the valid equations
        """
        equations = cls.parse_input(in_str)
        total = 0
        for idx, equation in enumerate(equations):
            print (f"Calculating: {idx/len(equations):.0%}", end="\r")
            if cls.check_equation(equation, [mul, add, cls.concat_integers]):
                total += equation[0]
        return total
