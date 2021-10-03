import discord, time, asyncio, os, random, json
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, cooldown, MissingPermissions, check, Cog
from discord.utils import get

class App(commands.Cog):
    def __init__(self, client):
        self.client = client
        print("Counting Cog Running")

    @Cog.listener()
    async def on_message(self, message):
        if message.channel.id != 807281186623062066:
            return
        if message.author.bot:
            await message.add_reaction("❌")
            await asyncio.sleep(0.2)
            await message.delete()
            return

        with open("data/count.json") as f:
            num = json.load(f)
            f.close()

        try:
            new_num = int(message.content)
        except:
            await message.add_reaction("❌")
            await asyncio.sleep(0.2)
            await message.delete()
            return

        if new_num != num["num"]+1:
            await message.add_reaction("❌")
            await asyncio.sleep(0.2)
            await message.delete()
            return

        if num["old"] == message.author.id:
            await message.add_reaction("❌")
            await asyncio.sleep(0.2)
            await message.delete()
            return

        num["num"] = new_num
        num["old"] = message.author.id

        await message.add_reaction("✅")

        if new_num == num["target"]:
            await message.pin()
            num["target"] = num["target"] + 100

        with open("data/count.json", "w+") as f:
            json.dump(num, f)
            f.close()



def setup(client):
    client.add_cog(App(client))
