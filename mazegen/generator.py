"""Core maze generator module.

This module provides the :class:`MazeGenerator` class, which implements
a random maze generator using the Recursive Backtracker (depth-first search)
algorithm.

Wall bitmask encoding (per cell):

    Bit 0 (LSB) – North wall closed
    Bit 1       – East  wall closed
    Bit 2       – South wall closed
    Bit 3       – West  wall closed

A bit value of ``1`` means the wall is **closed** (present);
``0`` means the wall is **open** (passage exists).
"""

import random
from collections import deque
from typing import Deque, Dict, List, Optional, Tuple


# Direction constants (bit position in the wall bitmask)
NORTH: int = 0
EAST: int = 1
SOUTH: int = 2
WEST: int = 3

# Opposite direction for each cardinal direction
_OPPOSITE: Dict[int, int] = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST: WEST,
    WEST: EAST,
}

# Row/col delta for each direction
_DELTA: Dict[int, Tuple[int, int]] = {
    NORTH: (-1, 0),
    EAST: (0, 1),
    SOUTH: (1, 0),
    WEST: (0, -1),
}

# Direction letter for output / path encoding
_DIR_LETTER: Dict[int, str] = {
    NORTH: "N",
    EAST: "E",
    SOUTH: "S",
    WEST: "W",
}


class MazeGenerator:
    """Generate and solve a grid-based maze.

    The maze is represented as a 2-D list (``grid[row][col]``) where each
    cell holds an integer bitmask encoding which of its four walls are closed.

    Attributes:
        width:   Number of cells along the horizontal axis.
        height:  Number of cells along the vertical axis.
        perfect: When ``True`` the generator produces a *perfect* maze
                 (exactly one path between any two cells).
        seed:    Optional integer seed for the random-number generator,
                 allowing reproducible results.
        grid:    Wall bitmask grid (populated after :meth:`generate` is
                 called).

    Example::

        gen = MazeGenerator(width=20, height=15, seed=42)
        gen.generate()
        path = gen.solve(entry=(0, 0), exit=(19, 14))
    """

    def __init__(
        self,
        width: int,
        height: int,
        perfect: bool = True,
        seed: Optional[int] = None,
    ) -> None:
        """Initialise the generator with maze dimensions and options.

        Args:
            width:   Number of columns (cells) in the maze.  Must be > 0.
            height:  Number of rows (cells) in the maze.    Must be > 0.
            perfect: Generate a perfect maze when ``True`` (default).
            seed:    Seed for the PRNG.  ``None`` uses a random seed.

        Raises:
            ValueError: When *width* or *height* is not a positive integer.
        """
        if width <= 0 or height <= 0:
            raise ValueError(
                f"width and height must be positive integers, "
                f"got width={width}, height={height}"
            )
        self.width: int = width
        self.height: int = height
        self.perfect: bool = perfect
        self.seed: Optional[int] = seed
        # grid[row][col] – all walls closed until generate() is called
        self.grid: List[List[int]] = [
            [0xF] * width for _ in range(height)
        ]
        self._rng: random.Random = random.Random(seed)
        self._generated: bool = False

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate(self) -> "MazeGenerator":
        """Generate the maze using the Recursive Backtracker algorithm.

        The grid is reset to all-walls-closed before generation begins, so
        calling this method more than once re-generates the maze (using the
        same seed produces the same result).

        Returns:
            ``self`` – to allow method chaining.
        """
        # Reset
        self.grid = [[0xF] * self.width for _ in range(self.height)]
        self._rng = random.Random(self.seed)

        # Carve passages via iterative DFS (avoids Python recursion limit)
        visited: List[List[bool]] = [
            [False] * self.width for _ in range(self.height)
        ]
        stack: List[Tuple[int, int]] = [(0, 0)]
        visited[0][0] = True

        while stack:
            row, col = stack[-1]
            directions = list(_DELTA.keys())
            self._rng.shuffle(directions)
            moved = False
            for direction in directions:
                dr, dc = _DELTA[direction]
                nr, nc = row + dr, col + dc
                if (
                    0 <= nr < self.height
                    and 0 <= nc < self.width
                    and not visited[nr][nc]
                ):
                    # Remove wall between (row, col) and (nr, nc)
                    self._remove_wall(row, col, direction)
                    visited[nr][nc] = True
                    stack.append((nr, nc))
                    moved = True
                    break
            if not moved:
                stack.pop()

        self._generated = True
        return self

    def solve(
        self,
        entry: Tuple[int, int],
        exit: Tuple[int, int],
    ) -> List[str]:
        """Find the shortest path from *entry* to *exit* using BFS.

        Args:
            entry: ``(x, y)`` coordinates of the entrance cell
                   where ``x`` is the column and ``y`` is the row.
            exit:  ``(x, y)`` coordinates of the exit cell.

        Returns:
            A list of direction characters (``'N'``, ``'E'``, ``'S'``, ``'W'``)
            representing the shortest path.  Returns an empty list when *entry*
            equals *exit*.

        Raises:
            ValueError:  When the maze has not been generated yet, or when
                         *entry* / *exit* coordinates are out of bounds.
            RuntimeError: When no path exists between *entry* and *exit*.
        """
        if not self._generated:
            raise ValueError(
                "Maze has not been generated yet; call generate() first."
            )

        ex, ey = entry
        tx, ty = exit
        self._check_bounds("entry", ex, ey)
        self._check_bounds("exit", tx, ty)

        if entry == exit:
            return []

        # BFS
        # Coordinates are (col, row) = (x, y) convention
        start = (ey, ex)   # (row, col)
        target = (ty, tx)  # (row, col)

        queue: Deque[Tuple[Tuple[int, int], List[str]]] = deque()
        queue.append((start, []))
        visited_bfs: List[List[bool]] = [
            [False] * self.width for _ in range(self.height)
        ]
        visited_bfs[start[0]][start[1]] = True

        while queue:
            (row, col), path = queue.popleft()
            for direction in _DELTA:
                if self._wall_open(row, col, direction):
                    dr, dc = _DELTA[direction]
                    nr, nc = row + dr, col + dc
                    if not visited_bfs[nr][nc]:
                        new_path = path + [_DIR_LETTER[direction]]
                        if (nr, nc) == target:
                            return new_path
                        visited_bfs[nr][nc] = True
                        queue.append(((nr, nc), new_path))

        raise RuntimeError(
            f"No path found from {entry} to {exit} in the current maze."
        )

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _remove_wall(self, row: int, col: int, direction: int) -> None:
        """Remove the wall between a cell and its neighbour in *direction*.

        Both sides of the shared wall are updated to keep the grid coherent.

        Args:
            row:       Row index of the source cell.
            col:       Column index of the source cell.
            direction: One of :data:`NORTH`, :data:`EAST`,
                       :data:`SOUTH`, :data:`WEST`.
        """
        dr, dc = _DELTA[direction]
        # Clear the wall bit in the source cell
        self.grid[row][col] &= ~(1 << direction)
        # Clear the opposing wall bit in the neighbour
        nr, nc = row + dr, col + dc
        self.grid[nr][nc] &= ~(1 << _OPPOSITE[direction])

    def _wall_open(self, row: int, col: int, direction: int) -> bool:
        """Return ``True`` if the wall in *direction* from (row, col) is open.

        A wall is *open* when the corresponding bit in the cell's bitmask is 0
        *and* the neighbour exists inside the grid bounds.

        Args:
            row:       Row index of the cell.
            col:       Column index of the cell.
            direction: One of :data:`NORTH`, :data:`EAST`,
                       :data:`SOUTH`, :data:`WEST`.

        Returns:
            ``True`` when a passage exists; ``False`` otherwise.
        """
        dr, dc = _DELTA[direction]
        nr, nc = row + dr, col + dc
        if not (0 <= nr < self.height and 0 <= nc < self.width):
            return False
        return (self.grid[row][col] & (1 << direction)) == 0

    def _check_bounds(self, name: str, x: int, y: int) -> None:
        """Raise :exc:`ValueError` if ``(x, y)`` is outside the maze grid.

        Args:
            name: Label used in the error message (e.g. ``'entry'``).
            x:    Column index (0-based).
            y:    Row index (0-based).

        Raises:
            ValueError: When the coordinate is out of bounds.
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise ValueError(
                f"{name} coordinate ({x}, {y}) is out of bounds for a "
                f"{self.width}x{self.height} maze."
            )
