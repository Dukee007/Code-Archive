from discord.ext.commands import Bot as DiscordBot
from discord.ext.commands import cooldown, BucketType, CommandOnCooldown, has_role, MissingRole
from datetime import datetime
from gtts import gTTS
import json
import asyncio
import random
import discord

running_games = []
game_data = {}
votee = True
lobbys = {}

client = DiscordBot(command_prefix="am!")
TOKEN = "NzU3NjUzMjg0MzU3MTQ0NzA3.X2jhmw.zEAyYGrMv62OHZa_xLGwiBj3p0w"

@client.event
async def on_ready():
        print("online")

#                                                  -----SIGNUP_CMDS-----


@client.command()
@has_role("Among Us Admin")
async def createlobby(ctx):
    global lobbys
    users = ""
    lobbys[ctx.author.id] = [ctx.author]

    for user in lobbys[ctx.author.id]:
        users = users + f"{user}\n"

    embed = discord.Embed(title=f"Lobby Created!")
    embed.add_field(name="Users:", value=users, inline=False)
    embed.set_footer(
        text=f"To join this lobby type am!join @{ctx.author.name}")
    await ctx.send(embed=embed)


@client.command()
async def join(ctx, lobby: discord.User = None):
    global lobbys
    if lobby == None:
        await ctx.send("You need to tell me what lobby you wanna join!")
        return
    if lobby.id not in lobbys:
        await ctx.send("This lobby cannot be found!")
        return
    if ctx.author.id in lobbys[lobby.id]:
        await ctx.send("You are already in this lobby!")
    lobbys[lobby.id].append(ctx.author)
    await ctx.send(f"You have joined **{lobby.name}'s** lobby'")


@client.command()
async def lobby(ctx):
    global lobbys
    if ctx.author.id not in lobbys:
        await ctx.send("You don't own a lobby!")
        return

    users = ""

    for user in lobbys[ctx.author.id]:
        users = users + f"{user}\n"

    embed = discord.Embed(title=f"Current Lobby")
    embed.add_field(name="Users:", value=users, inline=False)
    embed.set_footer(
        text=f"To join this lobby type am!join @{ctx.author.name}")
    await ctx.send(embed=embed)

#                                                  -----NON_GAME_CMDS-----


@client.command()
async def dev(ctx):
    await ctx.send("My Staff Team!\nCreator - **MES#1788**\nDeveloper and Server Manager - **LUNA#7756**")


@client.command()
async def invite(ctx):
    await ctx.send("https://discord.com/api/oauth2/authorize?client_id=757653284357144707&permissions=8&scope=bot")


@client.command()
@has_role("Among Us Admin")
async def mute(ctx, user: discord.Member = None):
    if user == None:
        await ctx.send("You might wanna tell me who to mute!")
        return
    await user.edit(mute=True)
    await ctx.send(f"{user.name} Has been muted!")


@client.command()
@has_role("Among Us Admin")
async def unmute(ctx, user: discord.Member = None):
    if user == None:
        await ctx.send("You might wanna tell me who to unmute!")
        return
    await user.edit(mute=False)
    await ctx.send(f"{user.name} Has been unmuted!")


#                                                  -----CMDS-----

@client.command()
@has_role("Among Us Admin")
async def create(ctx):
    global running_games, game_data
    if ctx.author.voice == None:
        await ctx.send("You need to be in a voice channel to use this command!")
        return

    running_games = []
    game_data = {}
    votee = True
    alive = []
    dead = []
    for each_user in ctx.author.voice.channel.members:
        await each_user.edit(mute=False)
        if each_user.id != 757653284357144707:
            alive.append(each_user)
    game_data[ctx.author.voice.channel.id] = {"dead": dead, "alive": alive, }
    running_games.append(ctx.author.voice.channel.id)
    currently_alive = game_data[ctx.author.voice.channel.id]["alive"]
    currently_alive_text = ""

    for u in currently_alive:
        currently_alive_text = currently_alive_text + f"{u}\n"

    embed = discord.Embed(title=f"Game Created",
                          description="Current Game Data:")
    embed.add_field(name="Alive:", value=currently_alive_text, inline=False)
    await ctx.send(embed=embed)


@client.command()
@has_role("Among Us Admin")
async def start(ctx):
    global running_games, game_data
    if ctx.author.voice == None:
        await ctx.send("You need to be in a voice channel to use this command!")
        return

    elif ctx.author.voice.channel.id not in running_games:
        await ctx.send("This game has not been started yet! \n Use `am!start` to start it.")
        return
    for each_user in ctx.author.voice.channel.members:
        if each_user.id != 757653284357144707:
            await each_user.edit(mute=True)
    await ctx.send("Game Started! (everyone muted)")


@client.command()
@has_role("Among Us Admin")
async def out(ctx, user: discord.Member = None):
    global running_games, game_data
    if ctx.author.voice == None:
        await ctx.send("You need to be in a voice channel to use this command!")
        return

    elif ctx.author.voice.channel.id not in running_games:
        ctx.send("This game has not been started yet! \n Use `am!start` to start it.")
        return

    await user.edit(mute=True)

    currently_alive = game_data[ctx.author.voice.channel.id]["alive"]
    currently_dead = game_data[ctx.author.voice.channel.id]["dead"]
    currently_dead.append(user)
    currently_alive.remove(user)

    currently_alive_text = ""
    currently_dead_text = ""

    currently_alive_num = 0
    currently_dead_num = 0

    for u in currently_alive:
        currently_alive_text = currently_alive_text + f"{u}\n"
        currently_alive_num += 1
    for u in currently_dead:
        currently_dead_text = currently_dead_text + f"{u}\n"
        currently_dead_num += 1

    if currently_dead_text == "":
        currently_dead_text = "Nobody"

    if currently_alive_text == "":
        currently_alive_text = "Nobody"

    if currently_dead_num == 1 or currently_dead_num == 2:
        embed = discord.Embed(title=f"Imposters Win!")
        await ctx.send(embed=embed)
        return

    embed = discord.Embed(
        title=f"{user.name} Has Been Killed!", description="Current Game Data:")
    embed.add_field(name="Alive:", value=currently_alive_text, inline=False)
    embed.add_field(name="Dead:", value=currently_dead_text, inline=False)
    await ctx.send(embed=embed)


@client.command()
@has_role("Among Us Admin")
async def new(ctx):
    global running_games, game_data
    if ctx.author.voice == None:
        await ctx.send("You need to be in a voice channel to use this command!")
        return

    elif ctx.author.voice.channel.id not in running_games:
        await ctx.send("This game has not been created yet! \n Use `am!create` to start it.")
        return

    running_games = []
    game_data = {}
    votee = True
    alive = []
    dead = []
    for each_user in ctx.author.voice.channel.members:
        if each_user.id != 757653284357144707:
            await each_user.edit(mute=False)
            alive.append(each_user)
    game_data[ctx.author.voice.channel.id] = {"dead": dead, "alive": alive, }
    running_games.append(ctx.author.voice.channel.id)
    await ctx.send("Game Ready To Start!")


@client.command()
@has_role("Among Us Admin")
async def vote(ctx):
    global running_games, game_data, votee
    if ctx.author.voice == None:
        await ctx.send("You need to be in a voice channel to use this command!")
        return

    elif ctx.author.voice.channel.id not in running_games:
        ctx.send("This game has not been started yet! \n Use `am!start` to start it.")
        return
    if votee == True:
        for each_user in ctx.author.voice.channel.members:
            if each_user.id != 757653284357144707:
                if each_user.id not in game_data[ctx.author.voice.channel.id]["dead"]:
                    await each_user.edit(mute=False)
        await ctx.send("Voting time!")
        votee = False
    else:
        for each_user in ctx.author.voice.channel.members:
            if each_user.id != 757653284357144707:
                await each_user.edit(mute=True)
        await ctx.send("Voting time over!")
        votee = True


@client.command()
@has_role("Among Us Admin")
async def end(ctx):
    global running_games, game_data
    if ctx.author.voice == None:
        await ctx.send("You need to be in a voice channel to use this command!")
        return

    elif ctx.author.voice.channel.id not in running_games:
        ctx.send("This game has not been started yet! \n Use `am!start` to start it.")
        return
    running_games = []
    game_data = {}
    for each_user in ctx.author.voice.channel.members:
        await each_user.edit(mute=False)
    await ctx.send("Game Ended")

#                                                  -----ERRORS-----


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, MissingRole):
        await ctx.send("Your not aloud to do that!")
        return
    else:
        raise error

#                                                  -----RUN-----

client.run(TOKEN)
