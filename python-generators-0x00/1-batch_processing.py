#!/usr/bin/python3
"""Batch processing utilities using generators."""
import seed


def stream_users_in_batches(batch_size):
    """Yield lists of user dicts in batches of batch_size.

    Yields an empty list when no more rows are present (stops iteration).
    """
    connection = seed.connect_to_prodev()
    if not connection:
        return

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        yield rows

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """Process batches and print users older than 25.

    Uses stream_users_in_batches and prints filtered users.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            try:
                age = int(user.get('age', 0))
            except Exception:
                continue
            if age > 25:
                print(user)
                print()  # match sample output spacing
