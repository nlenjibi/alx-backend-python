#!/usr/bin/python3
"""Database helper for ALX_prodev user_data table.

Provides:
- connect_db(): Connect to MySQL server (no DB selected).
- create_database(connection): create ALX_prodev if not exists.
- connect_to_prodev(): connect to ALX_prodev database and return connection.
- create_table(connection): create user_data table if not exists.
- insert_data(connection, data): insert rows from CSV file path.

Environment variables (optional): MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_PORT
Defaults: host=localhost, user=root, password="", port=3306
"""
import csv
import os
from mysql.connector import connect, Error, IntegrityError


def _db_credentials():
    return {
        'host': os.environ.get('MYSQL_HOST', 'localhost'),
        'user': os.environ.get('MYSQL_USER', 'root'),
        'password': os.environ.get('MYSQL_PASSWORD', ''),
        'port': int(os.environ.get('MYSQL_PORT', 3306)),
    }


def connect_db():
    """Connect to MySQL server (no specific database).

    Returns a mysql.connector.connection object or None on failure.
    """
    try:
        creds = _db_credentials()
        conn = connect(host=creds['host'], user=creds['user'], password=creds['password'], port=creds['port'])
        return conn
    except Error as e:
        print(f"Error connecting to MySQL server: {e}")
        return None


def create_database(connection):
    """Create the ALX_prodev database if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        cursor.close()
        connection.commit()
    except Error as e:
        print(f"Error creating database: {e}")


def connect_to_prodev():
    """Connect to the ALX_prodev database.

    Returns connection or None.
    """
    try:
        creds = _db_credentials()
        conn = connect(host=creds['host'], user=creds['user'], password=creds['password'], port=creds['port'], database='ALX_prodev')
        return conn
    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None


def create_table(connection):
    """Create the user_data table if it does not exist."""
    ddl = (
        "CREATE TABLE IF NOT EXISTS user_data ("
        "user_id VARCHAR(36) PRIMARY KEY,"
        "name VARCHAR(255) NOT NULL,"
        "email VARCHAR(255) NOT NULL,"
        "age DECIMAL(5,0) NOT NULL"
        ");"
    )
    try:
        cursor = connection.cursor()
        cursor.execute(ddl)
        cursor.close()
        connection.commit()
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")


def insert_data(connection, data):
    """Insert rows from a CSV file into user_data.

    CSV is expected to have headers: user_id,name,email,age
    Rows already present (same primary key) will be skipped.
    """
    if not os.path.exists(data):
        print(f"CSV file not found: {data}")
        return

    insert_sql = "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)"
    try:
        cursor = connection.cursor()
        with open(data, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                vals = (row.get('user_id'), row.get('name'), row.get('email'), int(float(row.get('age'))))
                try:
                    cursor.execute(insert_sql, vals)
                except IntegrityError:
                    # duplicate primary key -> skip
                    continue
        connection.commit()
        cursor.close()
    except Error as e:
        print(f"Error inserting data: {e}")
