"""Day 5 of Advent of Code 2024"""
from functools import cmp_to_key
from utils.abstract_day import Day

class DayCode(Day):
    """
    Solutions to Day 5 of AOC, which you can find here: https://adventofcode.com/2024/day/5
    """

    @classmethod
    def parse_input(cls, in_str: str) -> tuple[dict[int, set[int]], list[list[int]]]:
        """
        Parse the input string from AoC, which is a list of sorting rules followed by
        the data to process.

        Args:
            in_str: The input data, which is a pair of Rules and Data, which are separated
             by two '\\n' characters.  
             Rules are defined as a list of integer pairs (A,B) separated by '\\n' characters,
             where each pair is separated with a '|' character.  
             Data is defined as a list of lists of integers, separated by '\\n' characters,
             where each entry is separated from others by a ',' character

        Returns:
            A tuple (Rules, Data)  
                Rules - A dictionary mapping each A character to all of its B characters.  
                Data - A list of all input lists of digits.
        """
        rules = {}
        data = []
        rules_str, data_str = in_str.split("\n\n")

        for rule_str in rules_str.splitlines():
            a, b = rule_str.split("|")
            successors = rules.setdefault(int(a), set())
            successors.add(int(b))

        for entry in data_str.splitlines():
            data.append([int(page) for page in entry.split(",")])
        return rules, data

    @classmethod
    def make_update_valid(cls, rules: dict[int, set[int]], update: list[int]) -> list[int]:
        """
        For a given update, sort it so that it becomes valid

        Args:
            rules: The set of rules from the input
            update: The list of pages to re-sort

        Returns:
            The sorted update
        """
        def compare_pages(x, y):
            if x in rules and y in rules[x]:
                return -1
            if y in rules and x in rules[y]:
                return 1
            return 0
        return sorted(update, key=cmp_to_key(compare_pages))

    @classmethod
    def part_1(cls, in_str: str) -> str:
        """
        Today's challenge is to use a custom set of sorting rules to verify that a given
        set of input numbers (a list of "updates", where each int is a "page number")
        is sorted. The rules are each a pair of integers, [A,B], indicating that number
        A must precede number B if both appear in the given input. If a given input
        list does not violate any rule, we should record the middle number.
        To facilitate this, each input list always contains at least 3 digits, and the
        count of numbers in a list will always be odd. Based on the problem text, I'm
        anticipating that part 2 will involve sorting these lists by the custom rules.
        I've noticed that for at least the sample data, the rules are transitive -- if a
        rule says A|B and another rule says B|C, no rule will ever say C|A.

        I initially solved this part with a naive approach which iteratively checked every
        page number to ensure that every number following it was not disallowed by the rules.
        However, after solving part 2, I came back and reused the custom sort function here
        to solve it more efficiently. See the writeup for that section for details. I could
        have designed a function to return early as soon as it became clear that the entry
        was not sorted, but I didn't think that was worth the rewrite, especially since
        there's a pretty good chance that they would compile to the same result anyways.

        Args:
            in_str: The input string, which is a list of sorting rules followed by the
            data to process.

        Returns:
            The total of all middle values of the lists which are already sorted
        """
        middle_sum = 0
        rules, data = cls.parse_input(in_str)
        for entry in data:
            if entry != cls.make_update_valid(rules, entry):
                continue
            middle_sum += entry[len(entry) // 2]
        return middle_sum

    @classmethod
    def part_2(cls, in_str: str) -> str:
        """
        As expected, part 2 is to sort the updates according to the provided rules. The instructions
        are to sum the middles values of only the updates which were invalid before, but only after
        sorting them to make them valid.

        I initially solved this question with a naive solution, since this type of problem could
        have weird edge cases to handle, such as contradictory rules or unsortable lists. I was
        specifically anticipating a case where a rule two rules could come together to imply a
        third rule, as often happens in similar problems. However, upon further review of the
        problem, I realized that this doesn't happen in the input, and probably isn't possible given
        the problem description. This allowed me to use a much simpler approach, which is just a
        custom comparator function which simply checks the rules to define whether an element must
        go in front of, behind, or to either side of an arbitrary other element. Doing this means we
        can just call the built in sort function on the list to sort it. I would have liked to use a
        key function instead of a comparator, as is recommended for modern python, but I wasn't able
        to think of a way to define this relationship as a key without overcomplicating it.

        Args:
            in_str: The input string, which is a list of sorting rules followed by the
            data to process.

        Returns:
            The total of all of the middle values of the previously invalid entries, after sorting.
        """
        middle_sum = 0
        rules, data = cls.parse_input(in_str)
        for entry in data:
            sorted_entry = cls.make_update_valid(rules, entry)
            if entry != sorted_entry:
                middle_sum += sorted_entry[len(entry) // 2]
        return middle_sum
