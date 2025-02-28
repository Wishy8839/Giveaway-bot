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






class giveaway_stuff(commands.GroupCog, group_name="giveaway"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="create",description="Create an giveaway")
    async def create_giveaway(self, interaction: discord.Interaction, prize: str, amount: int):
        interaction.response.send_message("Pass",ephemeral=True)


