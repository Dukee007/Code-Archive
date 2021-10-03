import discord, time, asyncio, os, random, json, praw
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, cooldown, MissingPermissions, check, Cog
from discord.utils import get

def is_wiggle_or_luna(ctx):
    return ctx.author.id in [508372340904558603]

class App(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.data = {}
        self.startup()
        print("Money Cog Running")

    #                        <-- functions -->

    async def gainxp(self, msg):
        xp = 1
        xp = xp * self.ammount_of_words_in(msg.content)

        with open("data/money.json") as f:
            money = json.load(f)
            f.close()

        with open("data/bank-queue.json") as f:
            queue = json.load(f)
            f.close()

        try:
            bal = money[str(msg.author.id)]
        except:
            bal = 0

        bal += xp

        queue.append(-xp)

        money[str(msg.author.id)] = bal

        with open("data/money.json", "w+") as f:
            json.dump(money, f)
            f.close()

        with open("data/bank-queue.json", "w+") as f:
            json.dump(queue, f)
            f.close()

    def startup(self):
        with open("data/words.txt") as f:
            allwords = f.readlines()
            f.close()
        self.data["words"] = []
        for word in allwords:
            self.data["words"].append(str(word.replace("\n", "")))
        allwords = None

    def ammount_of_words_in(self, text):
        text = text.strip()
        ammount = 0
        for word in self.data["words"]:
            if word in text:
                ammount += 1
        return ammount

    #                        <-- events -->

    @Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            await self.gainxp(message)


def setup(client):
    client.add_cog(App(client))
