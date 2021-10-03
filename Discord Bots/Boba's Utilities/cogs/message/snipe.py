import discord, time, asyncio, os, random, json
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, cooldown, MissingPermissions, check
from discord.utils import get
from datetime import datetime, date
from termcolor import colored

class Invites(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.cache = {}

        print("Messages - Snipe                   "+colored('Running', 'green'))

    @commands.command()
    async def snipe(self, ctx):
        try:
            embed=discord.Embed(title="Message Snipe", description=self.cache[str(ctx.channel.id)][0], timestamp=self.cache[str(ctx.channel.id)][2])
            embed.set_author(name=self.cache[str(ctx.channel.id)][1].name, icon_url=self.cache[str(ctx.channel.id)][1].avatar_url)
            embed.set_footer(text="Boba's Utilities - Message Snipe | Message was deleted at")
            await ctx.send(embed=embed)
        except KeyError:
            await ctx.send("Nothing to snipe :)")


    @commands.Cog.listener()
    async def on_message_delete(self, message):
        now = datetime.now()
        self.cache[str(message.channel.id)] = [message.content, message.author, now]



def setup(client):
    client.add_cog(Invites(client))
