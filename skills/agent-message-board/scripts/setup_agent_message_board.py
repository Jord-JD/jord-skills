"""Create the shared message board, preserving any existing posts."""

import argparse
from board_store import run, setup, status


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--status", action="store_true", help="Check configuration without creating anything")
    action.add_argument("--database", help="Absolute database file path explicitly chosen by the user")
    args = parser.parse_args()
    return run(status if args.status else lambda: setup(args.database))


if __name__ == "__main__":
    raise SystemExit(main())
