from discord_webhook import DiscordWebhook, DiscordEmbed

webhook = DiscordWebhook(url='https://discord.com/api/webhooks/825788651312250920/_I9u6EwZ5hCu28EjahF7CGNbUEBwA148Y9HrT2DY3CCUhdznZXlWLxTk9JAHhtg62Ejy')

embed = DiscordEmbed(title=f"{user.name}#{user.identifier} has been banned!", colour=0x00ffff, description=f"<:profile:825645321328525322> **Member:** {user.name}#{user.identifier} **[{user.id}]**\n<:rightArrow:825645321400614952> **Reason:** Account joined during raid and was too young!", timestamp=datetime.now(), username="Boba's Utilities", avatar_url=self.client.user.avatar_url)

embed.set_thumbnail(url=user.avatar_url)
embed.set_footer(text="Boba's Utilities | User was banned at")

embed.add_field(name="More Details:", value=f"<:NoDM:825645320993374220> **Member Direct Messaged?** <:Cross:825645321160753182>\n<:Ban:825788207173992478> **Member Punished?** <:Check:825645321140305930>")

webhook.add_embed(embed)
response = webhook.execute()
