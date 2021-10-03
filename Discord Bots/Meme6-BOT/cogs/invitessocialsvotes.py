import discord, time, os, praw, random, json
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, MissingPermissions
from discord.utils import get
from itertools import cycle
import datetime as dt
from datetime import datetime

class App(commands.Cog):
    def __init__(self, client):
        self.client = client
        print("Loading Cog: INVITESSOCIALSVOTES")

    @commands.command()
    async def invite(self, ctx):
        embed=discord.Embed(title="Bot Invite", url='https://discordapp.com/api/oauth2/authorize?client_id=693789629039771739&permissions=8&scope=bot')
        embed.set_author(name="Meme6", icon_url='https://m.media-amazon.com/images/I/71anlsy6v6L._SS500_.jpg')
        embed.set_footer(text="Meme6 [2.0]")
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(App(client))
