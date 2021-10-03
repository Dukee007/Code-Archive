import discord, time, asyncio, os, random, json, requests
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, cooldown, MissingPermissions, check
from discord.utils import get
from datetime import datetime, date
from discord_webhook import DiscordWebhook, DiscordEmbed
from termcolor import colored

class Website(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.server_update.start()

        self.server_url = "http://localhost:5000/"

        self.bot_auth_key = "*&T&tn6tn897m9ymhuhhihimnNY^BB^MM7789m89u008977809789765656IM<UHTY(*&^%^*)"

        self.first = True

        print("Website - Update                 "+colored('Running', 'green'))

    @tasks.loop(seconds = 10) # minutes = 5
    async def server_update(self):
        if self.first:
            await asyncio.sleep(6)
            self.first = False
        bot_count = 0
        member_count = 0
        all_count = 0
        role_count = 0
        cat_channel_count = 0
        vc_channel_count = 0
        txt_channel_count = 0
        nws_channel_count = 0
        has_invite_splash = False
        has_news_channels = False
        has_animated_icon = False
        has_banner = False
        has_vanity_url = False
        for member in self.client.guilds[0].members:
            if member.bot:
                bot_count += 1
            else:
                member_count += 1
            all_count += 1

        for role in self.client.guilds[0].roles:
            role_count += 1

        for channel in self.client.guilds[0].channels:
            type = str(channel.type)
            if type == "text":
                txt_channel_count += 1
            elif type == "voice":
                vc_channel_count += 1
            elif type == "category":
                cat_channel_count += 1
            elif type == "news":
                nws_channel_count += 1

        if self.client.guilds[0].splash_url != "":
            has_invite_splash = True

        for channel in self.client.guilds[0].channels:
            if str(channel.type) == "news":
                    has_news_channels = True

        if self.client.guilds[0].is_icon_animated:
            has_animated_icon = True

        if self.client.guilds[0].banner_url != "":
            has_banner = True

        try:
            await self.client.guilds[0].vanity_invite()
            has_vanity_url = True
        except Exception as e:
            if "Invite code is either invalid or taken." in str(e):
                pass#
            else:
                raise e

        upload_json = {"member_count": {"all": all_count, "bots": bot_count, "users": member_count}, "role_count": role_count, "channel_count": {"text": txt_channel_count, "voice": vc_channel_count, "category": cat_channel_count, "news" : nws_channel_count}, "server_features": {"has_invite_splash": has_invite_splash, "has_news_channels": has_news_channels, "has_animated_icon": has_animated_icon, "has_banner": has_banner, "has_vanity_url": has_vanity_url}}
        r = requests.post(f"{self.server_url}update-data", headers={"authorization_key": self.bot_auth_key, "update-mode": "server-info"}, json=upload_json)

def setup(client):
    client.add_cog(Website(client))
