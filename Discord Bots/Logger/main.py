from datetime import datetime

import discord
import requests
from discord.ext import commands, tasks

TOKEN = "Nzg4ODYyNzUyNzIxNzMxNjU0.X9prsA.sF7_6NRatSxFjsOCylLK5miXxcI"
POST_KEY = "v&%^TUD796tgyRE(%&^FGv68R6p8f97%RTGd6fg8rOF*)*Fo7do7tD*O"

POST_URL = "http://localhost:5000/post"

queue = {}

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix="l!", intents=intents)


@client.event
async def on_ready():
    print("Bot Online!")
    #send_queue_to_server.start()
    #scan_servers.start()


# TASKS

@tasks.loop(seconds=3)
async def send_queue_to_server():
    global queue
    if len(queue) != 0:
        r = requests.post(POST_URL, json=queue, headers={"auth": POST_KEY, "reason": "data_update"})
        print(r.text)
        if str(r.status_code) != "200":
            await log_api_error("Logger Server Bad Request!", "The server send back a error code!", r.status_code, r.text)

        queue = {}

@tasks.loop(seconds=1)
async def scan_servers():
    for guild in client.guilds:
        print(guild.name)

# FUNCTIONS

def add_msg_to_queue(log_type, user, content, guild, channel=None):
    global queue
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    try:
        if queue[guild]["message"] == "":
            pass
    except KeyError:
        queue[guild] = {
            "message": [],
            "member": [],
            "server": [],
        }
    queue[guild][log_type].insert(0, {"user": user, "content": content, "time": dt_string, "channel": str(channel)})


async def log_api_error(reason, content, code, error):
    channel = client.get_channel(789433408036012062)
    await channel.send(
        f'<@&751873207325425805> - Reason: {str(reason)} Code: {str(code)} Content: {str(content)} Error: {error}')


# UPDATE EVENTS

@client.event
async def on_guild_join(guild):
    r = requests.post(POST_URL,
                      headers={"auth": POST_KEY, "reason": "add_guild", "id": str(guild.id), "name": guild.name,
                               "avatar": str(guild.icon_url),},
                      json=guild.channels)
    if str(r.status_code) == "409":
        pass
    elif str(r.status_code) != "200":
        await log_api_error("Logger Server Bad Request!", "The server send back a error code!", r.status_code, r.text)


# LOGGING EVENTS

@client.event
async def on_message(message):
    add_msg_to_queue("message", {"name": message.author.display_name, "avatar": str(message.author.avatar_url)},
                 message.content, str(message.guild.id), message.channel.id)

    if message.author.bot is not True:
        await client.process_commands(message)


@client.event
async def on_member_join(member):
    add_to_queue("member", {"name": member.author.display_name, "avatar": str(member.author.avatar_url)},
                 "Has joined the server!", str(member.guild.id))


@client.event
async def on_member_remove(member):
    add_to_queue("member", {"name": member.author.display_name, "avatar": str(member.author.avatar_url)},
                 "Has left the server!", str(member.guild.id))


client.run(TOKEN)
