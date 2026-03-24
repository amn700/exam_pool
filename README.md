*This project has been created as part of the 42 curriculum by amn700.*

# A-Maze-ing

A Python maze generator built as part of the 42 school curriculum.
The program reads a configuration file, generates a random (optionally perfect) maze,
writes it to an output file using a hexadecimal wall representation, and renders it
visually in the terminal.

---

## Table of Contents

1. [Description](#description)
2. [Requirements](#requirements)
3. [Installation & Setup](#installation--setup)
4. [Usage](#usage)
5. [Configuration File Format](#configuration-file-format)
6. [Output File Format](#output-file-format)
7. [Maze Generation Algorithm](#maze-generation-algorithm)
8. [Visual Representation](#visual-representation)
9. [Reusable `mazegen` Package](#reusable-mazegen-package)
10. [Building the Package](#building-the-package)
11. [Linting & Type Checking](#linting--type-checking)
12. [Project Structure](#project-structure)
13. [Team / Project Management](#team--project-management)
14. [Resources & AI Usage](#resources--ai-usage)

---

## Description

A-Maze-ing generates random mazes from a simple text configuration file.
Key features (planned / in progress):

- Configurable width, height, entry/exit coordinates, and random seed
- Optional *perfect* maze mode (exactly one path between any two cells)
- Hexadecimal wall-encoded output file
- BFS-based shortest-path solution embedded in the output
- ASCII terminal rendering with interactive controls
- A reusable `mazegen` Python package installable via `pip`

---

## Requirements

- Python 3.10 or later
- `pip` (for dependency installation)
- `build` (for building the `mazegen` wheel)
- `flake8` and `mypy` (for linting / type checking)

---

## Installation & Setup

```bash
# 1. (Recommended) create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install project dependencies
make install
```

---

## Usage

```bash
# Run with the default config
make run

# Run with a custom config file
python3 a_maze_ing.py my_config.txt

# Run in debug mode (pdb)
make debug

# Clean caches
make clean
```

---

## Configuration File Format

The configuration file uses a simple `KEY=VALUE` format (one pair per line).
Lines starting with `#` are comments and are ignored.

### Mandatory keys

| Key           | Type            | Description                              | Example         |
|---------------|-----------------|------------------------------------------|-----------------|
| `WIDTH`       | positive int    | Number of cells horizontally             | `WIDTH=20`      |
| `HEIGHT`      | positive int    | Number of cells vertically               | `HEIGHT=15`     |
| `ENTRY`       | `x,y` int pair  | Entrance cell coordinates (0-indexed)    | `ENTRY=0,0`     |
| `EXIT`        | `x,y` int pair  | Exit cell coordinates (0-indexed)        | `EXIT=19,14`    |
| `OUTPUT_FILE` | path string     | Path to write the maze output file       | `OUTPUT_FILE=maze.txt` |
| `PERFECT`     | bool (`True`/`False`) | Generate a perfect maze (single path) | `PERFECT=True` |

### Optional keys

| Key    | Type | Description                        | Example   |
|--------|------|------------------------------------|-----------|
| `SEED` | int  | Random seed for reproducibility    | `SEED=42` |

### Example `config.txt`

```
# A-Maze-ing default configuration
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

---

## Output File Format

Each cell is encoded as a single hexadecimal digit whose bits indicate closed walls:

| Bit | Direction |
|-----|-----------|
| 0 (LSB) | North |
| 1       | East  |
| 2       | South |
| 3       | West  |

A `1` bit means the wall is **closed**; `0` means **open**.

- Cells are written row by row, one row per line.
- After an empty line, three additional lines follow:
  1. Entry coordinates
  2. Exit coordinates
  3. Shortest path (sequence of `N`, `E`, `S`, `W` letters)

---

## Maze Generation Algorithm

**Planned algorithm: Recursive Backtracker (Depth-First Search)**

### Why this algorithm?

- Produces *perfect* mazes (exactly one path between any two cells) naturally,
  satisfying the `PERFECT=True` requirement without extra post-processing.
- Simple to implement and understand.
- Produces mazes with long, winding corridors—visually interesting and well-suited
  for pathfinding demonstrations.
- Trivially seeded via Python's `random` module for full reproducibility.

### Brief description

1. Start at the entry cell; mark it visited.
2. Choose a random unvisited neighbour; remove the wall between them.
3. Recurse into that neighbour.
4. Backtrack when no unvisited neighbours remain.
5. Repeat until all cells are visited.

For non-perfect mazes (`PERFECT=False`), a post-processing step will randomly
remove additional walls while respecting the no-large-open-area constraint
(corridors may not exceed 2 cells wide) and the "42" pattern requirement.

---

## Visual Representation

The maze will be rendered in the terminal using ASCII box-drawing characters.
Planned interactive controls:

| Key / Action         | Effect                              |
|----------------------|-------------------------------------|
| `r`                  | Re-generate a new maze              |
| `p`                  | Show / hide the shortest path       |
| `c`                  | Cycle through wall colour themes    |
| `q` / `Ctrl-C`       | Quit                                |

---

## Reusable `mazegen` Package

The maze generation logic lives in the standalone `mazegen` package so it can be
installed and reused in other projects.

### Installation from the pre-built wheel

```bash
pip install mazegen-0.1.0-py3-none-any.whl
```

### API overview

```python
from mazegen import MazeGenerator

# Instantiate with size and optional seed
gen = MazeGenerator(width=20, height=15, seed=42)

# Generate the maze (returns self for chaining)
gen.generate()

# Access the wall grid: list of lists of int (hex bitmask per cell)
grid = gen.grid         # grid[row][col] -> int 0-15

# Access the solution path
path = gen.solve(entry=(0, 0), exit=(19, 14))   # list of 'N'|'E'|'S'|'W'
```

### Custom parameters

```python
# Non-perfect maze with specific seed
gen = MazeGenerator(width=30, height=20, perfect=False, seed=7)
gen.generate()
```

### Accessing the structure

- `gen.grid` — 2-D list `[row][col]` of integers (wall bitmask, same encoding as
  the output file).
- `gen.solve(entry, exit)` — returns a list of direction characters representing
  the shortest path (BFS).

---

## Building the Package

```bash
# Install the build tool (once)
pip install build

# Build the wheel and sdist into dist/
python -m build

# The wheel will be at dist/mazegen-0.1.0-py3-none-any.whl
# A copy is also committed to the repository root as mazegen-0.1.0-py3-none-any.whl
```

---

## Linting & Type Checking

```bash
# Standard lint (mandatory flags)
make lint

# Strict lint (optional but recommended)
make lint-strict
```

The `lint` target runs:

```bash
flake8 .
mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports \
       --disallow-untyped-defs --check-untyped-defs
```

---

## Project Structure

```
exam_pool/
├── a_maze_ing.py          # Main entrypoint
├── config.txt             # Default configuration file
├── Makefile               # Automation rules
├── pyproject.toml         # Package build config (mazegen)
├── README.md              # This file
├── .gitignore             # Python artifact exclusions
├── mazegen-0.1.0-py3-none-any.whl  # Pre-built wheel (committed)
└── mazegen/               # Reusable maze generation package
    ├── __init__.py
    └── generator.py
```

---

## Team / Project Management

This is a **solo** project.

| Role                   | Responsibility                         |
|------------------------|----------------------------------------|
| Developer              | All implementation, testing, docs      |
| Architect              | Algorithm design, package API design   |
| Reviewer               | Self-review, flake8/mypy compliance    |

Work is tracked via GitHub issues and pull requests on the
[amn700/exam_pool](https://github.com/amn700/exam_pool) repository.

---

## Resources & AI Usage

### References

- [Python `random` module](https://docs.python.org/3/library/random.html) — seeded RNG
- [Maze generation algorithms (Wikipedia)](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Recursive backtracker explained](https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking)
- [Python Packaging Guide (PEP 517/518)](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [mypy documentation](https://mypy.readthedocs.io/en/stable/)
- [flake8 documentation](https://flake8.pycqa.org/)

### AI Usage

GitHub Copilot (powered by large language models) was used to:

- Draft the initial project skeleton and boilerplate (Makefile, pyproject.toml,
  .gitignore).
- Suggest docstring and type-hint formatting to comply with PEP 257 / mypy.
- Provide guidance on the recursive backtracker algorithm and its Python idioms.

All AI-generated code was reviewed, tested, and adapted manually to meet the
project requirements.
