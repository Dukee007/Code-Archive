from itertools import cycle
from termcolor import colored
from datetime import datetime

import os
import json
import asyncio

import discord
from discord import ActionRow, Button, ButtonColor
from discord.ext import commands, tasks
from discord.ext.commands import check
from discord.utils import get
from discord_slash import SlashCommand, SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_permission, create_option, create_choice
from discord_slash.model import SlashCommandPermissionType


class System(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.staff_team_role_id = 861212427697913876
        self.registration_category_id = 861213711187968080
        self.registration_channel_id = 858801105029824532
        self.staff_registraion_request_channel_id = 861215400254898176
        self.discord_access_role_id = 858792050663882752
        self.discord_log_channel_id = 861217758439800893

        self.age_roles = {
            "13-17": 822617169694687243,
            "18-25": 822617228078874624,
            "26+": 822617266918129695
        }

        self.warnage = 50
        self.kick_delay = 60

        self.client.registration_sessions = {}
        self.client.session_text_channel_ids_to_user_ids = {}

    async def delcheck(self, member, before, after):
        if before.channel is not None and after.channel is not self.client.registration_sessions[str(member.id)]["voice"]:
            if before.channel.id == self.client.registration_sessions[str(member.id)]["voice"].id:
                await self.client.registration_sessions[str(member.id)]["voice"].delete()
                await self.client.registration_sessions[str(member.id)]["text"].delete()

                request_components = [
                    ActionRow(
                        Button(label='Accept',
                            custom_id='accept',
                            emoji="✅",
                            style=ButtonColor.green),

                        Button(label='Deny',
                                custom_id='deny',
                                emoji="❌",
                                style=ButtonColor.red)
                    )
                ]

                canceled_request_embed = discord.Embed(title=f"{member.name} Has canceled their request!",
                    colour=discord.Colour.red(),
                    description=f"This request has been canceled before a staff member could accept it, please make sure this user isn't abusing the system!")

                if self.client.registration_sessions[str(member.id)]["status"] == "waiting":
                    await self.client.registration_sessions[str(member.id)]["staff_request_msg"].edit(embed=canceled_request_embed, components=[request_components[0].disable_all_buttons()])
                    await self.log(mode="early_leave", early_leave={
                        "member_avatar": self.client.registration_sessions[str(member.id)]["member_obj"].avatar_url,
                        "member_name": self.client.registration_sessions[str(member.id)]["member_obj"].name,
                        "member_id": self.client.registration_sessions[str(member.id)]["member_obj"].id,
                        "time_created": self.client.registration_sessions[str(member.id)]["time_created"],
                        "time_deleted": str(datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
                    })

                elif self.client.registration_sessions[str(member.id)]["status"] == "accepted":
                    await self.log(mode="leave", early_leave={
                        "member_avatar": self.client.registration_sessions[str(member.id)]["member_obj"].avatar_url,
                        "member_name": self.client.registration_sessions[str(member.id)]["member_obj"].name,
                        "member_id": self.client.registration_sessions[str(member.id)]["member_obj"].id,
                        "time_created": self.client.registration_sessions[str(member.id)]["time_created"],
                        "time_deleted": str(datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
                    })

    async def log(self, mode, early_leave=None, staff_request=None, underage_kick=None, staff_confirm=None):
        log_channel = get(self.client.guilds[0].channels, id=self.discord_log_channel_id)

        print(mode)

        if mode == "early_leave":
            embed = discord.Embed(title="A request has been canceled early", colour=discord.Colour.orange(), description=f'<:profile:861068393066921984> **Member:** {early_leave["member_name"]} **[{early_leave["member_id"]}]**\n<:sortRight:861068393049620561> Member left channel while request was active.\n<:space:861068392802942977><:arrowRight:861068392613543947> Time Created: {early_leave["time_created"]}\n<:space:861068392802942977><:arrowRight:861068392613543947> Time Deleted: {early_leave["time_deleted"]}')

            embed.set_thumbnail(url=early_leave["member_avatar"])
            embed.set_footer(text="Harry's Registration - Assessment")

            embed.add_field(name="More details:", value="<:kick:861068392919203852> Member Kicked <:cross:861068392822865951>")

            await log_channel.send(embed=embed)

        elif mode == "leave":
            embed = discord.Embed(title="An assessment has been canceled!", colour=discord.Colour.red(), description=f'<:profile:861068393066921984> **Member:** {early_leave["member_name"]} **[{early_leave["member_id"]}]**\n<:sortRight:861068393049620561> Member left channel while assessment was active.\n<:space:861068392802942977><:arrowRight:861068392613543947> Time Created: {early_leave["time_created"]}\n<:space:861068392802942977><:arrowRight:861068392613543947> Time Deleted: {early_leave["time_deleted"]}')

            embed.set_thumbnail(url=early_leave["member_avatar"])
            embed.set_footer(text="Harry's Registration - Assessment")

            await log_channel.send(embed=embed)

        elif mode == "staff_request":
            if staff_request["mode"] == "deny":
                embed = discord.Embed(title="A request has been denied by a staff member", colour=discord.Colour.red(), description=f'<:profile:861068393066921984> **Member:** {staff_request["member_name"]} **[{staff_request["member_id"]}]**\n<:trustedAdmin:861068393130229790> **Staff Member:** {staff_request["staff_name"]} **[{staff_request["staff_id"]}]**\n<:sortRight:861068393049620561> A request was denied by a staff member.\n<:space:861068392802942977><:arrowRight:861068392613543947> Time Created: {staff_request["time_created"]}\n<:space:861068392802942977><:arrowRight:861068392613543947> Time Denied: {staff_request["time_denied"]}')

                embed.set_thumbnail(url=staff_request["member_avatar"])
                embed.set_footer(text="Harry's Registration - Assessment")

                embed.add_field(name="More details:", value="<:kick:861068392919203852> Member Kicked <:cross:861068392822865951>")

                await log_channel.send(embed=embed)

            elif staff_request["mode"] == "accept":
                embed = discord.Embed(title="A request has been accepted by a staff member", colour=discord.Colour.green(), description=f'<:profile:861068393066921984> **Member:** {staff_request["member_name"]} **[{staff_request["member_id"]}]**\n<:trustedAdmin:861068393130229790> **Staff Member:** {staff_request["staff_name"]} **[{staff_request["staff_id"]}]**\n<:sortRight:861068393049620561> A request was accepted by a staff member.\n<:space:861068392802942977><:arrowRight:861068392613543947> Time Created: {staff_request["time_created"]}\n<:space:861068392802942977><:arrowRight:861068392613543947> Time Accepted: {staff_request["time_accepted"]}')

                embed.set_thumbnail(url=staff_request["member_avatar"])
                embed.set_footer(text="Harry's Registration - Assessment")

                await log_channel.send(embed=embed)

        elif mode == "underage_kick":
            embed = discord.Embed(title="A member has been kicked!", colour=discord.Colour.red(), description=f'<:profile:861068393066921984> **Member:** {underage_kick["member_name"]} **[{underage_kick["member_id"]}]**\n<:sortRight:861068393049620561> A member has been kicked for being underage.\n<:space:861068392802942977><:arrowRight:861068392613543947> Time Created: {underage_kick["time_created"]}\n<:space:861068392802942977><:arrowRight:861068392613543947> Time Kicked: {underage_kick["time_kicked"]}')

            embed.set_thumbnail(url=underage_kick["member_avatar"])
            embed.set_footer(text="Harry's Registration - Assessment")

            embed.add_field(name="More details:", value="<:kick:861068392919203852> Member Kicked <:checkMark:861068392546697237>")

            await log_channel.send(embed=embed)

        elif mode == "staff_confirm":
            if staff_confirm["mode"] == "deny":
                embed = discord.Embed(title="A assessment has been completed by a staff member", colour=discord.Colour.red(), description=f'<:profile:861068393066921984> **Member:** {staff_confirm["member_name"]} **[{staff_confirm["member_id"]}]**\n<:trustedAdmin:861068393130229790> **Staff Member:** {staff_confirm["staff_name"]} **[{staff_confirm["staff_id"]}]**\n<:sortRight:861068393049620561> A assessment was completed by a staff member, the user has been kicked.\n<:space:861068392802942977><:arrowRight:861068392613543947> Time Created: {staff_confirm["time_created"]}\n<:space:861068392802942977><:arrowRight:861068392613543947> Time Kicked: {staff_confirm["time_denied"]}\n<:space:861068392802942977><:arrowRight:861068392613543947> Given Age: {staff_confirm["age"]}')

                embed.set_thumbnail(url=staff_confirm["member_avatar"])
                embed.set_footer(text="Harry's Registration - Assessment")

                embed.add_field(name="More details:", value="<:kick:861068392919203852> Member Kicked <:checkMark:861068392546697237>")

                await log_channel.send(embed=embed)

            elif staff_confirm["mode"] == "confirm":
                embed = discord.Embed(title="A assessment has been completed by a staff member", colour=discord.Colour.green(), description=f'<:profile:861068393066921984> **Member:** {staff_confirm["member_name"]} **[{staff_confirm["member_id"]}]**\n<:trustedAdmin:861068393130229790> **Staff Member:** {staff_confirm["staff_name"]} **[{staff_confirm["staff_id"]}]**\n<:sortRight:861068393049620561> A assessment was completed by a staff member, the user has been verified.\n<:space:861068392802942977><:arrowRight:861068392613543947> Time Created: {staff_confirm["time_created"]}\n<:space:861068392802942977><:arrowRight:861068392613543947> Time Kicked: {staff_confirm["time_confirmed"]}\n<:space:861068392802942977><:arrowRight:861068392613543947> Given Age: {staff_confirm["age"]}')

                embed.set_thumbnail(url=staff_confirm["member_avatar"])
                embed.set_footer(text="Harry's Registration - Assessment")

                embed.add_field(name="More details:", value="<:kick:861068392919203852> Member Kicked <:cross:861068392822865951>\n<:whitelistUser:861068393142681620> Roles Added <:checkMark:861068392546697237>")

                await log_channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        await self.delcheck(member, before, after)

        if before.channel is None and after.channel is not None:
            if after.channel.id == self.registration_channel_id:
                staff_team_role = get(self.client.guilds[0].roles, id=self.staff_team_role_id)
                registration_category = get(self.client.guilds[0].channels, id=self.registration_category_id)
                staff_registration_request_channel = get(self.client.guilds[0].channels, id=self.staff_registraion_request_channel_id)

                vc_overwrites = {
                    self.client.guilds[0].default_role: discord.PermissionOverwrite(view_channel=False),
                    member: discord.PermissionOverwrite(stream=True, view_channel=True, connect=True, speak=True),
                    staff_team_role: discord.PermissionOverwrite(stream=True, view_channel=True, connect=False, speak=True, mute_members=True, deafen_members=True)
                }

                txt_overwrites = {
                    self.client.guilds[0].default_role: discord.PermissionOverwrite(view_channel=False),
                    member: discord.PermissionOverwrite(view_channel=True, attach_files=True, read_message_history=True, send_messages=True, embed_links=True, add_reactions=True),
                    staff_team_role: discord.PermissionOverwrite(view_channel=True, attach_files=True, read_message_history=True, send_messages=False, embed_links=True, add_reactions=True, manage_messages=True, kick_members=True, ban_members=True, use_slash_commands=True)
                }

                self.client.registration_sessions[str(member.id)] = {}

                self.client.registration_sessions[str(member.id)]["status"] = "waiting"

                self.client.registration_sessions[str(member.id)]["voice"] = await self.client.guilds[0].create_voice_channel(f'registration-{member.name}', overwrites=vc_overwrites, category=registration_category, user_limit=2, reason=f"Channel auto-made for registration! (user: {member})")
                self.client.registration_sessions[str(member.id)]["text"] = await self.client.guilds[0].create_text_channel(f'registration-{member.name}', overwrites=txt_overwrites, category=registration_category, reason=f"Channel auto-made for registration! (user: {member})")

                self.client.session_text_channel_ids_to_user_ids[str(self.client.registration_sessions[str(member.id)]["text"].id)] = member.id

                self.client.registration_sessions[str(member.id)]["member_obj"] = member

                self.client.registration_sessions[str(member.id)]["time_created"] = str(datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))

                await member.move_to(self.client.registration_sessions[str(member.id)]["voice"], reason="Auto-move to personal channel for request!")
                waiting_msg = await self.client.registration_sessions[str(member.id)]["text"].send(f"{member.mention} Hello, we have pinged the staff team, they will be with you shortly. During this time feel free to do anything. Please note: If you leave, your request will be canceled!")

                request_components = [
                    ActionRow(
                        Button(label='Accept',
                            custom_id='accept',
                            emoji="✅",
                            style=ButtonColor.green),

                        Button(label='Deny',
                                custom_id='deny',
                                emoji="❌",
                                style=ButtonColor.red)
                    )
                ]

                request_embed = discord.Embed(title="New assessment request!", colour=discord.Colour(0xffff), description=f"<:profile:861068393066921984> **Member:** {member} **[{member.id}]**\n<:sortRight:861068393049620561> Account requesting assessment.\n")

                request_embed.set_thumbnail(url=member.avatar_url)
                request_embed.set_footer(text="Harry's Registration - Assessment")

                request_embed.add_field(name="More Details:", value="<:alarm:861068392626126850> Member Pinged <:checkMark:861068392546697237>\n <:textChannelCreated:861068393024716800> Private Channels Made <:checkMark:861068392546697237>")


                ping = await staff_registration_request_channel.send(staff_team_role.mention)
                await ping.delete()
                request_msg = await staff_registration_request_channel.send(embed=request_embed, components=request_components)

                self.client.registration_sessions[str(member.id)]["staff_request_msg"] = request_msg

                def _check(i: discord.RawInteractionCreateEvent):
                    return i.message == request_msg

                request_interaction: discord.RawInteractionCreateEvent = await self.client.wait_for('interaction_create', check=_check)
                button_id = request_interaction.button.custom_id

                await request_interaction.defer()

                accepted_embed = discord.Embed(title=f"{member}'s request has been accepted by {request_interaction.member}",
                    colour=discord.Colour.green(),
                    description=f"Request accepted!")

                denied_embed = discord.Embed(title=f"{member}'s request has been denied by {request_interaction.member}",
                    colour=discord.Colour.red(),
                    description=f"Request deleted!")

                if button_id == "deny":
                    await request_interaction.edit(embed=denied_embed, components=[request_components[0].disable_all_buttons()])
                    await waiting_msg.delete()
                    await self.client.registration_sessions[str(member.id)]["text"].send(f"{member.mention} Hey sorry but {request_interaction.member.mention} has denied your request!\nThis channel will be deleted in 1 minute!")

                    await self.log(mode="staff_request", staff_request={
                        "mode": "deny",
                        "member_avatar": self.client.registration_sessions[str(member.id)]["member_obj"].avatar_url,
                        "member_name": self.client.registration_sessions[str(member.id)]["member_obj"].name,
                        "member_id": self.client.registration_sessions[str(member.id)]["member_obj"].id,
                        "staff_name": request_interaction.member.name,
                        "staff_id": request_interaction.member.id,
                        "time_created": self.client.registration_sessions[str(member.id)]["time_created"],
                        "time_denied": str(datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
                    })

                    self.client.registration_sessions[str(member.id)]["status"] = "denied"

                    await asyncio.sleep(60)

                    await self.client.registration_sessions[str(member.id)]["voice"].delete()
                    await self.client.registration_sessions[str(member.id)]["text"].delete()

                    return

                elif button_id == "accept":
                    await request_interaction.edit(embed=accepted_embed, components=[request_components[0].disable_all_buttons()])

                    await self.client.registration_sessions[str(member.id)]["voice"].set_permissions(request_interaction.member, connect=True)
                    await self.client.registration_sessions[str(member.id)]["text"].set_permissions(request_interaction.member, send_messages=True)

                    await self.log(mode="staff_request", staff_request={
                        "mode": "accept",
                        "member_avatar": self.client.registration_sessions[str(member.id)]["member_obj"].avatar_url,
                        "member_name": self.client.registration_sessions[str(member.id)]["member_obj"].name,
                        "member_id": self.client.registration_sessions[str(member.id)]["member_obj"].id,
                        "staff_name": request_interaction.member.name,
                        "staff_id": request_interaction.member.id,
                        "time_created": self.client.registration_sessions[str(member.id)]["time_created"],
                        "time_accepted": str(datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
                    })

                    self.client.registration_sessions[str(member.id)]["status"] = "accepted"

                    await waiting_msg.delete()
                    await self.client.registration_sessions[str(member.id)]["text"].send(f"{member.mention} Hey {request_interaction.member.mention} will be taking you assessment!")

                    gettingAge = True

                    def _check(msg):
                        return msg.author.id == member.id and msg.channel.id == self.client.registration_sessions[str(member.id)]["text"].id

                    while gettingAge:
                        await self.client.registration_sessions[str(member.id)]["text"].send(f"{member.mention} Please tell me your age?\nYou have 1 minute!")

                        try:
                            givenAgeMessage = await self.client.wait_for('message', check=_check, timeout=60)
                            try:
                                givenAge = int(givenAgeMessage.content)
                            except:
                                await givenAgeMessage.reply(f"Thats not an age!")
                                await self.client.registration_sessions[str(member.id)]["text"].send(f"{request_interaction.member.mention} If the user doesnt answer this question correctly please help them, but if they are being silly please type `hr!deny`!")
                                continue

                        except Exception as e:
                            raise e

                        gettingAge = False

                    self.client.registration_sessions[str(member.id)]["age"] = givenAge

                    if givenAge > self.warnage:
                        await self.client.registration_sessions[str(member.id)]["text"].send(f"{request_interaction.member.mention} Hey staff, please note if the use is trolling please type `hr!deny`")

                    elif givenAge <= 12:
                        await self.client.registration_sessions[str(member.id)]["voice"].delete(reason="Auto-delete Deleted because user is to young (meeting ended)")
                        await self.client.registration_sessions[str(member.id)]["text"].set_permissions(request_interaction.member, send_messages=False, reason="Auto-edit removing staff perms from channel, so we can kick the user!")

                        await givenAgeMessage.reply(f"{member.mention} Unfortunately, you are too young to be a member of this server as Discord ToS requires members to be at least 13 years of age. This bot will remove you from our server in 60 seconds. Thank you for your interest.")

                        await self.log(mode="underage_kick", underage_kick={
                            "member_avatar": self.client.registration_sessions[str(member.id)]["member_obj"].avatar_url,
                            "member_name": self.client.registration_sessions[str(member.id)]["member_obj"].name,
                            "member_id": self.client.registration_sessions[str(member.id)]["member_obj"].id,
                            "time_created": self.client.registration_sessions[str(member.id)]["time_created"],
                            "time_kicked": str(datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
                        })

                        await asyncio.sleep(self.kick_delay)

                        await self.client.registration_sessions[str(member.id)]["text"].delete()

                        self.client.registration_sessions[str(member.id)]["status"] = "kicked"

                        try:
                            await member.kick(reason="Auto-kick Member is to young!")
                        except:
                            pass
                        return

                    await givenAgeMessage.reply(f"{member.mention} Thank you!")
                    await self.client.registration_sessions[str(member.id)]["text"].send(f"{request_interaction.member.mention} Please can you use methods you see fit to verify this age!")

                    gettingStaffConfirm = True

                    def _check(msg):
                        return msg.author.id == request_interaction.member.id and msg.channel.id == self.client.registration_sessions[str(member.id)]["text"].id

                    while gettingStaffConfirm:
                        await self.client.registration_sessions[str(member.id)]["text"].send("When you have your decision please respond with either: `confirm` or `deny`.")

                        try:
                            givenConfirmMessage = await self.client.wait_for('message', check=_check, timeout=60)

                            if givenConfirmMessage.content.lower() == "deny":
                                await self.client.registration_sessions[str(member.id)]["voice"].delete(reason="Auto-delete Deleted because user is to young (meeting ended)")
                                await self.client.registration_sessions[str(member.id)]["text"].set_permissions(request_interaction.member, send_messages=False, reason="Auto-edit removing staff perms from channel, so we can kick the user!")

                                await givenConfirmMessage.reply(f"{member.mention} Unfortunately, you are too young to be a member of this server as Discord ToS requires members to be at least 13 years of age. This bot will remove you from our server in 60 seconds. Thank you for your interest.")

                                await self.log(mode="staff_confirm", staff_confirm={
                                    "mode": "deny",
                                    "member_avatar": self.client.registration_sessions[str(member.id)]["member_obj"].avatar_url,
                                    "member_name": self.client.registration_sessions[str(member.id)]["member_obj"].name,
                                    "member_id": self.client.registration_sessions[str(member.id)]["member_obj"].id,
                                    "staff_name": request_interaction.member.name,
                                    "staff_id": request_interaction.member.id,
                                    "time_created": self.client.registration_sessions[str(member.id)]["time_created"],
                                    "time_denied": str(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")),
                                    "age": self.client.registration_sessions[str(member.id)]["age"]
                                })

                                await asyncio.sleep(self.kick_delay)

                                await self.client.registration_sessions[str(member.id)]["text"].delete()

                                self.client.registration_sessions[str(member.id)]["status"] = "kicked"

                                try:
                                    await member.kick(reason="Auto-kick Member is to young!")
                                except:
                                    pass
                                return

                            elif givenConfirmMessage.content.lower() == "confirm":
                                await givenConfirmMessage.reply("Thanks for your help!\nI will now remove you from this channel!")

                                await self.client.registration_sessions[str(member.id)]["voice"].delete(reason="Auto-delete Deleted because user has completed assessment (meeting ended)")
                                await self.client.registration_sessions[str(member.id)]["text"].set_permissions(request_interaction.member, send_messages=False, reason="Auto-edit removing staff perms from channel, so we can end the meeting!")
                                await self.client.registration_sessions[str(member.id)]["text"].set_permissions(member, send_messages=False, read_message_history=True, view_channel=True, reason="Auto-edit removing user perms from channel, so we can end the meeting!")

                                await self.client.registration_sessions[str(member.id)]["text"].send(f"{member.mention} Thank you for completing this assessment, please wait while I log this and apply your roles!\nThis channel will be deleted in 30s")

                                await self.log(mode="staff_confirm", staff_confirm={
                                    "mode": "confirm",
                                    "member_avatar": self.client.registration_sessions[str(member.id)]["member_obj"].avatar_url,
                                    "member_name": self.client.registration_sessions[str(member.id)]["member_obj"].name,
                                    "member_id": self.client.registration_sessions[str(member.id)]["member_obj"].id,
                                    "staff_name": request_interaction.member.name,
                                    "staff_id": request_interaction.member.id,
                                    "time_created": self.client.registration_sessions[str(member.id)]["time_created"],
                                    "time_confirmed": str(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")),
                                    "age": self.client.registration_sessions[str(member.id)]["age"]
                                })

                                if givenAge > 12 and givenAge <= 18:
                                    age_role =  get(self.client.guilds[0].roles, id=self.age_roles["13-17"])
                                    await member.add_roles(age_role, reason="Auto-role given age role to member")

                                elif givenAge > 17 and givenAge <= 25:
                                    age_role = get(self.client.guilds[0].roles, id=self.age_roles["18-25"])
                                    await member.add_roles(age_role, reason="Auto-role given age role to member")

                                else:
                                    age_role = get(self.client.guilds[0].roles, id=self.age_roles["26+"])
                                    await member.add_roles(age_role, reason="Auto-role given age role to member")

                                access_role = get(self.client.guilds[0].roles, id=self.discord_access_role_id)
                                await member.add_roles(access_role, reason="Auto-role given access role to member")



                                self.client.registration_sessions[str(member.id)]["status"] = "complete"

                                await asyncio.sleep(25)

                                await self.client.registration_sessions[str(member.id)]["text"].delete(reason="Auto-delete assessment over")

                            else:
                                await givenConfirmMessage.reply(f"Thats not an option!")
                                continue

                        except Exception as e:
                            raise e

                        gettingStaffConfirm = False







def setup(client):
    client.add_cog(System(client))
