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


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

        print("Util Commands - Users          " + colored('Running', 'green'))

    @commands.command()
    async def pfp(self, ctx, user : discord.Member = None):
        if user == None:
            user = ctx.author
        embed = discord.Embed(title=f"{user}'s profile picture!", color=0x00ffff)
        embed.set_image(url=user.avatar_url)
        embed.set_footer(text=f"DidoBot [1.0] - Close up of {user}")
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="pfp",
        description="Get your own or someone elses profile picture.",
        options=[
            create_option(
                name="user",
                description="If you want to get someone elses profile picture, choose them here.",
                option_type=6,
                required=False,
            )
        ])
    async def slash_pfp(self, ctx, user : discord.Member = None):
        if user == None:
            user = ctx.author
        embed = discord.Embed(title=f"{user}'s profile picture!", color=0x00ffff)
        embed.set_image(url=user.avatar_url)
        embed.set_footer(text=f"DidoBot [1.0] - Close up of {user}")
        await ctx.send(embed=embed)




def setup(client):
    client.add_cog(Help(client))
