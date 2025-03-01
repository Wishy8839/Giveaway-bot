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

class PersistentView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='🎉', style=discord.ButtonStyle.primary, custom_id='Giveaway_Button')
    async def green(self, interaction: discord.Interaction, button: discord.ui.Button):
        message = interaction.message.id
        giveaway = await data.fetch_giveaway(message)
        if not giveaway:
            await interaction.response.send_message("Something went wrong", ephemeral=True)
            return
        if await data.handle_entries(interaction.message.id):
            pass




class link(commands.GroupCog, group_name="giveaway"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="create", description="Create a giveaway")
    async def create_giveaway(self, interaction: discord.Interaction, prize: str, amount: int, end_time: str, role: discord.Role = None, partner_server: int = None):
        await interaction.response.send_message("I'll do you eventually", ephemeral=True)
        

# Setup the bot
async def setup(bot: commands.Bot):
    await bot.add_cog(link(bot))
