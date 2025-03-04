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
import db as data
from cogs.Giveaways.handle_giveaways import PersistentView, restore_persistent_views
loaded = 1
bot = commands.Bot(".", intents = discord.Intents.all())

# Load cogs
# initial_extensions = [
#     "cogs.Giveaways.handle_giveaways",
#     "cogs.debugging.setup"
# ]

# if __name__ == '__main__':
#     async def load():
#         for extension in initial_extensions:
#             try:
#                 await bot.load_extension(extension)
#                 print("loaded",extension)
#             except Exception as e:
#                 print(f"Failed to load extension {extension}")


# Add guild to database whenever the bot gets added to the server
@bot.event
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


@bot.command(name = "tree")
async def tree(ctx:commands.Context):
    await bot.tree.sync()
    await ctx.send("Tree sync'd")
    print("Tree updated")

@bot.command(name = "giveaways") 
async def giveaways(ctx:commands.Context):
    await ctx.send(f"`{await data.fetch_giveaway_raw()}`")






@bot.event
async def on_ready():
    await bot.load_extension('cogs.Giveaways.handle_giveaways')
    await data.init_db()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name =f"deez nutz"))
    print(f"bot account: {bot.user} | version: {discord.__version__}")
    bot.add_view(PersistentView())
    await restore_persistent_views(bot)

bot.run(os.getenv("DISCORD_TOKEN_TEST")) # better for testing tbh



