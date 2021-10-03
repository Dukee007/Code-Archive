import discord, time, asyncio, os, random, json, ezfile
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, cooldown, MissingPermissions, check
from discord.utils import get
from termcolor import colored
from threading import Thread

class App(commands.Cog):
    def __init__(self, client):
        self.client = client
        print("Money - Memberships               "+colored('Running', 'green'))

    def get_prefix(self, ctx):
        f = open("database/prefixs.json")
        prefixs = json.load(f)
        f.close()
        return prefixs[str(ctx.author.id)]

    @commands.command()
    async def membership(self, ctx, type : str = None):
        if type == None:
            embed=discord.Embed(title="Server Memberships", description="These are the memberships you can subscribe to in the server!", color=0x00ff1e)
            embed.set_thumbnail(url='https://www.pngitem.com/pimgs/m/113-1130365_badge-png-image-transparent-background-club-penguin-membership.png')
            embed.add_field(name="𝕯𝖊𝖒𝖔𝖓𝖎𝖈 𝕸𝖊𝖒𝖇𝖊𝖗𝖘𝖍𝖎𝖕", value=f"This is the highest tier membership in the server. You will need to pay `2500` weekly, to subscribe to this membership! Type `{str(self.get_prefix(ctx))}membership demonic` for more information on this one.", inline=False)
            embed.add_field(name="𝕻𝖑𝖆𝖙𝖎𝖓𝖚𝖒 𝕸𝖊𝖒𝖇𝖊𝖗𝖘𝖍𝖎𝖕", value=f"This is the Platinum tier membership. You will need to pay `1000` weekly, to subscribe to this membership! Type `{str(self.get_prefix(ctx))}membership platinum` for more information on this one.", inline=False)
            embed.add_field(name="𝕲𝖔𝖑𝖉 𝕸𝖊𝖒𝖇𝖊𝖗𝖘𝖍𝖎𝖕", value=f"This is the Gold tier membership. You will need to pay `750` weekly, to subscribe to this membership! Type `{str(self.get_prefix(ctx))}membership gold` for more information on this one.", inline=False)
            embed.add_field(name="𝕾𝖎𝖑𝖛𝖊𝖗 𝕸𝖊𝖒𝖇𝖊𝖗𝖘𝖍𝖎𝖕", value=f"This is the Silver tier membership. You will need to pay `300` weekly, to subscribe to this membership! Type `{str(self.get_prefix(ctx))}membership silver` for more information on this one.", inline=False)
            embed.add_field(name="𝕭𝖗𝖔𝖓𝖟𝖊 𝕸𝖊𝖒𝖇𝖊𝖗𝖘𝖍𝖎𝖕", value=f"This is the Bronze tier membership. You will need to pay `100` weekly, to subscribe to this membership! Type `{str(self.get_prefix(ctx))}membership bronze` for more information on this one.", inline=False)
            embed.set_footer(text="Robo Wizzz Currency System.")
            await ctx.send(embed=embed)

        elif type.lower() == "bronze":
            embed=discord.Embed(title="𝕭𝖗𝖔𝖓𝖟𝖊 𝕸𝖊𝖒𝖇𝖊𝖗𝖘𝖍𝖎𝖕", description="This is the lowest tier membership. To subscribe to this membership you will need to pay `100` weekly. Benefits of subscribing to this membership include, a `15%` chance to get a `x3` multiplier on every Ro-bucks earning you make.", color=0xff7b00)
            embed.set_thumbnail(url='https://purepng.com/public/uploads/large/purepng.com-bronze-medalmedalgold-medalbronze-medalsilvermedalawardribbon-1421526582563j3dkp.png')
            embed.set_footer(text="Robo Wizzz Currency System.")
            await ctx.send(embed=embed)

        elif type.lower() == "silver":
            embed=discord.Embed(title="𝕾𝖎𝖑𝖛𝖊𝖗 𝕸𝖊𝖒𝖇𝖊𝖗𝖘𝖍𝖎𝖕", description="This is the Silver Tier Membership. To subscribe to this membership you will need to pay `300` weekly. Benefits of subscribing to this membership include, a `35%` chance to get a `x3` multiplier on every Ro-bucks earning you make.", color=0x949494)
            embed.set_thumbnail(url='https://media.discordapp.net/attachments/811227367635681321/823898175718686750/New_Project.png?width=427&height=427')
            embed.set_footer(text="Robo Wizzz Currency System.")
            await ctx.send(embed=embed)

        elif type.lower() == "gold":
            embed=discord.Embed(title="𝕲𝖔𝖑𝖉 𝕸𝖊𝖒𝖇𝖊𝖗𝖘𝖍𝖎𝖕", description="This is the Gold Tier Membership. To subscribe to this membership you will need to pay `750` weekly. Benefits of subscribing to this membership include, a `55%` chance to get a `x3` multiplier on every Ro-bucks earning you make.", color=0xffee00)
            embed.set_thumbnail(url='https://media.discordapp.net/attachments/811227367635681321/823900598293364741/New_Project_1.png?width=427&height=427')
            embed.set_footer(text="Robo Wizzz Currency System.")
            await ctx.send(embed=embed)

        elif type.lower() == "platinum":
            embed=discord.Embed(title="𝕻𝖑𝖆𝖙𝖎𝖓𝖚𝖒 𝕸𝖊𝖒𝖇𝖊𝖗𝖘𝖍𝖎𝖕", description="This is the Platinum Tier Membership. To subscribe to this membership you will need to pay `1000` weekly. Benefits of subscribing to this membership include, a `75%` chance to get a `x3` multiplier on every Ro-bucks earning you make.", color=0xfafafa)
            embed.set_thumbnail(url='https://media.discordapp.net/attachments/811227367635681321/823901491009290240/New_Project_2.png?width=427&height=427')
            embed.set_footer(text="Robo Wizzz Currency System.")
            await ctx.send(embed=embed)

        elif type.lower() == "demonic":
            embed=discord.Embed(title="𝕯𝖊𝖒𝖔𝖓𝖎𝖈 𝕸𝖊𝖒𝖇𝖊𝖗𝖘𝖍𝖎𝖕", description="This is the Platinum Tier Membership. To subscribe to this membership you will need to pay `2500` weekly. Benefits of subscribing to this membership include, a `100%` chance to get a `x3` multiplier on every Ro-bucks earning you make.", color=0xff0000)
            embed.set_thumbnail(url='https://media.discordapp.net/attachments/811227367635681321/827458129138548747/robo_wizzz3.png')
            embed.set_footer(text="Robo Wizzz Currency System.")
            await ctx.send(embed=embed)

        else:
            await ctx.send("That tier could not be found!")

    @commands.command()
    async def subscribe():
        pass


def setup(client):
    client.add_cog(App(client))
