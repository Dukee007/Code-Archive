from matplotlib import pyplot as plt

import random
import json

import discord
from discord.ext import commands, tasks
from discord.ext.commands import check
from discord_slash import SlashCommand, SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_permission, create_option, create_choice
from discord_slash.model import SlashCommandPermissionType


class info(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def invite(self, ctx):
        await ctx.message.reply("You can add me here: https://discord.com/api/oauth2/authorize?client_id=859537103996846090&permissions=8&scope=bot%20applications.commands")







def setup(client):
    client.add_cog(info(client))
