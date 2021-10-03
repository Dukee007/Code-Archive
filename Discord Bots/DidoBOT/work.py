from discord.ext import commands
import discord
client = commands.Bot(command_prefix=".")
client.remove_command("help")


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Streaming(name="LUNA is working on me!", url="https://www.twitch.tv/lazarbeamtwitch"))
    print("client online")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Sorry but DidoBOT is currently under going work we should be back online soon!")
client.run("ODUzNzAyNjg0OTUwOTIxMjM2.YMZOlQ.-sHy52r4DwOAS7vD2anPUPwxxMU")
