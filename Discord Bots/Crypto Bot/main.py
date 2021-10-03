from itertools import cycle
from termcolor import colored

import os
import json

import discord
from discord.ext import commands, tasks
from discord.ext.commands import check
from discord_slash import SlashCommand, SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_permission, create_option, create_choice
from discord_slash.model import SlashCommandPermissionType

TOKEN = "ODU5NTM3MTAzOTk2ODQ2MDkw.YNuITw.PWKYbX4dceiQofI3Ock9olbkhHY"

client = commands.Bot(command_prefix=commands.when_mentioned_or('c!'), intents=discord.Intents.all(), case_insensitive=True)
client.remove_command("help")

slash = SlashCommand(client, sync_commands=True, sync_on_cog_reload=True)

status = ""
first = 0

#                               <-- events -->

@client.event
async def on_ready():
    global status, first

    print("ID: " + colored(f"{str(client.user.id)}", "green") + " NAME: " + colored(f"{client.user.name}", "green"))

    status = cycle([f"{str(len(client.users))} users!", f"{str(len(client.guilds))} servers!", "stocks!", "botcoin!"])

    if first == 0:
        change_status.start()
        first = 1


#                               <-- tasks -->

@tasks.loop(seconds=30)
async def change_status():
    global status
    await client.change_presence(status=discord.Status.dnd,
                                 activity=discord.Activity(type=discord.ActivityType.watching, name=next(status)))

#                               <-- functions -->

def is_authed(ctx):
    return ctx.author.id in [508372340904558603]


#                               <-- events -->

@client.event
async def on_message(message):
    if not message.author.bot:
        await client.process_commands(message)


#                               <-- commands -->

@client.command()
@check(is_authed)
async def reload(ctx, module: str = None):
    if module is None:
        try:
            for cogFolder in os.listdir('cogs'):
                print(colored(f'\nStarting {cogFolder} Cogs\n', 'yellow'))

                for cogPath, cogFilename in enumerate(os.listdir(f"./cogs/{cogFolder}")):
                    if cogFilename.endswith(".py"):
                        client.reload_extension(f"cogs.{cogFolder}.{cogFilename[:-3]}")

            await ctx.send(f"Reload successful!")
        except Exception as e:
            await ctx.send(f"Error while reloading!: {e}")
    else:
        try:
            client.reload_extension(f"cogs.{module}")
            await ctx.send(f"Reload successful!")
        except Exception as e:
            await ctx.send(f"Error while reloading!: {e}")

@reload.error
async def reload_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You can't do that!")
    else:
        raise error


#                               <-- run -->

for folder in os.listdir('cogs'):
    print(colored(f'\nStarting {folder} Cogs', 'yellow'))

    for i, filename in enumerate(os.listdir(f"./cogs/{folder}")):
        if filename.endswith(".py"):
            print(colored(f'    Starting {filename[:-3]}', 'green'))
            client.load_extension(f"cogs.{folder}.{filename[:-3]}")
print()

client.run(TOKEN)
