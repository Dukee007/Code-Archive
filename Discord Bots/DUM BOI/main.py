import discord, os
from discord.ext import commands, tasks

TOKEN = "ODAwNDYxMjg4OTY5ODYzMjM5.YASdqw.l7ldxA6Whc4rQuy0y0qtQAyRZQ8"

intents = discord.Intents().all()

client = commands.Bot(command_prefix=".", intents=intents)

data = {}

#############################__start__#############################

@client.event
async def on_ready():
    print("Bot Running!")
    print(f"ID: {str(client.user.id)}, NAME: {client.user.name}")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Over Toast's Server!"))

#############################__events__#############################

@client.event
async def on_message(message):
    if not message.author.bot:
        await client.process_commands(message)

#############################__run__#############################

for i, filename in enumerate(os.listdir("./cogs")):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

client.run(TOKEN)
