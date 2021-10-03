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

        print("Invites - Logger                   "+colored('Running', 'green'))

    def find_invite_by_code(self, invite_list, code):
        for inv in invite_list:
            if inv.code == code:
                return inv

    @commands.Cog.listener()
    async def on_ready(self):
        self.invites = await self.client.guilds[0].invites()

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        self.invites = await member.guild.invites()

    @commands.Cog.listener()
    async def on_member_join(self, member):

        invites_before_join = self.invites

        invites_after_join = await member.guild.invites()

        for invite in invites_before_join:

            if invite.uses < self.find_invite_by_code(invites_after_join, invite.code).uses:
                self.joinevent(member, invite)

                self.invites = invites_after_join

                return

    def joinevent(self, user, invite):
        print(f"Member {user.name} Joined")
        print(f"Invite Code: {invite.code}")
        print(f"Inviter: {invite.inviter}")


def setup(client):
    client.add_cog(Invites(client))
