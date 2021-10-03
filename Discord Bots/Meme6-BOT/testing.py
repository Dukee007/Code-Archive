@tasks.loop(seconds=10)
async def update_stats():
    print("running")
    print(client.guilds)
    for guild in client.guilds:
        print(guild.name + " " + str(guild.id))
        with open("statsoptionlist.json") as f:
            print("open statsoptionlist")
            data = json.load(f)
            print(data[str(guild.id)])
        for x in data[str(guild.id)]:
            print("x:" + x)
            for cat in guild.categories:
                if cat.name == "📊 Server Stats 📊":
                    print("true")
                    e = True
                    break
                else:
                    print("false")
                    e = False
            print("running")
            if e == False:
                await guild.create_category("📊 Server Stats 📊")
            print("b4 data read")
            bm = 0
            nm = 0
            am = 0
            bans = 0
            for ban in await guild.bans():
                bans += 1
            for mem in guild.members:
                if mem.bot == True:
                    bm += 1
                else:
                    nm += 1
                am += 1
            print("b4 text read")
            f = open("statdata_messages.txt")
            mes = str(f.read())
            f.close()
            print("after data read")
            for category in guild.categories:
                if cat.name == "📊 Server Stats 📊":
                    for channel in cat.channels:
                        print("channels")
                        print(channel.name)
                        if "All Members:" in channel.name:
                            print("in")
                            print(x)
                            if x["allmembers"] == True:
                                print("edit")
                                await channel.edit(name=f"All Members: {am}")
                            else:
                                await channel.delete()
                                print("del")
                        elif "Members:" in channel.name:
                            if x["allmembers"] == True:
                                await channel.edit(name=f"Members: {am}")
                            else:
                                await channel.delete()
                        elif "Bots:" in channel.name:
                            if x["allmembers"] == True:
                                await channel.edit(name=f"Bots: {am}")
                            else:
                                await channel.delete()
                        elif "Bans:" in channel.name:
                            if x["allmembers"] == True:
                                await channel.edit(name=f"Bans: {am}")
                            else:
                                await channel.delete()
                        elif "Messages:" in channel.name:
                            if x["allmembers"] == True:
                                await channel.edit(name=f"Messages: {mes}")
                            else:
                                await channel.delete()
