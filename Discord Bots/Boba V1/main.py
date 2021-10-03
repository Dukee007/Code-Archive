import discord, os, json, string, asyncio
from discord.ext import commands, tasks
from discord.ext.commands import has_role, has_permissions, check
from termcolor import colored
from itertools import cycle
import random

TOKEN = "no"

i = discord.Intents.all()

client = commands.Bot(command_prefix=".", intents=i)
client.remove_command("help")

status = ""

#############################__events__#############################

@client.event
async def on_ready():
    global status

    print("ID: "+colored(f"{str(client.user.id)}", "green")+" NAME: "+colored(f"{client.user.name}", "green"))

    status = cycle([f"over {str(len(client.guilds[0].members))} members!", "out for raids!", "for new heists!"])

    try:
        change_status.start()
    except:
        pass

#############################__tasks__#############################

@tasks.loop(seconds=7)
async def change_status():
    global status
    await client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=next(status)))

#############################__functions__#############################

def is_authed(ctx):
    return ctx.author.id in [508372340904558603]

#############################__messages__#############################

@client.event
async def on_message(message):
    if not message.author.bot:
        await client.process_commands(message)

#############################__commands__#############################

@client.command()
@check(is_authed)
async def reload(ctx, module : str = None):
    if module == None:
        try:
            for folder in os.listdir('cogs'):
                print(colored(f'\nStarting {folder} Cogs\n', 'yellow'))

                for i, filename in enumerate(os.listdir(f"./cogs/{folder}")):
                    if filename.endswith(".py"):
                        client.reload_extension(f"cogs.{folder}.{filename[:-3]}")

            await ctx.send(f"Reload successful!")
        except Exception as e:
            await ctx.send(f"Error while reloading!: {e}")
    else:
        try:
            client.reload_extension(f"cogs.{module}")
            await ctx.send(f"Reload successful!")
        except Exception as e:
            await ctx.send(f"Error while reloading!: {e}")

@client.command()
@check(is_authed)
async def load(ctx, module : str = None):
        try:
            client.load_extension(f"cogs.{module}")
            await ctx.send(f"Load successful!")
        except Exception as e:
            await ctx.send(f"Error while loading!: {e}")

@reload.error
async def reload_error(ctx, error):
    await ctx.send("❌ You can't do that!")

#############################__run__#############################

for folder in os.listdir('cogs'):
    print(colored(f'\nStarting {folder} Cogs\n', 'yellow'))

    for i, filename in enumerate(os.listdir(f"./cogs/{folder}")):
        if filename.endswith(".py"):
            client.load_extension(f"cogs.{folder}.{filename[:-3]}")

print("\n")

client.run(TOKEN)
