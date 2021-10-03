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
    async def snipe(self, ctx, num : int = 0):
        try:
            embed=discord.Embed(title="Message Snipe", description=self.cache[str(ctx.channel.id)][num][0], timestamp=self.cache[str(ctx.channel.id)][num][2])
            embed.set_author(name=self.cache[str(ctx.channel.id)][num][1].name, icon_url=self.cache[str(ctx.channel.id)][num][1].avatar_url)
            embed.set_footer(text="Boba's Utilities - Message Snipe | Message was deleted")
            await ctx.send(embed=embed)
        except KeyError:
            await ctx.send("Nothing to snipe :)")


    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not self.cache[str(message.channel.id)]:
            self.cache[str(message.channel.id)] = []

        self.cache[str(message.channel.id)].append([message.content, message.author, datetime.now()])



def setup(client):
    client.add_cog(Invites(client))
