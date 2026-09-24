"""Find posts by keyword or read a thread and its replies."""

import argparse
from board_store import page_limit, page_offset, positive_integer, read_thread, run, search


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--query", help="Literal search words; matches any word, ranked by relevance")
    target.add_argument("--thread", type=positive_integer, help="Read a thread and a page of replies")
    parser.add_argument("--project", help="Search this project plus global posts; default: all projects")
    parser.add_argument("--limit", type=page_limit, default=10, help="Page size, 1–100 (default: 10)")
    parser.add_argument("--offset", type=page_offset, default=0, help="Pagination offset (default: 0)")
    args = parser.parse_args()
    if args.thread is not None and args.project is not None:
        parser.error("--project applies to keyword searches, not thread reads")
    if args.thread is not None:
        return run(lambda: read_thread(args.thread, limit=args.limit, offset=args.offset))
    return run(lambda: search(args.query, project=args.project, limit=args.limit, offset=args.offset))


if __name__ == "__main__":
    raise SystemExit(main())
