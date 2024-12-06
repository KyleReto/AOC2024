"""Day 6 of Advent of Code 2024"""
from enum import Enum
from utils.abstract_day import Day

class DayCode(Day):
    """
    Solutions to Day 6 of AOC, which you can find here: https://adventofcode.com/2024/day/6
    """

    class Direction(Enum):
        """
        Enumerate directions of traversal
        """
        UP = (-1, 0)
        RIGHT = (0, 1)
        DOWN = (1, 0)
        LEFT = (0, -1)

        TURN_RIGHT = {UP: RIGHT, RIGHT: DOWN, DOWN: LEFT, LEFT: UP}

    @classmethod
    def part_1(cls, in_str: str) -> str:
        """
        Today's challenge is to analyze a "map" of a building, which is a 2D array containing
        three types of characters: '.', which represent empty spaces; '#', which represent
        walls, and one '^', which represents a guard (facing north). The guard moves following
        a simple algorithm: She always moves forward if able (not blocked),
        and if not, she turns 90 degrees to her right and tries to move forward again.
        The task is to simulate the guard's movement through the map and count the number of
        spaces she visits in her route. If she moves out of bounds, the route is over.

        I designed my solution anticipating that we'd need to check for loops as well, which
        I'd love to say was foresight but was actually just a misreading of the problem statement.
        As a result, the code is a bit more dense than it had to be. However, I didn't think it
        was worth removing since checking for loops does make some sense in this context, just not
        for this specific problem. At each timestep we first record the guard's current position
        and facing direction to the spaces_visited dict, then we either move the guard forward or
        have her turn depending on what's in front of her. If she ever enters the same space *and*
        is moving in the same direction as any previous iteration, we're done counting. This same
        effect could be achieved by only recording the first space and facing direction, but this
        method allows us to remember the specifics of each prior space visited, if necessary.

        Args:
            in_str: The input string, representing a map.

        Returns:
            The number of distinct spaces visited
        """
        # Map each space that's been visited to the direction(s) the guard was traveling in
            # when she visited that space.
        spaces_visited: dict[tuple[int, int], list[cls.Direction]] = {}
        grid = in_str.splitlines()
        curr_direction = cls.Direction.UP.value
        guard_raw_pos = in_str.find("^")
        # Assumption: The grid is always rectangular
        guard_pos = (guard_raw_pos // (len(grid[0]) + 1), guard_raw_pos % (len(grid[0]) + 1))

        while (guard_pos not in spaces_visited or
               curr_direction not in spaces_visited[guard_pos]):
            next_pos = (guard_pos[0] + curr_direction[0],
                        guard_pos[1] + curr_direction[1])
            spaces_visited.setdefault(guard_pos, [])
            spaces_visited[guard_pos].append(curr_direction)
            # If we leave the map, stop tracking
            if next_pos[0] not in range(0, len(grid)) or next_pos[1] not in range(0, len(grid[0])):
                break
            # If we hit a wall, turn
            if grid[next_pos[0]][next_pos[1]] == '#':
                curr_direction = cls.Direction.TURN_RIGHT.value[curr_direction]
                continue
            # Otherwise, move forward
            guard_pos = next_pos
        return len(spaces_visited)

    @classmethod
    def part_2(cls, in_str: str) -> str:
        """
        The twist for part 2 is that we now have to force the guard into a loop, which luckily my
        part 1 code can already detect. We do this by adding any single new obstruction ('#') to
        the grid. We need to count all possible additions that create a loop.

        My solution is rather slow. I'd like to optimize it, but I don't really have time today.
        It's fast enough, it only takes about 10 seconds to run, but I'm sure this solution could
        be instant with the right optimizations. All it does is iteratively run the code from part
        1 by inserting a '#' character somewhere in the grid. It does skip evaluating positions
        where a '#' character wouldn't be valid, e.g. where one already exists, but that doesn't
        meaningfully change the efficiency of the algorithm.

        Args:
            in_str: The input string, representing a map.

        Returns:
            The number of distinct spaces visited
        """
        loop_count = 0
        for char_idx, char in enumerate(in_str):
            print (f"Calculating: {char_idx/len(in_str):.0%}", end="\r")
            # If the space isn't empty, we can't put an obstruction there
            if char != '.':
                continue
            in_str_with_obstruction = in_str[:char_idx] + '#' + in_str[char_idx + 1:]
            # Map each space that's been visited to the direction(s) the guard was traveling in
                # when she visited that space.
            spaces_visited: dict[tuple[int, int], list[cls.Direction]] = {}
            grid = in_str_with_obstruction.splitlines()
            curr_direction = cls.Direction.UP.value
            guard_raw_pos = in_str_with_obstruction.find("^")
            # Assumption: The grid is always rectangular
            guard_pos = (guard_raw_pos // (len(grid[0]) + 1), guard_raw_pos % (len(grid[0]) + 1))

            while (guard_pos not in spaces_visited or
                curr_direction not in spaces_visited[guard_pos]):
                next_pos = (guard_pos[0] + curr_direction[0],
                            guard_pos[1] + curr_direction[1])
                spaces_visited.setdefault(guard_pos, [])
                spaces_visited[guard_pos].append(curr_direction)
                # If we leave the map, stop tracking
                if (next_pos[0] not in range(0, len(grid)) or
                    next_pos[1] not in range(0, len(grid[0]))):
                    break
                # If we hit a wall, turn
                if grid[next_pos[0]][next_pos[1]] == '#':
                    curr_direction = cls.Direction.TURN_RIGHT.value[curr_direction]
                    continue
                # Otherwise, move forward
                guard_pos = next_pos
            # If we exit the loop without a break, it's because a loop was detected
            else:
                loop_count += 1
        return loop_count
