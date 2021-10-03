import os
from itertools import cycle

import discord
import pymongo
from discord.ext import commands, tasks
from discord.ext.commands import check
from discord_slash import SlashCommand
from progress.bar import Bar
from termcolor import colored
from configparser import ConfigParser

main_parser = ConfigParser()

main_parser.read('config.ini')

TOKEN = main_parser.get('API', 'token')


client = commands.Bot(command_prefix=commands.when_mentioned_or("."), intents=discord.Intents.all(), case_insensitive=True)

client.remove_command("help")

slash = SlashCommand(client, sync_commands=True, sync_on_cog_reload=True)

status = ""
first = 0
cog_num = 0


#                               <-- events -->

@client.event
async def on_ready():
    global first

    await client.change_presence(status=discord.Status.offline,
                                 activity=discord.Activity(type=discord.ActivityType.watching, name="commands!"))

    print(colored(f'Discord ping recieved...\n', 'yellow'))
    print(colored(f'Starting Bot...\n', 'yellow'))

    print(colored(f'Bot running with the following application:\n', 'yellow'))
    print("Application ID: " + colored(str(client.user.id), "green")
          + "\nClient Username: " + colored(str(client.user.name), "green")
          + "\nLoaded Cogs: " + colored(str(cog_num), "green"))

    for i in client.guilds:
        print(i.name)


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
            print(colored(f'Loading cogs...\n', 'yellow'))

            for cogFolder in os.listdir('cogs'):
                print(colored(f'LOADING {str(cogFolder).upper()}', 'white'))

                for cogSubFolder in os.listdir(f'cogs/{cogFolder}'):
                    print(colored(f'    LOADING {str(cogSubFolder).upper()}', 'green'))

                    with Bar(colored(f'        LOADING COGS', 'green'),
                             max=len(os.listdir(f'cogs/{cogFolder}/{cogSubFolder}'))) as progressBar:
                        for cogPath, cogName in enumerate(os.listdir(f"cogs/{cogFolder}/{cogSubFolder}")):
                            if cogName.endswith(".py"):
                                client.reload_extension(f"cogs.{cogFolder}.{cogSubFolder}.{cogName[:-3]}")

                            progressBar.next()
                print()

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


@client.command()
@check(is_authed)
async def load(ctx, module: str = None):
    try:
        client.load_extension(f"cogs.{module}")
        await ctx.send(f"Load successful!")
    except Exception as e:
        await ctx.send(f"Error while loading!: {e}")


#                               <-- run -->

print(colored(f'Loading cogs...\n', 'yellow'))

for mainfolder in os.listdir('cogs'):
    print(colored(f'LOADING {str(mainfolder).upper()}', 'white'))

    with Bar(colored(f'        LOADING COGS', 'green'), max=len(os.listdir(f'cogs/{mainfolder}'))) as bar:
        for i, filename in enumerate(os.listdir(f"cogs/{mainfolder}")):
            if filename.endswith(".py"):
                client.load_extension(f"cogs.{mainfolder}.{filename[:-3]}")
                cog_num += 1

            bar.next()
    print()

print(colored(f'Cogs loaded...\n', 'yellow'))

print(colored(f'Pinging discord...\n', 'yellow'))

client.run(TOKEN)
