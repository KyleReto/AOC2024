"""Define an abstract class for an AOC Day of code"""
from abc import ABC, abstractmethod

class Day(ABC):
    """
    An abstract class for a Day of code
    """
    @classmethod
    @abstractmethod
    def part_1(cls, in_str: str) -> str:
        """
        Run code for part 1 of a day

        Args:
            in_str: The input string from AOC

        Returns:
            The output requested by AOC, as a string
        """

    @classmethod
    @abstractmethod
    def part_2(cls, in_str:str) -> str:
        """
        Run code for part 2 of a day

        Args:
            in_str: The input string from AOC

        Returns:
            The output requested by AOC, as a string
        """
