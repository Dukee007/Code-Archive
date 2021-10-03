import discord, time, os, praw, random, json
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, MissingPermissions
from discord.utils import get
from itertools import cycle
import datetime as dt
from datetime import datetime

reddit = praw.Reddit(client_id='m1HOyUizUb2SlQ', client_secret='RNpb2STGM-Z7CvttKju74rhI1Ig', user_agent='AGENT69')

def gp(ctx):
    with open("prefixs.json", "r") as all_prefixs:
        prefixs = json.load(all_prefixs)
    return prefixs[str(ctx.message.guild.id)]

embeddata = {}
embeddata["icon"] = "http://luna-development.orgfree.com/data/discord/meme6/logo.jpg"
embeddata["name"] = "Meme6"
embeddata["version"] = "2.0"

class App(commands.Cog):
    def __init__(self, client):
        self.client = client
        print("Loading Cog: FUN")

    @commands.command()
    async def info(self, ctx, who=None):
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
            who = who.replace("@", "").replace("!", "").replace(">", "").replace("<", "")
            who = int(who)
            user = ctx.message.guild.get_member(who)
            name = user.name
            if user.bot == True:
                bot = "Yes"
            else:
                bot = "No"
            pfp = user.avatar_url
        embed=discord.Embed(title=f"Here is the info for {name}", color=0x00eeff)
        embed.set_author(name=embeddata["name"], icon_url=embeddata["icon"])
        embed.set_thumbnail(url=pfp)
        embed.add_field(name="Username:", value=name, inline=False)
        embed.add_field(name="Id:", value=who, inline=False)
        embed.add_field(name="Bot:", value=bot, inline=False)
        embed.set_footer(text=embeddata["name"]+" ["+embeddata["version"]+"] - Type "+gp(ctx)+"pfp {username} to get a close up of the profile picture!")
        await ctx.send(embed=embed)

    @commands.command()
    async def pfp(self, ctx, who=None):
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
            who = who.replace("@", "").replace("!", "").replace(">", "").replace("<", "")
            who = int(who)
            user = ctx.message.guild.get_member(who)
            name = user.name
            if user.bot == True:
                bot = "Yes"
            else:
                bot = "No"
            pfp = user.avatar_url
        embed=discord.Embed(title=f"Here is a close up pic of {name}")
        embed.set_author(name=embeddata["name"], icon_url=embeddata["icon"])
        embed.set_image(url=pfp)
        embed.set_footer(text=embeddata["name"]+" ["+embeddata["version"]+f"] - Close up of {name}")
        await ctx.send(embed=embed)

    @commands.command()
    async def servers(self, ctx):
        ea = ""
        num = 0
        usernum = 0
        for server in self.client.guilds:
            ea = ea+"\n"+str(server)
            num += 1
            for user in server.members:
                usernum += 1
        embed=discord.Embed(title="Servers", color=0x00eeff)
        embed.set_author(name=embeddata["name"], icon_url=embeddata["icon"])
        embed.add_field(name="Serving", value=str(num)+" servers", inline=False)
        embed.add_field(name="Serving", value=str(usernum)+" users", inline=False)
        embed.add_field(name="Names", value=ea, inline=False)
        embed.set_footer(text=embeddata["name"]+" ["+embeddata["version"]+"]")
        await ctx.send(embed=embed)

    @commands.command()
    async def members(self, ctx):
        num = 0
        bots = 0
        for e in ctx.message.guild.members:
            if e.bot == True:
                bots += 1
            else:
                num += 1
        await ctx.send(f"We have {num} users and {bots} bots!")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.client.latency*1000)}ms")

    @commands.command()
    async def meme(self, ctx):
        memes_submissions = reddit.subreddit('memes').hot(limit=100)
        post_to_pick = random.randint(1, 100)
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)
        #await ctx.send(f"Here is your meme! 😀 {submission.url}")
        embed = discord.Embed(title=submission.title, description=f"Here is you meme! 😀 Made by: {submission.author}", color=0x13edf9)
        embed.set_author(name=embeddata["name"], icon_url=embeddata["icon"])
        embed.set_image(url=submission.url)
        embed.set_footer(text=embeddata["name"]+" ["+embeddata["version"]+"]")
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(App(client))
