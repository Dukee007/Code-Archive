import discord, time, asyncio, os, random, json
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, cooldown, MissingPermissions, check
from discord.utils import get
from termcolor import colored

class App(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.answers = ['It is certain.',
                   'It is decidedly so.',
                   'Without a doubt.',
                   'Yes – definitely.',
                   'You may rely on it.',
                   'As I see it, yes.',
                   'Reply hazy.',
                   'try again.',
                   'Ask again later.',
                   '*OH NO MY SYSTEM BROKE DOWN. I CANNOT DECIDE LOL.*',
                   'Better not tell you now, nub.',
                   'Dont count on it.',
                   'My reply is no.',
                   'My sources say no.',
                   'Outlook not so good.',
                   'Very doubtful.']
        print("Games                    "+colored('Running', 'green'))


    @commands.command(aliases = ['8ball'])
    async def _8ball(self, ctx, *, question):
        await ctx.send(f'{random.choice(self.answers)}') # **Question:** {question}\n**Answer:**

    @commands.command(aliases = ["gayrate"])
    async def gayr8(self, ctx):
        embed=discord.Embed(title="Lol....", color=0x00fffb)
        embed.set_author(name=f"You are {str(random.randint(0, 100))}% gay!")
        embed.set_thumbnail(url='https://images-ext-2.discordapp.net/external/58-_e2vUDLV77jSpBCUWP_Ka5s3ZvNNFZrLduCntMAk/https/hubpng.com/download/vtxIh7HLSJfyDFfrlJoywKHr535RDfwfLGkPIyzoRMGVHHxpFNraUrzVBPFIhratqCWpWQQV5pnxQKU1NSZ92xR9tYNRfnxEkjs0pS0aIHZRyyEzmOmJ1UwR3mMfGDmFnqP56Bjvu94n9u9zLXEXZCHDvRf4FGEKHXNzpGO8vrvW0VPN3lOA3nGQoF3koE6ijO9XsEmi/large?width=266&height=300')
        embed.set_footer(text="Fun Commands System.")
        await ctx.send(embed=embed)

    @commands.command(aliases = ["nubrate"])
    async def nubr8(self, ctx):
        embed=discord.Embed(title="Thats pathetic. I expect you to become 100% nub sometime soon.", color=0x00fbff)
        embed.set_author(name=f"You are {str(random.randint(0, 99))}% nub!")
        embed.set_thumbnail(url='https://media.discordapp.net/attachments/811227367635681321/816589744719790080/1474130d39ecf1ef59da571b459696a8.png')
        embed.set_footer(text="Fun Commands System.")
        await ctx.send(embed=embed)



def setup(client):
    client.add_cog(App(client))
