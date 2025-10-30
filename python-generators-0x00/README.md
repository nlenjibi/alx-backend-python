Python generators exercises (ALX)

Files added:

- `seed.py`: helpers to create/connect database, create table and insert CSV data. Uses mysql-connector-python. Credentials can be provided via environment variables: MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_PORT.
- `0-stream_users.py`: stream_users() generator yielding rows one-by-one.
- `1-batch_processing.py`: stream_users_in_batches(batch_size) and batch_processing(batch_size) to process users in batches and print users over 25.
- `2-lazy_paginate.py`: paginate_users(page_size, offset) and lazy_pagination(page_size) for page-wise lazy fetching.
- `4-stream_ages.py`: stream_user_ages() generator and average_age() to compute average without loading all rows.
- `requirements.txt`: mysql-connector-python

Quick usage (ensure MySQL server available and package installed):

1. Install dependency:

   pip install -r requirements.txt

2. Set environment variables if needed (optional):

   $env:MYSQL_HOST = 'localhost'; $env:MYSQL_USER = 'root'; $env:MYSQL_PASSWORD = ''

3. Seed the database (example script not included here — use provided `seed` functions from a small runner):

   Use a small driver like the provided `0-main.py` in the exercise instructions to call `seed.connect_db()`, `seed.create_database()`, `seed.connect_to_prodev()`, `seed.create_table()` and `seed.insert_data('user_data.csv')`.

4. Stream users:

   Import and call `stream_users()` from `0-stream_users.py`.

Notes:

- This code assumes a running MySQL server and a `user_data.csv` file formatted as described in the exercise.
- The modules use environment variables for connection settings to avoid hardcoding credentials.
