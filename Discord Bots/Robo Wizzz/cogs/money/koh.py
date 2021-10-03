import discord, time, asyncio, os, random, json, ezfile
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, cooldown, MissingPermissions, check
from discord.utils import get
from termcolor import colored

class App(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.current_koh = {}
        self.koh_give_money.start()
        self.first = True
        print("Money - KOH               "+colored('Running', 'green'))

    @tasks.loop(seconds=60)
    async def koh_give_money(self):
        if self.current_koh != {}:
            if self.first:
                await asyncio.sleep(5)
                self.first = False
            try:
                user = get(self.client.guilds[0].members, id=self.current_koh["id"])
            except:
                self.current_koh = {}
                return

            bals = ezfile.loadjson("money_databases/bals.json")

            bals[str(user.id)]["wallet"] += 2

            ezfile.savejson("money_databases/bals.json", bals)

            self.current_koh["time"] += 1

            if self.current_koh["time"] > 60:
                criminal_role = get(self.client.guilds[0].roles, id=822869746391318568)
                try:
                    await user.remove_roles(criminal_role)
                except:
                    pass

                self.current_koh = {}

                await user.send("**I have take your criminal role and now I have become the criminal >:)!**")


    @commands.command()
    @commands.cooldown(1, 1200, commands.BucketType.user)
    async def koh(self, ctx):
        chance = random.choice([True, True, True, False])
        if not chance:
            embed=discord.Embed(title="Your attempt to get the Criminal Role was unsuccessful.", description="You can try again in 20 mins.", color=0xff0000)
            embed.set_thumbnail(url='https://media.discordapp.net/attachments/811227367635681321/817408731691876422/336-3367416_red-x-emoji-png-not-allowed.png?width=427&height=427')
            embed.set_footer(text="Robo Wizzz Currency System.")
            await ctx.send(embed=embed)
            return

        try:
            old_id = self.current_koh["id"]
        except:
            criminal_role = get(ctx.guild.roles, id=822869746391318568)

            self.current_koh = {"id": ctx.author.id, "time": 0}

            await ctx.author.add_roles(criminal_role)
            embed=discord.Embed(title="You have successfully attained the Criminal Role!", description="For every 1 min that you have this role, you will get 2 Ro bucks.", color=0x00ff44)
            embed.set_thumbnail(url='https://media.discordapp.net/attachments/811227367635681321/817660568898633748/1474130d39ecf1ef59da571b459696a8_5.png')
            embed.set_footer(text="Robo Wizzz Currency System.")
            await ctx.send(embed=embed)
            return

        old_user = get(ctx.guild.members, id=old_id)

        await old_user.send(f"Your KOH Criminal Role has been taken away by {ctx.author.mention}!")

        criminal_role = get(ctx.guild.roles, id=822869746391318568)

        self.current_koh = {"id": ctx.author.id, "time": 0}

        try:
            await old_user.remove_roles(criminal_role)
        except:
            pass

        await ctx.author.add_roles(criminal_role)
        embed=discord.Embed(title="You have successfully attained the Criminal Role!", description="For every 1 min that you have this role, you will get 2 Ro bucks.", color=0x00ff44)
        embed.set_thumbnail(url='https://media.discordapp.net/attachments/811227367635681321/817660568898633748/1474130d39ecf1ef59da571b459696a8_5.png')
        embed.set_footer(text="Robo Wizzz Currency System.")
        await ctx.send(embed=embed)

    @koh.error
    async def koh_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            errorr = round(float(str(error).replace("You are on cooldown. Try again in ", "").replace("s", "")))
            hrs = round(errorr)
            embed=discord.Embed(title="Hey! This command is on a cooldown.", description=f"You can use this command only once in 1 hour. You don't wanna work to much!\nTry again in {hrs}s", color=0x44ff00)
            embed.set_thumbnail(url='https://images-ext-2.discordapp.net/external/N8LpKSOO52iNCGjQQ6yJOqlW89RJkzSbDSNjOOa_mVg/%3Fwidth%3D427%26height%3D427/https/media.discordapp.net/attachments/798968646336249928/816351655812792410/kKMxMuzufRPMRxioYgWq_XylZQ1cP0nJ89Za3Bo0VxNGypkybermjXlzOhjW-gCEuT675G4cz_CBDo5Db7Qow5sUuR70FUlXVwag.png?width=300&height=300')
            embed.set_footer(text="Robo Wizzz Currency System.")
            await ctx.send(embed=embed)







def setup(client):
    client.add_cog(App(client))
