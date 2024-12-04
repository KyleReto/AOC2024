"""Day 4 of Advent of Code 2024"""
from enum import Enum
from utils.abstract_day import Day

class DayCode(Day):
    """
    Solutions to Day 4 of AOC, which you can find here: https://adventofcode.com/2024/day/4
    """

    @classmethod
    def parse_input(cls, in_str: str) -> list[list[str]]:
        """
        Parse the input into a 2D list of strings

        Args:
            in_str: The raw text input, where each row is separated by \\n and each character is
            a column.

        Returns:
            A 2D list of strings, indexed as [row][col]
        """
        out_list = []
        for line in in_str.splitlines():
            out_list.append([])
            for char in line:
                out_list[-1].append(char)
        return out_list

    class Direction(Enum):
        """
        Enumerate valid directions of traversal.
        Values are stored as the (row, col) values to use to travel in this direction.
        """
        UP = (-1, 0)
        RIGHT = (0, 1)
        DOWN = (1, 0)
        LEFT = (0, -1)
        UP_RIGHT = (-1, 1)
        DOWN_RIGHT = (1, 1)
        DOWN_LEFT = (1, -1)
        UP_LEFT = (-1, -1)

    @classmethod
    def find_xmases_from_here(cls, in_list: list[list[str]], row: int,
                              col: int) -> list[tuple[int, int, Direction]]:
        """
        From any point in the grid, find all instances of XMAS starting at this location

        Args:
            in_list: The input grid
            row: The row of the position to check
            col: The column of the position to check

        Returns:
            The list of XMAS instances, as a list of their start positions and directions 
        """
        search_str = "XMAS"
        # The first character is shared by all directions
        if in_list[row][col] != search_str[0]:
            return []

        xmas_instances = []
        for direction in cls.Direction:
            search_row, search_col = row, col
            for search_char in search_str[1:]:
                search_row += direction.value[0]
                search_col += direction.value[1]
                # If we go out of bounds, stop checking this direction.
                if search_row < 0 or search_row >= len(in_list) or \
                        search_col < 0 or search_col >= len(in_list[search_row]):
                    break
                next_char = in_list[search_row][search_col]
                # If the character is wrong, stop checking this direction
                if next_char != search_char:
                    break
            # Just found out that for-else is a thing in python. Cool!
            else:
                # If all search characters matched, this is a valid XMAS.
                xmas_instances.append([row, col, direction])
        return xmas_instances


    @classmethod
    def part_1(cls, in_str: str) -> str:
        """
        Today's problem is a word search. We're looking for all instances of the string "XMAS" in
        a large block of text, but it can occur in any of the 8 cardinal directions and diagonals.
        I'm not sure how part 2 is going to change this, so I'll take a naive approach and modify it
        as necessary.
        My approach was to write a separate function to start from any point and check all 8
        directions, matching each to the string "XMAS" and returning all instances of it (Instances
        rather than count in case part 2 asks for instances). Since each XMAS string must start at
        an "X", and each X uniquely identifies its substrings, we can call this on every position in
        the input and find the count of these instances to get the number of XMASes.

        Args:
            in_str: A block of text containing an unknown number of "XMAS" strings

        Returns:
            The count of XMAS strings in the text
        """
        grid = cls.parse_input(in_str)
        total = 0
        for row_idx, row_val in enumerate(grid):
            for col_idx, _ in enumerate(row_val):
                total += len(cls.find_xmases_from_here(grid, row_idx, col_idx))
        return str(total)

    @classmethod
    def check_x_mas(cls, in_list: list[list[str]], row: int, col: int) -> bool:
        """
        Check if the current position is the center of an X-MAS

        Args:
            in_list: The input grid
            row: The row of the position to check
            col: The column of the position to check

        Returns:
            True if this position is the center of an X-MAS, False otherwise
        """
        # If the center character isn't "A", we can skip checking it.
        if in_list[row][col] != "A":
            return False
        return True

    @classmethod
    def part_2(cls, in_str: str) -> str:
        """
        Part 2 is totally different from what I expected. It's asking for X-MASes, which are
        two "MAS" strings in an X configuration, e.g.:
        M.M
        .A.
        S.S
        As before, the MAS strings can be written in any direction.

        Args:
            in_str: A block of text containing an unknown number of "MAS"es in the shape
            of an X.

        Returns:
            The number of X-MASes
        """
        grid = cls.parse_input(in_str)
        total = 0
        for row_idx, row_val in enumerate(grid):
            for col_idx, _ in enumerate(row_val):
                total += cls.check_x_mas(grid, row_idx, col_idx)
        return str(total)
