import discord, time, asyncio, os, random, json, ezfile
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, cooldown, MissingPermissions, check
from discord.utils import get
from termcolor import colored

class App(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.rob_immune = [508372340904558603, 797783028252016651]
        print("Money - Commands               "+colored('Running', 'green'))

    @commands.command()
    async def bal(self, ctx):
        user = ctx.author
        bals = ezfile.loadjson("money_databases/bals.json")
        bank_space = ezfile.loadjson("money_databases/bank_space.json")

        try:
            bal = bals[str(user.id)]
        except KeyError:
            bals[str(user.id)] = {"bank": 30, "wallet": 20}

        try:
            bank = bank_space[str(user.id)]
        except:
            bank_space[str(user.id)] = 300

        ezfile.savejson("money_databases/bals.json", bals)
        ezfile.savejson("money_databases/bank_space.json", bank_space)

        embed=discord.Embed(title="This is your current Ro-bucks balance:", color=0x00ff44)
        embed.set_thumbnail(url='https://media.discordapp.net/attachments/811227367635681321/817408107293835274/emoji-money-png-3.png?width=427&height=427')
        embed.add_field(name="Bank:", value=str(bals[str(user.id)]["bank"])+"/"+str(bank_space[str(user.id)]), inline=True)
        embed.add_field(name="Wallet:", value=str(bals[str(user.id)]["wallet"]), inline=True)
        embed.set_footer(text="Use the Currency command to get help on the currency system.")
        embed.set_footer(text="Robo Wizzz Currency System.")
        await ctx.send(embed=embed)

    @commands.command(aliases = ['with'])
    async def withdraw(self, ctx, amount : int = None):
        if amount == None:
            await ctx.send("You need to tell me how much you want to withdraw! Don't try to break me.")
            return

        bals = ezfile.loadjson("money_databases/bals.json")
        bank_space = ezfile.loadjson("money_databases/bank_space.json")

        user = ctx.author

        try:
            bal = bals[str(user.id)]
        except KeyError:
            bals[str(user.id)] = {"bank": 30, "wallet": 20}

        try:
            bank = bank_space[str(user.id)]
        except:
            bank_space[str(user.id)] = 300

        if bals[str(ctx.author.id)]["bank"] < amount:
            await ctx.send("You cannot afford to do that!")
            return

        bals[str(ctx.author.id)]["bank"] -= amount
        bals[str(ctx.author.id)]["wallet"] += amount

        ezfile.savejson("money_databases/bals.json", bals)
        ezfile.savejson("money_databases/bank_space.json", bank_space)

        await ctx.send(f"You have withdrawn `{str(amount)}`")

    @commands.command(aliases = ['dep'])
    async def deposit(self, ctx, amount : int = None):
        if amount == None:
            await ctx.send("You need to tell me how much you want to deposit! Don't try to break me.")
            return

        bals = ezfile.loadjson("money_databases/bals.json")
        bank_space = ezfile.loadjson("money_databases/bank_space.json")

        user = ctx.author

        try:
            bal = bals[str(user.id)]
        except KeyError:
            bals[str(user.id)] = {"bank": 30, "wallet": 20}

        try:
            bank = bank_space[str(user.id)]
        except:
            bank_space[str(user.id)] = 300

        if bals[str(ctx.author.id)]["wallet"] < amount:
            await ctx.send("You cannot afford to do that!")
            return

        if bals[str(ctx.author.id)]["bank"] == bank_space[str(ctx.author.id)]:
            await ctx.send("Your bank is full!")
            return

        if bank_space[str(ctx.author.id)] < amount+bals[str(ctx.author.id)]["bank"]:
            await ctx.send("You dont have enough space for that!")
            return

        bals[str(ctx.author.id)]["bank"] += amount
        bals[str(ctx.author.id)]["wallet"] -= amount

        ezfile.savejson("money_databases/bals.json", bals)
        ezfile.savejson("money_databases/bank_space.json", bank_space)

        await ctx.send(f"You have deposited `{str(amount)}`")

    @commands.command()
    @commands.cooldown(1, 14400, commands.BucketType.user)
    async def work(self, ctx):
        bals = ezfile.loadjson("money_databases/bals.json")
        bank_space = ezfile.loadjson("money_databases/bank_space.json")

        user = ctx.author

        try:
            bal = bals[str(user.id)]
        except KeyError:
            bals[str(user.id)] = {"bank": 30, "wallet": 20}

        try:
            bank = bank_space[str(user.id)]
        except:
            bank_space[str(user.id)] = 300

        if bals[str(ctx.author.id)]["wallet"] < 15:
            await ctx.send("You need 15 coins in your wallet to be able to work!")
            return

        choice = random.randint(0, 100)

        good_events = ["You welcomed a new member and the owner gave you some Ro-bucks.",
                       "You helped a person who just started using Discord.",
                       "You fixed a few bugs when i was updated.",
                       "Raider joined the server? Thanks for letting me know.",
                       "Im your favorite bot? OMG! Thank you so much.",
                       "You reported a underage user to discord!",
                       "Omg you just helped <@735013221936922644> read through the applications! Here, take your reward"]

        bad_events = ["Dang you spammer >:( Im taking away some Ro-bucks.",
                      "Stop exploiting in Roblox! This is your punishment.",
                      "You raided a server? Bad person. Im taking away some Ro-bucks.",
                      "You said <@508372340904558603> can't code, well he coded this and now you lose coins :)"]

        if choice < 60:
            event = random.choice(good_events)
            good = True
        else:
            event = random.choice(bad_events)
            good = False

        if good:
            mongot = random.randint(20, 30)
            bals[str(ctx.author.id)]["wallet"] += mongot
            embed=discord.Embed(title=f"You have earned {str(mongot)} Ro-bucks!", description=event, color=0x44ff00)
            embed.set_thumbnail(url='https://media.discordapp.net/attachments/811227367635681321/817408107293835274/emoji-money-png-3.png?width=427&height=427')
            embed.set_footer(text="Robo Wizzz Currency System.")
            await ctx.send(embed=embed)
        else:
            mongot = random.randint(10, 15)
            bals[str(ctx.author.id)]["wallet"] -= mongot
            embed=discord.Embed(title=f"You have lost {str(mongot)} Ro-bucks!", description=event, color=0xff0000)
            embed.set_thumbnail(url='https://media.discordapp.net/attachments/811227367635681321/817408731691876422/336-3367416_red-x-emoji-png-not-allowed.png?width=427&height=427')
            embed.set_footer(text="Robo Wizzz Currency System.")
            await ctx.send(embed=embed)

        ezfile.savejson("money_databases/bals.json", bals)
        ezfile.savejson("money_databases/bank_space.json", bank_space)

    @work.error
    async def work_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            errorr = round(float(str(error).replace("You are on cooldown. Try again in ", "").replace("s", "")))
            hrs = round(errorr/60)
            embed=discord.Embed(title="Hey! This command is on a cooldown.", description=f"You can use this command only once in 4 hours. You don't wanna work to much!\nTry again in {hrs}mins", color=0x44ff00)
            embed.set_thumbnail(url='https://images-ext-2.discordapp.net/external/N8LpKSOO52iNCGjQQ6yJOqlW89RJkzSbDSNjOOa_mVg/%3Fwidth%3D427%26height%3D427/https/media.discordapp.net/attachments/798968646336249928/816351655812792410/kKMxMuzufRPMRxioYgWq_XylZQ1cP0nJ89Za3Bo0VxNGypkybermjXlzOhjW-gCEuT675G4cz_CBDo5Db7Qow5sUuR70FUlXVwag.png?width=300&height=300')
            embed.set_footer(text="Robo Wizzz Currency System.")
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 8200, commands.BucketType.user)
    async def crime(self, ctx):
        bals = ezfile.loadjson("money_databases/bals.json")
        bank_space = ezfile.loadjson("money_databases/bank_space.json")

        user = ctx.author

        try:
            bal = bals[str(user.id)]
        except KeyError:
            bals[str(user.id)] = {"bank": 30, "wallet": 20}

        try:
            bank = bank_space[str(user.id)]
        except:
            bank_space[str(user.id)] = 300

        if bals[str(ctx.author.id)]["wallet"] < 25:
            await ctx.send("You need 25 coins in your wallet to be able to commit crime!")
            return

        choice = random.randint(0, 100)

        good_events = ["You stole someone's items in Roblox Islands. You exchanged them and got some Ro-bucks!",
                       "You stole <@508372340904558603>'s pog abilities :( You exchanged his pog abilities for Ro-bucks! Now im pog >:)",
                       "You stole <@735013221936922644>'s artwork. I like it so i payed you some Ro-bucks!"]

        bad_events = ["You just raided someone's server. Legal actions have been taken, lol.",
                      "You almost crashed me >:( You gonna get punished now...",
                      "You just raided someone's server. Legal actions have been taken, lol."]

        if choice < 25:
            event = random.choice(good_events)
            good = True
        else:
            event = random.choice(bad_events)
            good = False

        if good:
            mongot = random.randint(45, 55)
            bals[str(ctx.author.id)]["wallet"] += mongot
            embed=discord.Embed(title=f"You have stole {str(mongot)} Ro-bucks!", description=event, color=0x44ff00)
            embed.set_thumbnail(url='https://media.discordapp.net/attachments/811227367635681321/817408107293835274/emoji-money-png-3.png?width=427&height=427')
            embed.set_footer(text="Robo Wizzz Currency System.")
            await ctx.send(embed=embed)
        else:
            mongot = random.randint(15, 25)
            bals[str(ctx.author.id)]["wallet"] -= mongot
            embed=discord.Embed(title=f"You have lost {str(mongot)} Ro-bucks!", description=event, color=0xff0000)
            embed.set_thumbnail(url='https://media.discordapp.net/attachments/811227367635681321/817408731691876422/336-3367416_red-x-emoji-png-not-allowed.png?width=427&height=427')
            embed.set_footer(text="Robo Wizzz Currency System.")
            await ctx.send(embed=embed)

        ezfile.savejson("money_databases/bals.json", bals)
        ezfile.savejson("money_databases/bank_space.json", bank_space)

    @crime.error
    async def crime_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            errorr = round(float(str(error).replace("You are on cooldown. Try again in ", "").replace("s", "")))
            hrs = round(errorr/60)
            embed=discord.Embed(title="Hey! This command is on a cooldown.", description=f"You can use this command only once in 2 hours. You don't wanna commit too many crimes!\nTry again in {hrs}mins", color=0x44ff00)
            embed.set_thumbnail(url='https://images-ext-2.discordapp.net/external/N8LpKSOO52iNCGjQQ6yJOqlW89RJkzSbDSNjOOa_mVg/%3Fwidth%3D427%26height%3D427/https/media.discordapp.net/attachments/798968646336249928/816351655812792410/kKMxMuzufRPMRxioYgWq_XylZQ1cP0nJ89Za3Bo0VxNGypkybermjXlzOhjW-gCEuT675G4cz_CBDo5Db7Qow5sUuR70FUlXVwag.png?width=300&height=300')
            embed.set_footer(text="Robo Wizzz Currency System.")
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 150, commands.BucketType.user)
    async def rob(self, ctx, user : discord.Member = None):
        if user == None:
            await ctx.send("You need to tell me who you want to rob!")
            return

        if user.id in self.rob_immune:
            await ctx.send("You can't rob that user!")
            return

        bals = ezfile.loadjson("money_databases/bals.json")
        bank_space = ezfile.loadjson("money_databases/bank_space.json")

        userr = ctx.author

        try:
            bal = bals[str(userr.id)]
        except KeyError:
            bals[str(userr.id)] = {"bank": 30, "wallet": 20}

        try:
            bank = bank_space[str(userr.id)]
        except:
            bank_space[str(userr.id)] = 300

        try:
            bal = bals[str(user.id)]
        except KeyError:
            bals[str(user.id)] = {"bank": 30, "wallet": 20}

        try:
            bank = bank_space[str(user.id)]
        except:
            bank_space[str(user.id)] = 300

        if bals[str(user.id)]["wallet"] < 20:
            await ctx.send("That person doesnt even have 20 coins. Leave them alone!")
            return

        if bals[str(ctx.author.id)]["wallet"] < 10:
            await ctx.send("You need at least 10 coins in your wallet to rob someone!")
            return

        if random.randint(0, 100) < 65:
            amount_stolen = random.randint(10, 20)
            bals[str(user.id)]["wallet"] -= amount_stolen
            bals[str(ctx.author.id)]["wallet"] += amount_stolen

            await ctx.send(f"You stole {str(amount_stolen)} Ro-bucks from {user.mention}")

        else:
            amount_to_take = random.randint(5, 10)
            bals[str(user.id)]["wallet"] += amount_to_take
            bals[str(ctx.author.id)]["wallet"] -= amount_to_take

            await ctx.send(f"{user.mention} caught you stealing from them! You payed them {str(amount_to_take)} Ro-bucks for them to not call the police.")

        ezfile.savejson("money_databases/bals.json", bals)
        ezfile.savejson("money_databases/bank_space.json", bank_space)

    @rob.error
    async def rob_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            errorr = round(float(str(error).replace("You are on cooldown. Try again in ", "").replace("s", "")))
            mins = round(errorr/60)
            embed=discord.Embed(title="Hey! This command is on a cooldown.", description=f"You can use this command only once in 2 mins 30s. You don't wanna steal to much!\nTry again in {mins}mins", color=0x44ff00)
            embed.set_thumbnail(url='https://images-ext-2.discordapp.net/external/N8LpKSOO52iNCGjQQ6yJOqlW89RJkzSbDSNjOOa_mVg/%3Fwidth%3D427%26height%3D427/https/media.discordapp.net/attachments/798968646336249928/816351655812792410/kKMxMuzufRPMRxioYgWq_XylZQ1cP0nJ89Za3Bo0VxNGypkybermjXlzOhjW-gCEuT675G4cz_CBDo5Db7Qow5sUuR70FUlXVwag.png?width=300&height=300')
            embed.set_footer(text="Robo Wizzz Currency System.")
            await ctx.send(embed=embed)






def setup(client):
    client.add_cog(App(client))
