"""Class-based context manager for a SQLite database connection.

Usage:
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        print(cursor.fetchall())
"""
import sqlite3


class DatabaseConnection:
    def __init__(self, db_path='users.db'):
        self.db_path = db_path
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            try:
                self.conn.close()
            except Exception:
                pass
        # Do not suppress exceptions
        return False


if __name__ == '__main__':
    # Demo: use the context manager to run a simple query
    with DatabaseConnection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
        print(rows)
