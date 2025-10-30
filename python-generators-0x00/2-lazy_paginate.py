#!/usr/bin/python3
"""Lazy pagination generator for user_data."""
import seed


def paginate_users(page_size, offset):
    """Fetch a single page of users starting at offset. Returns list of dicts."""
    connection = seed.connect_to_prodev()
    if not connection:
        return []
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """Generator yielding pages (lists of user dicts) lazily.

    Uses a single loop to request pages only when needed.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
