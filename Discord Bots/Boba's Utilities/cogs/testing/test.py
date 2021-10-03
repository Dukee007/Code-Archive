import discord, time, asyncio, os, random, json, requests
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, cooldown, MissingPermissions, check
from discord.utils import get
from datetime import datetime, date
from discord_webhook import DiscordWebhook, DiscordEmbed
from termcolor import colored

class Website(commands.Cog):
    def __init__(self, client):
        self.client = client

        print("Testing - Cog                 "+colored('Running', 'green'))

    @commands.command()
    async def testt(self, ctx):
        has_invite_splash = False
        has_news_channels = False
        has_animated_icon = False
        has_banner = False
        has_vanity_url = False

        if ctx.guild.splash_url != "":
            has_invite_splash = True

        for channel in self.client.guilds[0].channels:
            if str(channel.type) == "news":
                    has_news_channels = True

        if ctx.guild.is_icon_animated:
            has_animated_icon = True

        if ctx.guild.banner_url != "":
            has_banner = True

        try:
            await ctx.guild.vanity_invite()
            has_vanity_url = True
        except Exception as e:
            if "Invite code is either invalid or taken." in str(e):
                pass#
            else:
                raise e

        await ctx.send([has_invite_splash, has_news_channels, has_animated_icon, has_banner, has_vanity_url])

def setup(client):
    client.add_cog(Website(client))
