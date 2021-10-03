import discord, time, asyncio, os, random, json, praw
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, cooldown, MissingPermissions, check, Cog
from discord.utils import get

class App(commands.Cog):
    def __init__(self, client):
        self.client = client
        print("Custom Cog Running")

    @commands.command()
    async def ruby(self, ctx):
        await ctx.send("Join Rubys Server:\nhttps://discord.gg/W6EcztAPJH")


def setup(client):
    client.add_cog(App(client))
