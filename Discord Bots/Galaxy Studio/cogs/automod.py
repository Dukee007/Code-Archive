import discord, time, asyncio, os, random, json
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, cooldown, MissingPermissions, check, Cog
from discord.utils import get

class App(commands.Cog):
    def __init__(self, client):
        self.client = client
        print("Automod Cog Running")

        f = open("setup/banned_words.json")
        self.banned_words = json.load(f)
        f.close()

        self.mute_timer.start()

    @tasks.loop(seconds=1)
    async def warn_timer(self):
        f = open("data/warns.json")
        warns = json.load(f)
        f.close()

        for user in warns:
            for that_warn in user:
                warns[user]


    @tasks.loop(seconds=1)
    async def mute_timer(self):
        f = open("data/muted.json")
        mutes = json.load(f)
        f.close()

        tounmute = []

        for user in mutes:
            user["countdown"] = user["countdown"] - 1
            if user["countdown"] < 0:
                tounmute.append(user)

        for user in tounmute:
            mutes.remove(user)
            member = get(self.client.guilds[0].members, id=int(user["user"]))
            muted = get(self.client.guilds[0].roles, id=801164212259782661)
            await member.remove_roles(muted)

        f = open("data/muted.json", "w+")
        json.dump(mutes, f)
        f.close()



    async def mute(self, user, time):
        f = open("data/muted.json")
        mutes = json.load(f)
        f.close()

        if user not in mutes:
            muted = get(user.guild.roles, id=801164212259782661)
            await user.add_roles(muted)
            mutes.append({"user": str(user.id), "countdown": time})

        f = open("data/muted.json", "w+")
        json.dump(mutes, f)
        f.close()

    async def offence(self, user):
        f = open("data/warns.json")
        warns = json.load(f)
        f.close()

        try:
            warnings = warns[str(user.id)]
        except:
            warns[str(user.id)] = {"ammount": 1, "timer": 86400}

        ammount_of_warnings = warns[str(user.id)]["ammount"]

        print(ammount_of_warnings)

        if ammount_of_warnings == 1:
            await user.send(f"Hey {user.mention}, Please can you try to refrain from using that type of language in Galaxy Studio.\nThis is a warning next time you will be muted!\nWarnings expire after 30days.")

        elif ammount_of_warnings == 2:
            await user.send(f"Hey {user.mention}, Please can you try to refrain from using that type of language in Galaxy Studio.\nYou have been muted!\nThis mute will expire after 6 hours.")
            await self.mute(user, 21600)

        f = open("data/warns.json", "w+")
        json.dump(warns, f)
        f.close()

    @Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        ammount_of_banned_words = 0

        for banned_word in self.banned_words:
            if banned_word in message.content.lower():
                ammount_of_banned_words += 1

        if ammount_of_banned_words > 0:
            await message.delete()
            await self.offence(message.author)



def setup(client):
    client.add_cog(App(client))
