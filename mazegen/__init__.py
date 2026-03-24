"""mazegen – reusable maze generation package.

Public API
----------
MazeGenerator
    The main class for generating and solving mazes.

Example usage::

    from mazegen import MazeGenerator

    gen = MazeGenerator(width=20, height=15, seed=42)
    gen.generate()

    # Wall grid: list[list[int]], one hex bitmask per cell
    grid = gen.grid

    # Shortest path from entry to exit
    path = gen.solve(entry=(0, 0), exit=(19, 14))
    print(path)  # e.g. ['E', 'E', 'S', ...]
"""

from mazegen.generator import MazeGenerator

__all__ = ["MazeGenerator"]
__version__ = "0.1.0"
