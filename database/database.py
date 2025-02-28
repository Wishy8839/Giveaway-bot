import sqlite3
import aiosqlite
import asyncio



async def init_db():
    async with aiosqlite.connect('data.db') as db:
        db.execute('''
            CREATE TABLE IF NOT EXISTS Server_Data (
                Server_ID INTEGER PRIMARY KEY,
                Server_Owner INTEGER
            )
        ''')

        # Creates database for giveways
        db.execute('''
            CREATE TABLE IF NOT EXISTS Giveaways (
                ID INTEGER PRIMARY KEY,
                Prize STRING,
                Description  STRING,
                Start STRING,
                End STRING,
                Role_Requirement INTEGER,
                Amount INTEGER,
                Host INTEGER,
                Winners INTEGER,
                Server_Host INTEGER,
                Target_Server INTEGER
            )
        ''')

    await db.commit()