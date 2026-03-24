"""Main entrypoint for the A-Maze-ing project.

Usage:
    python3 a_maze_ing.py config.txt

The program reads a configuration file, validates all mandatory keys,
and (once the maze generator is implemented) produces a maze output file.
"""

import sys
from typing import Any, Dict, Tuple


CONFIG_MANDATORY_KEYS = {
    "WIDTH",
    "HEIGHT",
    "ENTRY",
    "EXIT",
    "OUTPUT_FILE",
    "PERFECT",
}


def parse_config(path: str) -> Dict[str, str]:
    """Parse a KEY=VALUE configuration file.

    Lines starting with '#' are treated as comments and ignored.
    Empty lines are also ignored.

    Args:
        path: Path to the configuration file.

    Returns:
        A dictionary mapping key strings to their raw value strings.

    Raises:
        SystemExit: On any file or parse error.
    """
    config: Dict[str, str] = {}
    try:
        with open(path, "r") as fh:
            for lineno, raw in enumerate(fh, start=1):
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    print(
                        f"Error: line {lineno} in '{path}' is not a valid "
                        f"KEY=VALUE pair: {line!r}",
                        file=sys.stderr,
                    )
                    sys.exit(1)
                key, _, value = line.partition("=")
                config[key.strip()] = value.strip()
    except FileNotFoundError:
        print(
            f"Error: configuration file not found: '{path}'",
            file=sys.stderr,
        )
        sys.exit(1)
    except OSError as exc:
        print(
            f"Error: cannot read configuration file '{path}': {exc}",
            file=sys.stderr,
        )
        sys.exit(1)
    return config


def validate_config(config: Dict[str, str]) -> Dict[str, Any]:
    """Validate mandatory configuration keys and convert them to typed values.

    Mandatory keys:
        WIDTH     -- positive integer (number of cells, horizontal)
        HEIGHT    -- positive integer (number of cells, vertical)
        ENTRY     -- "x,y" integer coordinate pair
        EXIT      -- "x,y" integer coordinate pair
        OUTPUT_FILE -- non-empty string path
        PERFECT   -- boolean ("True" / "False", case-insensitive)

    Optional keys are passed through unchanged in the returned dict.

    Args:
        config: Raw string dictionary produced by :func:`parse_config`.

    Returns:
        A dictionary with validated and type-converted values.

    Raises:
        SystemExit: When any mandatory key is missing or has an invalid value.
    """
    missing = CONFIG_MANDATORY_KEYS - config.keys()
    if missing:
        print(
            f"Error: missing mandatory configuration key(s): "
            f"{', '.join(sorted(missing))}",
            file=sys.stderr,
        )
        sys.exit(1)

    validated: Dict[str, Any] = dict(config)

    # WIDTH
    try:
        width = int(config["WIDTH"])
        if width <= 0:
            raise ValueError("must be positive")
        validated["WIDTH"] = width
    except ValueError as exc:
        print(
            f"Error: WIDTH must be a positive integer, "
            f"got {config['WIDTH']!r}: {exc}",
            file=sys.stderr,
        )
        sys.exit(1)

    # HEIGHT
    try:
        height = int(config["HEIGHT"])
        if height <= 0:
            raise ValueError("must be positive")
        validated["HEIGHT"] = height
    except ValueError as exc:
        print(
            f"Error: HEIGHT must be a positive integer, "
            f"got {config['HEIGHT']!r}: {exc}",
            file=sys.stderr,
        )
        sys.exit(1)

    # ENTRY
    validated["ENTRY"] = _parse_coordinate("ENTRY", config["ENTRY"])

    # EXIT
    validated["EXIT"] = _parse_coordinate("EXIT", config["EXIT"])

    # OUTPUT_FILE
    if not config["OUTPUT_FILE"]:
        print("Error: OUTPUT_FILE must not be empty.", file=sys.stderr)
        sys.exit(1)

    # PERFECT
    perfect_raw = config["PERFECT"].strip().lower()
    if perfect_raw == "true":
        validated["PERFECT"] = True
    elif perfect_raw == "false":
        validated["PERFECT"] = False
    else:
        print(
            f"Error: PERFECT must be 'True' or 'False', "
            f"got {config['PERFECT']!r}",
            file=sys.stderr,
        )
        sys.exit(1)

    return validated


def _parse_coordinate(key: str, raw: str) -> Tuple[int, int]:
    """Parse a "x,y" coordinate string into an (int, int) tuple.

    Args:
        key:  The configuration key name (used in error messages).
        raw:  The raw string value to parse.

    Returns:
        A ``(x, y)`` tuple of integers.

    Raises:
        SystemExit: When *raw* cannot be parsed as two comma-separated
            integers.
    """
    try:
        parts = raw.split(",")
        if len(parts) != 2:
            raise ValueError("expected exactly two comma-separated integers")
        x, y = int(parts[0].strip()), int(parts[1].strip())
        return (x, y)
    except ValueError as exc:
        print(
            f"Error: {key} must be an 'x,y' integer coordinate pair, "
            f"got {raw!r}: {exc}",
            file=sys.stderr,
        )
        sys.exit(1)


def run(config: Dict[str, Any]) -> None:
    """Execute the maze generation pipeline.

    This is a stub.  The full maze generator will be implemented in a later
    iteration once the :mod:`mazegen` package is complete.

    Args:
        config: Validated configuration dictionary produced by
            :func:`validate_config`.
    """
    print(
        f"Configuration loaded: {config['WIDTH']}x{config['HEIGHT']} maze, "
        f"entry={config['ENTRY']}, exit={config['EXIT']}, "
        f"perfect={config['PERFECT']}, output='{config['OUTPUT_FILE']}'"
    )
    print("Maze generation is not yet implemented (stub).")


def main() -> None:
    """Parse CLI arguments, load the configuration, and run the generator."""
    if len(sys.argv) != 2:
        print(
            f"Usage: python3 {sys.argv[0]} <config_file>",
            file=sys.stderr,
        )
        sys.exit(1)

    config_path = sys.argv[1]
    raw_config = parse_config(config_path)
    validated = validate_config(raw_config)
    run(validated)


if __name__ == "__main__":
    main()
