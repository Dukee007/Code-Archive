import discord, time, asyncio, os, random, json, re
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, cooldown, MissingPermissions, check, has_role
from discord.utils import get
from termcolor import colored
from datetime import datetime, date
from urlextract import URLExtract

class Utils(commands.Cog):
    def __init__(self, client):
        self.client = client

        print("Commands - Lock          "+colored('Running', 'green'))

    @commands.command()
    @has_permissions(manage_channels=True)
    async def lock(self, ctx):
        async with ctx.typing():
            members_role = get(ctx.guild.roles, id=824464395136139274)
            await ctx.channel.set_permissions(members_role, send_messages=False)
            await ctx.send("Channel Locked!")

    @commands.command()
    @has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        async with ctx.typing():
            members_role = get(ctx.guild.roles, id=824464395136139274)
            await ctx.channel.set_permissions(members_role, send_messages=True)
            await ctx.send("Channel Unlocked!")


def setup(client):
    client.add_cog(Utils(client))
