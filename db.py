import aiosqlite
import discord
import re
import datetime
import asyncio
async def init_db():
    async with aiosqlite.connect("data.db") as db:
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
        await db.execute('''
            CREATE TABLE IF NOT EXISTS Giveaways (
                Message_ID INTEGER PRIMARY KEY,
                ID INTEGER,
                Prize STRING,   
                Description STRING,
                Start STRING,
                End INTEGER,
                Role_Requirement INTEGER,
                Amount INTEGER,
                Host INTEGER,
                Winners STRING,
                Server_Host INTEGER,
                Target_Server STRING,
                Target_Server_Name STRING,
                Target_Server_ID INTEGER
            )
        ''')

        await db.execute('''
            CREATE TABLE IF NOT EXISTS Member_Data (
                Member_ID INTEGER,
                Server_ID INTEGER,
                is_server_blacklisted INTEGER
            )
        ''')

        await db.execute('''
            CREATE TABLE IF NOT EXISTS Entries (
                Member_ID INTEGER,
                Server_ID INTEGER
            )
        ''')
        await db.commit()
    print("Database initialized with no issues (hopefully)")

def parse_message_link(url: str, message_type: str):
    Message_Data = re.search(r"https://discord.com/channels/(?P<g>\d+)/(?P<c>\d+)/(?P<m>\d+)", url)
    if not Message_Data:
        print("bad")
        return None
    return int(Message_Data[message_type])

async def update_owner(new_id: int, server: int):
    async with aiosqlite.connect('data.db') as db:
        await db.execute('''
            UPDATE Server_Data SET Server_Owner = ? WHERE Server_ID = ?
        ''', (new_id, server))
        await db.commit()
    print(f"Updated {new_id} as server owner for {server}")

async def add_server_to_db(id: int, Name: str, Description: str, Owner: int, Members: int):
    async with aiosqlite.connect('data.db') as db:
        await db.execute('''
            INSERT OR IGNORE INTO Server_Data
            (Server_Id, Server_Name, Server_Description, Server_Owner, Members, Is_Blacklisted)
            VALUES (?,?,?,?,?,?)
        ''', (id, Name, Description, Owner, Members, None))
        await db.commit()
    print(f"Added & Joined {Name} | {id} to Server_Data")

async def remove_server_from_db(id: int, Name: str):
    async with aiosqlite.connect('data.db') as db:
        await db.execute('''
            DELETE FROM Server_Data WHERE Server_ID = ?
        ''', (id,))
        await db.execute('''
            DELETE FROM Giveaways WHERE Server_Host = ?
        ''', (id,))
        await db.commit()
    print(f"Removed {Name} | {id} from Server_Data & Server_Host")

async def handle_entries(Member_ID: int, Member_Name: str, Server_ID: int, Message_ID: int):
    async with aiosqlite.connect('data.db') as db:
        cursor = await db.execute('''
            SELECT * FROM Entries WHERE Member_ID = ? AND Message_ID = ?
        ''', (Member_ID, Message_ID))
        entry = await cursor.fetchone()
        if entry:
            await remove_entry(Member_ID, Member_Name, Message_ID)
            return None
        else:
            await add_entry(Member_ID, Member_Name, Server_ID, Message_ID)
            return True

async def add_entry(Member_ID: int, Member_Name: str, Server_ID: int, Message_ID: int):
    async with aiosqlite.connect('data.db') as db:
        await db.execute('''
            INSERT INTO Entries (Member_ID, Server_ID, Message_ID) VALUES (?,?,?)
        ''', (Member_ID, Server_ID, Message_ID))
        await db.commit()
    print(f"{Member_Name} | {Member_ID} Joined giveaway id: {Message_ID} in server {Server_ID}")

async def remove_entry(Member_ID: int, Member_Name: str, Message_ID: int):
    async with aiosqlite.connect('data.db') as db:
        await db.execute('''
            DELETE FROM Entries WHERE Member_ID = ? AND Message_ID = ?
        ''', (Member_ID, Message_ID))
        await db.commit()
    print(f"{Member_Name} | {Member_ID} left id: {Message_ID}")

async def check_in_server(member_id, server_id):
    async with aiosqlite.connect('data.db') as db:
        cursor = await db.execute('''
            SELECT * FROM Member_Data WHERE Member_ID = ? AND Server_ID = ?
        ''', (member_id,server_id,))
        result = await cursor.fetchone()
        if not result:
            return False
        else:
            return True


async def add_member(member_id,server_id):
    async with aiosqlite.connect('data.db') as db:
        if not await check_in_server(member_id,server_id):
            await db.execute('''
                INSERT INTO Member_Data (Member_ID, Server_ID VALUES (?,?)
            ''', (member_id, server_id))
            await db.commit()
        else:
            return

async def remove_member(member_id,server_id):
    async with aiosqlite.connect('data.db') as db:
        await db.execute('''
            DELETE FROM Member_Data WHERE Member_ID = ? AND Server_ID = ?
        ''', (member_id, server_id))
        await db.commit()


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
        result = await cursor.fetchone()
        await cursor.close()
        return result

async def fetch_giveaway_raw():
    async with aiosqlite.connect('data.db') as db:
        cursor = await db.execute('''
            SELECT * FROM giveaways
        ''')
        result = await cursor.fetchall()
        await cursor.close()
        return result

async def create_giveaway(Prize: str, Description: str, amount: int, host: str, host_server: int, end: int, partner_server: int = None, message_id: int = None, role: int = None, partner_server_name: str = None, partner_server_id: str = None):
    unique_id = None
    start = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    async with aiosqlite.connect('data.db') as db:
        cursor = await db.execute("SELECT * FROM giveaways")
        results = await cursor.fetchall()
        unique_id = len(results) + 1
        await db.execute('''
            INSERT INTO giveaways (Message_ID, ID, Prize, Description, Start, End, Role_Requirement, Amount, Host, Server_Host, Target_Server, Target_Server_Name)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        ''', (message_id, unique_id, Prize, Description, start, end, role, amount, host, host_server, partner_server,partner_server_name))
        await db.commit()

async def update_giveaway_embed(message_id: int):
    giveaway = await fetch_giveaway(message_id)
    entries = await fetch_entries(message_id)
    desc = (f'''
            {giveaway[3]}\n
            Ends: <t:{giveaway}:f>"
            Winners: {giveaway[7]}
            Entries: {len(entries)}
       ''')
    if giveaway[6]:
        desc += f"\nRequirement: <@&{giveaway[6]}>"
    if giveaway[11]:
        desc += f"\nHave to be in: [{giveaway[12]}]({giveaway[11]})"

    embed = discord.Embed(
            title=giveaway[2],
            description=desc
        )
    embed.set_footer(text=f"Hosted by {giveaway[8]} | ")
    return embed
