import discord, time, asyncio, os, random, json
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, cooldown, MissingPermissions, check
from discord.utils import get
from datetime import datetime, date
from termcolor import colored

class Utils(commands.Cog):
    def __init__(self, client):
        self.client = client

        print("Invites - Tracker                   "+colored('Running', 'green'))

    @commands.command()
    async def invites(self, ctx, usr : discord.Member = None):
        if usr == None:
           user = ctx.author
        else:
           user = usr
        total_invites = 0
        for i in await ctx.guild.invites():
            if i.inviter == user:
                total_invites += i.uses
        embed=discord.Embed(title=f"{user.name}'s Invites!", description="Read below:", color=0x00ffff)
        embed.add_field(name="Invites:", value=str(total_invites), inline=False)
        embed.set_footer(text="Boba's Utilities - Invites")
        await ctx.send(embed=embed)

    @invites.error
    async def invites_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send("That user could not be found!")
            return

def setup(client):
    client.add_cog(Utils(client))
