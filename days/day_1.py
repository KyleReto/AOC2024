"""Day 1 of Advent of Code 2024"""
from utils.abstract_day import Day

class DayCode(Day):
    """
    Solutions to Day 1 of AOC, which you can find here: https://adventofcode.com/2024/day/1
    """
    @classmethod
    def parse_input(cls, in_str: str) -> tuple[list[int]]:
        """
        Parse the given input into two lists

        Args:
            in_str: The input string, as two columnar lists separated by three spaces.

        Returns:
            The lists as a tuple of list objects
        """
        out_lists = ([], [])
        for line in in_str.strip().split("\n"):
            entries = line.split("   ")
            for idx, out_list in enumerate(out_lists):
                out_list.append(int(entries[idx]))
        return out_lists

    @classmethod
    def part_1(cls, in_str: str) -> str:
        """
        We're given two unordered lists of "location IDs" (two columns of input,
        where each is a list, split by three spaces), and we have to iteratively
        find the differences between each smallest/second-smallest/third-smallest/etc
        entry in the lists, then return their sums.

        My approach here is to simply sort the lists, iterate over both,
        and total up their differences. It's not necessarily optimal, but it
        is simple, which I prefer over optimality.

        Args:
            in_str: The input string from AOC

        Returns:
            The sum of differences between location IDs
        """
        list_a, list_b = cls.parse_input(in_str)
        list_a = sorted(list_a)
        list_b = sorted(list_b)
        total = 0
        for idx, _ in enumerate(list_a):
            total += abs(list_a[idx] - list_b[idx])
        return str(total)

    @classmethod
    def part_2(cls, in_str: str) -> str:
        """
        The input is the same, but the problem changed. Now, we have to
        find the "similarity" between the two lists, which is defined as
        the sum of (each entry in list a * the number of times that value
        appears in list b). For example, if list a is [3, 3] and list b is [3, 3, 4],
        the similarity score would be (3 * 2) + (3 * 2) = 12.

        My approach here is straightforward. I first iterate over list B to create a
        map of each value to its frequency, then I iterate over list A to get the similarity
        scores by checking said map.

        Args:
            in_str: The input string from AOC

        Returns:
            The total similarity score
        """
        list_a, list_b = cls.parse_input(in_str)
        freq_dict = {}

        for entry in list_b:
            frequency = freq_dict.get(entry, 0)
            freq_dict[entry] = frequency + 1

        similarity = 0
        for entry in list_a:
            frequency = freq_dict.get(entry, 0)
            similarity += entry * frequency

        return str(similarity)
