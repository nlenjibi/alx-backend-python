import time
import sqlite3
import functools


def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()

    return wrapper


def retry_on_failure(retries=3, delay=2):
    """Decorator factory that retries the wrapped function if it raises an
    exception. The wrapped function is expected to accept a sqlite3.Connection
    as its first argument (when used with `with_db_connection`).
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt == retries:
                        # No retries left; re-raise
                        raise
                    time.sleep(delay)

            # Shouldn't reach here, but re-raise if it does
            if last_exc:
                raise last_exc

        return wrapper

    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


if __name__ == '__main__':
    users = fetch_users_with_retry()
    print(users)
