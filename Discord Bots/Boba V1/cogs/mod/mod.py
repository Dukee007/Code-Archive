import discord, time, asyncio, os, random, json
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, cooldown, MissingPermissions, check
from discord.utils import get
from datetime import datetime, date
from termcolor import colored

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

        print("Commands - Moderation             "+colored('Running', 'green'))

    @commands.command()
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.User = None, reason = None):
        if member == None or member == ctx.message.author:
            error_message = await ctx.channel.send("❌ You cannot ban yourself")
            return
        if reason == None:
            e  = datetime.now()
            e = e.strftime("%H:%M:%S")
            reason = f"Reason Unknown - Banned {date.today()} At {e}"
        else:
            reason = reason+f""" - Banned {date.today()} At {datetime.now().strftime("%H:%M:%S")}"""
        embed=discord.Embed(title=f"You have been banned from {ctx.guild.name} for {reason}", color=0x00fffb)
        await member.send(embed=embed)
        await ctx.guild.ban(member, reason=reason)
        await ctx.channel.send(f"✅ {member} is banned!")

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            msg = await ctx.send("❌ You need to tell me who to ban!")
            return

        elif isinstance(error, commands.BotMissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            _message = '❌ I need the **{}** permission(s) to run this command.'.format(fmt)
            msg = await ctx.send(_message)

        elif isinstance(error, commands.MissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            _message = '❌ You need the **{}** permission(s) to use this command.'.format(fmt)
            msg = await ctx.send(_message)
            return
        elif isinstance(error, commands.UserNotFound):
            await ctx.send("❌ That user could not be found!")
        else:
            raise error

    @commands.command()
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.User = None, reason = None):
        if member == None or member == ctx.message.author:
            error_message = await ctx.channel.send("❌ You cannot kick yourself")
            return
        if reason == None:
            e  = datetime.now()
            e = e.strftime("%H:%M:%S")
            reason = f"Reason Unknown - Kicked {date.today()} At {e}"
        else:
            reason = reason+f""" - Kicked {date.today()} At {datetime.now().strftime("%H:%M:%S")}"""
        try:
            embed=discord.Embed(title=f"You have been Kicked from {ctx.guild.name} for {reason}", color=0x00fffb)
            await member.send(embed=embed)
        except:
            pass
        await ctx.guild.kick(member, reason=reason)
        await ctx.channel.send(f"✅ {member} has been kicked!")

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            msg = await ctx.send("❌ You need to tell me who to kick!")
            return

        elif isinstance(error, commands.BotMissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            _message = '❌ I need the **{}** permission(s) to run this command.'.format(fmt)
            msg = await ctx.send(_message)
            return

        elif isinstance(error, commands.MissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            _message = '❌ You need the **{}** permission(s) to use this command.'.format(fmt)
            msg = await ctx.send(_message)
            return
        else:
            raise error

    @commands.command()
    @has_permissions(manage_messages=True)
    async def clear(self, ctx, data):
        await ctx.message.delete()
        data = str(data)
        try:
            await ctx.channel.purge(limit=int(data))
            msg = await ctx.send(f"✅ Cleared by {ctx.author.mention}")
            await asyncio.sleep(2)
            await msg.delete()
        except:
            if "<@!" in data and ">" in data:
                data = int(data.replace("<@!", "").replace(">", ""))
                user = ctx.guild.get_member(data)
                user_id = user.id
                all_msgs = await ctx.channel.history(limit=500).flatten()
                for msg in all_msgs:
                    if int(msg.author.id) == int(user_id):
                        try:
                            await msg.delete()
                        except:
                            pass

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            msg = ctx.send("❌ You need to tell me how many messages you wanna clear!")
            return

        elif isinstance(error, commands.BotMissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            _message = '❌ I need the **{}** permission(s) to run this command.'.format(fmt)
            msg = await ctx.send(_message)
            return

        elif isinstance(error, commands.MissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            _message = '❌ You need the **{}** permission(s) to use this command.'.format(fmt)
            msg = await ctx.send(_message)
            return
        else:
            raise error

def setup(client):
    client.add_cog(Moderation(client))
