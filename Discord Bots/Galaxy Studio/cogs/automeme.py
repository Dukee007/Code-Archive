import discord, time, asyncio, os, random, json, asyncpraw
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, cooldown, MissingPermissions, check, Cog
from discord.utils import get

class App(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.isfirst = True
        self.reddit = asyncpraw.Reddit(client_id='m1HOyUizUb2SlQ',
                     client_secret='RNpb2STGM-Z7CvttKju74rhI1Ig',
                     user_agent='AGENT69')
        self.send_meme.start()
        print("Automeme Cog Running")

    @tasks.loop(seconds=15)
    async def send_meme(self):
        if self.isfirst:
            await asyncio.sleep(5)
            self.isfirst = False
        with open("data/automeme.json") as f:
            meme = json.load(f)
            f.close()

        if meme["mode"] == "on":
            meme_channel = get(self.client.guilds[0].channels, id=801164213048836115)
            memes_submissions = self.reddit.subreddit('memes').hot(limit=5000)
            post_to_pick = random.randint(1, 100)
            for i in range(0, post_to_pick):
                submission = next(x for x in memes_submissions if not x.stickied)
            embed = discord.Embed(title=submission.title,
                                  description=f"😀 Sent by: {submission.author}", color=0x00fffb)
            embed.set_image(url=submission.url)
            embed.set_footer(text="Galaxy Bot Automeme")
            await meme_channel.send(embed=embed)

    @commands.command()
    @has_permissions(manage_channels=True)
    async def automeme(self, ctx, mode : str = None):
        if mode == None or mode not in ["on", "off"]:
            embed=discord.Embed(title="Incorrect command usage!", description=".automeme [on/off]", color=0x00ffff)
            await ctx.send(embed=embed)
            return

        with open("data/automeme.json") as f:
            meme = json.load(f)
            f.close()

        meme["mode"] = mode

        with open("data/automeme.json", "w+") as f:
            json.dump(meme, f)
            f.close()

        await ctx.send("Settings Updated!")


def setup(client):
    client.add_cog(App(client))
