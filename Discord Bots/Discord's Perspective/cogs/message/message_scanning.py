import discord, time, asyncio, os, random, json, ast
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, cooldown, MissingPermissions, check
from discord.utils import get
from googleapiclient import discovery
from termcolor import colored

class App(commands.Cog):
    def __init__(self, client):
        self.client = client


        self.client = discovery.build(
          "commentanalyzer",
          "v1alpha1",
          developerKey='no',
          discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
          static_discovery=False,
        )

        print("Messages - Message Scan             "+colored('Running', 'green'))


    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            if message.channel.id in [829738174564925440, 807054423929913384, 807054520882036766, 819849093584781312, 816373744334536774, 808781494385901620, 817409600902660137, 826630432296402964, 823542746601226280, 823542714817314848, 823542458880884766, 823542482180636673, 823498940962963456, 808553514459856896, 807084157737107476, 821524228595384330, 821524196470292490, 821524253660545054, 807058277720260628, 807000415160893520, 807496511163990037, 807119740160966656, 807119857484431380, 816349893064654899, 823947236823531571, 816312447836225566, 807119900975300628, 816349867089461318, 816339906023522304, 808787721291563068, 809982270877204560]:
                await self.scanmessage(message)

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
