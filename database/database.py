import sqlite3
import aiosqlite
import asyncio
import discord


async def init_db():
    async with aiosqlite.connect('data.db') as db:
        # Create database for the servers the bot in with some basic data
        db.execute('''
            CREATE TABLE IF NOT EXISTS Server_Data (
                Server_ID INTEGER PRIMARY KEY,
                Server_Name STRING,
                Server_Description STRING,
                Server_Owner INTEGER,
                Members INTEGER,
                Is_Blacklisted INTEGER
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
    print("Database initilized with no issues (hopefully)")


async def Add_Server_To_DB(id: int, Name: str, Description: str, Owner: int, Members: int):
    # Adds an server to the database
    async with aiosqlite.connect('data.db') as db:
        db.execute('''
            INSERT OR IGNORE INTO Server_Data
            (Server_Id, Server_Name, Server_Description , Server_Owner, Members, Is_Blacklisted)
            VALUES (?,?,?,?,?,?)
        '''), (id,Name,Description,Owner,Members,None)
    await db.commit()
    print(f"Added & Joined {Name} | {id} to Server_Data")

