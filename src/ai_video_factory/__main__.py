from __future__ import annotations

import argparse
import json
from pathlib import Path

from .db import connect
from .ingest import ingest_folder
from .memory import add_memory, retrieve


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="AI Video Factory asset and memory CLI")
    commands = root.add_subparsers(dest="command", required=True)
    for name in ("init", "ingest", "remember", "retrieve", "summary"):
        command = commands.add_parser(name)
        command.add_argument("--db", type=Path, required=True)
    commands.choices["ingest"].add_argument("--product", required=True)
    commands.choices["ingest"].add_argument("--source", type=Path, required=True)
    remember = commands.choices["remember"]
    remember.add_argument("--product")
    remember.add_argument("--kind", required=True)
    remember.add_argument("--content", required=True)
    remember.add_argument("--evidence", required=True)
    remember.add_argument("--status", default="candidate")
    search = commands.choices["retrieve"]
    search.add_argument("--product", required=True)
    search.add_argument("--query", required=True)
    search.add_argument("--limit", type=int, default=10)
    commands.choices["summary"].add_argument("--product", required=True)
    return root


def main() -> None:
    args = parser().parse_args()
    connection = connect(args.db)
    if args.command == "init":
        print(json.dumps({"database": str(args.db), "status": "ready"}, ensure_ascii=False))
    elif args.command == "ingest":
        print(json.dumps(ingest_folder(connection, args.product, args.source), ensure_ascii=False))
    elif args.command == "remember":
        memory_id = add_memory(
            connection, args.product, args.kind, args.content, args.evidence, args.status
        )
        print(json.dumps({"memory_id": memory_id, "status": args.status}, ensure_ascii=False))
    elif args.command == "retrieve":
        rows = retrieve(connection, args.product, args.query, args.limit)
        print(json.dumps([dict(row) for row in rows], ensure_ascii=False, indent=2))
    elif args.command == "summary":
        row = connection.execute(
            """
            SELECT
                (SELECT count(*) FROM assets WHERE product_id = ?) AS assets,
                (SELECT count(*) FROM creative_memory WHERE product_id = ?) AS memories,
                (SELECT count(*) FROM creative_memory WHERE product_id = ? AND status = 'approved') AS approved_memories,
                (SELECT count(*) FROM video_runs WHERE product_id = ?) AS video_runs
            """,
            (args.product, args.product, args.product, args.product),
        ).fetchone()
        print(json.dumps(dict(row), ensure_ascii=False))


if __name__ == "__main__":
    main()
