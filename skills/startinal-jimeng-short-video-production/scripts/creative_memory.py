#!/usr/bin/env python3
"""Maintain an explicit, local-only production-memory ledger.

The ledger stores confirmed user preferences and evidence-backed production
observations. It never inspects, uploads, or copies media, credentials, or
personal/payment data.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


SCHEMA_VERSION = 1
PREFERENCE_STATUSES = {"candidate", "confirmed", "retired"}
OBSERVATION_OUTCOMES = {"accepted", "rejected", "untested"}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def empty_memory() -> dict[str, object]:
    return {
        "schema_version": SCHEMA_VERSION,
        "created_utc": now(),
        "privacy_note": "Store no credentials, customer data, payment data, raw personal data, or unverified product claims.",
        "preferences": [],
        "benchmarks": [],
        "observations": [],
    }


def load(path: Path) -> dict[str, object]:
    if not path.exists():
        return empty_memory()
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("Unsupported creative-memory schema version")
    for key in ("preferences", "benchmarks", "observations"):
        if not isinstance(payload.get(key), list):
            raise ValueError(f"creative-memory field {key} must be a list")
    return payload


def save(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def add_preference(args: argparse.Namespace) -> None:
    if args.status not in PREFERENCE_STATUSES:
        raise ValueError("Invalid preference status")
    payload = load(args.memory)
    entry = {
        "id": f"pref-{len(payload['preferences']) + 1:03d}",
        "scope": args.scope,
        "status": args.status,
        "key": args.key,
        "value": args.value,
        "evidence": args.evidence,
        "updated_utc": now(),
    }
    payload["preferences"].append(entry)
    save(args.memory, payload)
    print(f"Recorded preference {entry['id']} ({args.status}): {args.key}")


def add_benchmark(args: argparse.Namespace) -> None:
    payload = load(args.memory)
    entry = {
        "id": f"benchmark-{len(payload['benchmarks']) + 1:03d}",
        "scope": args.scope,
        "status": "confirmed",
        "name": args.name,
        "path": args.path,
        "criteria": args.criteria,
        "evidence": args.evidence,
        "updated_utc": now(),
    }
    payload["benchmarks"].append(entry)
    save(args.memory, payload)
    print(f"Recorded benchmark {entry['id']}: {args.name}")


def add_observation(args: argparse.Namespace) -> None:
    if args.outcome not in OBSERVATION_OUTCOMES:
        raise ValueError("Invalid observation outcome")
    payload = load(args.memory)
    entry = {
        "id": f"obs-{len(payload['observations']) + 1:03d}",
        "scope": args.scope,
        "kind": args.kind,
        "outcome": args.outcome,
        "summary": args.summary,
        "cause_hypothesis": args.cause_hypothesis,
        "correction": args.correction,
        "evidence": args.evidence,
        "updated_utc": now(),
    }
    payload["observations"].append(entry)
    save(args.memory, payload)
    print(f"Recorded observation {entry['id']} ({args.outcome}): {args.kind}")


def show(args: argparse.Namespace) -> None:
    payload = load(args.memory)
    if args.confirmed_only:
        payload["preferences"] = [item for item in payload["preferences"] if item.get("status") == "confirmed"]
        payload["benchmarks"] = [item for item in payload["benchmarks"] if item.get("status") == "confirmed"]
        payload["observations"] = [item for item in payload["observations"] if item.get("outcome") == "accepted"]
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def export_portable(args: argparse.Namespace) -> None:
    """Export only user-confirmed, non-product-specific lessons for transfer."""
    payload = load(args.memory)
    portable = {
        "schema_version": SCHEMA_VERSION,
        "kind": "portable-confirmed-creative-memory",
        "exported_utc": now(),
        "privacy_note": "Contains confirmed user-global preferences and benchmark criteria only; inspect before sharing.",
        "preferences": [item for item in payload["preferences"] if item.get("scope") == "user-global" and item.get("status") == "confirmed"],
        "benchmarks": [{key: value for key, value in item.items() if key != "path"} for item in payload["benchmarks"] if item.get("scope") == "user-global" and item.get("status") == "confirmed"],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(portable, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Exported {len(portable['preferences'])} preference(s) and {len(portable['benchmarks'])} benchmark(s): {args.output}")


def import_portable(args: argparse.Namespace) -> None:
    """Merge a reviewed portable export without importing product/job history."""
    incoming = json.loads(args.input.read_text(encoding="utf-8"))
    if incoming.get("schema_version") != SCHEMA_VERSION or incoming.get("kind") != "portable-confirmed-creative-memory":
        raise ValueError("Input is not a supported portable creative-memory export")
    payload = load(args.memory)
    preferences = incoming.get("preferences", [])
    benchmarks = incoming.get("benchmarks", [])
    if not isinstance(preferences, list) or not isinstance(benchmarks, list):
        raise ValueError("Portable export preferences and benchmarks must be lists")
    known_preferences = {(item.get("key"), item.get("value")) for item in payload["preferences"]}
    known_benchmarks = {(item.get("name"), item.get("criteria")) for item in payload["benchmarks"]}
    added_preferences = 0
    added_benchmarks = 0
    for source in preferences:
        if source.get("scope") != "user-global" or source.get("status") != "confirmed" or (source.get("key"), source.get("value")) in known_preferences:
            continue
        item = dict(source)
        item["id"] = f"pref-{len(payload['preferences']) + 1:03d}"
        item["updated_utc"] = now()
        payload["preferences"].append(item)
        known_preferences.add((item.get("key"), item.get("value")))
        added_preferences += 1
    for source in benchmarks:
        if source.get("scope") != "user-global" or source.get("status") != "confirmed" or (source.get("name"), source.get("criteria")) in known_benchmarks:
            continue
        item = dict(source)
        item["id"] = f"benchmark-{len(payload['benchmarks']) + 1:03d}"
        item["path"] = "Portable criterion only; choose a local benchmark path in this workspace."
        item["updated_utc"] = now()
        payload["benchmarks"].append(item)
        known_benchmarks.add((item.get("name"), item.get("criteria")))
        added_benchmarks += 1
    save(args.memory, payload)
    print(f"Imported preferences={added_preferences}, benchmarks={added_benchmarks}")


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="Maintain an explicit local creative-memory ledger.")
    sub = root.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Create a ledger only when it does not already exist.")
    init.add_argument("--memory", required=True, type=Path)
    init.set_defaults(func=lambda args: (save(args.memory, empty_memory()) if not args.memory.exists() else print(f"Memory already exists: {args.memory}")))

    pref = sub.add_parser("add-preference", help="Record a user preference with explicit evidence.")
    pref.add_argument("--memory", required=True, type=Path)
    pref.add_argument("--key", required=True)
    pref.add_argument("--value", required=True)
    pref.add_argument("--evidence", required=True)
    pref.add_argument("--scope", default="user-global", choices=("user-global", "product", "job"))
    pref.add_argument("--status", default="confirmed", choices=tuple(PREFERENCE_STATUSES))
    pref.set_defaults(func=add_preference)

    benchmark = sub.add_parser("add-benchmark", help="Record a user-approved quality benchmark.")
    benchmark.add_argument("--memory", required=True, type=Path)
    benchmark.add_argument("--name", required=True)
    benchmark.add_argument("--path", required=True)
    benchmark.add_argument("--criteria", required=True)
    benchmark.add_argument("--evidence", required=True)
    benchmark.add_argument("--scope", default="user-global", choices=("user-global", "product", "job"))
    benchmark.set_defaults(func=add_benchmark)

    observation = sub.add_parser("add-observation", help="Record an evidence-backed model or workflow result.")
    observation.add_argument("--memory", required=True, type=Path)
    observation.add_argument("--kind", required=True, choices=("model", "reference-pack", "gpt-scene", "prompt", "action", "assembly"))
    observation.add_argument("--outcome", required=True, choices=tuple(OBSERVATION_OUTCOMES))
    observation.add_argument("--summary", required=True)
    observation.add_argument("--cause-hypothesis", default="Not established.")
    observation.add_argument("--correction", default="None recorded.")
    observation.add_argument("--evidence", required=True)
    observation.add_argument("--scope", default="job", choices=("user-global", "product", "job"))
    observation.set_defaults(func=add_observation)

    display = sub.add_parser("show", help="Print the ledger without changing it.")
    display.add_argument("--memory", required=True, type=Path)
    display.add_argument("--confirmed-only", action="store_true")
    display.set_defaults(func=show)

    export = sub.add_parser("export-confirmed", help="Export reviewed user-global preferences and benchmark criteria for manual transfer.")
    export.add_argument("--memory", required=True, type=Path)
    export.add_argument("--output", required=True, type=Path)
    export.set_defaults(func=export_portable)

    imported = sub.add_parser("import-confirmed", help="Merge a reviewed portable export without product/job history.")
    imported.add_argument("--memory", required=True, type=Path)
    imported.add_argument("--input", required=True, type=Path)
    imported.set_defaults(func=import_portable)
    return root


def main() -> int:
    args = parser().parse_args()
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
