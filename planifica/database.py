from __future__ import annotations

import hashlib
import json
from typing import Any

from planifica.db_backend import get_connection
from planifica.utils import empty_plan_payload, generate_id, utc_now


def hash_pin(pin: str) -> str:
    return hashlib.sha256(pin.strip().encode()).hexdigest()


SCHEMA = """
CREATE TABLE IF NOT EXISTS accounts (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    pin_hash TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS plans (
    id TEXT PRIMARY KEY,
    account_id TEXT NOT NULL,
    title TEXT NOT NULL,
    payload TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'borrador',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS app_stats (
    key TEXT PRIMARY KEY,
    value INTEGER NOT NULL
);
"""


def init_schema() -> None:
    with get_connection() as conn:
        conn.executescript(SCHEMA)
        conn.commit()


def row_to_dict(row) -> dict[str, Any]:
    return dict(row) if row else {}


def register_account(name: str, pin: str) -> dict[str, Any]:
    name = name.strip()
    aid = generate_id("acc")
    now = utc_now()
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO accounts (id, name, pin_hash, created_at) VALUES (?, ?, ?, ?)",
            (aid, name, hash_pin(pin), now),
        )
        conn.commit()
    return {"id": aid, "name": name}


def login_account(name: str, pin: str) -> dict[str, Any] | None:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, name FROM accounts WHERE name = ? AND pin_hash = ?",
            (name.strip(), hash_pin(pin)),
        ).fetchone()
    return row_to_dict(row) if row else None


def list_plans(account_id: str) -> list[dict[str, Any]]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, title, status, created_at, updated_at, payload
            FROM plans WHERE account_id = ?
            ORDER BY updated_at DESC
            """,
            (account_id,),
        ).fetchall()
    out = []
    for row in rows:
        d = row_to_dict(row)
        d["payload"] = json.loads(d.pop("payload"))
        out.append(d)
    return out


def get_plan(plan_id: str, account_id: str) -> dict[str, Any] | None:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM plans WHERE id = ? AND account_id = ?",
            (plan_id, account_id),
        ).fetchone()
    if not row:
        return None
    d = row_to_dict(row)
    d["payload"] = json.loads(d["payload"])
    return d


def create_plan(account_id: str, title: str, payload: dict | None = None) -> dict[str, Any]:
    pid = generate_id("plan")
    now = utc_now()
    body = json.dumps(payload or empty_plan_payload(), ensure_ascii=False)
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO plans (id, account_id, title, payload, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, 'borrador', ?, ?)
            """,
            (pid, account_id, title.strip(), body, now, now),
        )
        conn.commit()
    return get_plan(pid, account_id)  # type: ignore[return-value]


def update_plan(plan_id: str, account_id: str, *, title: str | None, payload: dict, status: str | None) -> None:
    now = utc_now()
    with get_connection() as conn:
        if title is not None and status is not None:
            conn.execute(
                "UPDATE plans SET title = ?, payload = ?, status = ?, updated_at = ? WHERE id = ? AND account_id = ?",
                (title.strip(), json.dumps(payload, ensure_ascii=False), status, now, plan_id, account_id),
            )
        elif title is not None:
            conn.execute(
                "UPDATE plans SET title = ?, payload = ?, updated_at = ? WHERE id = ? AND account_id = ?",
                (title.strip(), json.dumps(payload, ensure_ascii=False), now, plan_id, account_id),
            )
        else:
            conn.execute(
                "UPDATE plans SET payload = ?, updated_at = ? WHERE id = ? AND account_id = ?",
                (json.dumps(payload, ensure_ascii=False), now, plan_id, account_id),
            )
        conn.commit()


def delete_plan(plan_id: str, account_id: str) -> None:
    with get_connection() as conn:
        conn.execute("DELETE FROM plans WHERE id = ? AND account_id = ?", (plan_id, account_id))
        conn.commit()


def duplicate_plan(plan_id: str, account_id: str) -> dict[str, Any] | None:
    src = get_plan(plan_id, account_id)
    if not src:
        return None
    title = f"{src['title']} (copia)"
    return create_plan(account_id, title, src["payload"])


def get_usage_count() -> int:
    with get_connection() as conn:
        row = conn.execute("SELECT value FROM app_stats WHERE key = 'sessions'").fetchone()
    return int(row[0]) if row else 0


def increment_usage() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO app_stats (key, value) VALUES ('sessions', 1)
            ON CONFLICT(key) DO UPDATE SET value = value + 1
            """
        )
        conn.commit()
