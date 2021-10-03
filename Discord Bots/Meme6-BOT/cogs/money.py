import discord, time, os, praw, random, json
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, MissingPermissions
from discord.utils import get
from itertools import cycle
import datetime as dt
from datetime import datetime

done3 = []

beg_lim_users = []
timers = {}
done = []

steal_lim_users = []
timers2 = {}
done2 = []

embeddata = {}
embeddata["icon"] = "http://luna-development.orgfree.com/data/discord/meme6/logo.jpg"
embeddata["name"] = "Meme6"
embeddata["version"] = "2.0"

class App(commands.Cog):
    def __init__(self, client):
        self.client = client
        print("Loading Cog: MONEY")

    @commands.command(aliases=["resetmoney", "moneyreset"])
    @has_permissions(administrator=True)
    async def moneysetup(self, ctx):
        os.chdir("money/")
        folder = str(str(ctx.guild.id)+"/")
        try:
            os.chdir(folder)
        except:
            os.mkdir(folder)
            os.chdir(folder)
        usr_num = 0
        bot_num = 0
        for user in ctx.guild.members:
            if user.bot == True:
                bot_num += 1
            elif user.id in done3:
                pass
            else:
                done3.append(user.id)
                f = open(f"__{user.id}__.json", "w+")
                f.write("500")
                f.close()
                usr_num += 1
        embed=discord.Embed(title="SETUP", description="Running Setup", color=0x00eeff)
        embed.set_author(name=embeddata["name"], icon_url=embeddata["icon"])
        embed.add_field(name="Guild id:", value=str(ctx.guild.id), inline=False)
        embed.add_field(name="Users", value=str(usr_num), inline=False)
        embed.add_field(name="Bots", value=str(bot_num), inline=True)
        embed.set_footer(text=embeddata["name"]+" ["+embeddata["version"]+"]")
        await ctx.send(embed=embed)
        os.chdir("..")
        os.chdir("..")

    @commands.command(aliases=["bal", "bank"])
    async def balance(self, ctx, who=None):
        os.chdir("money/")
        folder = str(str(ctx.guild.id)+"/")
        try:
            os.chdir(folder)
        except:
            os.mkdir(folder)
            os.chdir(folder)
        if who == None:
            who = int(ctx.message.author.id)
        else:
            who = who.replace("@", "").replace("!", "").replace(">", "").replace("<", "")
            who = int(who)
        f = open(f"__{who}__.json", "r")
        bal = f.read()
        f.close()
        embed=discord.Embed(title="Balance", color=0x00eeff)
        embed.set_author(name=embeddata["name"], icon_url=embeddata["icon"])
        embed.add_field(name="Total", value="£"+str(bal), inline=False)
        embed.set_footer(text=embeddata["name"]+" ["+embeddata["version"]+"]")
        await ctx.send(embed=embed)
        os.chdir("..")
        os.chdir("..")

    @tasks.loop(seconds = 1)
    async def begtimer():
        for user_id in beg_lim_users:
            if user_id in done:
                pass
                old = timers[user_id]
                new = old - 1
                timers[user_id] = new
                if timers[user_id] == 0:
                    beg_lim_users.remove(user_id)
                    timers.pop(user_id)
                    done.remove(user_id)
            else:
                done.append(user_id)
                timers[user_id] = 50

    @tasks.loop(seconds = 1)
    async def stealtimer():
        for user_id in steal_lim_users:
            if user_id in done2:
                pass
                old = timers2[user_id]
                new = old - 1
                timers2[user_id] = new
                if timers2[user_id] == 0:
                    steal_lim_users.remove(user_id)
                    timers2.pop(user_id)
                    done2.remove(user_id)
            else:
                done2.append(user_id)
                timers2[user_id] = 50

    @commands.command()
    async def beg(self, ctx):
        os.chdir("money/")
        folder = str(str(ctx.guild.id)+"/")
        try:
            os.chdir(folder)
        except:
            os.mkdir(folder)
            os.chdir(folder)
        if ctx.message.author.id in beg_lim_users:
            left = timers[ctx.message.author.id]
            await ctx.send(f"You need to wait {left} seconds before you can use this again!")
            os.chdir("..")
            os.chdir("..")
            return
        else:
            beg_lim_users.append(ctx.message.author.id)
            x = random.randint(0, 100)
            if x > 25:
                c = True
            else:
                c = False
                await ctx.send("No Coins for you!")
            if c == True:
                amm = random.randint(50, 300)
                if amm > 295:
                    amm = random.randint(400, 500)
                await ctx.send(f"Here have {amm} coins!")
                f = open(f"__{ctx.message.author.id}__.json")
                c_b = f.read()
                f.close()
                c_b =int(c_b)+int(amm)
                f = open(f"__{ctx.message.author.id}__.json", "w+")
                f.write(str(c_b))
                f.close()
        os.chdir("..")
        os.chdir("..")

    @commands.command()
    async def passive(self, ctx, choice):
        if choice == "on":
            with open("passive.json") as f:
                passive_list = json.load(f)

            passive_list[ctx.message.author.id] = True

            with open("passive.json", "w+") as f:
                json.dump(passive_list, f)
            await ctx.send(f"Passive mode now {choice}")
        elif choice == "off":
            with open("passive.json") as f:
                passive_list = json.load(f)

            passive_list[ctx.message.author.id] = False

            with open("passive.json", "w+") as f:
                json.dump(passive_list, f)
            await ctx.send(f"Passive mode now {choice}")
        else:
            await ctx.send(f"{choice} is not a valid option, please choose from on or off")

    @commands.command()
    async def steal(self, ctx, who=None):
        with open("passive.json") as f:
            passive_list = json.load(f)
        p = passive_list[str(ctx.message.author.id)]

        if p == True:
            await ctx.send("You can't steal, your in passive mode you can change that using the passive command")
            return
        if ctx.message.author.id in steal_lim_users:
            left = timers2[ctx.message.author.id]
            await ctx.send(f"You need to wait {left} seconds before you can use this again!")
            os.chdir("..")
            os.chdir("..")
            return
        else:
            steal_lim_users.append(ctx.message.author.id)
            os.chdir("money/")
            folder = str(str(ctx.guild.id)+"/")
            try:
                os.chdir(folder)
            except:
                os.mkdir(folder)
                os.chdir(folder)
            w = who
            if who == None:
                await ctx.send("You need to tell me who to steal from!")
            else:
                who = who.replace("@", "").replace("!", "").replace(">", "").replace("<", "")
                who = int(who)
                f = open(f"__{who}__.json")
                ee = f.read()
                if int(ee) < 400:
                    await ctx.send("This person does not have more than 400 in there bank its not worth it!")
                    f.close()
                    return
                f.close()
                chance = random.randint(0, 100)
                if chance > 30:
                    x = True
                else:
                    await ctx.send("Oh no, you have been caught!")
                    x = False
            if x == True:
                amm = random.randint(1, 400)
                await ctx.send(f"You stole {amm} from {w}")
                f = open(f"__{ctx.message.author.id}__.json")
                c = f.read()
                f.close()
                c = int(c)+amm
                f = open(f"__{ctx.message.author.id}__.json", "w+")
                f.write(str(c))
                f.close()
                f = open(f"__{who}__.json")
                c = f.read()
                f.close()
                c = int(c)-amm
                f = open(f"__{who}__.json", "w+")
                f.write(str(c))
                f.close()
            os.chdir("..")
            os.chdir("..")
    begtimer.start()
    stealtimer.start()
def setup(client):
    client.add_cog(App(client))
