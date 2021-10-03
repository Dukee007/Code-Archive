import discord, time, asyncio, os, random, json
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, cooldown, MissingPermissions, check
from discord.utils import get

class App(commands.Cog):
    def __init__(self, client):
        self.client = client
        print("Mod Cog Running")

    @commands.command()
    @has_permissions(ban_members=True)
    async def ban(self, ctx, user : discord.Member = None, reason : str = None):
        if user == None:
            embed=discord.Embed(title="Incorrect command usage!", description=".ban @user reason", color=0x00ffff)
            await ctx.send(embed=embed)
            return

        if reason == None:
            reason = "Not Provided"

        try:
            await user.ban(reason=reason)
            embed=discord.Embed(title="User banned", description=f"{user.name} has been banned", color=0x00ffff)
            embed.add_field(name="Reason:", value=reason, inline=False)
            embed.add_field(name="Moderator:", value=ctx.author.name, inline=False)
            await ctx.send(embed=embed)
        except:
            embed=discord.Embed(title="Error", description="I cannot ban this user!", color=0x00ffff)
            await ctx.send(embed=embed)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"❌ Hey, {ctx.author.name} you can't do that!")

    @commands.command()
    @has_permissions(kick_members=True)
    async def kick(self, ctx, user : discord.Member = None, reason : str = None):
        if user == None:
            embed=discord.Embed(title="Incorrect command usage!", description=".kick @user reason", color=0x00ffff)
            await ctx.send(embed=embed)
            return

        if reason == None:
            reason = "Not Provided"

        try:
            await user.ban(reason=reason)
            embed=discord.Embed(title="User kicked", description=f"{user.name} has been kicked", color=0x00ffff)
            embed.add_field(name="Reason:", value=reason, inline=False)
            embed.add_field(name="Moderator:", value=ctx.author.name, inline=False)
            await ctx.send(embed=embed)
        except:
            embed=discord.Embed(title="Error", description="I cannot ban this user!", color=0x00ffff)
            await ctx.send(embed=embed)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"❌ Hey, {ctx.author.name} you can't do that!")

    @commands.command()
    @has_permissions(manage_messages=True)
    async def clear(self, ctx, limit : int = None):
        if limit == None:
            embed=discord.Embed(title="Incorrect command usage!", description=".ban @user reason", color=0x00ffff)
            await ctx.send(embed=embed)
            return

        await ctx.channel.purge(limit=limit+1)
        msg = await ctx.send(f"Cleared by {ctx.author.mention}")
        await asyncio.sleep(2)
        await msg.delete()

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"❌ Hey, {ctx.author.name} you can't do that!")

    @commands.command()
    @has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds : str = None):
        if seconds == "off":
            await ctx.channel.edit(slowmode_delay=0)
            await ctx.send(f"I have turned off slowmode!")
            return
        seconds = int(seconds)
        if seconds == None:
            embed=discord.Embed(title="Incorrect command usage!", description=".slowmode {number}", color=0x00ffff)
            await ctx.send(embed=embed)
            return
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"Set the slowmode delay in this channel to {seconds} seconds!")

    @slowmode.error
    async def slowmode_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"❌ Hey, {ctx.author.name} you can't do that!")

def setup(client):
    client.add_cog(App(client))
