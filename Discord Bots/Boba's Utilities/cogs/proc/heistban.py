import discord, time, asyncio, os, random, json, re
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, cooldown, MissingPermissions, check, has_role
from discord.utils import get
from discord_webhook import DiscordWebhook, DiscordEmbed
from termcolor import colored
from urlextract import URLExtract

class Utils(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.switch = False

        print("System - Heist Leave Ban          "+colored('Running', 'green'))

    def is_authed(ctx):
        authed = []
        return ctx.authod.id in authed

    @commands.command()
    @has_permissions(administrator=True)
    async def heistban(self, ctx):
        self.switch = True
        await ctx.send("Now banning leaves for 2hrs!")

        t_end = time.time() + 7200
        while time.time() < t_end:
            pass
            await asyncio.sleep(1)

        self.switch = False

    @commands.command()
    @has_permissions(administrator=True)
    async def stopheistban(self, ctx):
        self.switch = False
        await ctx.send("Ok, Stopped banning leaves!")


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if self.switch:
            user = member
            await member.ban(reason="Heist Ban - Banned because they left after a heist!")
            cnl = self.client.get_channel(825335559617642516)
            webhook = DiscordWebhook(url='https://discord.com/api/webhooks/826912364984533012/7DYr0Pe5nDT0p5_Jy10-xhNvqO3MFB-dfxRQc2ahHUyF0pGA-zUe2Nw67tKNiJgbsp-0')

            embed = DiscordEmbed(title=f"{user.name}#{user.discriminator} has been banned!", colour="00ffff", description=f"<:profile:825645321328525322> **Member:** {user.name}#{user.discriminator} **[{user.id}]**\n<:rightArrow:825645321400614952> **Reason:** Account left after a heist!", username="Boba's Utilities", avatar_url=f"{self.client.user.avatar_url}")

            embed.set_thumbnail(url=f"{user.avatar_url}")
            embed.set_footer(text="Boba's Utilities - Heist Ban")

            embed.add_embed_field(name="More Details:", value=f"<:NoDM:825645320993374220> **Member Direct Messaged?** <:Cross:825645321160753182>\n<:Ban:825788207173992478> **Member Punished?** <:Check:825645321140305930>")

            webhook.add_embed(embed)
            response = webhook.execute()







def setup(client):
    client.add_cog(Utils(client))
