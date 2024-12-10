"""Day 8 of Advent of Code 2024"""
from utils.abstract_day import Day

class DayCode(Day):
    """
    Solutions to Day 8 of AOC, which you can find here: https://adventofcode.com/2024/day/8
    """

    @classmethod
    def parse_input(cls, in_str: str) -> list[list[str]]:
        """
        Parse the input into a 2D array of characters

        Args:
            in_str: The string describing the grid of antennae

        Returns:
            The grid of antenna, parsed
        """
        output = []
        for line in in_str.splitlines():
            output.append(list(line))
        return output

    @classmethod
    def get_both_antinodes(cls, antennae: list[tuple[int, int]]) -> list[tuple[int, int]]:
        """
        Get the antinode positions for all antennae of a given frequency.
        Does not check whether a position is in bounds or not.

        Args:
            antennae: The list of antenna positions for a given frequency

        Returns:
            The list of antinode positions, as (row, col) tuples
        """
        output = []
        for a_idx, (a_row, a_col) in enumerate(antennae[:-1]):
            for _, (b_row, b_col) in enumerate(antennae[a_idx+1:]):
                vector = (b_row - a_row, b_col - a_col)
                antinode_back = (a_row - vector[0], a_col - vector[1])
                antinode_forward = (b_row + vector[0], b_col + vector[1])
                output += [antinode_back, antinode_forward]
        return output

    @classmethod
    def part_1(cls, in_str: str) -> str:
        """
        The problem today is a bit complex. We're given a map of antenna positions, which is
        a grid of characters on a map. Empty positions are marked with ".", while positions
        with antennae are marked with a different character, which represents that antenna's
        frequency (Specifically, digits or case-sensitive letters). An "antinode" is a point
        on the line drawn connecting two antenna where one antenna is twice as far away as the
        other. This means that each pair of antennae of a given frequency has two antinodes,
        one on either side. In effect, this looks like drawing a line between the two antenna
        and extending it to triple its original length, then placing an antinode at both ends.
        Antinodes can overlap with both each other and antenna positions.

        My approach here looks a bit convoluted, but that's because accessing points in a 2D
        array is a bit of a pain. For future days, I'll work on a dedicated grid helper class
        to simplify this. In the meantime, the solution works by first collecting a dictionary
        of all antennae positions for each frequency. Then, for each frequency, we iterate over
        each unique pair of antennae in the list. For each pair, we find the vector describing
        the line between the two points, then use that to find each of the two antinode positions
        that the two antennae create. Lastly, we maintain a list of all valid antinodes, adding
        each of these points found to the list if they're in bounds. In actuality, this is a dict
        mapping points in the grid to the frequency of the corresponding antinode, both because
        this makes it easier to ensure that no duplicate entries are made, and because it might
        be useful to keep track of frequencies of antinodes for part 2.

        Args:
            in_str: The input string from AoC, describing a map of antenna positions and frequencies

        Returns:
            The count of positions in the bounds of the grid with at least one antinode
        """
        grid = cls.parse_input(in_str)

        antennae: dict[str, list[tuple[int, int]]] = {}
        for i, row in enumerate(grid):
            for j, char in enumerate(row):
                if char != ".":
                    frequency_antennae = antennae.setdefault(char, [])
                    frequency_antennae.append((i, j))

        antinodes: dict[tuple[int, int], list[int]] = {}
        for frequency, positions in antennae.items():
            freq_antinodes = cls.get_both_antinodes(positions)
            for antinode in freq_antinodes:
                if (antinode[0] not in range(0, len(grid)) or
                    antinode[1] not in range(0, len(grid[0]))):
                    continue
                antinodes_here = antinodes.setdefault(antinode, [])
                antinodes_here.append(frequency)
        return len(antinodes)

    @classmethod
    def get_all_antinodes(cls, antennae: list[tuple[int, int]], grid_size: tuple[int, int]
                          ) -> list[tuple[int, int]]:
        """
        Get the antinode positions for all antennae of a given frequency.
        Does not check whether a position is in bounds or not.

        Args:
            antennae: The list of antenna positions for a given frequency
            grid_size: The size of the grid, as a (row count, col count) tuple

        Returns:
            The list of antinode positions, as (row, col) tuples
        """
        output = []
        for a_idx, a_pos in enumerate(antennae[:-1]):
            for _, b_pos in enumerate(antennae[a_idx+1:]):
                forward = a_pos, (b_pos[0] - a_pos[0], b_pos[1] - a_pos[1])
                back = b_pos, (-forward[1][0], -forward[1][1])
                for start_pos, vector in [forward, back]:
                    antinode_pos = start_pos
                    while (antinode_pos[0] in range(0, grid_size[0]) and
                           antinode_pos[1] in range(0, grid_size[1])):
                        antinode_pos = (antinode_pos[0] + vector[0], antinode_pos[1] + vector[1])
                        output += [(antinode_pos[0], antinode_pos[1])]
        return output

    @classmethod
    def part_2(cls, in_str: str) -> str:
        """
        For part 2, the twist is that there's now an infinite number of antinodes for each
        pair of points, bounded only by the extent of the grid. In part 1, each pair only
        created one antinode to each side. Now, the pairs create one antinode to the side,
        then the line continues along and creates another antinode, and another, and so on
        until the edge of the grid is reached.

        For my solution, I only rewrote the get_antinodes function, reworking the part that gets
        pairs of nodes into a loop that continues to find antinode positions in a given direction
        until the position is out of bounds. This runs on both forward and backward vectors, and
        can be easily modified to work in more directions if necessary. The triple for loop is a bit
        messy, so for future days I'm definitely going to write proper grid and vector classes to
        more easily manage 2D arrays, since these types of operations are very common in AoC and
        are difficult to express concisely in python without external libraries.

        Args:
            in_str: The input string from AoC, describing a map of antenna positions and frequencies

        Returns:
            The count of positions in the bounds of the grid with at least one antinode
        """
        grid = cls.parse_input(in_str)

        antennae: dict[str, list[tuple[int, int]]] = {}
        for i, row in enumerate(grid):
            for j, char in enumerate(row):
                if char != ".":
                    frequency_antennae = antennae.setdefault(char, [])
                    frequency_antennae.append((i, j))

        antinodes: dict[tuple[int, int], list[int]] = {}
        for frequency, positions in antennae.items():
            freq_antinodes = cls.get_all_antinodes(positions, (len(grid), len(grid[0])))
            for antinode in freq_antinodes:
                if (antinode[0] not in range(0, len(grid)) or
                    antinode[1] not in range(0, len(grid[0]))):
                    continue
                antinodes_here = antinodes.setdefault(antinode, [])
                antinodes_here.append(frequency)
        return len(antinodes)
