#!/usr/bin/python3
"""Stream user ages and compute average using generators."""
import seed


def stream_user_ages():
    """Generator that yields ages (int) one by one from user_data."""
    connection = seed.connect_to_prodev()
    if not connection:
        return
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")

    while True:
        row = cursor.fetchone()
        if not row:
            break
        # convert DECIMAL to int
        try:
            yield int(row.get('age'))
        except Exception:
            continue

    cursor.close()
    connection.close()


def average_age():
    """Calculate and print the average age using the stream_user_ages generator.

    Uses a single loop over the generator (no full dataset in memory).
    """
    total = 0
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1

    avg = total / count if count else 0
    print(f"Average age of users: {avg}")


if __name__ == '__main__':
    average_age()
