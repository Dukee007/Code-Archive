import discord, time, asyncio, os, random, json
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, cooldown, MissingPermissions, check, Cog
from discord.utils import get

class App(commands.Cog):
    def __init__(self, client):
        self.client = client
        print("Reminders Cog Running")

    @Cog.listener()
    async def on_member_join(self, member):
        f = open("data/remind.json")
        remindme = json.load(f)
        f.close()
        for user in remindme["join"]:
            user = get(member.guild.members, id=int(user))
            await user.send(f"{user.mention} Hey, {member.name} just joined the server. Be sure to greet them. You can turn these reminders off using the `.remindme join off/on` command.")

    @Cog.listener()
    async def on_member_remove(self, member):
        f = open("data/remind.json")
        remindme = json.load(f)
        f.close()
        for user in remindme["leave"]:
            user = get(member.guild.members, id=int(user))
            await user.send(f"{user.mention} Hey, {member.name} just left the server. You can turn these reminders off using the `.remindme leave off/on` command.")

    @commands.command()
    async def remindme(self, ctx, reminder : str = None, mode : str = None):
        if reminder == None or reminder not in ["join", "leave"] or mode == None or mode not in ["on", "off"]:
            embed=discord.Embed(title="Incorrect command usage!", description=".remindme {option} [on/off]", color=0x00ffff)
            await ctx.send(embed=embed)
            return

        f = open("data/remind.json")
        remindme = json.load(f)
        f.close()

        try:
            try:
                remindme[reminder].pop(str(ctx.author.id))
            except:
                if mode == "on":
                    remindme[reminder].append(str(ctx.author.id))
                else:
                    pass
        except:
            remindme[reminder] = []
            try:
                remindme[reminder].pop(str(ctx.author.id))
            except:
                if mode == "on":
                    remindme[reminder].append(str(ctx.author.id))
                else:
                    pass

        f = open("data/remind.json", "w+")
        json.dump(remindme, f)
        f.close()

        await ctx.send("Settings Updated!")


def setup(client):
    client.add_cog(App(client))
