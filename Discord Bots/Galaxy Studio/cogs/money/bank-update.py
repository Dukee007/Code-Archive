import discord, time, asyncio, os, random, json
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, cooldown, MissingPermissions, check, Cog
from discord.utils import get

def is_wiggle_or_luna(ctx):
    return ctx.author.id in [508372340904558603]

class App(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.update.start()
        self.first = True
        print("Bank Update Cog Running")


    @tasks.loop(seconds=3)
    async def update(self):
        if self.first:
            await asyncio.sleep(5)
            bank_channel = get(self.client.guilds[0].channels, id=807668843232362508)
            messages = await bank_channel.history(limit=10).flatten()
            await messages[0].edit(content="Loading...")
            self.first = False

        bank_channel = get(self.client.guilds[0].channels, id=807668843232362508)

        with open("data/bank-queue.json") as f:
            queue = json.load(f)
            f.close()
        with open("data/bank-queue.json", "w+") as f:
            f.write("[]")
            f.close()
        with open("data/bankbal.txt") as f:
            bankbal = int(f.read())
            f.close()

        sum = bankbal

        for action in queue:
            sum = sum + action

        with open("data/bankbal.txt", "w+") as f:
            f.write(str(sum))
            f.close()

        messages = await bank_channel.history(limit=10).flatten()

        await messages[0].edit(content=f"BANK: {str(sum)}")







def setup(client):
    client.add_cog(App(client))
