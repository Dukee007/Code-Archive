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
        print("Info                    "+colored('Running', 'green'))


    @commands.command(aliases = ['robowizzz'])
    async def bot(self, ctx):
        embed=discord.Embed(title="I think i am the best bot here! How about you?", color=0x00fffb)
        embed.set_footer(text="Epic bot")
        await ctx.send(embed=embed)

    #@commands.command(aliases = ['help1'])
    async def roles(self, ctx):
        embed=discord.Embed(title="These are the roles you need to know about:", color=0x00ffff)
        embed.add_field(name="Owner", value="The owner of the server!", inline=False)
        embed.add_field(name="Co Owner", value="The second owner of the server!", inline=False)
        embed.add_field(name="Bot Manager", value="The developer for <@!810909952183894136> And main server admin!", inline=False)
        embed.add_field(name="Staff Manager", value="Members with this role recruit staff and manage their training. They also promote and demote staff after discussion with higher roles!", inline=False)
        embed.add_field(name="Moderation Staff", value="Members with this role moderate the server!", inline=False)
        embed.add_field(name="Support Staff", value="Members with this role are part of the staff and help members if they have queries!", inline=False)
        embed.add_field(name="Youtubers", value="Members are given this role if they have the requirements!", inline=False)
        embed.add_field(name="Contributors", value="Members are given this role if they have contributed to the owner or to the server in any way.", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def group(self, ctx):
        embed = discord.Embed(title="Join the Wizard Community!", colour=discord.Colour(0x00ffff), url="https://www.roblox.com/groups/8023342/The-Wizard-Community#!/about", description="**Join my roblox group now!\nRemember you need to be in the group for atleast 3 days so that if you need to claim robux there is no delay!**\n\n[Join Here](https://www.roblox.com/groups/8023342/The-Wizard-Community#!/about)")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/805767946193731604/816305708151996426/icon.png")
        embed.set_footer(text="Official Wizard Community Roblox Group.", icon_url="https://media.discordapp.net/attachments/805767946193731604/816301259304861706/das.png")

        await ctx.send(embed=embed)

    @commands.command(aliases = ['latency'])
    async def ping(self, ctx):
        embed=discord.Embed(title="Report to owner if the bot is lagging. If the latency is above 500ms, the bot is probably lagging.", color=0x00ffee)
        embed.set_author(name=f"Current Bot Latency is {str(round(self.client.latency * 1000))}ms.")
        embed.set_thumbnail(url='https://media.discordapp.net/attachments/798968646336249928/816354387051151400/das.png')
        embed.set_footer(text="Robo Wizzz Latency.")
        await ctx.send(embed=embed)

    @commands.command(aliases = ['higherroles'])
    async def staff(self, ctx):
        embed=discord.Embed(title="To apply for staff, you need to wait till we open staff applications. When we open them we will inform everyone.", color=0x00fffb)
        embed.set_author(name="Its not yet time!")
        embed.set_footer(text="Staff Applications Prompt.")
        await ctx.send(embed=embed)



def setup(client):
    client.add_cog(App(client))
