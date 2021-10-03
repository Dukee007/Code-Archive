from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ext import tasks
from discord.utils import get
from itertools import cycle
from PIL import Image, ImageDraw, ImageFilter
import time
import os
import random
import json
import discord
import urllib.request
import praw
import requests

client = commands.Bot(command_prefix=".")

os.chdir("money/")
client.remove_command("help")

reddit = praw.Reddit(client_id='m1HOyUizUb2SlQ',
                     client_secret='RNpb2STGM-Z7CvttKju74rhI1Ig',
                     user_agent='AGENT69')
no_touch = [690571751570014219, 726949689278070804, 508372340904558603]
money = {}
done = []
loops = 0
number = 0


@client.event
async def on_ready():
    print("client online")
    await client.change_presence(activity=discord.Streaming(name="DidoBOT [1.0]｜.help", url="https://www.twitch.tv/luna7756"))
'''
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found! ☹️")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You need to be a staff member to use this command! ☹️")
    #elif isinstance(error, commands.CommandInvokeError):
        #await ctx.send("Please use this command corectly! ☹️")
    else:
        error_code = random.randint(10000, 99999)
        await ctx.send(f"Hey looks like you have found an error! Please DM <@!508372340904558603> and give him this the command you were using the responce and this code: {error_code}")
        os.chdir("..")
        f = open("errors.txt")
        data = f.read()
        f.close()
        f = open("errors.txt", "w+")
        f.write(data + "\n" + f"Error Code: {error_code}, Error: {error}")
        os.chdir("money/")
'''


@client.command()
async def help(ctx, num=0):
    if num == 0:
        embed = discord.Embed(
            title="Help", description="Please pick a section (.help {section number})", color=0x00eeff)
        embed.set_author(
            name="DidoBOT", icon_url='https://yt3.ggpht.com/a/AATXAJxRZWxXZ-9gpcfJHQTToBl59iEe3_Z3uoHenT23=s100-c-k-c0xffffffff-no-rj-mo')
        embed.add_field(name="1. Money",
                        value="The money system", inline=False)
        embed.add_field(name="2. Custom",
                        value="The User suggested commands", inline=False)
        embed.add_field(name="3. Moderation",
                        value="The Moderator only commands", inline=False)
        embed.add_field(name="4. Youtube",
                        value="The Youtube commands", inline=False)
        embed.add_field(name="5. Fun", value="The Fun commands", inline=False)
        embed.set_footer(text="DidoBot [1.0]")
        await ctx.send(embed=embed)
    elif num == 1:
        embed = discord.Embed(
            title="Help", description="Money System", color=0x00eeff)
        embed.set_author(
            name="DidoBOT", icon_url='https://yt3.ggpht.com/a/AATXAJxRZWxXZ-9gpcfJHQTToBl59iEe3_Z3uoHenT23=s100-c-k-c0xffffffff-no-rj-mo')
        embed.add_field(name=".bal {username/blank}",
                        value="Allows you to see your own/other people balance", inline=False)
        embed.add_field(
            name=".beg", value="Allows you to beg for money", inline=False)
        embed.add_field(
            name=".steal {username}", value="Allows you to steal money from other users", inline=False)
        embed.add_field(name=".sell {what} {who} {price}",
                        value="Allows mods to sell stuff to users", inline=False)
        embed.set_footer(text="DidoBot [1.0]")
        await ctx.send(embed=embed)
    elif num == 2:
        embed = discord.Embed(
            title="Help", description="Custom Commands", color=0x00eeff)
        embed.set_author(
            name="DidoBOT", icon_url='https://yt3.ggpht.com/a/AATXAJxRZWxXZ-9gpcfJHQTToBl59iEe3_Z3uoHenT23=s100-c-k-c0xffffffff-no-rj-mo')
        embed.add_field(name=".deanoisthebest",
                        value="Tells you why Deano is the best", inline=False)
        embed.add_field(
            name=".say", value="Lets you make the bot say anything", inline=False)
        embed.add_field(
            name=".hug {username}", value="Allows you to send a virtual hug", inline=False)
        embed.add_field(
            name=".social", value="Allows you to see all of DidoASMR's socials", inline=False)
        embed.add_field(
            name=".info", value="Allows you to see info about a user", inline=False)
        embed.add_field(
            name=".pfp", value="Allows you to see a users profile pic", inline=False)
        embed.set_footer(text="DidoBot [1.0]")
        await ctx.send(embed=embed)
    elif num == 3:
        embed = discord.Embed(
            title="Help", description="Moderator commands", color=0x00eeff)
        embed.set_author(
            name="DidoBOT", icon_url='https://yt3.ggpht.com/a/AATXAJxRZWxXZ-9gpcfJHQTToBl59iEe3_Z3uoHenT23=s100-c-k-c0xffffffff-no-rj-mo')
        embed.add_field(
            name=".clear {amount/all}", value="Allows Mods to clear a channel", inline=False)
        embed.add_field(name=".shutdown",
                        value="Allows Mods to Shutdown the bot", inline=False)
        embed.add_field(
            name=".invite", value="Allows you to invite the bot to your server", inline=False)
        embed.add_field(
            name=".servers", value="Allows you to see all the servers DidoBOT is in!", inline=False)
        embed.set_footer(text="DidoBot [1.0]")
        await ctx.send(embed=embed)
    elif num == 4:
        embed = discord.Embed(
            title="Help", description="Youtube commands", color=0x00eeff)
        embed.set_author(
            name="DidoBOT", icon_url='https://yt3.ggpht.com/a/AATXAJxRZWxXZ-9gpcfJHQTToBl59iEe3_Z3uoHenT23=s100-c-k-c0xffffffff-no-rj-mo')
        embed.add_field(
            name=".latest", value="Tells you DidoASMR's latest video", inline=False)
        embed.add_field(
            name=".stats", value="Tells you DidoASMR's youtube channel stats", inline=False)
        embed.add_field(
            name=".intro", value="Allows you to get didos intro anywhere", inline=False)
        embed.set_footer(text="DidoBot [1.0]")
        await ctx.send(embed=embed)
    elif num == 5:
        embed = discord.Embed(
            title="Help", description="Fun commands", color=0x00eeff)
        embed.set_author(
            name="DidoBOT", icon_url='https://yt3.ggpht.com/a/AATXAJxRZWxXZ-9gpcfJHQTToBl59iEe3_Z3uoHenT23=s100-c-k-c0xffffffff-no-rj-mo')
        embed.add_field(
            name=".meme", value="""Send you a "new" meme from reddit""", inline=False)
        embed.set_footer(text="DidoBot [1.0]")
        await ctx.send(embed=embed)
    else:
        await ctx.send("That's not a section")

###########################################################################___ADS___################################################################################################


@client.command()
async def dev(ctx):
    await ctx.send("I have been coded and am currently being hosted by <@!508372340904558603>")

###########################################################################___MONEY___################################################################################################


@client.event
async def on_member_join(member):
    f = open(f"__{member.id}__.json", "w+")
    f.write("500")
    f.close()


@client.command()
@has_permissions(administrator=True)
async def setup(ctx):
    usr_num = 0
    bot_num = 0
    for user in ctx.message.guild.members:
        if user.bot == True:
            bot_num += 1
        elif user.id in done:
            pass
        else:
            f = open(f"__{user.id}__.json", "w+")
            f.write("500")
            f.close()
            usr_num += 1
    embed = discord.Embed(
        title="SETUP", description="Running Setup", color=0x00eeff)
    embed.set_author(
        name="DidoBOT", icon_url='https://yt3.ggpht.com/a/AATXAJxRZWxXZ-9gpcfJHQTToBl59iEe3_Z3uoHenT23=s100-c-k-c0xffffffff-no-rj-mo')
    embed.add_field(name="Users", value=str(usr_num), inline=False)
    embed.add_field(name="Bots", value=str(bot_num), inline=True)
    embed.set_footer(text="DidoBot [1.0]")
    await ctx.send(embed=embed)


@client.command()
@has_permissions(administrator=True)
async def no_t(ctx, who):
    w = who
    who = who.replace("@", "").replace("!",
                                       "").replace(">", "").replace("<", "")
    who = int(who)
    no_touch.append(who)
    await ctx.send(f"{w} Now cant bee stole from")


@client.command()
@has_permissions(administrator=True)
async def sell(ctx, wht, who, price):
    w = who
    who = who.replace("@", "").replace("!",
                                       "").replace(">", "").replace("<", "")
    who = int(who)
    f = open(f"__{who}__.json")
    x = int(f.read())
    f.close()
    if int(x) < int(price):
        await ctx.send(f"{w} Does not have the money to buy {wht}")
    else:
        x -= int(price)
        f = open(f"__{who}__.json", "w+")
        f.write(str(x))
        f.close()
        await ctx.send(f"You have sold {w} {wht} for {str(price)}")


@client.command()
async def bal(ctx, who=None):
    if who == None:
        who = int(ctx.message.author.id)
    else:
        who = who.replace("@", "").replace("!",
                                           "").replace(">", "").replace("<", "")
        who = int(who)
    f = open(f"__{who}__.json", "r")
    bal = f.read()
    f.close()
    embed = discord.Embed(title="Balance", color=0x00eeff)
    embed.set_author(
        name="DidoBOT", icon_url='https://yt3.ggpht.com/a/AATXAJxRZWxXZ-9gpcfJHQTToBl59iEe3_Z3uoHenT23=s100-c-k-c0xffffffff-no-rj-mo')
    embed.add_field(name="Total", value="£" + str(bal), inline=False)
    embed.set_footer(text="DidoBot [1.0]")
    await ctx.send(embed=embed)


@client.command()
async def beg(ctx):
    x = random.randint(0, 100)
    if x > 25:
        c = True
    else:
        c = False
        await ctx.send("No Coins for you!")
    if c == True:
        amm = random.randint(50, 300)
        if amm > 295:
            amm = random.randint(400, 500)
        await ctx.send(f"Here have {amm} coins!")
        f = open(f"__{ctx.message.author.id}__.json")
        c_b = f.read()
        f.close()
        c_b = int(c_b) + int(amm)
        f = open(f"__{ctx.message.author.id}__.json", "w+")
        f.write(str(c_b))
        f.close()


@client.command()
async def steal(ctx, who=None):
    w = who
    if who == None:
        await ctx.send("You need to tell me who to steal from!")
    else:
        who = who.replace("@", "").replace("!",
                                           "").replace(">", "").replace("<", "")
        who = int(who)
        chance = random.randint(0, 100)
        if chance > 30:
            x = True
        else:
            await ctx.send("Oh no you have been caught!")
            x = False
    if x == True:
        if ctx.message.author.id == 508372340904558603:
            amm = random.randint(900, 1000)
        else:
            amm = random.randint(1, 400)
        await ctx.send(f"You stole {amm} from {w}")
        f = open(f"__{ctx.message.author.id}__.json")
        c = f.read()
        f.close()
        c = int(c) + amm
        f = open(f"__{ctx.message.author.id}__.json", "w+")
        f.write(str(c))
        f.close()
        f = open(f"__{who}__.json")
        c = f.read()
        f.close()
        c = int(c) - amm
        f = open(f"__{who}__.json", "w+")
        f.write(str(c))
        f.close()


@client.command()
@has_permissions(administrator=True)
async def give(ctx, who, what):
    await ctx.send("Sending money")
    who = who.replace("@", "").replace("!",
                                       "").replace(">", "").replace("<", "")
    who = int(who)
    f = open(f"__{who}__.json")
    old = int(f.read())
    f.close()
    old += int(what)
    f = open(f"__{who}__.json", "w+")
    f.write(str(old))
    f.close()


@client.command()
@has_permissions(administrator=True)
async def take(ctx, who, what):
    await ctx.send("Taking money")
    who = who.replace("@", "").replace("!",
                                       "").replace(">", "").replace("<", "")
    who = int(who)
    f = open(f"__{who}__.json")
    old = int(f.read())
    f.close()
    old -= int(what)
    f = open(f"__{who}__.json", "w+")
    f.write(str(old))
    f.close()


@client.command()
async def bet(ctx, amm=None):
    if amm == None:
        await ctx.send("You need to tell me what you want to bet lol")
    else:
        try:
            amm = int(amm)
            passs = True
        except:
            await ctx.send("Thats not a number dum dum")
            passs = False
        if passs == True:
            f = open(f"__{ctx.message.author.id}__.json")
            bal = int(f.read())
            f.close()
            if amm > bal:
                await ctx.send("You can't afford that bet lol")
            else:
                new_bal = bal - amm
                f = open(f"__{ctx.message.author.id}__.json", "w+")
                f.write(str(new_bal))
                f.close()
                you = random.randint(0, 10)
                bot = random.randint(0, 10)
                if you > bot:
                    text = f"Congrats you win £{amm*2}"
                    embed = discord.Embed(title="BET", description=text)
                    embed.set_author(
                        name="DidoBOT", icon_url='https://yt3.ggpht.com/a/AATXAJxRZWxXZ-9gpcfJHQTToBl59iEe3_Z3uoHenT23=s100-c-k-c0xffffffff-no-rj-mo')
                    embed.add_field(name="You:", value=you, inline=True)
                    embed.add_field(name="Me:", value=bot, inline=True)
                    embed.set_footer(text="DidoBot [1.0]")
                    await ctx.send(embed=embed)
                    f = open(f"__{ctx.message.author.id}__.json", "w+")
                    f.write(str(bal + amm))
                    f.close()
                else:
                    text = f"Oh no you lose £{amm}"
                    embed = discord.Embed(title="BET", description=text)
                    embed.set_author(
                        name="DidoBOT", icon_url='https://yt3.ggpht.com/a/AATXAJxRZWxXZ-9gpcfJHQTToBl59iEe3_Z3uoHenT23=s100-c-k-c0xffffffff-no-rj-mo')
                    embed.add_field(name="You:", value=you, inline=True)
                    embed.add_field(name="Me:", value=bot, inline=True)
                    embed.set_footer(text="DidoBot [1.0]")
                    await ctx.send(embed=embed)

###########################################################################___MOD___################################################################################################


@client.command(pass_context=True)
@has_permissions(administrator=True)
async def clear(ctx, limit=None):
    if limit == None:
        await ctx.send("You need to tell me how many messages to clear")
    elif limit == "all":
        limit = 10000
        await ctx.channel.purge(limit=limit)
        await ctx.send(f"Cleared by {ctx.author.mention}")
        time.sleep(0.5)
        await ctx.channel.purge(limit=1)
    else:
        limit = int(limit)
        limit += 1
        await ctx.channel.purge(limit=limit)
        time.sleep(1)
        await ctx.send(f"Cleared by {ctx.author.mention}")
        time.sleep(2)
        await ctx.channel.purge(limit=1)


@client.command()
@commands.has_permissions(administrator=True)
async def shutdown(ctx):
    await ctx.send("Shutting down!")
    await client.change_presence(status=discord.Status.offline, activity=discord.Game("Shutting Down..."))
    exit()


@client.command()
async def invite(ctx):
    await ctx.send("Here you go: https://discord.com/api/oauth2/authorize?client_id=732653402139525239&permissions=8&scope=bot")


@client.command()
async def members(ctx):
    num = 0
    bots = 0
    for e in ctx.message.guild.members:
        if e.bot == True:
            bots += 1
        else:
            num += 1
    await ctx.send(f"We have {num} users and {bots} bots!")


@client.command()
async def servers(ctx):
    ea = ""
    num = 0
    for server in client.guilds:
        ea = ea + "\n" + str(server)
        num += 1
    embed = discord.Embed(title="Servers", color=0x00eeff)
    embed.set_author(
        name="DidoBOT", icon_url='https://yt3.ggpht.com/a/AATXAJxRZWxXZ-9gpcfJHQTToBl59iEe3_Z3uoHenT23=s100-c-k-c0xffffffff-no-rj-mo')
    embed.add_field(name="Serving", value=str(num) + " servers", inline=False)
    embed.add_field(name="Names", value=ea, inline=False)
    embed.set_footer(text="DidoBot [1.0]")
    await ctx.send(embed=embed)


@client.command()
async def workmode(ctx):
    if ctx.message.author.id != 508372340904558603:
        await ctx.send("I'm sorry but only <@!508372340904558603> can use this command!")
    else:
        await ctx.send("WorkMode now Active!")
        os.chdir("..")
        os.system("start work.py")
        exit()


###########################################################################___YT___################################################################################################

@client.command()
async def stats(ctx):
    channel_id = "UCyoTDnXaBFX4KOG9KyvdPFw"
    api_key = "AIzaSyAydqfsNwTWhMIpWQeLtHTpIvx9Uf5Yu4U"

    data = urllib.request.urlopen(
        "https://www.googleapis.com/youtube/v3/channels?part=statistics&id=" + channel_id + "&key=" + api_key).read()
    x = subs = json.loads(data)["items"][0]["statistics"]
    subs = json.loads(data)["items"][0]["statistics"]["subscriberCount"]
    views = json.loads(data)["items"][0]["statistics"]["viewCount"]
    vids = json.loads(data)["items"][0]["statistics"]["videoCount"]
    avepervid = round(int(views) / int(vids), 0)
    embed = discord.Embed(title="DidoASMR's Sub Count",
                          url='https://www.youtube.com/channel/UCyoTDnXaBFX4KOG9KyvdPFw')
    embed.set_author(
        name="DidoBOT", icon_url='https://yt3.ggpht.com/a/AATXAJxRZWxXZ-9gpcfJHQTToBl59iEe3_Z3uoHenT23=s100-c-k-c0xffffffff-no-rj-mo')
    embed.add_field(name="Subscribers:", value=str(subs), inline=False)
    embed.add_field(name="Views:", value=str(views), inline=False)
    embed.add_field(name="Videos:", value=str(vids), inline=False)
    embed.add_field(name="Average views per video:",
                    value=str(avepervid), inline=False)
    embed.set_footer(text="DidoBOT [1.0]")
    await ctx.send(embed=embed)


@client.command()
async def latest(ctx):
    x = get_all_videos_in_a_channel("UCyoTDnXaBFX4KOG9KyvdPFw")
    x = x[0]
    embed = discord.Embed(title="DidoASMR's latest video",
                          url='https://www.youtube.com/channel/UCyoTDnXaBFX4KOG9KyvdPFw')
    embed.set_author(
        name="DidoBOT", icon_url='https://yt3.ggpht.com/a/AATXAJxRZWxXZ-9gpcfJHQTToBl59iEe3_Z3uoHenT23=s100-c-k-c0xffffffff-no-rj-mo')
    embed.add_field(name="Latest Video", value=x, inline=True)
    embed.set_footer(text="DidoBot [1.0]")
    await ctx.send(embed=embed)


def get_all_videos_in_a_channel(channel_id):
    api_key = "AIzaSyAydqfsNwTWhMIpWQeLtHTpIvx9Uf5Yu4U"

    base_video_url = 'https://www.youtube.com/watch?v='
    base_search_url = 'https://www.googleapis.com/youtube/v3/search?'

    first_url = base_search_url + \
        'key={}&channelId={}&part=snippet,id&order=date&maxResults=25'.format(
            api_key, channel_id)

    video_links = []
    url = first_url
    while True:
        inp = urllib.request.urlopen(url)
        resp = json.load(inp)

        for i in resp['items']:
            if i['id']['kind'] == "youtube#video":
                video_links.append(base_video_url + i['id']['videoId'])

        try:
            next_page_token = resp['nextPageToken']
            url = first_url + '&pageToken={}'.format(next_page_token)
        except:
            break
    return video_links

###########################################################################___USER_COMMANDS___################################################################################################


@client.command()
async def sure(ctx):
    e = random.randint(0, 100)
    await ctx.send(f"You are {e}% sure!")


@client.command()
async def say(ctx, *, wht):
    await ctx.send(wht)


@client.command()
async def deanoisthebest(ctx):
    await ctx.send(f"Hey {ctx.message.author.name} Let me explain why Deano is the best.")
    embed = discord.Embed(title="Why Deano Is The Best", color=0x00eeff)
    embed.set_author(
        name="DidoBOT", icon_url='https://yt3.ggpht.com/a/AATXAJxRZWxXZ-9gpcfJHQTToBl59iEe3_Z3uoHenT23=s100-c-k-c0xffffffff-no-rj-mo')
    embed.add_field(name="1.", value="Never missed a stream", inline=False)
    embed.add_field(name="2.", value="Never create beef", inline=False)
    embed.add_field(
        name="3.", value="Take no rubbish from trolls", inline=False)
    embed.set_footer(text="DidoBot [1.0]")
    await ctx.send(embed=embed)


@client.command()
async def hug(ctx, who=None):
    if who == None:
        await ctx.send("You need to tell me who you want to hug!")
        x = False
    else:
        x = True
    if x == True:
        await ctx.send(f"{ctx.message.author.mention} Has hugged {who}")


@client.command()
async def social(ctx):
    embed = discord.Embed(title="Here are all DidoASMR's Socials",
                          url='https://www.youtube.com/channel/UCyoTDnXaBFX4KOG9KyvdPFw', color=0x00eeff)
    embed.set_author(
        name="Socials", icon_url='https://yt3.ggpht.com/a/AATXAJxRZWxXZ-9gpcfJHQTToBl59iEe3_Z3uoHenT23=s100-c-k-c0xffffffff-no-rj-mo')
    embed.set_thumbnail(
        url='https://yt3.ggpht.com/a/AATXAJxRZWxXZ-9gpcfJHQTToBl59iEe3_Z3uoHenT23=s100-c-k-c0xffffffff-no-rj-mo')
    embed.add_field(
        name="Youtube", value="https://www.youtube.com/channel/UCyoTDnXaBFX4KOG9KyvdPFw", inline=True)
    embed.add_field(name="Instagram",
                    value="https://www.instagram.com/dido_asmr/", inline=True)
    embed.add_field(
        name="Twitter", value="https://twitter.com/didoasmr", inline=True)
    await ctx.send(embed=embed)


@client.command()
async def info(ctx, who=None):
    if who == None:
        ctx.message.guild.get_member(ctx.message.author.id)
        name = ctx.message.author.name
        if ctx.message.author.bot == True:
            bot = "Yes"
        else:
            bot = "No"
        pfp = ctx.message.author.avatar_url
        who = ctx.message.author.id
        w = ctx.message.author.id
    else:
        w = who
        who = who.replace("@", "").replace("!",
                                           "").replace(">", "").replace("<", "")
        who = int(who)
        user = ctx.message.guild.get_member(who)
        name = user.name
        if user.bot == True:
            bot = "Yes"
        else:
            bot = "No"
        pfp = user.avatar_url
    embed = discord.Embed(title=f"Here is the info for {name}", color=0x00eeff)
    embed.set_author(
        name="DidoBOT", icon_url='https://yt3.ggpht.com/a/AATXAJxRZWxXZ-9gpcfJHQTToBl59iEe3_Z3uoHenT23=s100-c-k-c0xffffffff-no-rj-mo')
    embed.set_thumbnail(url=pfp)
    embed.add_field(name="Username:", value=name, inline=False)
    embed.add_field(name="Id:", value=who, inline=False)
    embed.add_field(name="Bot:", value=bot, inline=False)
    embed.set_footer(
        text="DidoBot [1.0] - Type .pfp {username} to get a close up of the profile picture!")
    await ctx.send(embed=embed)


@client.command()
async def pfp(ctx, who=None):
    if who == None:
        ctx.message.guild.get_member(ctx.message.author.id)
        name = ctx.message.author.name
        if ctx.message.author.bot == True:
            bot = "Yes"
        else:
            bot = "No"
        pfp = ctx.message.author.avatar_url
        who = ctx.message.author.id
    else:
        w = who
        who = who.replace("@", "").replace("!",
                                           "").replace(">", "").replace("<", "")
        who = int(who)
        user = ctx.message.guild.get_member(who)
        name = user.name
        if user.bot == True:
            bot = "Yes"
        else:
            bot = "No"
        pfp = user.avatar_url
    embed = discord.Embed(title=f"Here is a close up pic of {name}")
    embed.set_image(url=pfp)
    embed.set_author(
        name="DidoBOT", icon_url='https://yt3.ggpht.com/a/AATXAJxRZWxXZ-9gpcfJHQTToBl59iEe3_Z3uoHenT23=s100-c-k-c0xffffffff-no-rj-mo')
    embed.set_footer(text=f"DidoBot [1.0] - Close up of {name}")
    await ctx.send(embed=embed)


@client.command()
async def intro(ctx):
    os.chdir("..")
    file = "intro.mp4"
    with open(file, "rb") as fh:
        f = discord.File(fh, filename=file)
        await ctx.send("Enjoy the intro", file=f)
    os.chdir("money/")


@client.command()
async def slap(ctx, who=None):
    os.chdir("..")
    os.chdir("images/")
    if who == None:
        who = ctx.message.author.id
    else:
        who = who.replace("@", "").replace("!",
                                           "").replace(">", "").replace("<", "")
        who = int(who)
    user = ctx.message.guild.get_member(who)
    with open('pic.webp', 'wb') as handle:
        response = requests.get(user.avatar_url, stream=True)
        if not response.ok:
            print(response)
        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)
    img = Image.open("pic.webp").convert("RGB")
    img.save("user.png")
    os.remove("pic.webp")
    slap = Image.open("slap_image.png")
    basewidth = 111
    img = Image.open('user.png')
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    img.save('user.png')
    user = Image.open("user.png")
    user.save("user.png")
    new = slap.copy()
    new.paste(user, (260, 67))
    new.save('done.png', quality=100)
    os.remove("user.png")
    file = "done.png"
    with open(file, "rb") as fh:
        f = discord.File(fh, filename=file)
        await ctx.send(file=f)
    os.remove("done.png")
    os.chdir("..")
    os.chdir("money/")
###########################################################################___FUN___################################################################################################


@client.command()
async def meme(ctx):
    memes_submissions = reddit.subreddit('memes').hot(limit=100)
    post_to_pick = random.randint(1, 100)
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)
    # await ctx.send(f"Here is your meme! 😀 {submission.url}")
    embed = discord.Embed(title=submission.title,
                          description=f"Here is your meme! 😀 Made by: {submission.author}", color=0x00eeff)
    embed.set_author(
        name="DidoBOT", icon_url='https://yt3.ggpht.com/a/AATXAJxRZWxXZ-9gpcfJHQTToBl59iEe3_Z3uoHenT23=s100-c-k-c0xffffffff-no-rj-mo')
    embed.set_image(url=submission.url)
    embed.set_footer(text="DidoBot [1.0]")
    await ctx.send(embed=embed)


@client.event
async def on_message(message):
    if message.author.bot == True:
        return
    await client.process_commands(message)
    os.chdir("..")
    f = open("badwords.txt")
    data = f.readlines()
    for d in data:
        d = d.replace("\n", "")
        z = d.upper()
        if d in message.content:
            await message.delete()
            await message.channel.send(f"Hey, {message.author.mention} try not to use that word please!")
        elif z in message.content:
            await message.delete()
            await message.channel.send(f"Hey, {message.author.mention} try not to use that word please!")
    if message.content == "<@!732653402139525239>":
        await message.channel.send(f"Hey {message.author.mention}, My prefix in guild {message.guild.name} is {gp(message)}")
    f = open("messages.cson")
    data = int(f.read())
    f.close()
    new = str(data + 1)
    f = open("messages.cson", "w+")
    f.write(new)
    f.close()
    os.chdir("money/")
    for channel in message.guild.channels:
        if "Messages:" in channel.name:
            await channel.edit(name=f"Messages: {new}")

client.run("ODUzNzAyNjg0OTUwOTIxMjM2.YMZOlQ.-sHy52r4DwOAS7vD2anPUPwxxMU")
