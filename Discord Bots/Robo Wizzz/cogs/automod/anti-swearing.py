import discord, time, asyncio, os, random, json, unidecode
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, cooldown, MissingPermissions, check
from discord.utils import get
from termcolor import colored

class App(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.first = True
        self.banned_words = ["fuck", "bitch", "cunt", "shit", "nigga", "nigger", "nogga", "dick", "bastard", "vagina"]
        print("Automod Swearing                    "+colored('Running', 'green'))

        self.mute_loop.start()

    @tasks.loop(seconds=5)
    async def mute_loop(self):
        if self.first:
            await asyncio.sleep(10)
            self.first = False
        with open("database/mutes.json") as f:
            database = json.load(f)
            f.close()

        todel = []

        for user in database:
            database[user] -= 5

            if database[user] < 0:
                todel.append(user)
                userobj = get(self.client.guilds[0].members, id=int(user))
                role = get(self.client.guilds[0].roles, id=804925673412100116)
                try:
                    await userobj.remove_roles(role)
                except:
                    pass

        for user in todel:
            del database[user]


        with open("database/mutes.json", "w+") as f:
            json.dump(database, f)
            f.close()

    async def mute(self, user, time):
        role = get(user.guild.roles, id=804925673412100116)
        await user.add_roles(role)
        with open("database/mutes.json") as f:
            database = json.load(f)
            f.close()

        try:
            test = database[user.id]
            return
        except:
            database[user.id] = time

        with open("database/mutes.json", "w+") as f:
            json.dump(database, f)
            f.close()

    async def reply(self, msg, channel):
        m = await channel.send(msg)
        await asyncio.sleep(10)
        await m.delete()

    async def punish(self, user, ctx, edit):
        with open("database/warn.json") as f:
            database = json.load(f)
            f.close()

        try:
            test = database[str(user.id)]
            database[str(user.id)] += 1
        except:
            database[str(user.id)] = 1

        if database[str(user.id)] < 3:
            if not edit:
                embed=discord.Embed(title="This is a warning. If you get 3 warnings, you will be muted for 8 hours. Swearing is strictly not allowed here.", color=0xff8800)
                embed.set_author(name="Hey! Please do not swear in this server.")
                embed.set_thumbnail(url='https://media.discordapp.net/attachments/798968646336249928/816351655812792410/kKMxMuzufRPMRxioYgWq_XylZQ1cP0nJ89Za3Bo0VxNGypkybermjXlzOhjW-gCEuT675G4cz_CBDo5Db7Qow5sUuR70FUlXVwag.png?width=427&height=427')
                embed.set_footer(text="Anti-Swear Automoderation.")
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(title="This is a warning. If you get 3 warnings, you will be muted for 8 hours. Swearing is strictly not allowed here. (yea we check edits aswell)", color=0xff8800)
                embed.set_author(name="Hey! Please do not swear in this server.")
                embed.set_thumbnail(url='https://media.discordapp.net/attachments/798968646336249928/816351655812792410/kKMxMuzufRPMRxioYgWq_XylZQ1cP0nJ89Za3Bo0VxNGypkybermjXlzOhjW-gCEuT675G4cz_CBDo5Db7Qow5sUuR70FUlXVwag.png?width=427&height=427')
                embed.set_footer(text="Anti-Swear Automoderation.")
                await ctx.send(embed=embed)

        if database[str(user.id)] == 3:
            embed=discord.Embed(title="You have been muted for excessive swearing.", color=0xff6600)
            embed.set_author(name="Hey @someone! You have been muted for 8 hours.")
            embed.set_thumbnail(url='https://media.discordapp.net/attachments/798968646336249928/816353131285446676/mute.png')
            embed.set_footer(text="Anti-Swear Automoderation.")
            await ctx.send(embed=embed)
            await self.mute(user, 28800)
            database[str(user.id)] = 0

        with open("database/warn.json", "w+") as f:
            json.dump(database, f)
            f.close()

    async def get_raw_message(self, text, ctx, edit):
        raw_text = unidecode.unidecode(text)
        raw_text = raw_text.strip().replace(" ", "")
        raw_text = raw_text.lower()
        version_1 = raw_text.replace("$", "s")
        version_2 = raw_text.replace("l", "i")
        version_3 = raw_text.replace("!", "i")
        version_4 = raw_text.replace("0", "o")
        message_is_to_be_punished = False
        for word in self.banned_words:
            if word in version_1 or word in version_2 or word in version_3 or word in version_4:
                message_is_to_be_punished = True

        if message_is_to_be_punished:
            await ctx.delete()
            await self.punish(ctx.author, ctx, edit)


    @commands.Cog.listener()
    async def on_message(self, message):
        await self.get_raw_message(message.content, message, edit=False)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        await self.get_raw_message(after.content, after, edit=True)

def setup(client):
    client.add_cog(App(client))
