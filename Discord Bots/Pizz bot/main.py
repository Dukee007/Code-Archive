import discord, json
from discord.ext import commands, has_permissions

TOKEN = "Nzk5OTUzNDAwODcwODYyODYy.YALEqQ.fJznq_NQ3Q1Fa0FLcdvNyo7_WZk"

client = commands.Bot(command_prefix="!")

data = {}

@client.event
async def on_ready():
    print("online")
    startup()

#                        <-- events -->

@client.event
async def on_message(message):
    if not message.author.bot:
        await gainxp(message)
        await client.process_commands(message)

#                        <-- commands -->

@client.command()
async def bal(ctx, user : discord.Member = None):
    with open("money.json") as f:
        money = json.load(f)
        f.close()

    if user == None:
        user = ctx.author

    embed=discord.Embed(title="Boogie Bal", color=0x00ffff)
    embed.add_field(name="Boogie Bucks:", value=f"${str(money[str(user.id)])}", inline=False)
    await ctx.send(embed=embed)

@client.command()
@has_permissions(administrator=True)
async def give(ctx, user : discord.User = None):
    if user == None:
        await ctx.send("Who you")

#                        <-- functions -->

async def gainxp(msg):
    xp = 1
    xp = xp * ammount_of_words_in(msg.content)

    with open("money.json") as f:
        money = json.load(f)
        f.close()

    try:
        bal = money[str(msg.author.id)]
    except:
        bal = 0

    bal += xp

    money[str(msg.author.id)] = bal

    with open("money.json", "w+") as f:
        json.dump(money, f)
        f.close()

def startup():
    global data
    with open("words.txt") as f:
        allwords = f.readlines()
        f.close()
    data["words"] = []
    for word in allwords:
        data["words"].append(str(word.replace("\n", "")))
    allwords = None

def ammount_of_words_in(text):
    global data
    text = text.strip()
    ammount = 0
    for word in data["words"]:
        if word in text:
            ammount += 1
    return ammount

client.run(TOKEN)
