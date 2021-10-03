import discord, time, asyncio, os, random, json, praw
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, cooldown, MissingPermissions, check, Cog
from discord.utils import get

def is_wiggle_or_luna(ctx):
    return ctx.author.id in [508372340904558603]

class App(commands.Cog):
    def __init__(self, client):
        self.client = client
        with open("setup/items.json") as f:
            self.items = json.load(f)
            f.close()
        print("Shop Cog Running")

    @commands.command()
    async def shop(self, ctx, page : str = "1"):
        pge = page

        real_pages = []
        for page in self.items:
            real_pages.append(str(page))

        if pge not in real_pages:
            embed=discord.Embed(title="Page not found!", color=0x00ffff)
            await ctx.send(embed=embed)
            return

        if pge == "1":
            embed=discord.Embed(title="Shop - Page 1", description="Boogie Store", color=0x00ffff)
            for item in self.items["1"]:
                embed.add_field(name=f"{item['rname']} - ${item['price']}", value=item["value"], inline=False)
            embed.set_footer(text="Galaxy Bot Shop - Adding more items soon")

        elif pge == "2":
            embed=discord.Embed(title="Shop - Page 2", description="Booster Store", color=0x00ffff)
            for item in self.items["2"]:
                embed.add_field(name=f"{item['rname']} - ${item['price']}", value=item["value"], inline=False)
            embed.set_footer(text="Galaxy Bot Shop - Adding more items soon")

        await ctx.send(embed=embed)





def setup(client):
    client.add_cog(App(client))
