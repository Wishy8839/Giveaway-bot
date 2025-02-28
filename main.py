import discord
import discord.ext.commands 
from discord.ext.commands import cooldown, BucketType
from discord import app_commands
from discord.ext import commands, tasks
from discord.ui import View, Button, Select, Modal, TextInput
from discord.utils import get
import asyncio
import random
import datetime 
import sqlite3
from discord import Interaction
from dotenv import load_dotenv
import time
import os
import re
import requests
from typing import Literal, Optional
import database.database as data
bot = commands.Bot(".", intents = discord.Intents.all())
# Load cogs
initial_extensions = [
    "Cogs.placeholder",
    "Cogs.placeholder"
]

if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f"Failed to load extension {extension}")


# Add guild to database whenever the bot gets added to the server
@bot.event()
async def on_guild_join(guild:discord.Guild):
    await data.add_server_to_db(id=guild.id,Name=guild.name,Description=guild.description,Owner=guild.owner,Members=guild.member_count)

@bot.event
async def on_guild_remove(guild:discord.Guild):
    await data.remove_server_from_db(id=guild.id,Name=guild.name)


# In theory this updates server owners
@bot.event
async def on_guild_update(before, after):
    if before.owner.id != after.owner.id:
        print(f"Old Owner: {before.owner.id} -> New Owner: {after.owner.id}")
        await data.update_owner(after.owner.id, after.id)

@bot.event
async def on_ready():
    await data.init_db()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name =f"deez nutz"))
    print(f"bot account: {bot.user} | version: {discord.__version__}")

bot.run("bleh")