import asyncio
from datetime import date, datetime

import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

role_lists = {
    "only_owner": [832981829581275197],
    "owner": [832981829581275197, 857001467449311252],
    "admin": [832981829581275197, 857001467449311252, 832981836392431656],
    "head_mod": [832981829581275197, 857001467449311252, 832981836392431656, 849844685617889330],
    "mod": [832981829581275197, 857001467449311252, 832981836392431656, 849844685617889330, 832981849004703794],
    "helper": [832981829581275197, 857001467449311252, 832981836392431656, 849844685617889330, 832981849004703794, 870598557319700520],
}

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(administrator=True)
    @commands.has_any_role(*role_lists["head_mod"])
    async def ban(self, ctx, member : discord.User = None, *, reason=None):
        await ctx.message.delete()

        if member is None or member == ctx.message.author:
            responce = await ctx.channel.send("Sorry but you cannot ban yourself.")
            await asyncio.sleep(3)
            await responce.delete()
            return

        time = datetime.now().strftime("%H:%M:%S")

        if reason is None:
            reason = f"Reason Unknown - Banned {date.today()} At {time}"
        else:
            reason = reason + f"""- Banned {date.today()} At {time}"""

        dm_embed = discord.Embed(title=f"You have been banned from {ctx.guild.name} for {reason}", color=0x00fffb)

        try:
            await member.send(embed=dm_embed)
        except discord.HTTPException:
            pass

        await ctx.guild.ban(member, reason=reason)

        responce = await ctx.channel.send(f"{member} Has been banned!")
        await asyncio.sleep(3)
        await responce.delete()

    @ban.error
    async def ban_error(self, ctx, error):
        await ctx.message.delete()
        if isinstance(error, commands.BotMissingPermissions):
            responce = await ctx.send("I currently don't have administrator permissions, please provide me with them to use me!")
            await asyncio.sleep(3)
            await responce.delete()

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'This command can not be used in private messages.')
            except discord.HTTPException:
                pass

        elif isinstance(error, commands.MissingAnyRole):
            responce = await ctx.send(f"Sorry you don't have permission to do that.")
            await asyncio.sleep(3)
            await responce.delete()

        else:
            await ctx.send(f"Looks like something went wrong. Error:\n```{error}```")

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(administrator=True)
    @commands.has_any_role(*role_lists["mod"])
    async def kick(self, ctx, member : discord.User = None, *, reason=None):
        await ctx.message.delete()

        if member is None or member == ctx.message.author:
            responce = await ctx.channel.send("Sorry but you cannot kick yourself.")
            await asyncio.sleep(3)
            await responce.delete()
            return

        time = datetime.now().strftime("%H:%M:%S")

        if reason is None:
            reason = f"Reason Unknown - Kicked {date.today()} At {time}"
        else:
            reason = reason + f"""- Kicked {date.today()} At {time}"""

        dm_embed = discord.Embed(title=f"You have been kicked from {ctx.guild.name} for {reason}", color=0x00fffb)

        try:
            await member.send(embed=dm_embed)
        except discord.HTTPException:
            pass

        await ctx.guild.kick(member, reason=reason)

        responce = await ctx.channel.send(f"{member} Has been kicked!")
        await asyncio.sleep(3)
        await responce.delete()

    @kick.error
    async def kick_error(self, ctx, error):
        await ctx.message.delete()
        if isinstance(error, commands.BotMissingPermissions):
            responce = await ctx.send("I currently don't have administrator permissions, please provide me with them to use me!")
            await asyncio.sleep(3)
            await responce.delete()

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'This command can not be used in private messages.')
            except discord.HTTPException:
                pass

        elif isinstance(error, commands.MissingAnyRole):
            responce = await ctx.send(f"Sorry you don't have permission to do that.")
            await asyncio.sleep(3)
            await responce.delete()

        else:
            await ctx.send(f"Looks like something went wrong. Error:\n```{error}```")

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(administrator=True)
    @commands.has_any_role(*role_lists["helper"]) # owner/co owner/admin/head mod/mod
    async def purge(self, ctx, user : discord.Member = None, limit : int = 10):
        await ctx.message.delete()

        if user == None:
            await ctx.channel.purge(limit=limit)
            responce = await ctx.send(f"✅ Cleared by {ctx.author.mention}")
            await asyncio.sleep(3)
            await responce.delete()

        else:
            if limit > 100:
                await ctx.send("Sorry you can only delete a max of 100 messages when specifying a user!")
                return
            await ctx.channel.purge(limit=amount, check=lambda message: message.author.id == user.id)


    @purge.error
    async def purge_error(self, ctx, error):
        await ctx.message.delete()
        if isinstance(error, commands.BotMissingPermissions):
            responce = await ctx.send("I currently don't have administrator permissions, please provide me with them to use me!")
            await asyncio.sleep(3)
            await responce.delete()

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'This command can not be used in private messages.')
            except discord.HTTPException:
                pass

        elif isinstance(error, commands.MissingAnyRole):
            responce = await ctx.send(f"Sorry you don't have permission to do that.")
            await asyncio.sleep(3)
            await responce.delete()

        else:
            await ctx.send(f"Looks like something went wrong. Error:\n```{error}```")


def setup(client):
    client.add_cog(Moderation(client))
