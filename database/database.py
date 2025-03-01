import aiosqlite
import discord
import re

async def init_db():
    async with aiosqlite.connect('data.db') as db:
        # Create database for the servers the bot in with some basic data
        await db.execute('''
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
        # DATE FORMAT WILL BE IN  MONTH/DAY/YEAR Hour:Minute
        await db.execute('''
            CREATE TABLE IF NOT EXISTS Giveaways (
                Message_ID INTEGER PRIMARY KEY,
                ID INTEGER,
                Prize STRING,   
                Description  STRING,
                Start STRING,
                End STRING,
                Role_Requirement INTEGER,
                Amount INTEGER,
                Host INTEGER,
                Winners STRING,
                Server_Host INTEGER,
                Target_Server INTEGER
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS Entries (
                Member_ID INTEGER,
                Server_ID INTEGER,
                Message_ID INTEGER
            )
        ''')
    await db.commit()
    print("Database initilized with no issues (hopefully)")

    # thanks to andrewthederp and Robin5605 for making it cleaner :)
def parse_message_link(url: str, message_type: str):
    Message_Data = re.search(r"https://discord.com/channels/(?P<g>\d+)/(?P<c>\d+)/(?P<m>\d+)", url)

    if not Message_Data:
        print("bad")
        return None
    return int(Message_Data[message_type])

async def update_owner(new_id: int,server: int):
    async with aiosqlite.connect('data.db') as db:
        await db.execute('''
        UPDATE Server_Data SET Server_Owner = ? WHERE Server_ID = ?
    '''), (new_id,server)
    await db.commit()
    print(f"Updated {new_id} as server owner for {server}")



async def add_server_to_db(id: int, Name: str, Description: str, Owner: int, Members: int):
    # Adds an server to the database
    async with aiosqlite.connect('data.db') as db:
        await db.execute('''
            INSERT OR IGNORE INTO Server_Data
            (Server_Id, Server_Name, Server_Description , Server_Owner, Members, Is_Blacklisted)
            VALUES (?,?,?,?,?,?)
        '''), (id,Name,Description,Owner,Members,None)
    await db.commit()
    print(f"Added & Joined {Name} | {id} to Server_Data")

async def remove_server_from_db(id: int, Name: str):
    async with aiosqlite.connect('data.db') as db:
        await db.execute('''
            DELETE FROM Server_Data WHERE Server_ID = ?
        '''), (id)
        await db.execute('''
            DELETE FROM Giveaways WHERE Server_Host = ?
        '''), (id)
    await db.commit()
    print(f"Removed  {Name} | {id} to Server_Data & Server_Host")


async def handle_entries(Member_ID: int, Member_Name: str, Server_ID: int, Message_ID: int):
    async with aiosqlite.connect('data.db') as db:
        cursor = await db.execute('''
            SELECT * FROM Entries WHERE Member_ID = ? and Message_ID = ?
        ''')
        entry = await cursor.fetchone()
        if entry:
            await remove_entry(Member_ID,Member_Name,Message_ID)
            return None
        else:
            await add_entry(Member_ID,Member_Name,Server_ID,Message_ID)
            return True
        
async def add_entry(Member_ID: int,Member_Name: str, Server_ID: int, Message_ID: int):
    async with aiosqlite.connect('data.db') as db:
        await db.execute('''
            INSERT INTO Entries (Member_ID, Server_ID, Message_ID) VALUES (?,?,?)
        '''), (Member_ID,Server_ID,Message_ID)
        await db.commit()
        print(f"{Member_Name} | {Member_ID} Joined giveaway id: {Message_ID} in server {Server_ID}")

async def remove_entry(Member_ID: int, Member_Name: str, Message_ID: int):
    async with aiosqlite.connect('data.db') as db:
        await db.execute('''
            DELETE FROM Entries WHERE Member_ID = ? AND Message_ID = ?
        '''), (Member_ID,Message_ID)
        await db.commit()
        print(f"{Member_Name} | {Member_ID} left id: {Message_ID}")

async def fetch_entries(message_id: int):
    async with aiosqlite.connect('data.db') as db:
        cursor = await db.execute('''
            SELECT * FROM entries WHERE Message_ID = ?
        ''', (message_id,))

        result = await cursor.fetchall()
        await cursor.close()  

        return result

async def fetch_giveaway(message_id: int):
    async with aiosqlite.connect('data.db') as db:
        cursor = await db.execute('''
            SELECT * FROM giveaways WHERE Message_ID = ?
        ''', (message_id,))

        result = await cursor.fetchall()
        await cursor.close()  

        return result
async def create_giveaway():
    # i'm cooked
    pass

async def create_giveaway_embed(message_id: int):
    giveaway = await fetch_giveaway(message_id)
    giveaway_embed = discord.Embed(title=giveaway[3],description=giveaway[4])
    giveaway_embed.add_field(name="Amount",value=giveaway[7],inline=True)
    giveaway_embed.add_field(name="Ends",value={5},inline=True)
    giveaway_embed.add_field(name="Entries",value=await len(fetch_entries(message_id)),inline=True)
    giveaway_embed.set_footer(text=f"Hosted by {giveaway} ")

    return giveaway_embed
                  