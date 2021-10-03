import discord, time, asyncio, os, random, json, requests
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, cooldown, MissingPermissions, check, Cog
from discord.utils import get
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageFont

class App(commands.Cog):
    def __init__(self, client):
        self.client = client

        with open("setup/banned_words.json") as f:
            self.banned_words = json.load(f)
            f.close()

        print("Welcome Cog Running")

    async def generate_image(self, user):
        url = user.avatar_url
        name = str(user)
        W, H = (1100,700)
        #               <-- download image -->

        img_data = requests.get(f"{url}?size=256", stream=True).content
        with open(f'images/cache/{name}.png', 'wb') as handler:
            handler.write(img_data)

        #               <-- make image circle -->

        size = (256, 256)
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)
        im = Image.open(f"images/cache/{name}.png")
        output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)
        output.save(f"images/cache/{name}.png")

        #               <-- make transparency black -->

        im = Image.open(f"images/cache/{name}.png")
        im = im.convert("RGBA")
        if im.mode in ('RGBA', 'LA'):
            background = Image.new(im.mode[:-1], im.size, (0,0,0))
            background.paste(im, im.split()[-1])
            im = background
        im.convert("RGB").save(f"images/cache/{name}.png")

        #               <-- paste image on card -->

        card = Image.open("images/card.png")
        logo = Image.open(f"images/cache/{name}.png")

        card.paste(logo, (420, 50))
        draw = ImageDraw.Draw(card)
        font = ImageFont.truetype("data/font.otf", 30)
        w, h = font.getsize(f"{name} Just joined the server!")
        draw.text(((W-w)/2,(H-h)/2), f"{name} Just joined the server!", (255,255,255), font=font)
        card.save('images/cache/card.png', quality=95)
        os.remove(f"images/cache/{name}.png")

        channel = self.client.get_channel(807665421137215539)
        await channel.send(f"Hey {user.mention}, welcome to Galaxy Studio!\nGo to <#801164212759953408> <#801285965981155328> <#801164212469891121>", file=discord.File('images/cache/card.png'))
        os.remove('images/cache/card.png')


    async def verify(self, user : discord.Member):
        muted = get(user.guild.roles, id=806974531842342912)
        citizen = get(user.guild.roles, id=801164212259782658)
        verify_channel = self.client.get_channel(806806294249209876)

        await user.add_roles(muted)
        await user.send("Hello, Welcome to galaxy city. Our systems are currently scaning your profile!\nThis should take no loger than 30 seconds\nPlease wait until this is done.")

        await asyncio.sleep(2)

        await verify_channel.send(f"{user.name} Has joined the server and is undergoing verification.")

        await asyncio.sleep(2)

        name = user.name
        banned_name = False

        for word in self.banned_words:
            if word in name:
                banned_name = True

        if banned_name == True:
            await user.send("I'm sorry but we have found a banned word in your name. Please change it and rejoin.\nIncase you dont have an invite: https://discord.gg/ReRYAj8wbs")
            await user.kick(reason="Banned word in name - Galaxy Bot Verification")
            await verify_channel.send(f"{user.name} Has been kicked for a rude name.")
            return False

        await user.send("Verification complete, you can now talk in galaxy city!")
        await verify_channel.send(f"{user.name} Has completed verification!")
        await user.remove_roles(muted)
        await user.add_roles(citizen)
        return True

    @Cog.listener()
    async def on_member_join(self, member):
        if await self.verify(member) == True:
            await self.generate_image(user=member)



def setup(client):
    client.add_cog(App(client))
