import discord, time, asyncio, os, random, json, ast
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, cooldown, MissingPermissions, check
from discord.utils import get
from googleapiclient import discovery
from termcolor import colored

class App(commands.Cog):
    def __init__(self, client):
        self.client = client

        print("Commands - Behaviour             "+colored('Running', 'green'))

    @commands.command()
    async def behaviour(self, ctx, user : discord.Member = None):
        if user != None:
            role = get(ctx.guild.roles, id=818566867324239893)
            if role not in ctx.author.roles:
                await ctx.send("You cannot check other peoples behaviour, check your own!")
                return
        else:
            user = ctx.author

        f = open("saved_actions.json")
        saved_actions = json.load(f)
        f.close()

        try:
            saved = saved_actions[str(user.id)]
        except KeyError:
            saved_actions[str(user.id)] = {"TOXICITY": 0, "INSULT": 0, "FLIRTATION": 0, "INCOHERENT": 0, "SPAM": 0}
            saved = saved_actions[str(user.id)]

        f = open("saved_actions.json", "w+")
        json.dump(saved_actions, f)
        f.close()

        embed=discord.Embed(title=f"{user.name}'s behaviour!", description="Each number show how many messages in that subject they have sent!", color=0x00ffff)
        embed.add_field(name="TOXICITY:", value=str(saved["TOXICITY"]), inline=False)
        embed.add_field(name="INSULTS:", value=str(saved["INSULT"]), inline=False)
        embed.add_field(name="FLIRTS:", value=str(saved["FLIRTATION"]), inline=False)
        embed.set_footer(text="Discord's Perspective 1.0")
        await ctx.send(embed=embed)

    async def scanmessage(self, message):
        analyze_request = {
          'comment': { 'text': message.content },
          'requestedAttributes': {"TOXICITY": {}, "INSULT": {}, "FLIRTATION": {}, "INCOHERENT": {}, "SPAM": {}}
        }

        api_response = self.client.comments().analyze(body=analyze_request).execute()

        api_parsed_data = ast.literal_eval(json.dumps(api_response))

        f = open("saved_actions.json")
        saved_actions = json.load(f)
        f.close()

        try:
            saved = saved_actions[str(message.author.id)]
            saved = None
        except KeyError:
            saved_actions[str(message.author.id)] = {"TOXICITY": 0, "INSULT": 0, "FLIRTATION": 0, "INCOHERENT": 0, "SPAM": 0}

        if api_parsed_data["attributeScores"]["TOXICITY"]["summaryScore"]["value"] > 0.6:
            await message.add_reaction("🤬")
            saved_actions[str(message.author.id)]["TOXICITY"] += 1

        if api_parsed_data["attributeScores"]["INSULT"]["summaryScore"]["value"] > 0.6:
            await message.add_reaction("🔫")
            saved_actions[str(message.author.id)]["INSULT"] += 1

        if api_parsed_data["attributeScores"]["FLIRTATION"]["summaryScore"]["value"] > 0.6:
            await message.add_reaction("💋")
            saved_actions[str(message.author.id)]["FLIRTATION"] += 1

        #if api_parsed_data["attributeScores"]["INCOHERENT"]["summaryScore"]["value"] > 0.6:
        #    await message.add_reaction("❌")
        #saved_actions[str(message.author.id)]["INCOHERENT"] += 1

        #if api_parsed_data["attributeScores"]["SPAM"]["summaryScore"]["value"] > 0.6:
        #    await message.add_reaction("💬")
        #saved_actions[str(message.author.id)]["SPAM"] += 1

        f = open("saved_actions.json", "w+")
        json.dump(saved_actions, f)
        f.close()




def setup(client):
    client.add_cog(App(client))
