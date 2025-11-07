import time
import sqlite3
import functools


query_cache = {}


def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()

    return wrapper


def cache_query(func):
    """Decorator that caches results based on the SQL query string.

    The wrapped function is expected to accept a sqlite3.Connection as the
    first argument and a `query` parameter as either a positional or keyword
    argument.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Try kwargs first
        q = kwargs.get('query')
        if q is None:
            # If positional args provided, the query often is the second argument
            if len(args) >= 2:
                q = args[1]
        # If no query found, just call through
        if q is None:
            return func(*args, **kwargs)

        if q in query_cache:
            return query_cache[q]

        result = func(*args, **kwargs)
        query_cache[q] = result
        return result

    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


if __name__ == '__main__':
    users = fetch_users_with_cache(query="SELECT * FROM users")
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print('First call rows:', len(users))
    print('Second call rows (from cache):', len(users_again))
