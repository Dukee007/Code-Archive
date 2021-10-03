import discord
import time
import asyncio
import os
import random
import json
import youtube_dl
import functools
import itertools
import math
import shutil
import locale
import requests
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, cooldown, MissingPermissions, check
from discord.utils import get
from datetime import datetime, date
from itertools import cycle
from youtubesearchpython import SearchVideos

TOKEN = "ODAwNjY2NDUzNjYxNTgxMzg0.YAVcvg.XKn5nUwk3m3Z3DkYnLEsj_RaLaM"
client = commands.Bot(command_prefix="b2!")
client.remove_command("help")

@client.event
async def on_ready():
    all_guild_num = 0
    for guild in client.guilds:
        all_guild_num += 1
    s_num = 0
    print(
        f'\nLogged in as: {client.user} - {client.user.id}\nVersion: {discord.__version__}\n')
    print(f"Currently in {all_guild_num} servers!")

#############################__important_funtions__#############################
def sendProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '⠀' * (length - filledLength)
    return(f'\r{prefix} |{bar}| {percent}% {suffix}')


def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '_' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    if iteration == total:
        print()

@client.command()
async def lyrics(ctx, *, songname):
    songname = songname.replace(" ", "+")
    try:
        r = requests.get(f"https://rovelapi.glitch.me/lyrics?name={songname}")
        l = json.loads(r.text)
        l = l["lyrics"]
        if len(l) > 1500:
            l = [l[i:i+1500] for i in range(0, len(l), 1500)]
            for ll in l:
                await ctx.send(f"```{ll}```")
        else:
            await ctx.send(f"```{l}```")
    except Exception as e:
        await ctx.send("Cannot get the lyrics to this song!")
        await ctx.send(f"```{r.text}```")



#############################__run__#############################

l_p = len(os.listdir("./cogs/__pycache__"))
l_m = len(os.listdir("./cogs"))

print("Resetting cache...")
printProgressBar(0, l_p, prefix = 'Progress:', suffix = 'Complete', length = 50)
os.chdir("cogs/")
for i, filename in enumerate(os.listdir("./__pycache__")):
    time.sleep(0.08)
    printProgressBar(i + 1, l_p, prefix = 'Progress:', suffix = f'Complete - Removeing: {filename}', length = 50)
try:
    shutil.rmtree("__pycache__")
except:
    pass
os.chdir("..")

print("Loading Cogs...")
printProgressBar(0, l_m, prefix = 'Progress:', suffix = 'Complete', length = 50)
for i, filename in enumerate(os.listdir("./cogs")):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")
    printProgressBar(i + 1, l_m, prefix = 'Progress:', suffix = f'Complete - Loading: {filename}', length = 50)

os.system("cls")

client.run(TOKEN)
