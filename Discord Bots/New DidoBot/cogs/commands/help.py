import asyncio
import discord
import pymongo
import urllib
import json
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions
from termcolor import colored


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

        print("Commands - Help          " + colored('Running', 'green'))




def setup(client):
    client.add_cog(Help(client))
