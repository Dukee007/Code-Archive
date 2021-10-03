import discord, time, os, praw, random, json, shutil, urllib, glob, operator
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, MissingPermissions, check
from discord.utils import get
from itertools import cycle
import datetime as dt
from datetime import datetime
from heapq import nlargest

TOKEN = "NjkzNzg5NjI5MDM5NzcxNzM5.XoCL8Q.DsdneGN8VFsJ5yeDQhZuk2kVlzs"

def it_is_me(ctx):
    return ctx.message.author.id == 508372340904558603

def get_prefix(client, message):
    with open("prefixs.json", "r") as all_prefixs:
        prefixs = json.load(all_prefixs)
    return prefixs[str(message.guild.id)]

client = commands.Bot(command_prefix = get_prefix)

client.remove_command("help")

status = cycle(["for your next command!", "over your discord server!", "over all my users", "Rick and Morty"])

embeddata = {}
embeddata["icon"] = "http://luna-development.orgfree.com/data/discord/meme6/logo.jpg"
embeddata["name"] = "Meme6"
embeddata["version"] = "2.0"

@client.event
async def on_ready():
    change_status.start()
    s_num = 0
    print(f'\nLogged in as: {client.user} - {client.user.id}\nVersion: {discord.__version__}\n')
    for s in client.guilds:
        s_num += 1
    print(f"Currently in {s_num} servers!")

##########################################################################___COGS___################################################################################################

@client.command()
@check(it_is_me)
async def reloadexentions(ctx):
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            client.reload_extension(f"cogs.{filename[:-3]}")

@client.command()
@check(it_is_me)
async def reload(ctx, extention):
    client.reload_extension(f"cogs.{extention}")

@client.command()
@check(it_is_me)
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")

@client.command()
@check(it_is_me)
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")

##########################################################################___STATUS_SYSTEM___################################################################################################

@tasks.loop(seconds=20)
async def change_status():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=next(status)))

##########################################################################___PERFIX_SYSTEM___################################################################################################

@client.command()
async def changeprefix(ctx, prefix):
    await ctx.message.guild.get_member(client.user.id).edit(nick=f"[{prefix}] Meme6")
    with open("prefixs.json", "r") as all_prefixs:
        prefixs = json.load(all_prefixs)

    prefixs[str(ctx.guild.id)] = prefix

    with open("prefixs.json", "w") as f:
        json.dump(prefixs, f, indent = 4)
    await ctx.send(f"Prefix for Guild {ctx.guild.id} is now {prefix}")

@client.event
async def on_guild_join(guild):
    await guild.get_member(client.user.id).edit(nick="[.] Meme6")
    with open("prefixs.json", "r") as all_prefixs:
        prefixs = json.load(all_prefixs)

    prefixs[str(guild.id)] = "."

    with open("prefixs.json", "w") as f:
        json.dump(prefixs, f, indent = 4)
    #################################################
    os.chdir("money/")
    folder = str(str(guild.id)+"/")
    try:
        os.chdir(folder)
    except:
        os.mkdir(folder)
        os.chdir(folder)
    for user in guild.members:
        if user.bot == True:
            pass
        else:
            f = open(f"__{user.id}__.json", "w+")
            f.write("500")
            f.close()
    os.chdir("..")
    os.chdir("..")
    ###################################################
    os.chdir("levels/")
    folder = str(str(guild.id)+"/")
    try:
        os.chdir(folder)
    except:
        os.mkdir(folder)
        os.chdir(folder)
    for user in guild.members:
        if user.bot == True:
            pass
        else:
            f = open(f"__{user.id}__.current", "w+")
            f.write("0")
            f.close()
            f = open(f"__{user.id}__.level", "w+")
            f.write("0")
            f.close()
            f = open(f"__{user.id}__.target", "w+")
            f.write("50")
            f.close()
    os.chdir("..")
    os.chdir("..")

@client.event
async def on_guild_remove(guild):
    with open("prefixs.json", "r") as all_prefixs:
        prefixs = json.load(all_prefixs)

    prefixs.pop(str(guild.id))

    with open("prefixs.json", "w") as f:
        json.dump(prefixs, f, indent = 4)
    #################################################
    os.chdir("money/")
    folder = str(str(guild.id)+"/")
    try:
        os.chdir(folder)
    except:
        return
    for file in glob.glob("*.json"):
        os.remove(file)
    os.chdir("..")
    os.chdir("..")
    ##################################################
    os.chdir("levels/")
    folder = str(str(guild.id)+"/")
    try:
        os.chdir(folder)
    except:
        os.mkdir(folder)
        os.chdir(folder)
    for file in glob.glob("*.target"):
        os.remove(file)
    for file in glob.glob("*.current"):
        os.remove(file)
    for file in glob.glob("*.level"):
        os.remove(file)
    os.chdir("..")
    os.chdir("..")
##########################################################################___LEVEL_SYSTEM___################################################################################################

@client.command()
async def levelsetup(ctx):
    os.chdir("levels/")
    folder = str(str(ctx.message.guild.id)+"/")
    try:
        os.chdir(folder)
    except:
        os.mkdir(folder)
        os.chdir(folder)
    for user in ctx.message.guild.members:
        if user.bot == True:
            pass
        else:
            f = open(f"__{user.id}__.current", "w+")
            f.write("0")
            f.close()
            f = open(f"__{user.id}__.level", "w+")
            f.write("0")
            f.close()
            f = open(f"__{user.id}__.target", "w+")
            f.write("50")
            f.close()
    os.chdir("..")
    os.chdir("..")

@client.event
async def on_member_join(member):
    if member.bot == True:
        return
    os.chdir("money/")
    folder = str(str(member.guild.id)+"/")
    try:
        os.chdir(folder)
    except:
        os.mkdir(folder)
        os.chdir(folder)

    f = open(f"__{member.id}__.json", "w+")
    f.write("500")
    f.close()
    os.chdir("..")
    os.chdir("..")
    ################################################
    os.chdir("levels/")
    folder = str(str(member.guild.id)+"/")
    try:
        os.chdir(folder)
    except:
        os.mkdir(folder)
        os.chdir(folder)
    f = open(f"__{member.id}__.current", "w+")
    f.write("0")
    f.close()
    f = open(f"__{member.id}__.level", "w+")
    f.write("0")
    f.close()
    f = open(f"__{member.id}__.target", "w+")
    f.write("50")
    f.close()
    os.chdir("..")
    os.chdir("..")

@client.command()
async def top(ctx):
    os.chdir("levels/")
    folder = str(str(ctx.message.guild.id)+"/")
    try:
        os.chdir(folder)
    except:
        os.mkdir(folder)
        os.chdir(folder)
    stats = {}
    for file in glob.glob("*.current"):
        id = file.replace("_", "").replace(".current", "")
        f = open(file)
        messages = f.read()
        f.close()
        stats[str(id)] = str(messages)
    three_largest = nlargest(3, stats, key=stats.get)
    first = int(three_largest[0])
    seccond = int(three_largest[1])
    third = int(three_largest[2])
    first = ctx.message.guild.get_member(first)
    seccond = ctx.message.guild.get_member(seccond)
    third = ctx.message.guild.get_member(third)
    embed=discord.Embed(title="Rank Leaderboard")
    embed.set_author(name=embeddata["name"], icon_url=embeddata["icon"])
    embed.add_field(name="First", value=first.mention, inline=False)
    embed.add_field(name="Seccond:", value=seccond.mention, inline=False)
    embed.add_field(name="Third:", value=third.mention, inline=False)
    embed.set_footer(text=embeddata["name"]+" ["+embeddata["version"]+"]")
    await ctx.send(embed=embed)
    os.chdir("..")
    os.chdir("..")

@client.command()
async def rank(ctx, who=None):
    if who == None:
        who = str(ctx.message.author.id)
    x = who.replace("@", "").replace("!", "").replace(">", "").replace("<", "")
    x = int(x)
    x = ctx.message.guild.get_member(x)
    if x.bot == True:
        return
    os.chdir("levels/")
    folder = str(str(ctx.message.guild.id)+"/")
    try:
        os.chdir(folder)
    except:
        os.mkdir(folder)
        os.chdir(folder)
    if who == None:
        who = int(ctx.message.author.id)
    else:
        who = who.replace("@", "").replace("!", "").replace(">", "").replace("<", "")
        who = int(who)
    f = open(f"__{who}__.current")
    old_current = int(f.read())
    f.close()
    f = open(f"__{who}__.level")
    old_level = int(f.read())
    f.close()
    f = open(f"__{who}__.target")
    old_target = int(f.read())
    f.close()
    x = old_target-old_current
    w = ctx.message.guild.get_member(who)
    embed=discord.Embed(title=f"{w.name}'s Rank")
    embed.set_author(name=w, icon_url=w.avatar_url)
    embed.add_field(name="Level:", value=old_level, inline=False)
    embed.add_field(name="Messages in server:", value=old_current, inline=True)
    embed.add_field(name="Messages until level up:", value=x, inline=True)
    embed.set_footer(text=embeddata["name"]+" ["+embeddata["version"]+"]")
    await ctx.send(embed=embed)
    os.chdir("..")
    os.chdir("..")

@client.event
async def on_message(message):
    await client.process_commands(message)
    if message.author.bot == True:
        return
    os.chdir(r"C:\Users\lagde\OneDrive\Desktop\Meme6-BOT\levels")
    folder = str(str(message.guild.id)+"/")
    try:
        os.chdir(folder)
    except:
        os.mkdir(folder)
        os.chdir(folder)
    f = open(f"__{message.author.id}__.current")
    old_current = int(f.read())
    f.close()
    f = open(f"__{message.author.id}__.level")
    old_level = int(f.read())
    f.close()
    f = open(f"__{message.author.id}__.target")
    old_target = int(f.read())
    f.close()
    if old_current > old_target:
        new_target = str(old_target+100)
        new_current = str(old_current+1)
        new_level = str(old_level+1)
        await message.channel.send(f"Congrats {message.author.mention}, You have reached level {new_level}!")
    else:
        new_target = str(old_target)
        new_current = str(old_current+1)
        new_level = str(old_level)
    f = open(f"__{message.author.id}__.current", "w+")
    f.write(new_current)
    f.close()
    f = open(f"__{message.author.id}__.level", "w+")
    f.write(new_level)
    f.close()
    f = open(f"__{message.author.id}__.target", "w+")
    f.write(new_target)
    f.close()
    os.chdir("..")
    os.chdir("..")

##########################################################################___LOG_SYSTEM___####################################################################################################

@client.command()
async def test(ctx, s):
    print(s)

@client.command()
async def log(ctx, choice=None, channel=None):
    if choice == None:
        await ctx.send("You need to tell me to trun it on or off!")
        return
    elif choice == "off" or choice == "no":
        await ctx.send(f"Logging system for guild {ctx.message.guild.id} now off!")
        with open("log_channels.json")as f:
            data = json.load(f)

        data.pop(str(ctx.message.guild.id))

        with open("log_channels.json", "w+")as f:
            json.dump(data, f)
        return

    if channel == None:
        await ctx.send("You need to tell me what channel!")
        return
    channel = channel.replace("<#", "").replace(">", "")
    chennel = client.get_channel(channel)
    with open("log_channels.json")as f:
        data = json.load(f)

    data[str(ctx.message.guild.id)] = channel.id

    with open("log_channels.json", "w+")as f:
        json.dump(data, f)

def get_log_channel_id(message):
    guild = message.guild
    channel = message.channel
    user = message.author


@client.event
async def on_message_delete(message):
    channel = client.get_channel(get_log_channel_id(message))

##########################################################################___ERROR_SYSTEM___################################################################################################
'''
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You need to higher permissions to use this command! ☹️")
    elif isinstance(error, discord.errors.HTTPException):
        await ctx.send("Sorry i'm having troble connecting to discord right now!")
    else:
        error_code = random.randint(10000, 999999999999)
        await ctx.send(f"Hey looks like you have found an error! Please contact meme6 support by joining our discord server and giveing a staff member this code: {error_code}")

        f = open("errors.txt")
        data = f.read()
        f.close()
        f = open("errors.txt", "w+")
        f.write(data + "\n" + f"Error Code: {error_code}, Error: {error}")
'''
#########################################################################################################################################################################################################

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")


client.run(TOKEN)
