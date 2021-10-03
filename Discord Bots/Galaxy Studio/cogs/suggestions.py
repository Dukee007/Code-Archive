import discord, time, asyncio, os, random, json, praw
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, cooldown, MissingPermissions, check, Cog
from discord.utils import get

class App(commands.Cog):
    def __init__(self, client):
        self.client = client
        print("Suggestions Cog Running")

    @Cog.listener()
    async def on_message(self, message):
        if message.channel.id != 807116807714111518 or message.author.bot == True:
            return

        content = message.content

        if ".ignore" not in content:
            await message.delete()

            embed=discord.Embed(title=f"New Suggestion, by {message.author}", description=content, color=0x00ffff)
            msg = await message.channel.send(embed=embed)

            await msg.add_reaction("✅")
            await msg.add_reaction("❌")


def setup(client):
    client.add_cog(App(client))
