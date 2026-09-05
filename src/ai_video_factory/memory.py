from __future__ import annotations

import sqlite3

from .db import ensure_product


def add_memory(
    connection: sqlite3.Connection,
    product_id: str | None,
    kind: str,
    content: str,
    evidence: str,
    status: str = "candidate",
) -> int:
    if status not in {"candidate", "approved", "retired"}:
        raise ValueError("status 必须是 candidate、approved 或 retired")
    if product_id:
        ensure_product(connection, product_id)
    cursor = connection.execute(
        """
        INSERT INTO creative_memory(product_id, kind, content, evidence, status)
        VALUES (?, ?, ?, ?, ?)
        """,
        (product_id, kind, content, evidence, status),
    )
    connection.commit()
    return int(cursor.lastrowid)


def retrieve(
    connection: sqlite3.Connection, product_id: str, query: str, limit: int = 10
) -> list[sqlite3.Row]:
    # FTS syntax treats punctuation as operators; simple word extraction keeps CLI input safe.
    terms = [term for term in query.replace("'", " ").split() if term]
    match = " OR ".join(f'"{term}"' for term in terms) or "*"
    return connection.execute(
        """
        SELECT m.memory_id, m.product_id, m.kind, m.content, m.evidence, m.status,
               bm25(memory_search) AS relevance
        FROM memory_search
        JOIN creative_memory AS m ON m.memory_id = memory_search.rowid
        WHERE memory_search MATCH ?
          AND m.status = 'approved'
          AND (m.product_id = ? OR m.product_id IS NULL)
        ORDER BY (m.product_id = ?) DESC, relevance
        LIMIT ?
        """,
        (match, product_id, product_id, limit),
    ).fetchall()
