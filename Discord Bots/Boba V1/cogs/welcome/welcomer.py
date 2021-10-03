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

        print("Welcome - Welcomer                 "+colored('Running', 'green'))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = discord.Embed(title="✶ __Welcome To Boba Dankers__ ✶", colour=discord.Colour(0x795d7a), description="➜ __We have **DAILY** 50M heists__\n➜ __Awesome Gambling team perks__\n➜ __3k Member event soon! (bolt cutter)__\n➜ __Loads of self roles to your preference__\n➜ __Custom bots **That you can talk with**__")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/813112735398363157/814191588925243412/Boba_Dankers_3.gif")
        embed.add_field(name="Things To Check Out First:", value="<#807058277720260628> __Daily 50m Heists__\n<#819849093584781312> __Talk With Boba Bot__\n<#807119740160966656> __Go trade!__")

        try:
            await member.send(embed=embed)
        except:
            pass

def setup(client):
    client.add_cog(Website(client))
