import discord, time, asyncio, os, random, json
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, cooldown, MissingPermissions, check, Cog
from discord.utils import get

def is_wiggle_or_luna(ctx):
    return ctx.author.id in [508372340904558603, 732315150266269817]

class App(commands.Cog):
    def __init__(self, client):
        self.client = client
        print("Money Commands Cog Running")

    #                        <-- commands -->

    @commands.command()
    async def bal(self, ctx, user : discord.Member = None):
        with open("data/money.json") as f:
            money = json.load(f)
            f.close()

        if user == None:
            user = ctx.author

        try:
            bux = str(money[str(user.id)])
        except:
            bux = 0

        embed=discord.Embed(title="Boogie Bal", color=0x00ffff)
        embed.add_field(name="Boogie Bucks:", value=f"${bux}", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @check(is_wiggle_or_luna)
    async def give(self, ctx, user : discord.User = None, num : int = None):
        if user == None or num == None:
            embed=discord.Embed(title="Incorrect command usage!", description=".give @user {number}", color=0x00ffff)
            await ctx.send(embed=embed)
            return

        with open("data/money.json") as f:
            money = json.load(f)
            f.close()

        with open("data/bank-queue.json") as f:
            queue = json.load(f)
            f.close()

        try:
            bal = money[str(user.id)]
        except:
            bal = 0

        bal += num

        queue.append(-num)

        money[str(user.id)] = bal

        with open("data/money.json", "w+") as f:
            json.dump(money, f)
            f.close()

        with open("data/bank-queue.json", "w+") as f:
            json.dump(queue, f)
            f.close()

        await ctx.send(f"I have gave {user.mention} {str(num)} Boogie bucks!")

    @give.error
    async def give_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f"❌ Hey, {ctx.author.name} you can't do that!")

    @commands.command()
    @check(is_wiggle_or_luna)
    async def take(self, ctx, user : discord.User = None, num : int = None):
        if user == None or num == None:
            embed=discord.Embed(title="Incorrect command usage!", description=".take @user {number}", color=0x00ffff)
            await ctx.send(embed=embed)
            return

        with open("data/money.json") as f:
            money = json.load(f)
            f.close()

        try:
            bal = money[str(user.id)]
        except:
            bal = 0

        bal -= num

        queue.append(num)

        money[str(user.id)] = bal

        with open("data/money.json", "w+") as f:
            json.dump(money, f)
            f.close()

        with open("data/bank-queue.json", "w+") as f:
            json.dump(queue, f)
            f.close()

        await ctx.send(f"I have taken {str(num)} Boogie bucks from {user.mention}!")

    @take.error
    async def take_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f"❌ Hey, {ctx.author.name} you can't do that!")

    @commands.command()
    @check(is_wiggle_or_luna)
    async def totalreset(self, ctx, num : int = None):
        if num == None:
            embed=discord.Embed(title="Incorrect command usage!", description=".totalreset {number}", color=0x00ffff)
            await ctx.send(embed=embed)
            return

        with open("data/money.json") as f:
            money = json.load(f)
            f.close()

        for user in money:
            money[user] = num

        with open("data/money.json", "w+") as f:
            json.dump(money, f)
            f.close()

        await ctx.send(f"I have reset all Boogie Bucks!")

    @take.error
    async def take_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f"❌ Hey, {ctx.author.name} you can't do that!")




def setup(client):
    client.add_cog(App(client))
