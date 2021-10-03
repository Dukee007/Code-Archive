import discord, time, asyncio, os, random, json, didumean
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, cooldown, MissingPermissions, check, Cog
from discord.utils import get

def is_wiggle_or_luna(ctx):
    return ctx.author.id in [508372340904558603]

class App(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.real_items = ["bphone"]
        print("Shop Buying Cog Running")

    @commands.command()
    async def buy(self, ctx, item : str = None):
        if item == None:
            embed=discord.Embed(title="Incorrect command usage!", description=".buy {item}", color=0x00ffff)
            await ctx.send(embed=embed)
            return
        item = item.lower()
        if item not in self.real_items:
            maby = str(didumean.correction(item))
            if maby in self.real_items:
                embed=discord.Embed(title="Item not found!", description=f"Maby you ment **{maby}**.", color=0x00ffff)
                await ctx.send(embed=embed)
                return
            embed=discord.Embed(title="Item not found!", color=0x00ffff)
            await ctx.send(embed=embed)
            return

        with open("data/money.json") as f:
            money = json.load(f)
            f.close()

        with open("data/inv.json") as f:
            inv = json.load(f)
            f.close()

        with open("setup/items.json") as f:
            items = json.load(f)
            f.close()

        with open("data/bank-queue.json") as f:
            queue = json.load(f)
            f.close()

        try:
            x = inv[str(ctx.author.id)]
        except:
            inv[str(ctx.author.id)] = {}

        try:
            bal = money[str(ctx.author.id)]
        except:
            bal = 0
            money[str(ctx.author.id)] = 0

        for page in items:
            for pitem in items[page]:
                if item == pitem["name"]:
                    if bal < pitem["rprice"]:
                        await ctx.send("You cannot afford that!")
                    else:
                        try:
                            inv[str(ctx.author.id)][pitem["name"]] += 1
                        except:
                            inv[str(ctx.author.id)][pitem["name"]] = 1
                        money[str(ctx.author.id)] -= pitem["rprice"]
                        queue.append(pitem["rprice"])
                        await ctx.send(f"You have brought a {pitem['rname']}")


        with open("data/money.json", "w+") as f:
            json.dump(money, f)
            f.close()

        with open("data/inv.json", "w+") as f:
            json.dump(inv, f)
            f.close()

        with open("data/bank-queue.json", "w+") as f:
            json.dump(queue, f)
            f.close()

    @commands.command()
    async def inv(self, ctx):
        with open("data/inv.json") as f:
            inv = json.load(f)
            f.close()

        embed=discord.Embed(title="Inventory", color=0x00ffff)

        empty = True

        try:
            test = inv[str(ctx.author.id)]
        except:
            inv[str(ctx.author.id)] = {}

        for i in ["bphone"]:
            try:
                test = inv[str(ctx.author.id)][i]
            except:
                inv[str(ctx.author.id)][i] = 0

        if inv[str(ctx.author.id)]["bphone"] > 0:
            embed.add_field(name=f"BPhone X - {inv[str(ctx.author.id)]['bphone']}", value="This item lets you post on social media", inline=False)
            empty = False

        if not empty:
            await ctx.send(embed=embed)
        else:
            await ctx.send("Your inv is empty!")


def setup(client):
    client.add_cog(App(client))
