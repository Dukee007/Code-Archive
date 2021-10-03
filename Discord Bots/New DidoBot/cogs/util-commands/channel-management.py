from itertools import cycle
from termcolor import colored

import os, json, urllib, difflib

import discord
from discord.ext import commands, tasks
from discord.ext.commands import check, has_permissions
from discord_slash import SlashCommand, SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_permission, create_option, create_choice
from discord_slash.model import SlashCommandPermissionType
from discord_components import DiscordComponents, Button


class RoleManagement(commands.Cog):
    def __init__(self, client):
        self.client = client

        print("Util Commands - Channels          " + colored('Running', 'green'))

    @commands.command()
    @has_permissions(manage_channels=True)
    async def delchannel(self, ctx, *, channel : str = None):
        if channel == None:
            await ctx.send("Please provide a channel search!")
            return

        channel_name_list = []

        for cnl in ctx.guild.channels:
            channel_name_list.append(cnl.name)

        channel = difflib.get_close_matches(channel, channel_name_list, n=1)

        try:
            channel = channel[0]
        except:
            await ctx.send("This channel could not be found!")
            return

        channel = get(ctx.guild.channels, name = channel)

        try:
            await channel.delete(reason=f"Action requested by: {ctx.author}")
            await ctx.send(f"Deleted {channel.name}!")
        except:
            await ctx.send(f"I couldn't delete {channel.mention}!")

    @cog_ext.cog_slash(name="delchannel",
        description="Delete a channel!",
        options=[
            create_option(
                name="channel",
                description="This is the channel you want to delete.",
                option_type=7,
                required=True,
            )
        ])
    async def slash_delchannel(self, ctx, channel : discord.TextChannel):
        if not ctx.author.guild_permissions.manage_channels:
            await ctx.send("You can't do that!", hidden=True)
            return

        try:
            await channel.delete(reason=f"Action requested by: {ctx.author}")
            await ctx.send(f"Deleted {channel.name}!", hidden=True)
        except:
            await ctx.send(f"I couldn't delete {channel.mention}!", hidden=True)

    @commands.command()
    @has_permissions(manage_channels=True, manage_roles=True)
    async def syncallchannels(self, ctx):
        msg = await ctx.send("Syncing channels!")

        for channel in ctx.guild.channels:
            await channel.edit(sync_permissions=True)

        await msg.edit(content="Synced Channels!")


def setup(client):
    client.add_cog(RoleManagement(client))
