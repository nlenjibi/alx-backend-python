"""Reusable query context manager that executes a query and returns results.

Usage:
    with ExecuteQuery(query, params) as results:
        print(results)
"""
import sqlite3
from typing import Any, Iterable, Optional, Tuple


class ExecuteQuery:
    def __init__(self, query: str, params: Optional[Iterable[Any]] = None, db_path: str = 'users.db'):
        self.query = query
        self.params = tuple(params) if params else ()
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        if self.params:
            self.cursor.execute(self.query, self.params)
        else:
            self.cursor.execute(self.query)
        self.results = self.cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if self.cursor:
                self.cursor.close()
        finally:
            if self.conn:
                try:
                    self.conn.close()
                except Exception:
                    pass
        # Do not suppress exceptions
        return False


if __name__ == '__main__':
    # Execute the requested query: users with age > 25
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)
    with ExecuteQuery(query, params) as results:
        print(results)
