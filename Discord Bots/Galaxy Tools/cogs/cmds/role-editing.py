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

class RoleEditing(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(administrator=True)
    @commands.has_any_role(*role_lists["owner"])
    async def role(self, ctx, mode, role : discord.Role):
        await ctx.message.delete()

        if mode not in ["humans", "rhumans", "all", "rall", "bots", "rbots"]:
            return

        if mode == "humans":
            responce = await ctx.send("Loading...")
            users = 0
            for member in ctx.guild.members:
                if not member.bot:
                    if role not in member.roles:
                        await member.add_roles(role)

            await responce.edit(content=f"Added {role.name} to {str(users)} members!")
            await asyncio.sleep(3)
            await responce.delete()

        elif mode == "rhumans":
            responce = await ctx.send("Loading...")
            users = 0
            for member in ctx.guild.members:
                if not member.bot:
                    users += 1
                    try:
                        await member.remove_roles(role)
                    except:
                        pass

            await responce.edit(content=f"Added {role.name} to {str(users)} members!")
            await asyncio.sleep(3)
            await responce.delete()

    @role.error
    async def role_error(self, ctx, error):
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
    client.add_cog(RoleEditing(client))
