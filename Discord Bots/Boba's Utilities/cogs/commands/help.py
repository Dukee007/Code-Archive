import discord, time, asyncio, os, random, json
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, cooldown, MissingPermissions, check
from discord.utils import get
from datetime import datetime, date
from termcolor import colored

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

        print("Commands - Help                   "+colored('Running', 'green'))

    @commands.command()
    @has_permissions(manage_messages=True)
    async def help(self, ctx, cmd : str = None):
        if cmd == None:
            embed = discord.Embed(title="Help", colour=discord.Colour(0x31a965), description="Here is a list of my commands\nType `.help {cmd}` for more info on a command.")

            embed.add_field(name="🥳 Giveaways", value="**1.** giftcr - Starts the giveaways creation wizard!\n**2.** giftdel - Deletes a giveaways!\n**3.** giftrrl - Re-Rolls the winner of a giveaway!", inline=False)
            embed.add_field(name="🔨 Moderation", value="**1.** ban - Bans a member!\n**2.** kick - Kicks a member!\n**3.** clear - Deletes a provided number a messages!", inline=False)
            embed.add_field(name="🧰 Utils", value="**1.** .addperm - Give a user access to the anti raid commands!\n**2.** .takeperm - Revokes a user's access to the anti raid commands!\n**3.** .heistban - Start's banning all leaves for 2 hours!\n**4.** .stopheistban - Stop's banning members who leave before 2hrs is over!\n**5.** .raid [start/stop] - Stop's an active raid!", inline=False)

            await ctx.send(embed=embed)

        else:
            await ctx.send("This feature is not ready yet!")

def setup(client):
    client.add_cog(Moderation(client))
