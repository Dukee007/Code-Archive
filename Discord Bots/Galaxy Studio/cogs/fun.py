import discord, time, asyncio, os, random, json, asyncpraw
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, cooldown, MissingPermissions, check
from discord.utils import get

class App(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.reddit = asyncpraw.Reddit(client_id='m1HOyUizUb2SlQ',
                     client_secret='RNpb2STGM-Z7CvttKju74rhI1Ig',
                     user_agent='AGENT69')
        print("Fun Cog Running")


    @commands.command()
    async def meme(self, ctx):
        memes_submissions = self.reddit.subreddit('memes').hot(limit=100)
        post_to_pick = random.randint(1, 100)
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)
        embed = discord.Embed(title=submission.title,
                              description=f"Here is your meme! 😀 Made by: {submission.author}", color=0x00fffb)
        embed.set_image(url=submission.url)
        embed.set_footer(text="Galaxy Bot")
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(App(client))
