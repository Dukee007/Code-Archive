import discord, time, asyncio, os, random, json
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, cooldown, MissingPermissions, check
from discord.utils import get
from termcolor import colored

class App(commands.Cog):
    def __init__(self, client):
        self.client = client
        print("Moderation               "+colored('Running', 'green'))

    @commands.command(aliases=['clear'])
    @has_permissions(manage_messages=True)
    async def purge(self, ctx, limit : int = 2):
        try:
            x = int(limit)
        except:
            await ctx.send("Thats not a number!")
            return

        await ctx.channel.purge(limit = limit)
        msg = await ctx.send(f"Cleared by {ctx.author.mention}")
        await asyncio.sleep(2)
        await msg.delete()

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title="This command can be used only by members who moderate the server.", color=0xff0000)
            embed.set_author(name="Hey! You are not allowed to do that!")
            embed.set_thumbnail(url='https://images-ext-2.discordapp.net/external/N8LpKSOO52iNCGjQQ6yJOqlW89RJkzSbDSNjOOa_mVg/%3Fwidth%3D427%26height%3D427/https/media.discordapp.net/attachments/798968646336249928/816351655812792410/kKMxMuzufRPMRxioYgWq_XylZQ1cP0nJ89Za3Bo0VxNGypkybermjXlzOhjW-gCEuT675G4cz_CBDo5Db7Qow5sUuR70FUlXVwag.png?width=300&height=300')
            embed.set_footer(text="Robo Wizzz Moderation.")
            await ctx.send(embed=embed)
        else:
            raise error


    @commands.command(aliases=['k'])
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason = "No reason has been provided by the Moderator."):
        name = member.name
        await member.kick(reason=reason)
        embed=discord.Embed(title=f"Reason: {reason}", description="ID: 1828392010192", color=0x24a800)
        embed.set_author(name=f"{name} has been kicked from the server.")
        embed.set_thumbnail(url='https://media.discordapp.net/attachments/811227367635681321/816702594361458708/woman-s-boot-emoji-clipart-sm.png')
        embed.set_footer(text="Robo Wizzz Moderation.")
        await ctx.send(embed=embed)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title="This command can be used only by members who moderate the server.", color=0xff0000)
            embed.set_author(name="Hey! You are not allowed to do that!")
            embed.set_thumbnail(url='https://images-ext-2.discordapp.net/external/N8LpKSOO52iNCGjQQ6yJOqlW89RJkzSbDSNjOOa_mVg/%3Fwidth%3D427%26height%3D427/https/media.discordapp.net/attachments/798968646336249928/816351655812792410/kKMxMuzufRPMRxioYgWq_XylZQ1cP0nJ89Za3Bo0VxNGypkybermjXlzOhjW-gCEuT675G4cz_CBDo5Db7Qow5sUuR70FUlXVwag.png?width=300&height=300')
            embed.set_footer(text="Robo Wizzz Moderation.")
            await ctx.send(embed=embed)
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send(f"❌ Hey, {ctx.author.name} I can't cannot kick this member!")
        else:
            raise error

    @commands.command(aliases=['b'])
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason = "No reason has been provided by the Moderator."):
        name = member.name
        await member.ban(reason=reason)
        embed=discord.Embed(title=f"Reason: {reason}", description="ID: 1828392010192", color=0x24a800)
        embed.set_author(name=f"{name} has been banned from the server.")
        embed.set_thumbnail(url='https://media.discordapp.net/attachments/811227367635681321/816702594361458708/woman-s-boot-emoji-clipart-sm.png')
        embed.set_footer(text="Robo Wizzz Moderation.")
        await ctx.send(embed=embed)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title="This command can be used only by members who moderate the server.", color=0xff0000)
            embed.set_author(name="Hey! You are not allowed to do that!")
            embed.set_thumbnail(url='https://images-ext-2.discordapp.net/external/N8LpKSOO52iNCGjQQ6yJOqlW89RJkzSbDSNjOOa_mVg/%3Fwidth%3D427%26height%3D427/https/media.discordapp.net/attachments/798968646336249928/816351655812792410/kKMxMuzufRPMRxioYgWq_XylZQ1cP0nJ89Za3Bo0VxNGypkybermjXlzOhjW-gCEuT675G4cz_CBDo5Db7Qow5sUuR70FUlXVwag.png?width=300&height=300')
            embed.set_footer(text="Robo Wizzz Moderation.")
            await ctx.send(embed=embed)
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send(f"❌ Hey, {ctx.author.mention} I can't cannot ban this member!")
        else:
            raise error

def setup(client):
    client.add_cog(App(client))
