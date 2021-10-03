import discord, time, asyncio, os, random, json, didumean
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, cooldown, MissingPermissions, check, Cog
from discord.utils import get

def is_wiggle_or_luna(ctx):
    return ctx.author.id in [508372340904558603]

class App(commands.Cog):
    def __init__(self, client):
        self.client = client
        print("Use Cog Running")

    async def use(self, ctx, item : str = None):
        if item == None:
            embed=discord.Embed(title="Incorrect command usage!", description=".buy {item}", color=0x00ffff)
            await ctx.send(embed=embed)
            return
        item = item.lower()
        if item not in ["bphone"]:
            maby = str(didumean.correction(item))
            if maby in ["bphone"]:
                embed=discord.Embed(title="Item not found!", description=f"Maby you ment **{maby}**.", color=0x00ffff)
                await ctx.send(embed=embed)
                return
            embed=discord.Embed(title="Item not found!", color=0x00ffff)
            await ctx.send(embed=embed)
            return

        with open("data/inv.json") as f:
            inv = json.load(f)
            f.close()


def setup(client):
    client.add_cog(App(client))
