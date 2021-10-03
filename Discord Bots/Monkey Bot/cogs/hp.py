import discord, time, asyncio, os, random, json
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, cooldown, MissingPermissions, check, has_role
from discord.utils import get
from datetime import datetime, date
from termcolor import colored

class Invites(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.invites = {}

        print("System - Hp Command                   "+colored('Running', 'green'))

    @commands.command()
    @has_role(814322687623036938)
    async def hp(self, ctx, *, data):
        await ctx.message.delete()
        await ctx.send(f"<@&812997017714294797>\n{data}")
    
    @commands.command()
    @has_role(814322687623036938)
    async def partnership(self, ctx, *, data):
        await ctx.message.delete()
        await ctx.send(f"<@&812997020364439592>\n{data}")
    
    @commands.command()
    @has_role(814322687623036938)
    async def heist(self, ctx, *, data):
        await ctx.message.delete()
        await ctx.send(f"<@&812874957817905152>\n{data}")


def setup(client):
    client.add_cog(Invites(client))
