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
        print("Loading Cog: MODERATION")

    @commands.command(aliases=['purge', 'clean', 'delete'])
    @has_permissions(manage_messages=True)
    async def clear(self, ctx, ammount=10):
        await ctx.channel.purge(limit=ammount+1)
        await ctx.send("Done")
        time.sleep(0.5)
        await ctx.channel.purge(limit=1)

    @commands.command()
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member:discord.User = None, reason = None):
        if member == None or member == ctx.message.author:
            await ctx.send("You cannot ban yourself")
            return
        if reason == None:
            reason = "Unknown"
        await ctx.send(f"{member} is banned!")
        await ctx.guild.ban(member, reason=reason)

    @commands.command(pass_context = True)
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if member == None or member == ctx.message.author:
            await ctx.send("You cannot kick yourself")
            return
        if reason == None:
            reason = "Unknown"
        await ctx.send(f"{member} has been kicked!")
        await member.kick(reason=reason)

def setup(client):
    client.add_cog(App(client))
