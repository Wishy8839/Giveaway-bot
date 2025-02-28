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
import importlib.util
from dotenv import load_dotenv
import time
import os
import re
import pytz
import requests
from typing import Literal, Optional
bot = commands.Bot(".", intents = discord.Intents.all())


# Load cogs
initial_extensions = [
    "Cogs.placeholder",
    "Cogs.placeholder"
]
print(initial_extensions)

if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f"Failed to load extension {extension}")

@bot.command


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name =f"deez nutz"))
    print(f"bot account: {bot.user} | version: {discord.__version__}")

bot.run("bleh")