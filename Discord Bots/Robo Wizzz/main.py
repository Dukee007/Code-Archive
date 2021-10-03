import discord, os, json, string
from discord.ext import commands
from discord.ext.commands import has_role, has_permissions, check
from termcolor import colored
import random

TOKEN = "ODEwOTA5OTUyMTgzODk0MTM2.YCqgvg.4MMyjbdXe-0Snb_JzYSYy4yo1pQ"

i = discord.Intents.all()

def get_prefix(client, message):
    f = open("database/prefixs.json")
    prefixs = json.load(f)
    f.close()
    return prefixs[str(message.author.id)]

client = commands.Bot(command_prefix=get_prefix, intents=i)

#############################__events__#############################

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('Free Robux! :D'))
    print("Bot Ready")
    print(f"ID: {str(client.user.id)} NAME: {client.user.name}")

@client.event
async def on_message(message):
    if not message.author.bot:
        await client.process_commands(message)

#############################__functions__#############################

def is_authed(ctx):
    return ctx.author.id in [508372340904558603, 797783028252016651]

#############################__prefix__#############################

@client.command()
async def prefix(ctx, prefix : str = None):
    if prefix == None:
        await ctx.send("You cannot have a blank prefix!")
        return
    if len(prefix) > 1:
        await ctx.send("Your prefix is too long!")
        return
    allowed = True

    print(str("""@#$%^&*().-<_=+/?\|""").split())

    if prefix not in str("""@ # $ % ^ & * ( ) . - < _ = + / ? \ |""").split(" "):
        allowed = False

    if not allowed:
        await ctx.send("Your prefix contains a non allowed character, please change it and try again!")
        return

    f = open("database/prefixs.json")
    prefixs = json.load(f)
    f.close()
    prefixs[str(ctx.author.id)] = prefix
    f = open("database/prefixs.json", "w+")
    json.dump(prefixs, f)
    f.close()

    embed=discord.Embed(title=f"Your custom prefix has been changed to {prefixs[str(ctx.author.id)]} successfully! Ping me if you forget your custom prefix!", color=0x00fffb)
    embed.set_author(name="Your prefix has been changed!")
    embed.set_thumbnail(url='https://media.discordapp.net/attachments/798968646336249928/816354387051151400/das.png')
    embed.set_footer(text="Custom Prefix Changer.")
    await ctx.send(embed=embed)


@client.event
async def on_member_add(member):
    f = open("database/prefixs.json")
    prefixs = json.load(f)
    f.close()
    prefixs[str(member.id)] = "?"
    f = open("database/prefixs.json", "w+")
    json.dump(prefixs, f)
    f.close()

@client.event
async def on_message(message):
    f = open("database/prefixs.json")
    prefixs = json.load(f)
    f.close()

    try:
        test = prefixs[str(message.author.id)]
    except:
        prefixs[str(message.author.id)] = "?"

    f = open("database/prefixs.json", "w+")
    json.dump(prefixs, f)
    f.close()

    if not message.author.bot:
        await client.process_commands(message)

    if message.content.strip().replace(" ", "") == f"<@!{client.user.id}>":
        embed=discord.Embed(title=f"Your custom prefix is {prefixs[str(message.author.id)]} To change your prefix type {prefixs[str(message.author.id)]}prefix [new prefix].", color=0x00fffb)
        embed.set_author(name="Did your forget your custom prefix? Dont worry!")
        embed.set_thumbnail(url='https://media.discordapp.net/attachments/798968646336249928/816354387051151400/das.png')
        embed.set_footer(text="Custom Prefix Changer.")
        await message.channel.send(embed=embed)

#############################__commands__#############################

@client.command()
@check(is_authed)
async def reload(ctx):
    try:
        for i, filename in enumerate(os.listdir("./cogs")):
            if filename.endswith(".py"):
                client.reload_extension(f"cogs.{filename[:-3]}")

        for i, filename in enumerate(os.listdir("./cogs/automod")):
            if filename.endswith(".py"):
                client.reload_extension(f"cogs.automod.{filename[:-3]}")

        for i, filename in enumerate(os.listdir("./cogs/money")):
            if filename.endswith(".py"):
                client.reload_extension(f"cogs.money.{filename[:-3]}")

        await ctx.send(f"Reload successful!")
    except Exception as e:
        await ctx.send(f"Error while reloading!: {e}")

@reload.error
async def reload_error(ctx, error):
    await ctx.send("❌ You can't do that!")

#############################__run__#############################

print(colored('\nStarting Main Cogs\n', 'yellow'))

for i, filename in enumerate(os.listdir("./cogs")):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

print(colored('\nStarting Automod Cogs\n', 'yellow'))

for i, filename in enumerate(os.listdir("./cogs/automod")):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.automod.{filename[:-3]}")

print(colored('\nStarting Money Cogs\n', 'yellow'))

for i, filename in enumerate(os.listdir("./cogs/money")):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.money.{filename[:-3]}")

client.run(TOKEN)
