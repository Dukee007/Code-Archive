import discord, time, os, praw, random, json, urllib
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, MissingPermissions
from discord.utils import get
from itertools import cycle
import datetime as dt
from datetime import datetime

embeddata = {}
embeddata["icon"] = "http://luna-development.orgfree.com/data/discord/meme6/logo.jpg"
embeddata["name"] = "Meme6"
embeddata["version"] = "2.0"

class App(commands.Cog):
    def __init__(self, client):
        self.client = client
        print("Loading Cog: YOUTUBE")

    @commands.command()
    async def stats(self, ctx, link):
        channel_id = link.split("/channel/")
        channel_id = channel_id[1]

        api_key = "AIzaSyAydqfsNwTWhMIpWQeLtHTpIvx9Uf5Yu4U"

        data = urllib.request.urlopen("https://www.googleapis.com/youtube/v3/channels?part=statistics&id="+channel_id+"&key="+api_key).read()

        x = subs = json.loads(data)["items"][0]["statistics"]
        subs = json.loads(data)["items"][0]["statistics"]["subscriberCount"]
        views = json.loads(data)["items"][0]["statistics"]["viewCount"]
        vids = json.loads(data)["items"][0]["statistics"]["videoCount"]
        avepervid = round(int(views)/int(vids), 0)

        embed=discord.Embed(title="YouTube Stats", url=link)
        embed.set_author(name=embeddata["name"], icon_url=embeddata["icon"])
        embed.add_field(name="Subscribers:", value=str(subs), inline=False)
        embed.add_field(name="Views:", value=str(views), inline=False)
        embed.add_field(name="Videos:", value=str(vids), inline=False)
        embed.add_field(name="Average views per video:", value=str(avepervid), inline=False)
        embed.set_footer(text=embeddata["name"]+" ["+embeddata["version"]+"]")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(App(client))
