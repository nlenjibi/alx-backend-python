#!/usr/bin/python3
"""Generator that streams users one by one from the database."""
import seed


def stream_users():
    """Yields users (dict) from user_data one by one.

    Uses a single loop to fetch rows from the DB via fetchone().
    """
    connection = seed.connect_to_prodev()
    if not connection:
        return

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    while True:
        row = cursor.fetchone()
        if not row:
            break
        yield row

    cursor.close()
    connection.close()
