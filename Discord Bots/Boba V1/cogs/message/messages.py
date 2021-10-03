import discord, time, asyncio, os, random, json, re
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, cooldown, MissingPermissions, check
from discord.utils import get
from termcolor import colored
from urlextract import URLExtract

class App(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.extractor = URLExtract()
        print("System - Message Scan             "+colored('Running', 'green'))


    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            if not message.author.guild_permissions.administrator:
                if not message.channel.id == 807412298212835329:
                    await self.scanmessage(message)

        if "luna" in message.content.strip().replace(" ", "").lower():
            emoji = get(self.client.guilds[0].emojis, name='luna')
            await message.add_reaction(emoji)

    async def scanformentions(self, string):
        return len(string.split("<@"))

    async def scanmessage(self, message):
        urls = self.extractor.find_urls(message.content)
        if len(urls) >= 1:
            await message.delete()
            await message.author.send(f"Hello {message.author.mention}. We deleted your message in {message.channel.mention} because we found the following link/s in it: {urls}")

        mentions = await self.scanformentions(message.content)
        if mentions >= 4:
            await message.delete()
            await message.author.send(f"Hello {message.author.mention}. We deleted your message in {message.channel.mention} because we found 3 or more mentions in it!")





def setup(client):
    client.add_cog(App(client))
