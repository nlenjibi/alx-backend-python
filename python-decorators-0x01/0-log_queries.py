import sqlite3
import functools


def log_queries():
    """Decorator factory that logs the SQL query string passed to the wrapped function.

    The wrapped function is expected to receive the SQL query either as a
    keyword argument named 'query' or as a positional argument (commonly the
    first or second positional argument depending on other decorators).
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Try to get query from kwargs first
            query = kwargs.get('query')
            if query is None:
                # If not in kwargs, try positional args. Find first string-looking arg
                for a in args:
                    if isinstance(a, str) and a.strip().upper().startswith(('SELECT', 'INSERT', 'UPDATE', 'DELETE')):
                        query = a
                        break
            print(f"Executing SQL query: {query}")
            return func(*args, **kwargs)

        return wrapper

    return decorator


@log_queries()
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


if __name__ == '__main__':
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)
