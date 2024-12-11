"""
A module for a grid data structure and related functions
"""

from collections import abc

class Grid(abc.MutableMapping):
    """
    A 2D grid emulating the behavior of a 2D list, but with support for sparse and unbounded grids
    """
    def __init__(self, default: any = None,
                 bounds: None | tuple[int, int] | tuple[int, int, int, int] = None):
        """
        Create an empty grid.

        Args:
            default: The default value for each element. Defaults to None.
            bounds: The bounds of the grid, expressed as one of the following&colon;
                None: The grid is unbounded.
                (height, width): The top-left corner of the grid is at (0,0), and the grid
                is {height} elements tall and {width} elements wide.
                (top, left, bottom, right): The top-left corner of the grid is at {top, left}
                , and the grid ends at coordinate {bottom, right}, exclusive.
        """
        if not bounds:
            self._bounds = None
        elif len(bounds) == 2:
            self._bounds = (0, 0, bounds[0], bounds[1])
        else:
            self._bounds = bounds
        self._default = default
        self._data: dict[tuple[int, int], any] = {}

    def __str__(self, col_sep = "\t", row_sep = "\n") -> str:
        bounds: tuple[int, int, int, int] = self._get_current_bounds()
        row_strs = []
        for i in range(bounds[0], bounds[2]):
            items = []
            for j in range(bounds[1], bounds[3]):
                items.append(str(self.__getitem__((i, j))))
            row_strs.append(col_sep.join(items))
        return row_sep.join(row_strs)

    def __contains__(self, x: "Coordinate | tuple[int, int]"):
        # If the grid has no bounds, then it contains an entry for every index.
        if not self._bounds:
            return True
        return (self._bounds[0] <= x[0] < self._bounds[2] and
                self._bounds[1] <= x[1] < self._bounds[3])

    def __len__(self):
        bounds = self._get_current_bounds()
        return (bounds[2] - bounds[0]) * (bounds[3] - bounds[1])

    def __iter__(self):
        bounds: tuple[int, int, int, int] = self._get_current_bounds()
        for i in range(bounds[0], bounds[2]):
            for j in range(bounds[1], bounds[3]):
                yield self.__getitem__((i, j))

    def __getitem__(self, position: "Coordinate | tuple[int, int]"):
        if position not in self:
            raise IndexError(f"index {position} is out of range ("
                             f"[{self._bounds[0]}] - [{self._bounds[2]}], "
                             f"[{self._bounds[1]}] - [{self._bounds[3]}])")
        return self._data.get((position[0], position[1]), self._default)

    def __setitem__(self, position: "Coordinate | tuple[int, int]", value: any) -> None:
        if position not in self:
            raise IndexError(f"index {position} is out of range ("
                             f"[{self._bounds[0]}] - [{self._bounds[2]}], "
                             f"[{self._bounds[1]}] - [{self._bounds[3]}])")
        return self._data.__setitem__((position[0], position[1]), value)

    def __delitem__(self, position: "Coordinate | tuple[int, int]"):
        if position not in self:
            raise IndexError(f"index {position} is out of range ("
                             f"[{self._bounds[0]}] - [{self._bounds[2]}], "
                             f"[{self._bounds[1]}] - [{self._bounds[3]}])")
        # Deleting an item that's in bounds should *not* raise an error, even
        # if that item wasn't actually being stored anywhere.
        if position in self._data:
            self._data.__delitem__((position[0], position[1]))

    def _get_current_bounds(self) -> tuple[int, int, int, int]:
        """
        Get an estimate of the bounding box for this grid, even if the user didn't specify one.

        Returns:
            The user-specified bounding box, if one exists.
            If not, returns the smallest rectangular bounding box possible for this grid
        """
        if self._bounds:
            return self._bounds
        if not self._data:
            return (0, 0, 0, 0)
        bounds = [None, None, None, None]
        bounds[0], _ = min(self._data.keys(), key=lambda item:item[0])
        bounds[2], _ = max(self._data.keys(), key=lambda item:item[0])
        _, bounds[1] = min(self._data.keys(), key=lambda item:item[1])
        _, bounds[3] = max(self._data.keys(), key=lambda item:item[1])
        bounds[2] += 1
        bounds[3] += 1
        return tuple(bounds)

    def items(self):
        bounds: tuple[int, int, int, int] = self._get_current_bounds()
        for i in range(bounds[0], bounds[2]):
            for j in range(bounds[1], bounds[3]):
                yield (Coordinate((i, j)), self[(i, j)])

    def non_default_items(self):
        """
        Returns an iterable object of all elements that have been set.
        Note that this *will* include elements that have been manually set to the same
        value as the default. To unset an element completely, use del().

        Yields:
            The key/value pair for each non-default item
        """
        for key, value in self._data.items():
            yield (Coordinate(key), value)

class Coordinate(tuple):
    """
    A coordinate on a 2D grid

    Args:
        tuple: The tuple to source the coordinate from, formatted as (row, col)
    """
    def __init__(self, data):
        self.data = data
        self.row = data[0]
        self.col = data[1]

    def __getitem__(self, index):
        return self.data[index]

    def __add__(self, other: 'Coordinate | tuple[int, int]'):
        return Coordinate((self[0] + other[0], self[1] + other[1]))

    def __sub__(self, other: 'Coordinate | tuple[int, int]'):
        return Coordinate((self[0] - other[0], self[1] - other[1]))

    def __str__(self):
        return str(self.data)
