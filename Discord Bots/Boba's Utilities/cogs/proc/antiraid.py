import discord, time, asyncio, os, random, json
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, cooldown, MissingPermissions, check
from discord.utils import get
from datetime import datetime, date
from discord_webhook import DiscordWebhook, DiscordEmbed
from termcolor import colored

class Utils(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.joinlogs = {}

        self.raid_bans = []

        self.raid_switch = False

        self.jointimer.start()

        self.slowmode_memory = {}

        f = open("data/slowmode_channels.json")
        self.channels_to_slowmode = json.load(f)
        f.close()

        print("System - AntiRaid                 "+colored('Running', 'green'))

    @commands.Cog.listener()
    async def on_ready(self):
        await asyncio.sleep(3)
        print("\nAntiRaid: "+colored("Ready!", "green"))

    async def ban_log(self, user):
        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/825788651312250920/_I9u6EwZ5hCu28EjahF7CGNbUEBwA148Y9HrT2DY3CCUhdznZXlWLxTk9JAHhtg62Ejy')

        embed = DiscordEmbed(title=f"{user.name}#{user.discriminator} has been banned!", colour="00ffff", description=f"<:profile:825645321328525322> **Member:** {user.name}#{user.discriminator} **[{user.id}]**\n<:rightArrow:825645321400614952> **Reason:** Account joined during raid and was too young!", username="Boba's Utilities", avatar_url=f"{self.client.user.avatar_url}")

        embed.set_thumbnail(url=f"{user.avatar_url}")
        embed.set_footer(text="Boba's Utilities - AntiRaid")

        embed.add_embed_field(name="More Details:", value=f"<:NoDM:825645320993374220> **Member Direct Messaged?** <:Cross:825645321160753182>\n<:Ban:825788207173992478> **Member Punished?** <:Check:825645321140305930>")

        webhook.add_embed(embed)
        response = webhook.execute()

    def is_authed(ctx):
        with open("data/authed.json") as f:
            authed = json.load(f)
            f.close()
        return ctx.author.id in authed

    def is_all(ctx):
        allperms = [484555838837489685, 694946210372517888, 508372340904558603]

        return ctx.author.id in allperms

    @commands.command()
    @check(is_all)
    async def addperm(self, ctx, user : discord.Member = None):
        with open("data/authed.json") as f:
            authed = json.load(f)
            f.close()

        if user.id in authed:
            pass

        else:
            authed.append(user.id)

        with open("data/authed.json", "w+") as f:
            json.dump(authed, f)
            f.close()

        await ctx.send("User added!")

    @commands.command()
    @check(is_all)
    async def takeperm(self, ctx, user : discord.Member = None):
        with open("data/authed.json") as f:
            authed = json.load(f)
            f.close()

        if user.id not in authed:
            pass

        else:
            authed.remove(user.id)

        with open("data/authed.json", "w+") as f:
            json.dump(authed, f)
            f.close()

        await ctx.send("User removed!")

    @commands.command()
    async def test(self, ctx):
        await ctx.send(ctx.channel.slowmode_delay)

    @commands.command()
    @check(is_authed)
    async def raid(self, ctx, mode : str = None):
        if mode.lower() == "start":
            if self.raid_switch == True:
                await ctx.send("A raid is already happening!")
                return
            self.slowmode_memory = {}
            self.raid_switch = True
            await ctx.send("Ok anyone's who account is under 1h old will now be banned!\nApplying slowmode...")

            num = 0
            async with ctx.typing():
                for channelid in self.channels_to_slowmode:
                    channel = self.client.get_channel(channelid)
                    self.slowmode_memory[str(channelid)] = channel.slowmode_delay
                    await channel.edit(slowmode_delay=20)
                    num += 1

            await ctx.send(f"Applied 20s slowmode to {str(num)} channels!")

            for member in self.joinlogs:
                try:
                    userobj = get(ctx.guild.members, id=int(member))
                except:
                    userobj = None

                if userobj != None:
                    hour_then = int(userobj.created_at.hour)
                    hour_rn = int(datetime.now().hour)

                    if hour_then == hour_rn or userobj.id == 731073576240939078:
                        await userobj.ban(reason="AntiRaid AutoBan - Banned because new account during raid!")
                        await self.ban_log(userobj)
                        self.raid_bans.append(userobj.id)
        elif mode.lower() == "stop":
            if self.raid_switch == False:
                await ctx.send("You need to start it first!")
                return
            self.raid_switch = False
            await ctx.send("Ok, Off!")
            cnl = self.client.get_channel(804101559965188126)
            endstring = ""
            for user in self.raid_bans:
                endstring += str(user)
            if endstring == "":
                endstring = "No one has been banned!"
            await ctx.send("Logging all bans in admin chat!")
            await cnl.send("Everyone banned during raid:")
            await cnl.send(endstring)
            self.raid_bans = []

            await ctx.send("Removing slowmode...")

            num = 0

            for channelid in self.channels_to_slowmode:
                channel = self.client.get_channel(channelid)
                try:
                    await channel.edit(slowmode_delay=self.slowmode_memory[str(channelid)])
                except KeyError:
                    await channel.edit(slowmode_delay=0)
                num += 1

            await ctx.send(f"Removed slowmode from {str(num)} channels!")
        else:
            await ctx.send("Mode not found, try again with [start/stop]!")

    @tasks.loop(seconds=1)
    async def jointimer(self):
        todel = []
        for member in self.joinlogs:
            self.joinlogs[member]["time"] -= 1
            if self.joinlogs[member]["time"] < 1:
                todel.append(member)

        for member in todel:
            del self.joinlogs[member]

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not self.raid_switch:
            self.joinlogs[str(member.id)] = {"id": member.id, "time": 30}

        else:
            hour_then = int(member.created_at.hour)
            hour_rn = int(datetime.now().hour)

            datemade = ctx.author.created_at.date()
            datenow = datetime.now().strftime("%Y-%m-%d")

            if hour_then == hour_rn and datemade == datenow:
                await member.ban(reason="AntiRaid AutoBan - Banned because new account during raid!")
                await self.ban_log(member)
                self.raid_bans.append(member.id)

def setup(client):
    client.add_cog(Utils(client))
