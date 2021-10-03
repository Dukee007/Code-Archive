import asyncio
from configparser import ConfigParser

import discord
from discord.ext import commands
from discord.ext.commands import check

TOKEN = 'Nzg4NTE1NzQ3NTc1NjI3Nzg2.X9kohA.YXNm0uRQBlYEXzFndMY_D0BW9fk'

parser = ConfigParser()
parser.read('config.ini')

client = commands.Bot(command_prefix='s!')

emojis = {
    "wave": "👋",
    "paper": "📜",
    "bell": "🔔",
    "message": "💬",
    "camera": "📷",
    "laugh": "🤣",
    "voice": "🔊",
    "staff": "🛑",
}


def is_staff(ctx):
    return ctx.author.id in [508372340904558603]


@client.event
async def on_ready():
    print("Bot online!")

    if parser.get("custom-bot-status", 'enabled') == "true":
        if parser.get("custom-bot-status", 'statustype') == "playing":
            await client.change_presence(activity=discord.Game(name=parser.get("custom-bot-status", 'customstatus')))

        elif parser.get("custom-bot-status", 'statustype') == "streaming":
            await client.change_presence(
                activity=discord.Streaming(name=parser.get("custom-bot-status", 'customstatus'),
                                           url=parser.get("custom-bot-status", 'streamurl')))

        elif parser.get("custom-bot-status", 'statustype') == "listening":
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,
                                                                   name=parser.get("custom-bot-status",
                                                                                   'customstatus')))

        elif parser.get("custom-bot-status", 'statustype') == "watching":
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                                   name=parser.get("custom-bot-status",
                                                                                   'customstatus')))

        else:
            await client.change_presence(activity=discord.Game(name="Error- Status Type Not Found"))

    else:
        await client.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name="Over Your Server!"))


@client.command()
@check(is_staff)
async def serverstatus(ctx):
    try:
        if parser.get('serverstatus') == "on":
            await ctx.send("Please choose an option: [update, off, on]")
        msg = await client.wait_for('message', check=lambda message: message.author == ctx.author)

    except asyncio.TimeoutError:
        await ctx.send("Timed Out!")
        return


@client.command()
async def test(ctx):
    print(parser.get("serverstatus", 'enabled'))


client.run(TOKEN)
