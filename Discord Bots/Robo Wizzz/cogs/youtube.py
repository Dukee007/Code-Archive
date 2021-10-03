import discord, time, asyncio, os, random, json, requests
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, cooldown, MissingPermissions, check, has_role
from discord.utils import get
from termcolor import colored

class App(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.api_key = "AIzaSyADpCI6QgLOiG8PH2vRnuRCNq_VGkvAVaA"
        print("Youtube                    "+colored('Running', 'green'))

    def get_video_data(self, url):
        if "?v=" in url:
            ID = url.split("?v=")[1]
        else:
            ID = url.split("/")[1]
        api = f'https://www.googleapis.com/youtube/v3/videos?id={ID}&key={self.api_key}&part=snippet'
        req = requests.get(api, timeout=1)
        data = json.loads(req.text)
        video = data["items"][0]["snippet"]
        api = f'https://www.googleapis.com/youtube/v3/videos?id={ID}&key={self.api_key}&part=statistics'
        req = requests.get(api, timeout=1)
        data = json.loads(req.text)
        vidstats = data["items"][0]["statistics"]
        return {"channel": video["channelId"], "thumbnail": video["thumbnails"][list(video["thumbnails"])[-1]]["url"], "title": video["title"], "likes": vidstats["likeCount"], "views": vidstats["viewCount"], "dislikes": vidstats["dislikeCount"], "comments": vidstats["commentCount"]}

    def get_channel_data(self, ID):
        api_data = f'https://www.googleapis.com/youtube/v3/channels?id={ID}&key={self.api_key}&part=snippet'
        api_stats = f'https://www.googleapis.com/youtube/v3/channels?id={ID}&key={self.api_key}&part=statistics'
        req_data = requests.get(api_data, timeout=1)
        req_stats = requests.get(api_stats, timeout=1)
        data = json.loads(req_data.text)
        stats = json.loads(req_stats.text)
        channel_data = data["items"][0]["snippet"]
        channel_stats = stats["items"][0]["statistics"]
        return {"logo": channel_data["thumbnails"][list(channel_data["thumbnails"])[-1]]["url"], "name": channel_data["title"], "subs": channel_stats["subscriberCount"], "subshidden": channel_stats["hiddenSubscriberCount"], "vids": channel_stats["videoCount"]}

    @commands.command()
    @has_role(804757145849036861)
    @commands.cooldown(1, 5400, commands.BucketType.user)
    async def youtube(self, ctx, mode : str = None):
        if not isinstance(ctx.channel, discord.channel.DMChannel):
            embed=discord.Embed(title="An interactive setup has been started up in your DMs.", color=0xff0000)
            embed.set_author(name="Please check your DMs.")
            embed.set_thumbnail(url='https://media.discordapp.net/attachments/798968646336249928/816350397178445844/youtube-logo-icon-transparent-ssss-in-2019-youtube-logo-youtube-logopng-3507_2480.png?width=604&height=427')
            embed.set_footer(text="Youtube Promotion Interactive Setup.")
            await ctx.send(embed=embed)

        embed=discord.Embed(title="Respond within 1 minute or setup will exit! Send me the link to the video.", color=0xff0000)
        embed.set_author(name="What video would you like to promote?")
        embed.set_footer(text="Youtube Promotion Interactive Setup.")
        msg = await ctx.author.send(embed=embed)

        def check_if_message_is_from_correct_author(m):
            return m.author.id == ctx.author.id and m.channel.id == msg.channel.id

        user_video_url = await self.client.wait_for('message', check=check_if_message_is_from_correct_author, timeout=60)
        if "youtube" in user_video_url.content.lower() or "youtu.be" in user_video_url.content.lower():
            embed=discord.Embed(title="This can take a few seconds.", color=0xff0000)
            embed.set_author(name="Please wait while I scan the video and channel!")
            embed.set_footer(text="Youtube Promotion Interactive Setup.")
            await ctx.author.send(embed=embed)
        else:
            embed=discord.Embed(title="The link which you have provided is not of a valid youtube video. Exiting Setup.", color=0xff0000)
            embed.set_author(name="Hey! Thats not a valid youtube video.")
            embed.set_thumbnail(url='https://www.freeiconspng.com/uploads/exit-icon-23.png')
            embed.set_footer(text="Youtube Promotion Interactive Setup Has Ended.")
            await ctx.author.send(embed=embed)
            return

        video = self.get_video_data(user_video_url.content)

        channel = self.get_channel_data(video["channel"])
        embed=discord.Embed(title="You have 2 minutes. Type skip to Skip!", color=0xff0000)
        embed.set_author(name="Please write a video description which describes your video.")
        embed.set_footer(text="Youtube Promotion Interactive Setup.")
        await ctx.author.send(embed=embed)
        user_video_description = await self.client.wait_for('message', check=check_if_message_is_from_correct_author, timeout=120)
        if user_video_description.content.lower() == "skip":
            embed=discord.Embed(title="Your description will not be in the youtube post.", color=0xff0000)
            embed.set_author(name="Description skipped!")
            embed.set_footer(text="Youtube Promotion Interactive Setup.")
            await ctx.author.send(embed=embed)
            user_video_description.content = None
        else:
            embed=discord.Embed(title="Your description will now be in the youtube post.", color=0xff0000)
            embed.set_author(name="Description added!")
            embed.set_footer(text="Youtube Promotion Interactive Setup.")
            await ctx.author.send(embed=embed)

        try:
            test = video["title"]
        except:
            embed=discord.Embed(title="I cannot find this video! Please make sure it is public, if that doesnt work contact a staff member! Exiting Setup.", color=0xff0000)
            embed.set_author(name="Your video has not been found.")
            embed.set_thumbnail(url='https://images-ext-2.discordapp.net/external/N8LpKSOO52iNCGjQQ6yJOqlW89RJkzSbDSNjOOa_mVg/%3Fwidth%3D427%26height%3D427/https/media.discordapp.net/attachments/798968646336249928/816351655812792410/kKMxMuzufRPMRxioYgWq_XylZQ1cP0nJ89Za3Bo0VxNGypkybermjXlzOhjW-gCEuT675G4cz_CBDo5Db7Qow5sUuR70FUlXVwag.png')
            embed.set_footer(text="Youtube Promotion Interactive Setup Has Ended.")
            await ctx.author.send(embed=embed)

        embed=discord.Embed(title="Your video post can be found on the Youtube Promotions channel in the server!", color=0xff0000)
        embed.set_author(name="Your video has successfully been posted!")
        embed.set_thumbnail(url='https://media.discordapp.net/attachments/798968646336249928/816346538204201032/checkmark-flat.png')
        embed.set_footer(text="Youtube Promotion Interactive Setup Has Ended.")
        await ctx.author.send(embed=embed)

        embed = discord.Embed(title=video["title"], colour=discord.Colour(0xff0000), url=user_video_url.content, description=user_video_url.content)

        if user_video_description.content != None:
            embed = discord.Embed(title=video["title"], colour=discord.Colour(0xff0000), url=user_video_url.content, description=f"{user_video_url.content}\n\n{user_video_description.content}")

        embed.set_image(url=video["thumbnail"])
        embed.set_thumbnail(url=channel["logo"])
        embed.set_author(name=channel["name"], url=f"https://www.youtube.com/channel/{video['channel']}")
        embed.set_footer(text=f"👍 {video['likes']} | 👎 {video['dislikes']} | 💬 {video['comments']} | 👁️ {video['views']}")

        yt_channel = get(ctx.guild.channels, id=804751386444169286)
        await yt_channel.send(embed=embed)

    @youtube.error
    async def youtube_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("You need the Youtuber role to do this command. To apply for it please type ?apply")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send("You need to wait 90 mins between posting videos!")
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send("This command cannot be used in dms!")
        else:
            raise error

    @commands.command()
    async def apply(self, ctx):
        if not isinstance(ctx.channel, discord.channel.DMChannel):
            await ctx.send("Please check your dms!")

        user = ctx.author

        msg = await user.send("**Please send me a link to your channel!**\nRespond within 1 minute or setup will exit!")

        def check_if_message_is_from_correct_author(m):
            return m.author.id == ctx.author.id and m.channel == msg.channel

        user_channel_url = await self.client.wait_for('message', check=check_if_message_is_from_correct_author, timeout=60)


        try:
            await user.send("Please wait while I scan your channel.")
            channel = self.get_channel_data(user_channel_url.content.split("/channel/")[1])
        except:
            await user.send("That channel could not be found. Please make sure it is the right url!")

        if not channel["subshidden"]:
            if int(channel["subs"]) < 11:
                await user.send("Sorry but you need more than 10 subs to apply!")
                return
        else:
            await user.send("Sorry but you need to have your sub count unhidden to be able to apply!")
            return
        if int(channel["vids"]) < 1:
            await user.send("Sorry you need to have at least 1 video to be able to apply!")
            return

        await user.send("Thanks for your application!")
        print(channel)

        youtube_discord_channel = self.client.get_channel(823230106394296381)

        embed = discord.Embed(title=f"{ctx.author.name} Wants this channel to be verifed as theres!", colour=discord.Colour(0xe8e924), description="Info:")

        embed.set_thumbnail(url=channel["logo"])

        embed.add_field(name="SUBS:", value=channel["subs"], inline=False)
        embed.add_field(name="NAME:", value=channel["name"], inline=False)
        embed.add_field(name="LINK:", value=f"[Click]({user_channel_url.content})", inline=False)
        embed.add_field(name="USER:", value=ctx.author.mention, inline=False)

        await youtube_discord_channel.send(embed=embed)








def setup(client):
    client.add_cog(App(client)) #YES
