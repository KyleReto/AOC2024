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
    def is_page_valid(cls, rules: dict[int, set[int]], update: list[int],
                      page_idx: int) -> bool:
        """
        Check whether all pages following this one follow all rules

        Args:
            rules: The set of rules from the input
            update: The list of pages to check
            page_idx: The index of the page in the update to check

        Returns:
            True if this page follows all rules w.r.t its successors, False otherwise.
        """

        for following_page in update[page_idx + 1:]:
            if following_page in rules and update[page_idx] in rules[following_page]:
                return False
        return True

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

        For my approach, I first tried using that transitive property. In the sample data,
        this is true, but also, if rules A|B and B|C exist, then rule A|C will exist.
        Using that, I tried creating a "super-rule", a list like [A, B, C] which defines the
        entire chain of rules, such that all valid lists could be constructed by removing
        one or more elements of the super-rule. Unfortunately, this doesn't hold true for the
        full input, so I resorted to individually checking each page number in an update to
        see if of the pages that follow it violate any rule. I considered doing this in reverse
        order, but I found that this didn't really remove any complexity, so I just used the
        naive approach.

        Args:
            in_str: The input string, which is a list of sorting rules followed by the
            data to process.

        Returns:
            The total of all middle values of the lists which are already sorted
        """
        middle_sum = 0
        rules, data = cls.parse_input(in_str)
        for entry in data:
            for page_idx, _ in enumerate(entry):
                if not cls.is_page_valid(rules, entry, page_idx):
                    break
            else:
                middle_sum += entry[len(entry) // 2]
        return middle_sum

    @classmethod
    def make_update_valid(cls, rules: dict[int, set[int]], update: list[int]) -> list[int]:
        """
        For a given invalid update, sort it so that it becomes valid

        Args:
            rules: The set of rules from the input
            update: The list of pages to re-sort

        Returns:
            The sorted update
        """
        sorted(update, key=cmp_to_key(
            lambda x,y : x
        ))

        sorted_update = []
        for page_to_add in update:
            sorted_update.insert(0, page_to_add)
            for idx, _ in enumerate(sorted_update):
                if cls.is_page_valid(rules, sorted_update, idx):
                    break
                temp = sorted_update[idx]
                sorted_update[idx] = sorted_update[idx+1]
                sorted_update[idx+1] = temp
        return sorted_update

    @classmethod
    def part_2(cls, in_str: str) -> str:
        """
        As expected, part 2 is to sort the updates according to the provided rules. The instructions
        are to sum the middles values of only the updates which were invalid before, but only after
        sorting them to make them valid.

        My approach here is to use a variation on the bubble sort algorithm, creating a new update
        from scratch and placing the old update items in it one at a time. Each time a new element
        is placed at the front of the new update list, we check if that page is valid w.r.t all
        elements that follow it. If not, we swap it with the next element, such that it bubbles up
        to its correct position. Unlike most sorting operations, 

        Args:
            in_str: The input string, which is a list of sorting rules followed by the
            data to process.

        Returns:
            The total of all of the middle values of the previously invalid entries, after sorting.
        """
        middle_sum = 0
        rules, data = cls.parse_input(in_str)
        for entry in data:
            for page_idx, _ in enumerate(entry):
                if not cls.is_page_valid(rules, entry, page_idx):
                    sorted_entry = cls.make_update_valid(rules, entry)
                    middle_sum += sorted_entry[len(entry) // 2]
                    break
        return middle_sum
