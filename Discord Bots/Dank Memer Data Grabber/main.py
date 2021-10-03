import discord, os, json, string, asyncio, random, requests
from discord.ext import commands, tasks
from discord.ext.commands import has_role, has_permissions, check
from termcolor import colored
from itertools import cycle

TOKEN = "NzMxMDczNTc2MjQwOTM5MDc4.YGyG4g.5z4_104-lIyvBsi7F0rs0ne7bwg"

i = discord.Intents.all()

client = commands.Bot(command_prefix="ddb!", intents=i, self_bot=True)
client.remove_command("help")

BOT_AUTH_KEY = "*&T&tn6tn897m9ymhuhhihimnNY^BB^MM7789m89u008977809789765656IM<UHTY(*&^%^*)"
server = "http://localhost:5000"

#############################__events__#############################

@client.event
async def on_ready():
    global status

    print("ID: "+colored(f"{str(client.user.id)}", "green")+" NAME: "+colored(f"{client.user.name}", "green"))

    scan_server.start()

#############################__functions__#############################

def is_authed(ctx):
    return ctx.author.id in [508372340904558603]

#############################__messages__#############################

@client.event
async def on_message(message):
    pass

#############################_tasks__#############################

@tasks.loop(seconds=2)
async def scan_server():
    global server, BOT_AUTH_KEY
    responce = requests.get(f"{server}/request-dank-requests", headers={"password": BOT_AUTH_KEY, "requests-mode": "dank"})
    data = json.loads(responce.text)
    print(data)
    listofrequests = data["json"]
    datatoreturn = {}
    for request in listofrequests:
        datatoreturn[str(request)] = await get_bal(str(request))

    if len(datatoreturn) != 0:
        requests.post(f"{server}/return-dank-requests", headers={"password": BOT_AUTH_KEY, "update-mode": "dank"}, json=dict(datatoreturn))

#############################__commands__#############################

async def get_bal(user):
    ctx = client.get_channel(829004959482642452)

    def check_for_dank(m):
        return m.author.id == 270904126974590976 and m.channel.id == ctx.id

    message_sent = await ctx.send(f"pls bal {user}")
    message_got = await client.wait_for('message', check=check_for_dank, timeout=10)

    embeds = message_got.embeds

    money_dict = embeds[0].to_dict()["description"].split("⏣")

    wallet = int(''.join(filter(str.isdigit, money_dict[1])))
    bank = int(''.join(filter(str.isdigit, money_dict[2])))

    return [wallet, bank]


#############################__run__#############################

client.run(TOKEN, bot=False)
