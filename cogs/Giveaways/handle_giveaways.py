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
import utils.time_stuff as tt

class PersistentView(discord.ui.View):
    def __init__(self, invite_url=None):
        super().__init__(timeout=None)
        self.invite_url = invite_url
        if invite_url: 
            self.add_item(self.JoinServerButton())

    @discord.ui.button(label='🎉', style=discord.ButtonStyle.primary, custom_id='Giveaway_Button')
    async def join_invite(self, interaction: discord.Interaction, button: discord.ui.Button):
        message = interaction.message.id
        giveaway = await data.fetch_giveaway(message)
        print(giveaway)
        invite_urll =  giveaway[11] if giveaway[11] else None
        invite_name = giveaway[12] if giveaway[12] else None
        if not giveaway:
            await interaction.response.send_message("Something went wrong", ephemeral=True)
            return
        if await data.handle_entries(Member_Name=interaction.user.global_name,Server_ID=interaction.guild.id,Message_ID=message,Member_ID=interaction.user.id):
            await interaction.response.send_message("You've joined the giveaway",ephemeral=True)
        else:
            await interaction.response.send_message("You've left the giveaway",ephemeral=True)
        await interaction.message.edit(embed=await data.update_giveaway_embed(message), view=PersistentView(invite_url=invite_urll if invite_urll else None))

    class JoinServerButton(discord.ui.Button):
        def __init__(self):
            super().__init__(label='Join Server', style=discord.ButtonStyle.secondary, custom_id='Join_Server_Button')

        async def callback(self, interaction: discord.Interaction):
            message = interaction.message.id
            giveaway = await data.fetch_giveaway(message)
            await interaction.response.send_message(f"You can join here!\n{giveaway[11]}",ephemeral=True)


async def restore_persistent_views(bot: commands.Bot):
    giveaways = await data.fetch_giveaway_raw()
    if not giveaways:
        return

    for giveaway in giveaways:
        message_id = giveaway[0]
        invite_url = giveaway[10] if giveaway[10] else None

        # Recreate the PersistentView
        view = PersistentView(invite_url=invite_url)

        
        try:
            channel = bot.get_channel(giveaway[11])  
            if channel:
                message = await channel.fetch_message(message_id)
                await message.edit(view=view)
        except Exception as e:
            print(f"Failed to restore view for message {message_id}: {e}")




class link(commands.GroupCog, group_name="giveaway"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def invite(self, url: str):
        invite_link = await self.bot.fetch_invite(url)
        return invite_link.url, invite_link.guild.name

    @app_commands.command(name="create", description="Create a giveaway")
    async def create_giveaway(self, interaction: discord.Interaction, prize: str, description: str, amount: int, end_time: str, role: discord.Role = None, invite: str = None):
        await interaction.response.defer()

        # will parste into database later
        if tt.string_to_seconds(end_time) is False:
            await interaction.followup.send(
                "Incorrect format used for the end date of the give\n"

                "Examples of proper use"
                "`1 month(s)`"
                "`4 day(s)`"
                "'1 hour'"
                "'30 minutes'"
                ""
            )
            return
        end_time = tt.seconds_to_discord_timestamp(tt.string_to_seconds(end_time))
        invite_link = await self.bot.fetch_invite(invite) if invite else None
        invite_name = invite_link.guild.name if invite_link else None
        role_id = role.id if role else None
        desc = (f'''
            {description}
            Ends: {end_time}
            Winners: {(amount)}
            Entries: 0
       ''')
        if role:
            desc += f"\nRequirement: <@&{role.id}>"
        if invite_link:
            desc += f"\nHave to be in: [{invite_link.guild.name}]({invite_link.url})"
        giveaway_embed = discord.Embed(
            title=prize,
            description=desc
        )
        giveaway_embed.set_footer(text=f"Hosted by {interaction.user.global_name} | ")
        
        message = await interaction.followup.send(embed=giveaway_embed, view=PersistentView(invite_url=invite_link.url if invite_link else None))
        ids = message.id
        
        await data.create_giveaway(prize,Description=desc,amount=amount,host=interaction.user.global_name,host_server=interaction.guild.name,end=end_time,partner_server=invite,message_id=ids,role=role_id,partner_server_name=invite_name)

# Setup the bot
async def setup(bot: commands.Bot):
    await bot.add_cog(link(bot))

