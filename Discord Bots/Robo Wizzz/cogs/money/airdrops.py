import discord, time, asyncio, os, random, json, ezfile
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, cooldown, MissingPermissions, check
from discord.utils import get
from termcolor import colored
from threading import Thread

class App(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.alrdone = []
        print("Money - AirDrops               "+colored('Running', 'green'))

    def is_authed(ctx):
        return ctx.author.id in [797783028252016651, 508372340904558603]

    @commands.command()
    @check(is_authed)
    async def airdrop(self, ctx):
        await ctx.message.delete()
        normal_role = get(ctx.guild.roles, id=804757170867666985)
        await ctx.channel.set_permissions(normal_role, send_messages=True)
        airdrop_channel = self.client.get_channel(823210507908415558)

        msg = await airdrop_channel.send("<@&819908604344664064>\n🎁🎁🎁 AIRDROP 🎁🎁🎁\nType `robucks` for free **MONEY**")

        def check_if_message_is_from_correct_author(m):
            return m.channel.id == 823210507908415558 and m.author.id not in self.alrdone

        t_end = time.time() + 30

        while time.time() < t_end:
            try:
                go = True
                message = await self.client.wait_for('message', check=check_if_message_is_from_correct_author, timeout=10)
            except:
                go = False

            if go:
                if message.content.lower() == "robucks":
                    self.alrdone.append(message.author.id)
                    await message.add_reaction("✅")
                    bals = ezfile.loadjson("money_databases/bals.json")

                    try:
                        bals[str(message.author.id)]["wallet"] += 20
                    except KeyError:
                        bals[str(message.author.id)] = {"bank": 30, "wallet": 20}
                        bals[str(message.author.id)]["wallet"] += 20

                    ezfile.savejson("money_databases/bals.json", bals)
                else:
                    if not message.author.bot:
                        await message.delete()

        await airdrop_channel.send("🎁🎁🎁 AIRDROP 🎁🎁🎁\n**This airdrop is over!**")
        self.alrdone = []
        await ctx.channel.set_permissions(normal_role, send_messages=False)



def setup(client):
    client.add_cog(App(client))
