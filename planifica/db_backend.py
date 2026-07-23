"""SQLite local o PostgreSQL en Streamlit Cloud (DATABASE_URL / secrets)."""

from __future__ import annotations

import os
import re
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "planifica.db"


def _get_database_url() -> str | None:
    url = os.environ.get("DATABASE_URL")
    if url:
        return _normalize_postgres_url(url)
    try:
        import streamlit as st

        if hasattr(st, "secrets") and "DATABASE_URL" in st.secrets:
            return _normalize_postgres_url(str(st.secrets["DATABASE_URL"]))
    except Exception:
        pass
    return None


def _normalize_postgres_url(url: str) -> str:
    cleaned = url.strip().strip('"').strip("'")
    if cleaned.startswith("postgres://"):
        cleaned = "postgresql://" + cleaned[len("postgres://") :]
    cleaned = re.sub(r"([?&])channel_binding=[^&]*&?", r"\1", cleaned)
    cleaned = cleaned.rstrip("&").rstrip("?")
    if cleaned.startswith("postgresql://") and "sslmode=" not in cleaned:
        if any(h in cleaned for h in ("neon.tech", "supabase.co", "railway.app")):
            cleaned = f"{cleaned}{'&' if '?' in cleaned else '?'}sslmode=require"
    return cleaned


def using_postgres() -> bool:
    url = _get_database_url()
    return bool(url and url.startswith("postgresql://"))


def is_ephemeral_storage() -> bool:
    """En Streamlit Cloud, SQLite se borra en cada redeploy/reboot."""
    if using_postgres():
        return False
    try:
        import streamlit as st

        host = ""
        if hasattr(st, "context") and hasattr(st.context, "headers"):
            headers = st.context.headers
            host = (headers.get("Host") or headers.get("host") or "").lower()
        return "streamlit.app" in host
    except Exception:
        return False


def _adapt_sql(sql: str) -> str:
    if using_postgres():
        return sql.replace("?", "%s")
    return sql


def row_to_dict(row: Any) -> dict[str, Any]:
    if row is None:
        return {}
    if isinstance(row, dict):
        return dict(row)
    return dict(row)


@contextmanager
def get_connection() -> Iterator[Any]:
    if using_postgres():
        import psycopg2
        import psycopg2.extras

        conn = psycopg2.connect(_get_database_url() or "")
        try:
            yield _PgConn(conn)
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    else:
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()


class _PgConn:
    """Adaptador mínimo: execute/executescript/commit con cursores RealDictCursor."""

    def __init__(self, conn: Any) -> None:
        self._conn = conn

    def execute(self, sql: str, params: tuple | list | None = None) -> Any:
        import psycopg2.extras

        cur = self._conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(_adapt_sql(sql), params or ())
        return _PgCursor(cur)

    def executescript(self, script: str) -> None:
        import psycopg2.extras

        cur = self._conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        for stmt in script.split(";"):
            s = stmt.strip()
            if not s:
                continue
            # SQLite FOREIGN KEY lines are fine in Postgres for our schema
            cur.execute(s)

    def commit(self) -> None:
        self._conn.commit()


class _PgCursor:
    def __init__(self, cur: Any) -> None:
        self._cur = cur

    def fetchone(self) -> Any:
        return self._cur.fetchone()

    def fetchall(self) -> list[Any]:
        return list(self._cur.fetchall())
