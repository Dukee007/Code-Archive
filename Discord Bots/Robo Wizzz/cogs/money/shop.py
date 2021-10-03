import discord, time, asyncio, os, random, json, ezfile
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, cooldown, MissingPermissions, check
from discord.utils import get
from termcolor import colored
from threading import Thread

class App(commands.Cog):
    def __init__(self, client):
        self.client = client
        print("Money - Shop               "+colored('Running', 'green'))

    

def setup(client):
    client.add_cog(App(client))
