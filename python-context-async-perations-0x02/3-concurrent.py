"""Run concurrent asynchronous SQLite queries using aiosqlite and asyncio.

This script provides two async functions that fetch users and older users and
runs them concurrently with asyncio.gather.
"""
import asyncio
import aiosqlite


async def async_fetch_users(db_path: str = 'users.db'):
    async with aiosqlite.connect(db_path) as db:
        cur = await db.execute("SELECT * FROM users")
        rows = await cur.fetchall()
        await cur.close()
        return rows


async def async_fetch_older_users(db_path: str = 'users.db'):
    async with aiosqlite.connect(db_path) as db:
        cur = await db.execute("SELECT * FROM users WHERE age > ?", (40,))
        rows = await cur.fetchall()
        await cur.close()
        return rows


async def fetch_concurrently():
    users_task = async_fetch_users()
    older_task = async_fetch_older_users()
    users, older = await asyncio.gather(users_task, older_task)
    print("All users:\n", users)
    print("\nUsers older than 40:\n", older)


if __name__ == '__main__':
    asyncio.run(fetch_concurrently())
