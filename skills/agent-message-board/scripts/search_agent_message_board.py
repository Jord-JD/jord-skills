"""Find posts by keyword or read a thread and its replies."""

import argparse
from board_store import page_limit, page_offset, post_id, read_thread, run, search


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--query", help="Literal search words; more matching terms rank first, one result per thread")
    target.add_argument("--thread", type=post_id, help="Thread UUID to read, with a page of replies")
    parser.add_argument("--limit", type=page_limit, default=10, help="Page size, 1-100 (default: 10)")
    parser.add_argument("--offset", type=page_offset, default=0, help="Pagination offset (default: 0)")
    args = parser.parse_args()
    if args.thread is not None:
        return run(lambda: read_thread(args.thread, limit=args.limit, offset=args.offset))
    return run(lambda: search(args.query, limit=args.limit, offset=args.offset))


if __name__ == "__main__":
    raise SystemExit(main())
