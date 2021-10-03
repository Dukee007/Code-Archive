from matplotlib import pyplot as plt
from bs4 import BeautifulSoup

import random
import json
import os
import asyncio
import requests

import discord
from discord.ext import commands, tasks
from discord.ext.commands import check
from discord_slash import SlashCommand, SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_permission, create_option, create_choice
from discord_slash.model import SlashCommandPermissionType


class stockGraphs(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def alltime(self, ctx):
        randomCode = random.randint(111111111111, 999999999999)

        with open("data/stock_history/botcoin.json") as f:
            botcoinHistoryDict = json.load(f)

        plt.plot(range(len(botcoinHistoryDict)), botcoinHistoryDict)

        plt.xlabel('Seconds')
        plt.ylabel('Value (GBP)')

        plt.title('Botcoin Value (All Time)')

        plt.savefig(f'data/temp/{str(ctx.author.id)}_{str(randomCode)}_tempGraph.png')

        await ctx.message.reply(file=discord.File(f'data/temp/{str(ctx.author.id)}_{str(randomCode)}_tempGraph.png'))
        await asyncio.sleep(2)
        os.remove(f'data/temp/{str(ctx.author.id)}_{str(randomCode)}_tempGraph.png')

    @commands.command()
    async def live(self, ctx, time : int = 5):
        randomCode = random.randint(111111111111, 999999999999)

        with open("data/stock_history/botcoin.json") as f:
            botcoinHistoryDict = json.load(f)

        plt.plot(range(len(botcoinHistoryDict)), botcoinHistoryDict)

        plt.xlabel('Seconds')
        plt.ylabel('Value (GBP)')

        plt.title('Botcoin Value (All Time)')

        plt.savefig(f'data/temp/{str(ctx.author.id)}_{str(randomCode)}_tempGraph.png')

        post_base_url = r"https://api.anonfiles.com/upload?token=06eaf77f939e5624"
        file_url = f'data/temp/{str(ctx.author.id)}_{str(randomCode)}_tempGraph.png'

        f = open(file_url, 'rb')
        files = {"file": (file_url, f)}
        re = requests.post(post_base_url, files = files)
        r = requests.get(json.loads(re.text)["data"]["file"]["url"]["full"])
        soup = BeautifulSoup(r.text, features="lxml")
        images = soup.find_all('img')
        for img in images:
            if img.has_attr('src'):
                if json.loads(re.text)["data"]["file"]["metadata"]["id"] in img["src"]:
                    imgScr = img["src"]

        embed = discord.Embed(title="Botcoin Value", description="All Time")
        embed.set_image(url=imgScr)

        liveEdit = await ctx.message.reply(embed = embed)

        await asyncio.sleep(time)

        while True:
            randomCode = random.randint(111111111111, 999999999999)

            with open("data/stock_history/botcoin.json") as f:
                botcoinHistoryDict = json.load(f)

            plt.plot(range(len(botcoinHistoryDict)), botcoinHistoryDict)

            plt.xlabel('Seconds')
            plt.ylabel('Value (GBP)')

            plt.title('Botcoin Value (All Time)')

            plt.savefig(f'data/temp/{str(ctx.author.id)}_{str(randomCode)}_tempGraph.png')

            post_base_url = r"https://api.anonfiles.com/upload?token=06eaf77f939e5624"
            file_url = f'data/temp/{str(ctx.author.id)}_{str(randomCode)}_tempGraph.png'

            f = open(file_url, 'rb')
            files = {"file": (file_url, f)}
            re = requests.post(post_base_url, files = files)
            r = requests.get(json.loads(re.text)["data"]["file"]["url"]["full"])
            soup = BeautifulSoup(r.text, features="lxml")
            images = soup.find_all('img')
            for img in images:
                if img.has_attr('src'):
                    if json.loads(re.text)["data"]["file"]["metadata"]["id"] in img["src"]:
                        imgScr = img["src"]

            embed = discord.Embed(title="Botcoin Value", description="All Time")
            embed.set_image(url=imgScr)

            await liveEdit.edit(embed = embed)
            await asyncio.sleep(time)



def setup(client):
    client.add_cog(stockGraphs(client))
