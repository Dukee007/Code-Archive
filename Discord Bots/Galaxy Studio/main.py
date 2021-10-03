import discord, os, json, random, asyncio
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, check
from discord.utils import get
from AntiSpam import AntiSpamHandler

TOKEN = "Nzk5MDYwODg1MTMzNTkwNTgw.X_-FcA.eZ3Xzgct8yeL2TPVb536fdmsVJs"

intents = discord.Intents().all()
client = commands.Bot(command_prefix=".", intents=intents)
client.remove_command("help")
client.handler = AntiSpamHandler(client)

data = {}

#############################__start__#############################

@client.event
async def on_ready():
    print("Bot Running!")
    print(f"ID: {str(client.user.id)}, NAME: {client.user.name}")
    start()


#############################__events__#############################

@client.event
async def on_message(message):
    global data
    if not message.author.bot:
        if not message.author.id in data["filter_immune"] and message.channel.id in data["antispam_channels"]:
            await client.handler.propagate(message)
        if message.author.id not in data["blacklist"]:
            await client.process_commands(message)
        else:
            if "." in message.content:
                await message.channel.send("You are blacklisted!")

#############################__functions__#############################

def start():
    global data
    with open("setup/antispam_channels.json") as f:
        data["antispam_channels"] = json.load(f)
        f.close()
    with open("setup/filter_immune.json") as f:
        data["filter_immune"] = json.load(f)
        f.close()
    with open("setup/blacklist.json") as f:
        data["blacklist"] = json.load(f)
        f.close()


def is_luna(ctx):
    return ctx.author.id == 508372340904558603

#############################__commands__#############################

@client.command()
@check(is_luna)
async def restart(ctx):
    await ctx.send("RESTARTING")
    await asyncio.sleep(2)
    await ctx.send("RELOADING")
    await reload(ctx)
    await asyncio.sleep(2)
    await ctx.send("RESTART DONE!!")

@restart.error
async def restart_error(ctx, error):
    await ctx.send("❌ You can't do that!, only LUNA can.")

#############################__cogs__#############################

@client.command()
@check(is_luna)
async def reload(ctx):
    try:
        for i, filename in enumerate(os.listdir("./cogs")):
            if filename.endswith(".py"):
                client.reload_extension(f"cogs.{filename[:-3]}")

        for i, filename in enumerate(os.listdir("./cogs/money")):
            if filename.endswith(".py"):
                client.reload_extension(f"cogs.money.{filename[:-3]}")
        await ctx.send(f"Reload successful!")
    except Exception as e:
        await ctx.send(f"Error while reloading!: {e}")

@reload.error
async def reload_error(ctx, error):
    await ctx.send("❌ You can't do that!, only LUNA can.")

@client.command()
@check(is_luna)
async def blacklist(ctx, user : discord.User):
    if user.id == 508372340904558603:
        await ctx.send("no")
        return
    global data
    with open("setup/blacklist.json") as f:
        data["blacklist"] = json.load(f)
        f.close()

    data["blacklist"].append(user.id)

    with open("setup/blacklist.json", "w+") as f:
        json.dump(data["blacklist"], f)
        f.close()

    await ctx.send("User has been blacklisted!")

@blacklist.error
async def blacklist_error(ctx, error):
    await ctx.send("❌ You can't do that!, only LUNA can.")

@client.command()
@check(is_luna)
async def unblacklist(ctx, user : discord.User):
    global data
    with open("setup/blacklist.json") as f:
        data["blacklist"] = json.load(f)
        f.close()

    data["blacklist"].remove(user.id)

    with open("setup/blacklist.json", "w+") as f:
        json.dump(data["blacklist"], f)
        f.close()

    await ctx.send("User has been removed from the blacklist!")

@unblacklist.error
async def unblacklist_error(ctx, error):
    await ctx.send("❌ You can't do that!, only LUNA can.")




#############################__run__#############################

for i, filename in enumerate(os.listdir("./cogs")):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

for i, filename in enumerate(os.listdir("./cogs/money")):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.money.{filename[:-3]}")

client.run(TOKEN)
