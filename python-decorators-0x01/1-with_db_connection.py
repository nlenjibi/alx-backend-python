import sqlite3
import functools


def with_db_connection(func):
    """Decorator that opens a sqlite3 connection to 'users.db', passes the
    connection as the first argument to the wrapped function, and ensures the
    connection is closed after the function returns (or raises).
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()

    return wrapper


@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


if __name__ == '__main__':
    user = get_user_by_id(user_id=1)
    print(user)
