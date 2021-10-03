import discord, asyncio, random, os
from discord.ext import commands, tasks

TOKEN = "ODEwNDU2MzY2MDkwMTU4MTAw.YCj6Tw.zOa1qdCLFPXgIbcnKNdpIIDtR5k"

intents = discord.Intents().all()

client = commands.Bot(command_prefix=".", intents=intents)

@client.event
async def on_ready():
    print("Online!")
    await startup()

#            <-- FUNCTIONS -->

async def startup():
    pass

#            <-- COGS -->

for i, filename in enumerate(os.listdir("./cogs")):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

#            <-- STARTUP -->

client.run(TOKEN)
