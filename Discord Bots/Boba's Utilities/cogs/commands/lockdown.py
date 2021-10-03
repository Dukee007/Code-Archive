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

        f = open("data/slowmode_channels.json")
        self.channels_to_slowmode = json.load(f)
        f.close()

        print("Commands - Lockdown          "+colored('Running', 'green'))

    @commands.command()
    @has_permissions(administrator=True)
    async def lockdown(self, ctx):
        num = 0
        async with ctx.typing():
            for channelid in self.channels_to_slowmode:
                channel = self.client.get_channel(channelid)
                members_role = get(ctx.guild.roles, id=824464395136139274)
                await channel.set_permissions(members_role, send_messages=False)
                embed=discord.Embed(title="Server Lockdown 🔒", description=":lock: We are locked down Because either Dank is down, or there was a raid, check <#807297379665182720> for info. :lock:", color=0xff0000, timestamp=datetime.now())
                embed.set_footer(text="Boba Dankers")
                await channel.send(embed=embed)
                num += 1

        await ctx.send(f"Locked {str(num)} channels!")

    @commands.command()
    @has_permissions(administrator=True)
    async def unlockdown(self, ctx):
        num = 0
        async with ctx.typing():
            for channelid in self.channels_to_slowmode:
                channel = self.client.get_channel(channelid)
                members_role = get(ctx.guild.roles, id=824464395136139274)
                await channel.set_permissions(members_role, send_messages=True)
                num += 1

        await ctx.send(f"Unlocked {str(num)} channels!")


def setup(client):
    client.add_cog(Utils(client))
