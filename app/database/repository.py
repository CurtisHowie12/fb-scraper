"""
Persistence layer for scraped ad data.

get_db_connection() (db_connection.py) handles connecting via the
DATABASE_* environment variables. Add new save/query functions here as
your needs grow — e.g. get_ads_by_site(), delete_stale_ads(), etc.
"""
import json

from app.database.db_connection import get_db_connection

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS scraped_ads (
    id SERIAL PRIMARY KEY,
    site_name TEXT NOT NULL,
    poster_name TEXT,
    poster_url TEXT,
    posted_with TEXT,
    body_text TEXT,
    media_url TEXT,
    shop_now_url TEXT,
    headline TEXT,
    status TEXT,
    library_id TEXT,
    started_running TEXT,
    platforms JSONB,
    multiple_versions BOOLEAN,
    scraped_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
"""

INSERT_SQL = """
INSERT INTO scraped_ads (
    site_name, poster_name, poster_url, posted_with, body_text,
    media_url, shop_now_url, headline, status, library_id,
    started_running, platforms, multiple_versions
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
"""


def _ensure_schema(conn) -> None:
    with conn.cursor() as cur:
        cur.execute(CREATE_TABLE_SQL)
    conn.commit()


def init_schema() -> None:
    """Create the scraped_ads table if it doesn't already exist."""
    conn = get_db_connection()
    try:
        _ensure_schema(conn)
    finally:
        conn.close()


def save_ads(site_name: str, ads: list[dict]) -> int:
    """
    Insert scraped ad dicts (as produced by scrape_ads_library) into the
    database. Returns the number of rows inserted.
    """
    if not ads:
        return 0

    conn = get_db_connection()
    try:
        _ensure_schema(conn)
        with conn.cursor() as cur:
            for ad in ads:
                cur.execute(INSERT_SQL, (
                    site_name,
                    ad.get("poster_name"),
                    ad.get("poster_url"),
                    ad.get("posted_with"),
                    ad.get("body_text"),
                    ad.get("media_url"),
                    ad.get("shop_now_url"),
                    ad.get("headline"),
                    ad.get("status"),
                    ad.get("library_id"),
                    ad.get("started_running"),
                    json.dumps(ad.get("platforms", [])),
                    ad.get("multiple_versions", False),
                ))
        conn.commit()
        return len(ads)
    finally:
        conn.close()
