import discord, time, asyncio, os, random, json, datetime, pytz
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, cooldown, MissingPermissions, check, Cog
from discord.utils import get

class App(commands.Cog):
    def __init__(self, client):
        self.client = client
        print("Utils Cog Running")

    @commands.command()
    async def time(self, ctx):
        est_time = str(datetime.datetime.now(pytz.timezone("EST")).strftime('%H:%M:%S'))
        gmt_time = str(datetime.datetime.now(pytz.timezone("GMT")).strftime('%H:%M:%S'))

        pst_time = gmt_time.split(":")
        pst_time.pop(2)
        hrs = int(pst_time[0]) - 8
        pst_time.pop(0)
        pst_time.insert(0, str(hrs))
        pst_time_l = pst_time
        pst_time = f"""{pst_time_l[0]}:{pst_time_l[1]}:{datetime.datetime.now(pytz.timezone("EST")).strftime('%S')}"""

        ast_time = gmt_time.split(":")
        ast_time.pop(2)
        hrs = int(ast_time[0]) - 4
        ast_time.pop(0)
        ast_time.insert(0, str(hrs))
        ast_time_l = ast_time
        ast_time = f"""{ast_time_l[0]}:{ast_time_l[1]}:{datetime.datetime.now(pytz.timezone("EST")).strftime('%S')}"""

        embed=discord.Embed(title="Time", description="This is the time for our members")
        embed.add_field(name="Wigglg, Sam and Fuzzy:", value=est_time, inline=False)
        embed.add_field(name="LUNA:", value=gmt_time, inline=False)
        embed.add_field(name="Blacklisted", value=pst_time, inline=False)
        embed.add_field(name="William Cole", value=ast_time, inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def cleardms(self, ctx):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            dontdel = await ctx.send("Clearing all messages (I can)")
            msgs = await ctx.channel.history(limit=100).flatten()
            for message in msgs:
                if message.id == dontdel.id:
                    continue
                if message.author == self.client.user:
                    try:
                        await message.delete()
                    except:
                        pass

        else:
            await ctx.send("This command can only be used in dms!")

    @commands.command()
    @has_permissions(administrator=True)
    async def grant(self, ctx, user : str = None, role : discord.Role = None):
        if user == None or role == None:
            embed=discord.Embed(title="Incorrect command usage!", description=".grant @user @role", color=0x00ffff)
            await ctx.send(embed=embed)
            return

        if user == "all" or user == "everyone":
            for user in ctx.guild.members:
                try:
                    await user.add_roles(role)
                except Exception as e:
                    print(e)
            await ctx.send(f"✅ I have given everyone (i can) the {role.name} role!")
            return

        try:
            await user.give_roles(role)
            await ctx.send(f"✅ I have given {user.mention} the {role.name} role!")
        except:
            await ctx.send("❌ I can't do that!")

    @commands.command()
    @has_permissions(administrator=True)
    async def deny(self, ctx, user : discord.Member = None, role : discord.Role = None):
        if user == None or role == None:
            embed=discord.Embed(title="Incorrect command usage!", description=".deny @user @role", color=0x00ffff)
            await ctx.send(embed=embed)
            return

        if role == "all" or role == "everyone":
            for user in ctx.guild.members:
                try:
                    await user.remove_roles(role)
                except:
                    pass
            await ctx.send(f"✅ I have taken the {role.name} role from everyone! (i can)")
            return

        user_id = int(str(user).replace("<@", "").replace(">", ""))

        user = get(ctx.guild.members, id=user_id)

        try:
            await user.remove_roles(role)
            await ctx.send(f"✅ I have taken the {role.name} role from {user.mention}!")
        except:
            await ctx.send("❌ I can't do that!")

    @commands.command()
    @has_permissions(administrator=True)
    async def syncall(self, ctx):
        for channel in ctx.guild.channels:
            await channel.edit(sync_permissions=True)
        await ctx.send("done!")

    @commands.command()
    async def report(self, ctx, user : discord.Member = None, link : str = None):
        if user == None or link == None:
            embed=discord.Embed(title="Incorrect command usage!", description=".report @user {message link}\nHow to get a message link:", color=0x00ffff)
            embed.set_image(url="https://i.ibb.co/nz8TwW8/copylink.gif")
            await ctx.send(embed=embed)
            return

        await ctx.message.delete()

        channel = self.client.get_channel(806527554541977731)
        embed=discord.Embed(title=f"Report, Sent by: {ctx.author}", description=f"User: {str(user)}\nMessage: [Click]({link})", color=0x00ffff)
        embed.set_footer(text="Galaxy Bot Reporting")
        await channel.send(embed=embed)
        await ctx.author.send("Your report has been sent and will be delt with soon\nWe have deleted the command so the user doesnt know they have been reported!\nThanks for your report!")
        msg = await ctx.send("Report Sent!")
        await asyncio.sleep(1)
        await msg.delete()

    @commands.command()
    async def byeworld(self, ctx):
        await ctx.send("Bye :wave:")
        await ctx.guild.leave()



def setup(client):
    client.add_cog(App(client))
