Python Decorators Exercises (ALX)

This folder contains short exercises that demonstrate using Python decorators
for database-related concerns (logging, connection handling, transactions,
retries, and caching). Each file is self-contained and includes a small
example `__main__` block.

Files:

- `0-log_queries.py` — `log_queries()` decorator that prints the SQL query before executing.
- `1-with_db_connection.py` — `with_db_connection` decorator to open/close sqlite3 connection.
- `2-transactional.py` — `transactional` decorator to commit/rollback transactions; includes `with_db_connection`.
- `3-retry_on_failure.py` — `retry_on_failure(retries, delay)` decorator to retry failing DB calls; includes `with_db_connection`.
- `4-cache_query.py` — `cache_query` decorator to cache results by query string; includes `with_db_connection`.

Notes:

- These scripts expect a SQLite database file named `users.db` with a table
  `users` for the examples to run. Create a small test DB before running, for
  example using sqlite3 CLI or Python.
- To run an example, execute the file directly:

  python python-decorators-0x01/0-log_queries.py

Next steps: request a manual QA review when ready.
