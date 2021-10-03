import discord, time, os, praw, random, json
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, MissingPermissions
from discord.utils import get
from itertools import cycle
import datetime as dt
from datetime import datetime

class App(commands.Cog):
    def __init__(self, client):
        self.client = client
        print("Loading Cog: HELP")

    def gp(ctx):
        with open("prefixs.json", "r") as all_prefixs:
            prefixs = json.load(all_prefixs)
        return prefixs[str(ctx.message.guild.id)]

    @commands.command(aliases=["commands"])
    async def help(self, ctx, page=0):
        if page == 0:
            embed=discord.Embed(title="Help", description="Please type help then the number to see the commands.", color=0x13edf9)
            embed.add_field(name="1. FUN", value="For fun commands", inline=False)
            embed.add_field(name="2. MOD", value="For moderation commands", inline=False)
            embed.add_field(name="3. MONEY", value="For the money commands", inline=False)
            embed.add_field(name="4. YOUTUBE", value="For the youtube commands", inline=False)
            await ctx.send(embed=embed)
        elif page == 1:
            embed=discord.Embed(title="Help", description="Fun:", color=0x13edf9)
            embed.add_field(name=gp(ctx)+"ping", value="Will tell you the clients ping", inline=False)
            embed.add_field(name=gp(ctx)+"meme", value="""Get you a "new" meme from reddit""", inline=False)
            embed.add_field(name=gp(ctx)+"servers", value="Shows you all the servers the bot is in", inline=False)
            embed.add_field(name=gp(ctx)+"members", value="Counts the ammount of members in your server", inline=False)
            await ctx.send(embed=embed)
        elif page == 2:
            embed=discord.Embed(title="Help", description="Mod:", color=0x13edf9)
            embed.add_field(name=gp(ctx)+"ban <who> [reason]", value="Bans a member", inline=False)
            embed.add_field(name=gp(ctx)+"kick <who> [reason]", value="Kicks a member", inline=False)
            embed.add_field(name=gp(ctx)+"clear <ammount>", value="Deletes a certain amount of messages in a channel", inline=False)
            await ctx.send(embed=embed)
        elif page == 3:
            embed=discord.Embed(title="Help", description="Money", color=0x13edf9)
            embed.add_field(name=gp(ctx)+"moneysetup", value="If auto setup failed for your server run this", inline=False)
            embed.add_field(name=gp(ctx)+"bal <user>", value="Allows you to see your/others balence", inline=False)
            embed.add_field(name=gp(ctx)+"beg", value="Allows you to beg for money every 50 secconds", inline=False)
            embed.add_field(name=gp(ctx)+"steal", value="Allows you to steal money from someone every 50 secconds", inline=False)
            embed.add_field(name=gp(ctx)+"passive <on/off>", value="Allows you to enable passive mode so you can't steal nor be stolen from", inline=False)
            await ctx.send(embed=embed)
        elif page == 4:
            embed=discord.Embed(title="Help", description="Youtube", color=0x13edf9)
            embed.add_field(name=gp(ctx)+"stats <link>", value="Gets stats from a youtube channel (some channels may not work)", inline=False)
            await ctx.send(embed=embed)
        elif page == 5:
            embed=discord.Embed(title="Help", description="Levels", color=0x13edf9)
            embed.add_field(name=gp(ctx)+"levelsetup", value="If auto setup failed for your server run this", inline=False)
            embed.add_field(name=gp(ctx)+"rank <user>", value="Gets you rank in the server!", inline=False)
            embed.add_field(name=gp(ctx)+"top", value="Gets the top 3 highest ranks in the server!", inline=False)
            await ctx.send(embed=embed)

        else:
            await ctx.send("Page not found!")
def setup(client):
    client.add_cog(App(client))
