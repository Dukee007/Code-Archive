from matplotlib import pyplot as plt

import random
import json

import discord
from discord.ext import commands, tasks
from discord.ext.commands import check
from discord_slash import SlashCommand, SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_permission, create_option, create_choice
from discord_slash.model import SlashCommandPermissionType


class stockChange(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.load_values()

        self.updateBotcoinPrice.start()


    def load_values(self):
        self.client.stock_values = {}
        self.client.stock_history = {}

        self.client.botcoinMaxValue = 100000
        self.client.botcoinMinValue = 3000

        with open("data/stock_values/botcoin.json") as f:
            botcoinValueDict = json.load(f)

        self.client.stock_values["botcoin"] = botcoinValueDict["value"]

    @tasks.loop(seconds=1)
    async def updateBotcoinPrice(self):
        if random.randint(1,2) == 2:
            self.client.stock_values["botcoin"] += random.randint(random.randint(10, 20), random.randint(25, 30))
        else:
            self.client.stock_values["botcoin"] -= random.randint(random.randint(10, 20), random.randint(25, 30))

        if self.client.stock_values["botcoin"] > self.client.botcoinMaxValue:
            e = random.randint(1,3)
            if e == 1:
                self.client.stock_values["botcoin"] -= random.randint(random.randint(10000, 15000), random.randint(15000, 20000))
            elif e == 2:
                self.client.stock_values["botcoin"] -= random.randint(random.randint(20000, 25000), random.randint(25000, 30000))
            else:
                self.client.stock_values["botcoin"] -= random.randint(random.randint(40000, 45000), random.randint(45000, 50000))
        elif self.client.stock_values["botcoin"] < self.client.botcoinMinValue:
            e = random.randint(1,3)
            if e == 1:
                self.client.stock_values["botcoin"] += random.randint(random.randint(1000, 1500), random.randint(1500, 2000))
            elif e == 2:
                self.client.stock_values["botcoin"] += random.randint(random.randint(2000, 2500), random.randint(2500, 3000))
            else:
                self.client.stock_values["botcoin"] += random.randint(random.randint(4000, 4500), random.randint(4500, 5000))

        newValue = self.client.stock_values["botcoin"]

        with open("data/stock_values/botcoin.json") as f:
            botcoinValueDict = json.load(f)

        botcoinValueDict["value"] = newValue

        with open("data/stock_values/botcoin.json", "w+") as f:
            json.dump(botcoinValueDict, f)

        with open("data/stock_history/botcoin.json") as f:
            botcoinHistoryDict = json.load(f)

        botcoinHistoryDict.append(newValue)

        with open("data/stock_history/botcoin.json", "w+") as f:
            json.dump(botcoinHistoryDict, f)







def setup(client):
    client.add_cog(stockChange(client))
