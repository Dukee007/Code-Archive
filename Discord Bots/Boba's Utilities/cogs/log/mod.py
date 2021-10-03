import discord, time, asyncio, os, random, json
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, cooldown, MissingPermissions, check
from discord.utils import get
from datetime import datetime, date
from termcolor import colored

class Invites(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.invites = {}

        print("Logs - Mod                   "+colored('Running', 'green'))

    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
        logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.ban).flatten()
        channel = guild.get_channel(825651199382388756)
        logs = logs[0]
        if logs.target == member:
            await channel.send(f'{logs.user} has just banned {logs.target} (The time is {logs.created_at}), and their reason for doing so is {logs.reason}')




def setup(client):
    client.add_cog(Invites(client))
